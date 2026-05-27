class BigQueryWarehouse:
    def __init__(self):
        self.project_id = os.getenv("GCP_PROJECT_ID")
        self.dataset_id = "guardrail_analytics"
        self.table_id = "llm_interaction_logs"
        
        if self.project_id:
            # Setting credentials=None forces the client to automatically look 
            # for your secure 'gcloud auth' terminal session! Keyless and secure.
            self.client = bigquery.Client(project=self.project_id, credentials=None)
            print("[GCP Warehouse]: Connected safely using Application Default Credentials.")
        else:
            self.client = None
            print("[GCP Warehouse Warning]: Missing GCP_PROJECT_ID environment variable.")