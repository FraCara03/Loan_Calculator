import math
import argparse

# Initialize the parser
parser = argparse.ArgumentParser(description="Loan Calculator")

# Adding the necessary arguments
parser.add_argument("--type", type=str, help="Type of payment: 'annuity' or 'diff'")
parser.add_argument("--principal", type=float, help="Loan principal")
parser.add_argument("--periods", type=int, help="Number of months")
parser.add_argument("--payment", type=float, help="Monthly payment")
parser.add_argument("--interest", type=float, help="Credit interest (without the percent sign)")

# Parsing the arguments
args = parser.parse_args()

# Validate that the interest is provided
if not args.interest:
    print("Incorrect parameters")
    exit()

# Calculate nominal interest rate
i = args.interest / (12 * 100)  # Monthly interest rate

# Check for valid parameter combinations and handle negative values
if args.type not in ["annuity", "diff"] or \
        (args.principal is not None and args.principal <= 0) or \
        (args.periods is not None and args.periods <= 0) or \
        (args.payment is not None and args.payment <= 0) or \
        args.interest <= 0:
    print("Incorrect parameters")
    exit()

# Ensure that only one of `principal`, `payment`, or `periods` is missing
if (args.principal is not None and args.payment is not None and args.periods is not None) or (
        args.principal is None and args.payment is None and args.periods is None):
    print("Incorrect parameters")
    exit()

# Handle "annuity" type calculations
if args.type == "annuity":
    if args.payment is None:
        # Calculate annuity payment
        A = args.principal * i * math.pow((1 + i), args.periods) / (math.pow((1 + i), args.periods) - 1)
        total_payment = math.ceil(A) * args.periods
        overpayment = total_payment - args.principal
        print(f"Your monthly payment = {math.ceil(A)}!")
        print(f"Overpayment = {int(overpayment)}")

    elif args.principal is None:
        # Calculate loan principal
        P = args.payment / (i * math.pow((1 + i), args.periods) / (math.pow((1 + i), args.periods) - 1))
        total_payment = args.payment * args.periods
        overpayment = total_payment - math.floor(P)
        print(f"Your loan principal = {math.floor(P)}!")
        print(f"Overpayment = {int(overpayment)}")

    elif args.periods is None:
        # Calculate the number of periods (months)
        n = math.log(args.payment / (args.payment - i * args.principal), 1 + i)
        n = math.ceil(n)
        total_payment = args.payment * n
        overpayment = total_payment - args.principal
        years = n // 12
        months = n % 12
        if years > 0 and months > 0:
            print(f"It will take {years} years and {months} months to repay this loan!")
        elif years > 0:
            print(f"It will take {years} years to repay this loan!")
        else:
            print(f"It will take {months} months to repay this loan!")
        print(f"Overpayment = {int(overpayment)}")

# Handle "diff" type (differentiated payments)
elif args.type == "diff":
    if args.principal and args.periods and args.interest:
        total_payment = 0
        for m in range(1, args.periods + 1):
            D = args.principal / args.periods + i * (args.principal - (args.principal * (m - 1)) / args.periods)
            total_payment += math.ceil(D)
            print(f"Month {m}: payment is {math.ceil(D)}")
        overpayment = total_payment - args.principal
        print(f"\nOverpayment = {int(overpayment)}")
    else:
        print("Incorrect parameters")
        exit()
