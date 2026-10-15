# Cloud Banking Data Lakehouse

An end-to-end data engineering project that demonstrates how to build a cloud-based banking data lakehouse using AWS, Python, PySpark, SQL, and Terraform.

The platform processes synthetic banking transactions through Bronze, Silver, and Gold layers, applies data-quality rules, and publishes analytical datasets for reporting.

## Architecture

```text
Synthetic Banking CSV Data
            |
            v
      Amazon S3 - Raw
            |
            v
       AWS Glue Crawler
            |
            v
      AWS Glue Data Catalog
            |
            v
     AWS Glue ETL Job
            |
            v
    Bronze / Silver Layers
            |
            v
      Gold Transformation
            |
            v
      Gold Summary Tables
            |
            v
      AWS Glue Crawler
            |
            v
   Athena / Analytical Queries
```

The local Python pipeline provides a development and testing path for the same Bronze, Silver, and Gold processing concepts.

## Technology Stack

- **Cloud:** AWS
- **Storage:** Amazon S3
- **Data processing:** Python, pandas, PySpark, AWS Glue
- **Metadata:** AWS Glue Data Catalog
- **Analytics:** Amazon Athena
- **Infrastructure as Code:** Terraform
- **Testing:** pytest
- **CI/CD:** GitHub Actions
- **Querying:** SQL

## Data Pipeline

### Bronze

Ingests raw banking CSV files into the Bronze layer.

### Silver

Validates transaction records, including:

- Required transaction, account, customer, and merchant identifiers
- Positive transaction amounts
- Supported currencies
- Valid transaction statuses and payment channels
- Duplicate transaction identifiers

Invalid records are identified with quarantine reasons.

### Gold

Creates analytical summaries, including:

- Daily transaction counts, totals, and average amounts
- Transaction summaries by city
- Transaction summaries by merchant category
- Customer transaction summaries

## Data Quality and Testing

The repository includes automated tests for Silver validation, data-quality checks, and Gold daily aggregation.

Run the tests locally:

```powershell
python -m pip install -r requirements.txt
python -m pytest tests -v
```

The current test suite contains 15 tests.

## AWS Infrastructure

Terraform manages the existing S3 bucket, Glue Data Catalog database, crawlers, ETL jobs, workflow, and conditional triggers.

The project also uses EventBridge to start the Glue workflow following matching raw CSV uploads. Failure notifications and a dead-letter queue support operational monitoring.

Terraform configuration is located in `infrastructure/terraform`.

**Safety:** Review every Terraform plan before applying changes to AWS. The GitHub Actions CI workflow validates configuration but does not deploy infrastructure.

## Continuous Integration

GitHub Actions runs the following checks on pushes and pull requests:

- Python source compilation
- Automated pytest suite
- Terraform formatting
- Terraform initialization and validation

## Repository Structure

```text
.
├── .github/workflows/    # GitHub Actions
├── config/               # Pipeline configuration
├── data/raw/             # Synthetic input datasets
├── docs/                 # Data dictionary and documentation
├── glue/jobs/            # AWS Glue job scripts
├── infrastructure/
│   └── terraform/        # Infrastructure as Code
├── scripts/              # Utility scripts
├── sql/                  # Analytical SQL
├── src/
│   ├── generators/       # Synthetic data generation
│   ├── quality/          # Data-quality validation
│   ├── schemas/          # Data schemas
│   └── transformers/     # Bronze, Silver, and Gold processing
├── tests/                # Automated tests
├── requirements.txt
└── README.md
```

## Data Privacy

The project uses synthetic banking data for demonstration and testing. No real customer banking records should be committed to the repository.

## Project Status

The local processing pipeline, AWS Glue workflow, Terraform resource tracking, and initial automated tests are implemented. GitHub Actions CI is being prepared for validation before publication.

Further enhancements include expanded integration tests, production observability, and controlled deployment automation.