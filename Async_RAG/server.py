from dotenv import load_dotenv

from fastapi import FastAPI , Query
from .queues.worker import process_query
from .client.rq_client import queue

load_dotenv()


app = FastAPI()

@app.get("/")
def root():
    return {"staus": "Server is up and running!"}


@app.post("/chat")
def chat(query: str = Query(..., description="The query to ask the AI")):
    # Enqueue the query for processing
    job = queue.enqueue(process_query, query)
    
    # # Wait for the job to finish and get the result
    # result = job.result  # This will block until the job is finished
    # return {"response": result}

    # Return the job ID to the client so they can check the status later    
    return {"status": "Your query has been received and is being processed.", "job_id": job.id}


@app.get("/job_status/{job_id}")
def job_status(job_id: str):
    job = queue.fetch_job(job_id=job_id)
    result = job.return_value()
    return {"status": job.get_status(), "result": job.result}