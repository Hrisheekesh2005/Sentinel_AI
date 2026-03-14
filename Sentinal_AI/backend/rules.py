import re


def rule_based_score(text):
    score = 0
    reasons = []
    text = text.lower()

    # --- LAYER 1: LEGITIMACY CHECK (Prevents False Positives) ---
    legit_triggers = {
        r"available balance": -50,
        r"debited from your a/c": -40,
        r"credited to your a/c": -40,
        r"if you did not request this": -25,
        r"do not share.*otp": -30,
        r"\d{2}-\w{3}-\d{4}": -15  # Matches dates like 14-Mar-2026
    }
    for pattern, pts in legit_triggers.items():
        if re.search(pattern, text):
            score += pts
            reasons.append("Legitimate service format")

    # --- LAYER 2: BROAD SCAM CATEGORIES (Friend's Logic) ---

    # 2.1 Credential Theft (Highest Risk)
    if re.search(r"share.*otp|provide.*otp|send.*otp|confirm.*pin|share.*password", text):
        score += 55
        reasons.append("Credential request scam")

    # 2.2 Financial Impersonation
    if re.search(r"\bbank\b|\bkyc\b|\baadhar\b|\bpan\b|\brbi\b", text):
        if re.search(r"click|update|verify|login|link|http", text):
            score += 35
            reasons.append("Financial impersonation attempt")

    # 2.3 Lottery & Reward Scams
    if re.search(r"you won|congratulations|lottery|jackpot|claim.*prize|reward.*waiting", text):
        score += 45
        reasons.append("Lottery or prize scam")

    # 2.4 Job & Earn Money Scams
    if re.search(r"work from home|earn.*per day|easy money|data entry job|no experience required", text):
        score += 35
        reasons.append("Job scam pattern")

    # 2.5 Tech Support & Security Scams
    if re.search(
            r"virus detected|malware detected|computer infected|windows security alert|download anydesk|remote access",
            text):
        score += 40
        reasons.append("Tech support scam")

    # 2.6 Loan & Delivery Scams
    if re.search(r"instant loan|loan approved|pre approved loan|package held|delivery failed|pay delivery fee", text):
        score += 35
        reasons.append("Loan or Delivery scam")

    # 2.7 Urgency & Threats
    if re.search(r"urgent|immediately|act now|last warning|final notice|account.*blocked|account.*suspended", text):
        score += 25
        reasons.append("Urgency or threat language")

    # --- LAYER 3: PATTERN MATCHING (Evidence) ---
    if re.search(r"http[s]?://|bit\.ly|tinyurl|t\.co|goo\.gl", text):
        score += 20
        reasons.append("Suspicious link detected")

    if re.search(r'[6789]\d{9}', text):
        score += 10
        reasons.append("Phone number detected")

    if re.search(r'[a-zA-Z0-9.\-_]+@[a-zA-Z]+', text):
        score += 15
        reasons.append("UPI ID detected")

    # --- LAYER 4: AGENTIC CORRELATION ---
    # If there is urgency AND a link, it's a huge red flag
    if (re.search(r"urgent|immediately", text)) and (re.search(r"http|click", text)):
        score += 20
        reasons.append("High-risk Urgency + Link combination")

    # Final result: No negative scores, unique reasons
    return max(0, score), list(set(reasons))