from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Google-FlowX Gateway API", version="2.0")

class RenderRequest(BaseModel):
    movie_title: str
    concept_prompt: str
    target_duration_minutes: int = 120

@app.get("/healthz")
def health_check():
    return {"status": "ok", "pipeline": "Google-FlowX Online"}

@app.post("/api/v1/movie/generate")
def start_movie_generation(request: RenderRequest, background_tasks: BackgroundTasks):
    if request.target_duration_minutes < 1:
        raise HTTPException(status_code=400, detail="Duration must be at least 1 minute.")
    
    # Trigger Airflow Orchestrator DAG in background
    background_tasks.add_task(print, f"Triggering DAG for {request.movie_title}")
    return {"message": "Movie rendering workflow queued successfully", "movie_title": request.movie_title}
