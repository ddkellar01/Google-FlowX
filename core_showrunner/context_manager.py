import redis
import json

class ContextManager:
    """Maintains scene-to-scene memory to ensure continuity across thousands of generated clips."""
    
    def __init__(self, redis_host='localhost', redis_port=6379):
        self.cache = redis.Redis(host=redis_host, port=redis_port, db=0)

    def save_scene_state(self, scene_id, characters, environment, lighting, inventory):
        state = {
            "characters": characters,
            "environment": environment,
            "lighting": lighting,
            "inventory": inventory # E.g., ensuring a character keeps the hat they put on in scene 4
        }
        self.cache.set(f"scene_state:{scene_id}", json.dumps(state))

    def get_previous_scene_state(self, current_scene_id):
        prev_scene_id = current_scene_id - 1
        data = self.cache.get(f"scene_state:{prev_scene_id}")
        return json.loads(data) if data else None
