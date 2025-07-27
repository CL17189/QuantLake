# workflows/prefect_pipeline.py

from prefect import flow, task
from prefect.deployments import DeploymentSpec
from prefect.orion.schemas.schedules import IntervalSchedule
from prefect_email import EmailServerCredentials, email_send_message
from datetime import timedelta
import subprocess

@task
def run_data_ingestion():
    subprocess.run(["python", "ingestion/fetch_stock_data.py"], check=True)

@task
def run_spark_etl():
    subprocess.run(["python", "etl/spark_job.py"], check=True)

@flow(name="Finance Data Pipeline")
def finance_pipeline():
    try:
        fetch = run_data_ingestion()
        etl = run_spark_etl(wait_for=[fetch])
    except Exception as e:
        # ⚠️ 发送失败通知
        creds = EmailServerCredentials.load("email-alert")
        email_send_message(
            email_server_credentials=creds,
            subject="🚨 Finance ETL Failed!",
            msg=f"ETL Flow failed: {str(e)}",
            email_to="your_email@example.com"
        )
        raise
# ✅ 每24小时运行一次
DeploymentSpec(
    flow=finance_pipeline,
    name="daily-finance-pipeline",
    schedule=IntervalSchedule(interval=timedelta(days=1)),
    tags=["daily"]
)
