from prefect import flow, task
from prefect_email import EmailServerCredentials, email_send_message
import subprocess

@task
def run_data_ingestion():
    subprocess.run(["python3", "../ingestion/fetch_stock_data.py"], check=True)

@task
def run_spark_etl():
    subprocess.run(["python3", "../etl/spark_job.py"], check=True)

@flow(name="Finance Data Pipeline")
def finance_pipeline():
    try:
        fetch = run_data_ingestion()
        etl = run_spark_etl(wait_for=[fetch])
    except Exception as e:
        creds = EmailServerCredentials.load("email-alert")
        email_send_message(
            email_server_credentials=creds,
            subject="🚨 Finance ETL Failed!",
            msg=f"ETL Flow failed: {str(e)}",
            email_to="your_email@example.com"
        )
        raise

if __name__ == "__main__":
    finance_pipeline()



