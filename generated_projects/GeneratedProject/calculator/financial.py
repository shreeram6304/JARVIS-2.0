class FinancialEngine:

    @staticmethod
    def calculate_loan(principal: float, annual_rate: float, years: int) -> dict:
        if principal <= 0 or annual_rate < 0 or years <= 0:
            raise ValueError("Invalid input parameters for loan calculation")

        monthly_rate = (annual_rate / 100) / 12
        total_payments = years * 12

        if monthly_rate == 0:
            monthly_payment = principal / total_payments
        else:
            monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** total_payments) / (((1 + monthly_rate) ** total_payments) - 1)

        total_paid = monthly_payment * total_payments
        total_interest = total_paid - principal

        return {
            "monthly_payment": round(monthly_payment, 2),
            "total_payment": round(total_paid, 2),
            "total_interest": round(total_interest, 2)
        }

    @staticmethod
    def calculate_compound_interest(principal: float, annual_rate: float, years: float, compound_frequency: int = 12) -> dict:
        if principal < 0 or annual_rate < 0 or years <= 0 or compound_frequency <= 0:
            raise ValueError("Invalid input parameters for compound interest")

        r = annual_rate / 100
        n = compound_frequency
        t = years

        future_value = principal * ((1 + (r / n)) ** (n * t))
        interest_earned = future_value - principal

        return {
            "future_value": round(future_value, 2),
            "total_interest": round(interest_earned, 2),
            "principal": round(principal, 2)
        }

    @staticmethod
    def calculate_bmi(weight_kg: float, height_cm: float) -> dict:
        if weight_kg <= 0 or height_cm <= 0:
            raise ValueError("Weight and height must be positive numbers")

        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        
        category = "Underweight"
        if 18.5 <= bmi < 24.9:
            category = "Normal weight"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        elif bmi >= 30:
            category = "Obesity"

        return {
            "bmi": round(bmi, 1),
            "category": category
        }