# FastAPI-insurance-project
# Insurance Premium Prediction API

This project provides a REST API built with **FastAPI** that predicts insurance premium categories based on personal and lifestyle data.

The API uses a **scikit-learn machine learning model** to categorize users into different insurance risk groups based on features like:

- Age and age group
- BMI (calculated from weight and height)
- Lifestyle risk (smoking and BMI)
- City tier
- Income (in LPA)
- Occupation

---

## Features

- **FastAPI backend** for quick API responses
- **Pydantic models** for input validation and computed fields
- Predicts insurance premium categories in real-time
- Handles categorical and numerical features

---

## Example Usage

**POST /predict**

```json
{
  "age": 30,
  "weight": 75,
  "height": 1.75,
  "income_lpa": 10,
  "smoker": "no",
  "city": "Delhi",
  "occupation": "private_job"
}
