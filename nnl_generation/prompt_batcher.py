from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

class PromptBatcher:
    """Groups visually similar scene prompts together to maximize GPU VRAM caching of LoRAs and context."""
    
    def __init__(self):
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')

    def optimize_render_queue(self, prompt_list: list, num_gpu_nodes: int) -> dict:
        print(f"Embedding {len(prompt_list)} prompts to find visual similarities...")
        embeddings = self.encoder.encode(prompt_list)
        
        # Cluster prompts so identical environments render on the same node
        kmeans = KMeans(n_clusters=num_gpu_nodes, random_state=42)
        clusters = kmeans.fit_predict(embeddings)
        
        batched_queues = {i: [] for i in range(num_gpu_nodes)}
        for prompt, cluster_id in zip(prompt_list, clusters):
            batched_queues[cluster_id].append(prompt)
            
        print(f"Optimized batching complete. Distributed across {num_gpu_nodes} nodes.")
        return batched_queues
