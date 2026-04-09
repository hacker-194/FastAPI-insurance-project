import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal
from fastapi.responses import JSONResponse
import pickle

# Load model
with open("model.plk", "rb") as f:
    model = pickle.load(f)

app = FastAPI()

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    
]

class User(BaseModel):
    age: int = Field(..., gt=0, lt=120)
    weight: int = Field(..., gt=0, description="Weight of the patient in kg")
    height: float = Field(..., gt=0, description="Height of the patient in meters")
    income_lpa: float
    smoker: Literal["yes", "no"]
    city: str
    occupation: Literal["retired","freelancer","students","government_job","business_owner","unemployed","private_job"]

    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)

    @property
    def lifestyle_risk(self) -> str:
        if self.smoker == "yes" and self.bmi > 30:
            return "high"
        elif self.smoker == "yes" or self.bmi > 27:
            return "medium"
        else:
            return "low"

    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"

    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3

@app.post("/predict")
def predict_premium(data: User):
    input_df = pd.DataFrame([{
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }])
    
    prediction = model.predict(input_df)[0]

    return JSONResponse(status_code=200, content={"predicted_category": prediction})