def generate_investigation_report(txn_summary, top_features, risk_score):
    features = ", ".join(top_features[:3])
    return {
        "what_happened": txn_summary,
        "why_is_risky": f"Risk score {risk_score:.1f}/100. Key risk factors: {features}.",
        "next_actions": "1. Review transaction. 2. Contact customer. 3. Block if suspicious."
    }