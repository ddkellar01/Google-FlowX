from vertexai.generative_models import GenerativeModel

class FeatureGenerator:
    """Autonomous AI engineer that writes code updates when test matrix scores fall below 95%."""
    
    def __init__(self):
        self.reasoning_engine = GenerativeModel("gemini-pro-thinking")

    def synthesize_bug_fix(self, failed_qa_reports: list, target_file_code: str) -> str:
        prompt = f"""
        The 1000-run test suite identified recurring rendering artifacts in the pipeline.
        QA Failure Summaries: {failed_qa_reports}
        
        Target Code File:
        ```python
        {target_file_code}
        ```
        
        Write an optimized, production-ready replacement for the Python code above that solves 
        these issues. Output ONLY valid Python code inside markdown backticks.
        """
        
        response = self.reasoning_engine.generate_content(prompt)
        return response.text.replace("```python", "").replace("```", "").strip()
