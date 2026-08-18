def financial_health_score(score):
    """
    Classifies a company's financial health based on a score.

    Score ranges:
        80 - 100 : Excellent
        60 - 79  : Good
        40 - 59  : Average
        Below 40 : Poor

    Returns:
        str: Financial health category.
    """

    # Handle missing score
    if score is None:
        return "Poor"

    # Convert score to numeric
    try:
        score = float(score)
    except (TypeError, ValueError):
        return "Poor"

    # Financial health classification
    if score >= 80:
        return "Excellent"

    elif score >= 60:
        return "Good"

    elif score >= 40:
        return "Average"

    else:
        return "Poor"