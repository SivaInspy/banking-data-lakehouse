import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

SILVER_TRANSACTIONS_FILE = Path(
    "data/silver/transactions.csv"
)

BRONZE_MERCHANTS_FILE = Path(
    "data/bronze/merchants.csv"
)

GOLD_DIR = Path(
    "data/gold"
)


# ---------------------------------------------------------
# Utility
# ---------------------------------------------------------

def save_gold_dataset(df, file_name):

    output_file = GOLD_DIR / file_name

    df.to_csv(
        output_file,
        index=False,
    )

    print(
        f"Created: {output_file}"
    )


# ---------------------------------------------------------
# Daily Transaction Summary
# ---------------------------------------------------------

def create_daily_summary(transactions):

    transactions["transaction_day"] = (
        transactions["transaction_date"]
        .dt.date
    )

    daily_summary = (
        transactions
        .groupby("transaction_day")
        .agg(
            transaction_count=(
                "transaction_id",
                "count",
            ),
            total_amount=(
                "amount",
                "sum",
            ),
            average_transaction_amount=(
                "amount",
                "mean",
            ),
        )
        .reset_index()
    )

    daily_summary["total_amount"] = (
        daily_summary["total_amount"]
        .round(2)
    )

    daily_summary[
        "average_transaction_amount"
    ] = (
        daily_summary[
            "average_transaction_amount"
        ].round(2)
    )

    daily_summary = daily_summary.sort_values(
        "transaction_day"
    )

    return daily_summary


# ---------------------------------------------------------
# City Summary
# ---------------------------------------------------------

def create_city_summary(transactions):

    city_summary = (
        transactions
        .groupby("city")
        .agg(
            transaction_count=(
                "transaction_id",
                "count",
            ),
            total_amount=(
                "amount",
                "sum",
            ),
            average_transaction_amount=(
                "amount",
                "mean",
            ),
        )
        .reset_index()
    )

    city_summary["total_amount"] = (
        city_summary["total_amount"]
        .round(2)
    )

    city_summary[
        "average_transaction_amount"
    ] = (
        city_summary[
            "average_transaction_amount"
        ].round(2)
    )

    city_summary = city_summary.sort_values(
        "total_amount",
        ascending=False,
    )

    return city_summary


# ---------------------------------------------------------
# Merchant Category Summary
# ---------------------------------------------------------

def create_category_summary(
        transactions,
        merchants,
):

    category_data = transactions.merge(
        merchants[
            [
                "merchant_id",
                "merchant_category",
            ]
        ],
        on="merchant_id",
        how="left",
    )

    category_summary = (
        category_data
        .groupby("merchant_category")
        .agg(
            transaction_count=(
                "transaction_id",
                "count",
            ),
            total_amount=(
                "amount",
                "sum",
            ),
            average_transaction_amount=(
                "amount",
                "mean",
            ),
        )
        .reset_index()
    )

    category_summary["total_amount"] = (
        category_summary["total_amount"]
        .round(2)
    )

    category_summary[
        "average_transaction_amount"
    ] = (
        category_summary[
            "average_transaction_amount"
        ].round(2)
    )

    category_summary = (
        category_summary.sort_values(
            "total_amount",
            ascending=False,
        )
    )

    return category_summary


# ---------------------------------------------------------
# Customer Summary
# ---------------------------------------------------------

def create_customer_summary(transactions):

    customer_summary = (
        transactions
        .groupby("customer_id")
        .agg(
            transaction_count=(
                "transaction_id",
                "count",
            ),
            total_amount=(
                "amount",
                "sum",
            ),
            average_transaction_amount=(
                "amount",
                "mean",
            ),
        )
        .reset_index()
    )

    customer_summary["total_amount"] = (
        customer_summary["total_amount"]
        .round(2)
    )

    customer_summary[
        "average_transaction_amount"
    ] = (
        customer_summary[
            "average_transaction_amount"
        ].round(2)
    )

    customer_summary = (
        customer_summary.sort_values(
            "total_amount",
            ascending=False,
        )
    )

    return customer_summary


# ---------------------------------------------------------
# Main Gold Pipeline
# ---------------------------------------------------------

def main():

    GOLD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(
        "Reading Silver transactions..."
    )

    transactions = pd.read_csv(
        SILVER_TRANSACTIONS_FILE
    )

    merchants = pd.read_csv(
        BRONZE_MERCHANTS_FILE
    )

    transactions["transaction_date"] = (
        pd.to_datetime(
            transactions[
                "transaction_date"
            ],
            errors="coerce",
        )
    )

    transactions["amount"] = pd.to_numeric(
        transactions["amount"],
        errors="coerce",
    )

    print(
        f"Silver transactions: {len(transactions)}"
    )

    print(
        f"Merchants: {len(merchants)}"
    )

    print()

    # -----------------------------------------------------
    # Create Gold datasets
    # -----------------------------------------------------

    daily_summary = create_daily_summary(
        transactions.copy()
    )

    city_summary = create_city_summary(
        transactions.copy()
    )

    category_summary = create_category_summary(
        transactions.copy(),
        merchants,
    )

    customer_summary = create_customer_summary(
        transactions.copy()
    )

    # -----------------------------------------------------
    # Save datasets
    # -----------------------------------------------------

    save_gold_dataset(
        daily_summary,
        "daily_transaction_summary.csv",
    )

    save_gold_dataset(
        city_summary,
        "transaction_summary_by_city.csv",
    )

    save_gold_dataset(
        category_summary,
        "transaction_summary_by_category.csv",
    )

    save_gold_dataset(
        customer_summary,
        "customer_transaction_summary.csv",
    )

    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------

    print()
    print(
        "Gold transformation completed."
    )

    print(
        f"Daily summary records    : {len(daily_summary)}"
    )

    print(
        f"City summary records     : {len(city_summary)}"
    )

    print(
        f"Category summary records : {len(category_summary)}"
    )

    print(
        f"Customer summary records : {len(customer_summary)}"
    )


# ---------------------------------------------------------
# Entry Point
# ---------------------------------------------------------

if __name__ == "__main__":
    main()