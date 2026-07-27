from fastapi import FastAPI, Path, HTTPException ,Query 
from fastapi.responses import JSONResponse
from pydantic import BaseModel , Field , computed_field
from typing import Literal , Annotated
import json

app = FastAPI()

class patient(BaseModel):

    id :Annotated[str, Field(...,description="ID of the patients",examples=["P001"])]
    name : Annotated[str, Field(...,description="Name of the patients")]
    city :Annotated[str, Field(...,description="City of the patients")]
    age :Annotated[int,Field(..., gt = 0, lt = 120 , description="Age of the patients")]
    gender : Annotated[Literal["Male","Female","Others"], Field(...,description="Gender of the patients")]
    height: Annotated[float, Field(...,gt=0,description="Height of the patients")]
    weight: Annotated[float, Field(...,gt=0,description="Weight of the patients")]

    @computed_field
    @property
    def  bmi(self)->float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi < 18.5:
            return "UnderWeight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi <30 :
            return "Normal"
        else:
            return "Obese"


def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)

    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)

@app.get("/")
def hello():
    return {"message":"PatieNT Management system"}

@app.get("/about")
def about():
    return {"message":"Fully Functional Patient API"}

@app.get("/view")
def view():
    data = load_data()

    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id:str = Path(..., description = "Enter the id of patient", examples=["P001"])):
    
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail="Patient Not Found")

@app.get("/sort")
def sort_patients(sort_by : str = Query(..., description="Sorted On the basis of height , weight or BMI"), order:str = Query('asc',description="Sort in asc or desc order")):

    data = load_data()

    sort_by = sort_by.lower()
    order = order.lower()

    valid_fields = ['weight','height','bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f"Invalid Field Selected from {valid_fields}")

    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail="Invalid Order selected from asc or desc")
    
    sort_order = True if order =='desc' else False

    sorted_data = sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order )

    return sorted_data
    

@app.post("/create")
def create_patient(patient:patient):

    # load the existing data
    data = load_data()

    # check whether it exists in the existing database
    if patient.id in data:
        raise HTTPException(status_code=400,detail="Patient already Exists")
    
    # add the patients details in database
    data[patient.id] = patient.model_dump(exclude=['id'])

    # save the data in json
    save_data(data)

    return JSONResponse(status_code=201,content={"message":"Patients created Sucessfully"})