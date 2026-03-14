import pickle
import os
import re
import requests
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
from rules import rule_based_score

# 1. Setup Base Directory and Load Assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = pickle.load(open(os.path.join(BASE_DIR, "model.pkl"), "rb"))
vectorizer = pickle.load(open(os.path.join(BASE_DIR, "vectorizer.pkl"), "rb"))

# 2. Semantic Memory: Known Scam Blueprints
scam_templates = [
    "your kyc is expired update immediately",
    "your bank account will be blocked verify now",
    "share otp to complete verification",
    "click link to update pan card details",
    "congratulations you won a lottery claim prize now",
    "urgent your account has been suspended verify immediately",
    "electricity bill pending disconnection tonight"
]
# Pre-vectorize templates for speed
template_vectors = vectorizer.transform(scam_templates)


# 3. Agentic Tool: URL Unmasker
def unmask_url(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        # Perform a HEAD request to follow redirects without downloading page content
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=3, stream=True)
        return response.url
    except:
        return url


# 4. Agentic Tool: Dynamic Template Engine
def generate_complaint_template(risk_data):
    reasons_str = " ".join(risk_data['reasons']).lower()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if "credential" in reasons_str or "otp" in reasons_str:
        category = "Credential Theft / Vishing"
        description = "Perpetrator attempted to harvest sensitive banking OTPs/Passwords via social engineering."
    elif "financial" in reasons_str or "kyc" in reasons_str:
        category = "Financial Impersonation"
        description = "Sender impersonated a financial institution claiming account expiry to induce panic."
    elif "blueprint" in reasons_str:
        category = "Pattern-Matched Fraud"
        description = "Message matches high-confidence known scam signatures stored in the Agent's memory."
    else:
        category = "Digital Scam Attempt"
        description = "A suspicious message was identified with intent to defraud using digital channels."

    return f"""
SENTINEL AI: OFFICIAL INCIDENT REPORT
-----------------------------------------
Report Timestamp: {timestamp}
Incident Category: {category}
Risk Severity: {risk_data['risk_score']}% ({risk_data['decision']})

EXECUTIVE SUMMARY:
{description}

EVIDENCE LOGGED BY AGENT:
- Source Contact: {risk_data['phone']}
- Unmasked Entity: {risk_data['upi']}
- Security Flags: {", ".join(risk_data['reasons'])}

LEGAL NOTICE:
This report is generated autonomously by Sentinel AI. I request investigation into this source for potential IT Act violations.
-----------------------------------------
""".strip()


# 5. Core Agentic Reasoning Loop
def analyze_message(text: str):
    # --- PHASE 1: OBSERVATION ---
    urls = re.findall(r'https?://\S+', text)
    unmasked_urls = [unmask_url(u) for u in urls]

    phone_match = re.search(r'(\+91[\-\s]?)?[6789]\d{9}', text)
    extracted_phone = phone_match.group(0) if phone_match else "None Detected"
    # Use unmasked link as the primary entity if available
    extracted_upi = unmasked_urls[0] if unmasked_urls else "None Detected"

    # --- PHASE 2: TRIPLE-LAYER ANALYSIS ---

    # Layer 1: ML Intent (Intuition)
    vector = vectorizer.transform([text])
    ml_prob = model.predict_proba(vector)[0][1]
    ml_score = int(ml_prob * 100)

    # Layer 2: Semantic Similarity (Memory)
    similarities = cosine_similarity(vector, template_vectors)
    max_sim = similarities.max()
    sim_score = 0
    sim_reason = None
    if max_sim > 0.70:
        sim_score = 40
        sim_reason = "Matches known scam blueprint"

    # Layer 3: Logic Rules (Verification)
    rule_score, reasons = rule_based_score(text)
    if sim_reason: reasons.append(sim_reason)

    # Agentic Check: Did unmasking reveal a lie?
    if any(u != o for u, o in zip(unmasked_urls, urls)):
        reasons.append("Hidden URL redirect unmasked")
        rule_score += 20

    # --- PHASE 3: SYNTHESIS ---
    # Final score is a weighted blend: 30% ML, 30% Similarity, 40% Rules
    final_score = min(int((ml_score * 0.3) + (sim_score * 0.3) + (rule_score * 0.4)), 99)

    if final_score >= 100:
        final_score = 99
    if final_score >= 75:
        decision = "SCAM"
    elif final_score >= 40:
        decision = "SUSPICIOUS"
    else:
        decision = "SAFE"

    # --- PHASE 4: ACTION PREPARATION ---
    risk_data = {
        "risk_score": final_score,
        "decision": decision,
        "reasons": reasons,
        "phone": extracted_phone,
        "upi": extracted_upi
    }

    return {
        **risk_data,
        "ml_confidence": round(ml_prob, 2),
        "unmasked_links": unmasked_urls,
        "dynamic_complaint": generate_complaint_template(risk_data)
    }