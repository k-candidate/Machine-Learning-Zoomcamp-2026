"""FastAPI service for customer churn predictions."""

import pickle
from typing import Literal
from pydantic import BaseModel, Field


from fastapi import FastAPI
import uvicorn



class Customer(BaseModel):
    """Customer features accepted by the prediction endpoint."""

    gender: Literal["male", "female"]
    seniorcitizen: Literal[0, 1]
    partner: Literal["yes", "no"]
    dependents: Literal["yes", "no"]
    phoneservice: Literal["yes", "no"]
    multiplelines: Literal["no", "yes", "no_phone_service"]
    internetservice: Literal["dsl", "fiber_optic", "no"]
    onlinesecurity: Literal["no", "yes", "no_internet_service"]
    onlinebackup: Literal["no", "yes", "no_internet_service"]
    deviceprotection: Literal["no", "yes", "no_internet_service"]
    techsupport: Literal["no", "yes", "no_internet_service"]
    streamingtv: Literal["no", "yes", "no_internet_service"]
    streamingmovies: Literal["no", "yes", "no_internet_service"]
    contract: Literal["month-to-month", "one_year", "two_year"]
    paperlessbilling: Literal["yes", "no"]
    paymentmethod: Literal[
        "electronic_check",
        "mailed_check",
        "bank_transfer_(automatic)",
        "credit_card_(automatic)",
    ]
    tenure: int = Field(..., ge=0)
    monthlycharges: float = Field(..., ge=0.0)
    totalcharges: float = Field(..., ge=0.0)


class PredictResponse(BaseModel):
    """Churn probability and threshold-based classification."""

    churn_probability: float
    churn: bool


# Load the trained preprocessing-and-model pipeline once when the service starts.
app = FastAPI(title="customer-churn-prediction")

with open('model.bin', 'rb') as f_in:
    pipeline = pickle.load(f_in)


def predict_single(customer):
    """Return the model's churn probability for one customer record."""
    result = pipeline.predict_proba(customer)[0, 1]
    return float(result)


@app.post("/predict")
def predict(customer: Customer) -> PredictResponse:
    """Predict churn and classify probabilities of 0.5 or higher as churn."""
    prob = predict_single(customer.model_dump())

    return PredictResponse(
        churn_probability=prob,
        churn=prob >= 0.5
    )


if __name__ == "__main__":
    # Allow requests from outside the local machine when running the service.
    uvicorn.run(app, host="0.0.0.0", port=9696)
