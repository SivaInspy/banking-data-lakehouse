import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

BRONZE_FILE = Path(
    "data/bronze/transactions.csv"
)

SILVER_DIR = Path(
    "data/silver"
)

QUARANTINE_DIR = Path(
    "data/quarantine"
)


VALID_TRANSACTION_STATUSES = {
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

VALID_CURRENCIES = {
    "INR",
}


# ---------------------------------------------------------
# Validation
# ---------------------------------------------------------

def validate_transactions(df):

    quarantine_reason = pd.Series(
        "",
        index=df.index,
        dtype="object",
    )

    # Required fields
    required_columns = [
        "transaction_id",
        "account_id",
        "customer_id",
        "merchant_id",
    ]

    for column in required_columns:

        invalid = (
                df[column].isna()
                | (df[column].astype(str).str.strip() == "")
        )

        quarantine_reason.loc[invalid] += (
            f"{column}_missing;"
        )

    # Amount validation
    invalid_amount = (
            pd.to_numeric(
                df["amount"],
                errors="coerce",
            ).isna()
            | (
                    pd.to_numeric(
                        df["amount"],
                        errors="coerce",
                    )
                    <= 0
            )
    )

    quarantine_reason.loc[invalid_amount] += (
        "invalid_amount;"
    )

    # Currency validation
    invalid_currency = ~df[
        "currency"
    ].isin(VALID_CURRENCIES)

    quarantine_reason.loc[invalid_currency] += (
        "invalid_currency;"
    )

    # Transaction status validation
    invalid_status = ~df[
        "transaction_status"
    ].isin(VALID_TRANSACTION_STATUSES)

    quarantine_reason.loc[invalid_status] += (
        "invalid_transaction_status;"
    )

    # Payment channel validation
    invalid_channel = ~df[
        "payment_channel"
    ].isin(VALID_PAYMENT_CHANNELS)

    quarantine_reason.loc[invalid_channel] += (
        "invalid_payment_channel;"
    )

    # Duplicate transaction ID
    duplicate_transaction = df[
        "transaction_id"
    ].duplicated(
        keep="first"
    )

    quarantine_reason.loc[
        duplicate_transaction
    ] += "duplicate_transaction;"

    df["quarantine_reason"] = (
        quarantine_reason
    )

    return df


# ---------------------------------------------------------
# Silver Transformation
# ---------------------------------------------------------

def transform_to_silver():

    SILVER_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    QUARANTINE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(
        "Reading Bronze transaction data..."
    )

    df = pd.read_csv(
        BRONZE_FILE
    )

    print(
        f"Bronze records: {len(df)}"
    )

    # Convert amount to numeric
    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce",
    )

    # Convert transaction date
    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"],
        errors="coerce",
    )

    # Validate
    df = validate_transactions(
        df
    )

    # Separate valid and invalid records
    quarantine_mask = (
            df["quarantine_reason"] != ""
    )

    quarantine_df = df[
        quarantine_mask
    ].copy()

    silver_df = df[
        ~quarantine_mask
    ].copy()

    # Remove technical validation column
    silver_df = silver_df.drop(
        columns=["quarantine_reason"]
    )

    # Write Silver
    silver_file = (
            SILVER_DIR
            / "transactions.csv"
    )

    silver_df.to_csv(
        silver_file,
        index=False,
    )

    # Write Quarantine
    quarantine_file = (
            QUARANTINE_DIR
            / "transactions_quarantine.csv"
    )

    quarantine_df.to_csv(
        quarantine_file,
        index=False,
    )

    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------

    print()
    print(
        "Silver transformation completed."
    )

    print(
        f"Bronze records      : {len(df)}"
    )

    print(
        f"Silver records      : {len(silver_df)}"
    )

    print(
        f"Quarantine records  : {len(quarantine_df)}"
    )

    print()

    print(
        "Quarantine reasons:"
    )

    print(
        quarantine_df[
            "quarantine_reason"
        ].value_counts()
    )

    print()

    print(
        f"Silver output     : {silver_file.resolve()}"
    )

    print(
        f"Quarantine output : {quarantine_file.resolve()}"
    )


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":

    transform_to_silver()