def financial_health_score(score):
    """
    Returns company health based on score.
    """

    if score >= 80:
        return "Excellent"

    elif score >= 60:
        return "Good"

    elif score >= 40:
        return "Average"

    else:
        return "Poor"