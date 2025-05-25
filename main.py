import json
import os
from fastapi import FastAPI, Query, HTTPException
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=False,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Load the student data from the JSON file
def load_students():
    try:
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct path to JSON file
        json_path = os.path.join(current_dir, "q-vercel-python.json")
        
        with open(json_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # Try relative path as fallback
        try:
            with open("q-vercel-python.json", "r") as f:
                return json.load(f)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Could not load student data: {str(e)}")
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Invalid JSON format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading data: {str(e)}")

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
    result = []
    # Filter by name if provided (can be multiple names)
    if name:
        for i in name:
            for j in students:
                if j["name"] == i:
                    result.append(j["marks"])
    
    return {"marks": result}