import redis
from google.cloud import logging

class StateRecoveryEngine:
    """Fault-tolerance monitor. Resumes rendering exactly where it left off if a GKE node dies."""
    
    def __init__(self, redis_url="redis://flowx-cache:6379/1"):
        self.db = redis.from_url(redis_url)
        self.logger = logging.Client().logger("flowx-recovery")

    def log_completed_chunk(self, movie_id: str, chunk_index: int):
        self.db.sadd(f"completed_chunks:{movie_id}", chunk_index)

    def get_missing_chunks(self, movie_id: str, total_chunks: int) -> list:
        completed = self.db.smembers(f"completed_chunks:{movie_id}")
        completed_indices = {int(x) for x in completed}
        
        missing = [i for i in range(total_chunks) if i not in completed_indices]
        if missing:
            self.logger.warning(f"Detected {len(missing)} failed/missing chunks. Re-queueing...")
            
        return missing
