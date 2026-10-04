from google.cloud import aiplatform
import time

class BatchPredictor:
    """Executes the 1,000-run test matrix using Vertex AI Batch Prediction."""
    
    def __init__(self, project: str, location: str):
        aiplatform.init(project=project, location=location)

    def trigger_matrix_test_suite(self, test_dataset_gcs_uri: str, output_gcs_uri: str):
        print("Launching 1,000 parallel test renders on Vertex AI Batch Prediction...")
        
        batch_job = aiplatform.BatchPredictionJob.create(
            job_display_name="google-flowx-1000-matrix-test",
            model_name="projects/google-flowx/locations/us-central1/models/veo-nnl-evaluator",
            instances_format="jsonl",
            gcs_source=test_dataset_gcs_uri,
            gcs_destination_output_uri_prefix=output_gcs_uri,
            machine_type="g2-standard-8",
            accelerator_type="NVIDIA_L4",
            accelerator_count=1
        )
        
        print(f"Batch Job ID: {batch_job.resource_name} initialized. Awaiting completion...")
        return batch_job
