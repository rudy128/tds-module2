import csv
import os
from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Configure CORS to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=False,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

class Student(BaseModel):
    studentId: int
    class_name: str

    class Config:
        fields = {
            'class_name': 'class'
        }

# Load the student data from the CSV file
def load_students():
    try:
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct path to CSV file
        csv_path = os.path.join(current_dir, "q-fastapi.csv")
        
        students = []
        with open(csv_path, "r") as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                students.append({
                    "studentId": int(row["studentId"]),
                    "class": row["class"]  # Using original column name from CSV
                })
        return students
    except FileNotFoundError:
        # Try relative path as fallback
        try:
            students = []
            with open("q-fastapi.csv", "r") as f:
                csv_reader = csv.DictReader(f)
                for row in csv_reader:
                    students.append({
                        "studentId": int(row["studentId"]),
                        "class": row["class"]
                    })
            return students
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Could not load student data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading data: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/api")
def get_students(
    class_param: Optional[List[str]] = Query(None, alias="class")
):
    """
    Get students data, optionally filtered by class.
    
    - If class query parameters are provided, only returns students in those classes
    - Returns data in the same row and column order as the CSV file
    """
    students = load_students()
    
    # Filter by class if the parameter is provided
    if class_param:
        students = [student for student in students if student["class"] in class_param]
    
    return {"students": students}