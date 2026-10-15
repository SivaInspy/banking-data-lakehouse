
import pandas as pd

from src.transformers.silver_transformation import validate_transactions
from src.transformers.gold_transformation import (
    create_daily_summary,
    create_city_summary,
    create_category_summary,
    create_customer_summary,
)
from src.quality.validate_pipeline import check_gold_reconciliation


def test_banking_pipeline_end_to_end():
    """Test valid and invalid transactions through Silver and Gold."""

    transactions = pd.DataFrame(
        {
            "transaction_id": [
                "TXN001",
                "TXN002",
                "TXN003",
                "TXN004",
                "TXN004",
            ],
            "account_id": [
                "ACC001",
                "ACC002",
                "ACC003",
                "ACC004",
                "ACC004",
            ],
            "customer_id": [
                "CUS001",
                "CUS002",
                "CUS003",
                "CUS004",
                "CUS004",
            ],
            "merchant_id": [
                "MER001",
                "MER002",
                "MER001",
                "MER002",
                "MER002",
            ],
            "transaction_date": pd.to_datetime(
                [
                    "2026-10-01",
                    "2026-10-01",
                    "2026-10-02",
                    "2026-10-02",
                    "2026-10-02",
                ]
            ),
            "amount": [100.00, 250.00, 150.00, 300.00, 300.00],
            "currency": ["INR", "INR", "INR", "INR", "INR"],
            "payment_channel": [
                "UPI",
                "CARD",
                "NET_BANKING",
                "ATM",
                "ATM",
            ],
            "transaction_status": [
                "SUCCESS",
                "FAILED",
                "PENDING",
                "SUCCESS",
                "SUCCESS",
            ],
            "city": [
                "Bengaluru",
                "Chennai",
                "Bengaluru",
                "Chennai",
                "Chennai",
            ],
        }
    )

    # Silver: validate records and separate valid from invalid.
    validated = validate_transactions(transactions.copy())
    invalid_mask = validated["quarantine_reason"] != ""

    silver = validated.loc[~invalid_mask].drop(
        columns=["quarantine_reason"]
    ).copy()
    quarantine = validated.loc[invalid_mask].copy()

    assert len(transactions) == 5
    assert len(silver) == 4
    assert len(quarantine) == 1
    assert quarantine["quarantine_reason"].str.contains(
        "duplicate_transaction;"
    ).all()

    # Gold: create all four aggregate datasets.
    merchants = pd.DataFrame(
        {
            "merchant_id": ["MER001", "MER002"],
            "merchant_category": ["Grocery", "Retail"],
        }
    )

    daily = create_daily_summary(silver.copy())
    city = create_city_summary(silver.copy())
    category = create_category_summary(silver.copy(), merchants)
    customer = create_customer_summary(silver.copy())

    # Reconcile transaction count and amount against Gold.
    check_gold_reconciliation(silver, daily)

    assert int(daily["transaction_count"].sum()) == 4
    assert round(daily["total_amount"].sum(), 2) == 800.00
    assert round(silver["amount"].sum(), 2) == 800.00

    assert set(city["city"]) == {"Bengaluru", "Chennai"}
    assert set(category["merchant_category"]) == {"Grocery", "Retail"}
    assert len(customer) == 4
