def sector_rating(roe):

    if roe >= 20:
        return "Excellent"

    elif roe >= 15:
        return "Very Good"

    elif roe >= 10:
        return "Good"

    else:
        return "Needs Improvement"