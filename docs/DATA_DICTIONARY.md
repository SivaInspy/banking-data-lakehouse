# Banking Data Dictionary

This document defines the business and technical meaning of the datasets used in the Cloud Banking Data Lakehouse project.

---

## 1. Customers

| Column | Description |
|---|---|
| customer_id | Unique identifier for the customer |
| customer_name | Full name of the customer |
| date_of_birth | Customer date of birth |
| gender | Customer gender |
| city | Customer city |
| state | Customer state |
| country | Customer country |
| customer_segment | Business segment assigned to the customer |
| registration_date | Date when the customer registered |

---

## 2. Accounts

| Column | Description |
|---|---|
| account_id | Unique identifier for the bank account |
| customer_id | Identifier of the customer who owns the account |
| account_type | Type of bank account |
| account_status | Current status of the account |
| account_open_date | Date when the account was opened |
| branch_code | Branch associated with the account |
| current_balance | Current account balance |

---

## 3. Transactions

| Column | Description |
|---|---|
| transaction_id | Unique identifier for the transaction |
| account_id | Account associated with the transaction |
| customer_id | Customer associated with the transaction |
| merchant_id | Merchant involved in the transaction |
| transaction_date | Date and time of the transaction |
| transaction_type | Type of transaction |
| amount | Transaction amount |
| currency | Currency used for the transaction |
| payment_channel | Channel through which the payment was made |
| transaction_status | Status of the transaction |
| city | City where the transaction occurred |

---

## 4. Merchants

| Column | Description |
|---|---|
| merchant_id | Unique identifier for the merchant |
| merchant_name | Name of the merchant |
| merchant_category | Business category of the merchant |
| city | Merchant city |
| state | Merchant state |
| country | Merchant country |