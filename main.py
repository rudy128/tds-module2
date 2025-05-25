import json
from fastapi import FastAPI, Query
from typing import Optional, List

app = FastAPI()

# Load the student data from the JSON file
def load_students():
    with open("q-vercel-python.json", "r") as f:
        return json.load(f)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/api")
def get_api_params(
    name: Optional[List[str]] = Query(None, description="Filter by name(s)"),
):
    """
    Get filtered student data based on query parameters.
    """
    students = load_students()
    list= []
    # Filter by name if provided (can be multiple names)
    if name:
        for i in name:
            for j in students:
                if j["name"] == i:
                    list.append(j["marks"])
        
    # Extract just the marks for the response in the original order
    # marks = [student["marks"] for student in filtered_students]
    
    return {"marks": list}