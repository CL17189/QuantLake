from workflows.prefect_pipeline import run_data_ingestion

def test_ingestion_runs():
    try:
        run_data_ingestion()
    except Exception as e:
        assert False, f"Data ingestion failed with error: {e}"