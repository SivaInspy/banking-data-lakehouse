import shutil
from pathlib import Path


RAW_DIR = Path("data/raw")
BRONZE_DIR = Path("data/bronze")


FILES_TO_INGEST = [
    "customers.csv",
    "accounts.csv",
    "merchants.csv",
    "transactions.csv",
]


def ingest_to_bronze():

    BRONZE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("Starting Bronze ingestion...")
    print()

    for file_name in FILES_TO_INGEST:

        source_file = RAW_DIR / file_name
        target_file = BRONZE_DIR / file_name

        if not source_file.exists():

            print(
                f"ERROR: Source file not found: {source_file}"
            )

            continue

        shutil.copy2(
            source_file,
            target_file,
        )

        print(
            f"Ingested: {file_name}"
        )

    print()
    print("Bronze ingestion completed.")
    print(
        f"Bronze location: {BRONZE_DIR.resolve()}"
    )


if __name__ == "__main__":
    ingest_to_bronze()