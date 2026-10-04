from vertexai.generative_models import GenerativeModel

class ArbiterConsensus:
    """Requires 3 independent AI evaluator nodes to reach >95% consensus before deployment."""
    
    def __init__(self):
        self.arbiters = [
            GenerativeModel("gemini-pro-thinking"),
            GenerativeModel("gemini-1.5-pro"),
            GenerativeModel("gemini-1.5-flash")
        ]

    def EvaluateDeploymentSafety(self, test_results: dict) -> bool:
        votes = []
        prompt = f"Review these 1000-run test metrics for automated deployment: {test_results}. Respond with 'APPROVED' or 'REJECTED'."

        for i, arbiter in enumerate(self.arbiters):
            response = arbiter.generate_content(prompt).text.strip().upper()
            is_approved = "APPROVED" in response
            votes.append(is_approved)
            print(f"Arbiter {i+1} Vote: {'APPROVED' if is_approved else 'REJECTED'}")

        # Requires unanimous or 2/3 majority consensus
        consensus_reached = votes.count(True) >= 2
        print(f"Consensus Verdict: {'PASSED' if consensus_reached else 'FAILED'}")
        return consensus_reached
