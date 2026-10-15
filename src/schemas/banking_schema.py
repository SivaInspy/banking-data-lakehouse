CUSTOMER_COLUMNS = [
    "customer_id",
    "customer_name",
    "date_of_birth",
    "gender",
    "city",
    "state",
    "country",
    "customer_segment",
    "registration_date",
]

ACCOUNT_COLUMNS = [
    "account_id",
    "customer_id",
    "account_type",
    "account_status",
    "account_open_date",
    "branch_code",
    "current_balance",
]

TRANSACTION_COLUMNS = [
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
]

MERCHANT_COLUMNS = [
    "merchant_id",
    "merchant_name",
    "merchant_category",
    "city",
    "state",
    "country",
]