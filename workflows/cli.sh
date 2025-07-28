prefect deployment build workflows/prefect_pipeline.py:finance_pipeline \
  --name daily-finance-pipeline \
  --schedule "R/2025-07-28T00:00:00Z/PT24H" \
  --tag daily
prefect deployment apply daily-finance-pipeline-deployment.yaml
prefect agent start
prefect deployment run daily-finance-pipeline/daily-finance-pipeline
`