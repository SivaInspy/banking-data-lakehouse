import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

SILVER_FILE = Path(
    "data/silver/transactions.csv"
)

GOLD_DAILY_FILE = Path(
    "data/gold/daily_transaction_summary.csv"
)

VALID_CURRENCIES = {
    "INR",
}

VALID_STATUSES = {
    "SUCCESS",
    "FAILED",
    "PENDING",
}

VALID_PAYMENT_CHANNELS = {
    "UPI",
    "CARD",
    "NET_BANKING",
    "ATM",
    "MOBILE_APP",
}


# ---------------------------------------------------------
# Validation Helpers
# ---------------------------------------------------------

def check_required_columns(df):

    required_columns = {
        "transaction_id",
        "account_id",
        "customer_id",
        "merchant_id",
        "transaction_date",
        "amount",
        "currency",
        "payment_channel",
        "transaction_status",
    }

    missing_columns = (
            required_columns
            - set(df.columns)
    )

    if missing_columns:

        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    print(
        "PASS: Required columns are present"
    )


def check_transaction_ids(df):

    if df["transaction_id"].isna().any():

        raise ValueError(
            "Null transaction_id found"
        )

    if df["transaction_id"].duplicated().any():

        raise ValueError(
            "Duplicate transaction_id found"
        )

    print(
        "PASS: Transaction IDs are unique"
    )


def check_amounts(df):

    if df["amount"].isna().any():

        raise ValueError(
            "Null transaction amount found"
        )

    if (df["amount"] <= 0).any():

        raise ValueError(
            "Non-positive transaction amount found"
        )

    print(
        "PASS: Transaction amounts are valid"
    )


def check_currency(df):

    invalid = set(
        df["currency"].dropna()
    ) - VALID_CURRENCIES

    if invalid:

        raise ValueError(
            f"Invalid currencies found: {invalid}"
        )

    print(
        "PASS: Currency values are valid"
    )


def check_status(df):

    invalid = set(
        df["transaction_status"].dropna()
    ) - VALID_STATUSES

    if invalid:

        raise ValueError(
            f"Invalid transaction statuses found: {invalid}"
        )

    print(
        "PASS: Transaction statuses are valid"
    )


def check_payment_channel(df):

    invalid = set(
        df["payment_channel"].dropna()
    ) - VALID_PAYMENT_CHANNELS

    if invalid:

        raise ValueError(
            f"Invalid payment channels found: {invalid}"
        )

    print(
        "PASS: Payment channels are valid"
    )


def check_gold_reconciliation(
        silver_df,
        gold_df,
):

    silver_count = len(
        silver_df
    )

    gold_count = int(
        gold_df["transaction_count"].sum()
    )

    silver_amount = round(
        silver_df["amount"].sum(),
        2,
    )

    gold_amount = round(
        gold_df["total_amount"].sum(),
        2,
    )

    if silver_count != gold_count:

        raise ValueError(
            "Silver and Gold transaction counts do not match"
        )

    if silver_amount != gold_amount:

        raise ValueError(
            "Silver and Gold transaction amounts do not match"
        )

    print(
        "PASS: Silver and Gold reconciliation"
    )

    print(
        f"      Transaction count: {silver_count}"
    )

    print(
        f"      Transaction amount: ₹{silver_amount:,.2f}"
    )


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    print(
        "Starting data-quality validation..."
    )

    print()

    silver_df = pd.read_csv(
        SILVER_FILE
    )

    gold_df = pd.read_csv(
        GOLD_DAILY_FILE
    )

    print(
        f"Silver records: {len(silver_df)}"
    )

    print()

    check_required_columns(
        silver_df
    )

    check_transaction_ids(
        silver_df
    )

    check_amounts(
        silver_df
    )

    check_currency(
        silver_df
    )

    check_status(
        silver_df
    )

    check_payment_channel(
        silver_df
    )

    check_gold_reconciliation(
        silver_df,
        gold_df,
    )

    print()
    print(
        "======================================"
    )
    print(
        "ALL DATA-QUALITY CHECKS PASSED"
    )
    print(
        "======================================"
    )


if __name__ == "__main__":
    main()