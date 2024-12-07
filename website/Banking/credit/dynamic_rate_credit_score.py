def get_dynamic_interest_rate(principal, credit_score):
    """
    Adjust the loan interest rate based on the user's credit score and loan amount.
    """
    if credit_score >= 750:
        base_rate = 0.05  # 5% interest for users with excellent credit
    elif credit_score >= 650:
        base_rate = 0.08  # 8% interest for users with average credit
    elif credit_score >= 550:
        base_rate = 0.12  # 12% interest for users with poor credit
    else:
        base_rate = 0.15  # 15% interest for users with very poor credit

    if principal > 10000:
        base_rate += 0.02  # Add a 2% higher interest for loans over $10,000
    
    return base_rate
