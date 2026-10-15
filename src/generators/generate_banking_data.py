import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

OUTPUT_DIR = Path("data/raw")

CUSTOMER_COUNT = 100
ACCOUNT_COUNT = 150
MERCHANT_COUNT = 30
TRANSACTION_COUNT = 1000

RANDOM_SEED = 42


# ---------------------------------------------------------
# Reference Data
# ---------------------------------------------------------

FIRST_NAMES = [
    "Arun",
    "Priya",
    "Karthik",
    "Divya",
    "Rahul",
    "Sneha",
    "Vijay",
    "Anitha",
    "Suresh",
    "Meena",
    "Ravi",
    "Kavya",
    "Ajay",
    "Deepa",
    "Manoj",
]

LAST_NAMES = [
    "Kumar",
    "Sharma",
    "Iyer",
    "Reddy",
    "Patel",
    "Nair",
    "Das",
    "Menon",
    "Rao",
    "Krishnan",
]

LOCATIONS = [
    ("Chennai", "Tamil Nadu", "India"),
    ("Bengaluru", "Karnataka", "India"),
    ("Mumbai", "Maharashtra", "India"),
    ("Hyderabad", "Telangana", "India"),
    ("Delhi", "Delhi", "India"),
    ("Pune", "Maharashtra", "India"),
    ("Kochi", "Kerala", "India"),
    ("Coimbatore", "Tamil Nadu", "India"),
]

CUSTOMER_SEGMENTS = [
    "RETAIL",
    "PREMIUM",
    "SALARY",
    "SME",
]

ACCOUNT_TYPES = [
    "SAVINGS",
    "CURRENT",
    "SALARY",
]

ACCOUNT_STATUSES = [
    "ACTIVE",
    "ACTIVE",
    "ACTIVE",
    "DORMANT",
    "CLOSED",
]

TRANSACTION_TYPES = [
    "PURCHASE",
    "WITHDRAWAL",
    "TRANSFER",
    "PAYMENT",
    "REFUND",
]

PAYMENT_CHANNELS = [
    "UPI",
    "CARD",
    "NET_BANKING",
    "ATM",
    "MOBILE_APP",
]

TRANSACTION_STATUSES = [
    "SUCCESS",
    "SUCCESS",
    "SUCCESS",
    "FAILED",
    "PENDING",
]

MERCHANT_CATEGORIES = [
    "GROCERY",
    "E_COMMERCE",
    "RESTAURANT",
    "TRAVEL",
    "FUEL",
    "ELECTRONICS",
    "HEALTHCARE",
    "ENTERTAINMENT",
]


# ---------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------

def random_date(start_date, end_date):
    """Generate a random date between two dates."""

    delta = end_date - start_date

    random_days = random.randint(0, delta.days)

    return start_date + timedelta(days=random_days)


def random_datetime(start_date, end_date):
    """Generate a random datetime between two dates."""

    delta = end_date - start_date

    random_seconds = random.randint(0, int(delta.total_seconds()))

    return start_date + timedelta(seconds=random_seconds)


def random_amount(min_amount=100, max_amount=100000):
    """Generate a realistic transaction amount."""

    return round(random.uniform(min_amount, max_amount), 2)


def write_csv(file_path, rows, fieldnames):
    """Write a list of dictionaries to CSV."""

    with open(file_path, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        writer.writerows(rows)


# ---------------------------------------------------------
# Customer Generator
# ---------------------------------------------------------

def generate_customers():

    customers = []

    start_date = datetime(2018, 1, 1)
    end_date = datetime(2025, 12, 31)

    for number in range(1, CUSTOMER_COUNT + 1):

        customer_id = f"CUST{number:05d}"

        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)

        city, state, country = random.choice(LOCATIONS)

        date_of_birth = random_date(
            datetime(1960, 1, 1),
            datetime(2000, 12, 31),
        )

        registration_date = random_date(
            start_date,
            end_date,
        )

        customer = {
            "customer_id": customer_id,
            "customer_name": f"{first_name} {last_name}",
            "date_of_birth": date_of_birth.strftime("%Y-%m-%d"),
            "gender": random.choice(["MALE", "FEMALE"]),
            "city": city,
            "state": state,
            "country": country,
            "customer_segment": random.choice(CUSTOMER_SEGMENTS),
            "registration_date": registration_date.strftime("%Y-%m-%d"),
        }

        customers.append(customer)

    return customers


# ---------------------------------------------------------
# Account Generator
# ---------------------------------------------------------

def generate_accounts(customers):

    accounts = []

    for number in range(1, ACCOUNT_COUNT + 1):

        account_id = f"ACC{number:06d}"

        customer = random.choice(customers)

        account = {
            "account_id": account_id,
            "customer_id": customer["customer_id"],
            "account_type": random.choice(ACCOUNT_TYPES),
            "account_status": random.choice(ACCOUNT_STATUSES),
            "account_open_date": random_date(
                datetime(2019, 1, 1),
                datetime(2025, 12, 31),
            ).strftime("%Y-%m-%d"),
            "branch_code": f"BR{random.randint(100, 999)}",
            "current_balance": round(
                random.uniform(1000, 1000000),
                2,
            ),
        }

        accounts.append(account)

    return accounts


# ---------------------------------------------------------
# Merchant Generator
# ---------------------------------------------------------

def generate_merchants():

    merchants = []

    for number in range(1, MERCHANT_COUNT + 1):

        merchant_id = f"MER{number:05d}"

        city, state, country = random.choice(LOCATIONS)

        merchant = {
            "merchant_id": merchant_id,
            "merchant_name": (
                f"{random.choice(['Global', 'Prime', 'Smart', 'Metro', 'Urban'])} "
                f"{random.choice(['Mart', 'Store', 'Foods', 'Services', 'Retail'])}"
            ),
            "merchant_category": random.choice(MERCHANT_CATEGORIES),
            "city": city,
            "state": state,
            "country": country,
        }

        merchants.append(merchant)

    return merchants


# ---------------------------------------------------------
# Transaction Generator
# ---------------------------------------------------------

def generate_transactions(accounts, customers, merchants):

    transactions = []

    customer_lookup = {
        customer["customer_id"]: customer
        for customer in customers
    }

    merchant_lookup = {
        merchant["merchant_id"]: merchant
        for merchant in merchants
    }

    start_date = datetime(2026, 1, 1)
    end_date = datetime(2026, 9, 30)

    for number in range(1, TRANSACTION_COUNT + 1):

        account = random.choice(accounts)

        customer_id = account["customer_id"]

        customer = customer_lookup[customer_id]

        merchant = random.choice(merchants)

        transaction_id = f"TXN{number:08d}"

        transaction_date = random_datetime(
            start_date,
            end_date,
        )

        transaction = {
            "transaction_id": transaction_id,
            "account_id": account["account_id"],
            "customer_id": customer_id,
            "merchant_id": merchant["merchant_id"],
            "transaction_date": transaction_date.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "transaction_type": random.choice(
                TRANSACTION_TYPES
            ),
            "amount": random_amount(),
            "currency": "INR",
            "payment_channel": random.choice(
                PAYMENT_CHANNELS
            ),
            "transaction_status": random.choice(
                TRANSACTION_STATUSES
            ),
            "city": customer["city"],
        }

        transactions.append(transaction)

    return transactions


# ---------------------------------------------------------
# Add Data Quality Issues
# ---------------------------------------------------------

def add_data_quality_issues(transactions):

    # Duplicate record
    duplicate_record = transactions[0].copy()

    transactions.append(duplicate_record)

    # Missing customer ID
    transactions[1]["customer_id"] = ""

    # Negative transaction amount
    transactions[2]["amount"] = -500

    # Invalid transaction status
    transactions[3]["transaction_status"] = "UNKNOWN"

    # Invalid currency
    transactions[4]["currency"] = "XYZ"

    # Invalid payment channel
    transactions[5]["payment_channel"] = "UNKNOWN"

    return transactions


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    random.seed(RANDOM_SEED)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("Generating banking datasets...")

    customers = generate_customers()

    accounts = generate_accounts(
        customers
    )

    merchants = generate_merchants()

    transactions = generate_transactions(
        accounts,
        customers,
        merchants,
    )

    transactions = add_data_quality_issues(
        transactions
    )

    write_csv(
        OUTPUT_DIR / "customers.csv",
        customers,
        [
            "customer_id",
            "customer_name",
            "date_of_birth",
            "gender",
            "city",
            "state",
            "country",
            "customer_segment",
            "registration_date",
        ],
        )

    write_csv(
        OUTPUT_DIR / "accounts.csv",
        accounts,
        [
            "account_id",
            "customer_id",
            "account_type",
            "account_status",
            "account_open_date",
            "branch_code",
            "current_balance",
        ],
        )

    write_csv(
        OUTPUT_DIR / "merchants.csv",
        merchants,
        [
            "merchant_id",
            "merchant_name",
            "merchant_category",
            "city",
            "state",
            "country",
        ],
        )

    write_csv(
        OUTPUT_DIR / "transactions.csv",
        transactions,
        [
            "transaction_id",
            "account_id",
            "customer_id",
            "merchant_id",
            "transaction_date",
            "transaction_type",
            "amount",
            "currency",
            "payment_channel",
            "transaction_status",
            "city",
        ],
        )

    print()
    print("Data generation completed.")
    print(f"Customers    : {len(customers)}")
    print(f"Accounts     : {len(accounts)}")
    print(f"Merchants    : {len(merchants)}")
    print(f"Transactions : {len(transactions)}")
    print()
    print(f"Output directory: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()