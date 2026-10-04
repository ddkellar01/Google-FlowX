import requests

class TaskRouter:
    """Routes distributed tasks between AI APIs, ML instances, and GKE GPU rendering nodes."""
    
    def __init__(self, api_gateway_url):
        self.gateway = api_gateway_url

    def route_payload(self, task_type, payload):
        endpoints = {
            "llm_inference": "/api/v1/llm/generate",
            "nnl_render": "/api/v1/nnl/render",
            "ml_upscale": "/api/v1/ml/upscale",
            "watermark_clean": "/api/v1/ml/unblend",
            "test_matrix": "/api/v1/qa/1000_test"
        }
        
        target = endpoints.get(task_type)
        if not target:
            raise ValueError(f"Unknown routing task: {task_type}")
            
        response = requests.post(f"{self.gateway}{target}", json=payload)
        return response.json()
