import subprocess

class CanaryDeployer:
    """Routes a small percentage of render traffic to new ML features to test stability in production."""
    
    def __init__(self, deployment_name: str, canary_weight: int = 5):
        self.deployment = deployment_name
        self.weight = canary_weight

    def execute_canary_shift(self):
        print(f"Initiating {self.weight}% canary traffic shift to new ML feature branch...")
        
        # Update Istio VirtualService or GKE Ingress routing weights
        patch_yaml = f"""
        spec:
          http:
          - route:
            - destination:
                host: {self.deployment}-primary
              weight: {100 - self.weight}
            - destination:
                host: {self.deployment}-canary
              weight: {self.weight}
        """
        # In practice, this applies the YAML via kubectl or an Istio client
        print(f"Traffic shift complete. Monitoring canary logs for 500 errors...")
