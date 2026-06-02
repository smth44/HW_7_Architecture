from fastapi import FastAPI
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

USD_TO_RUB = 100  # фиксированный курс


class Transaction(BaseModel):
    amount: float
    currency: str
    timestamp: str


@app.post("/risk")
def calculate_risk(transaction: Transaction):

    logging.info(
        f"Received transaction: amount={transaction.amount}, "
        f"currency={transaction.currency}, "
        f"timestamp={transaction.timestamp}"
    )

    amount_rub = transaction.amount

    if transaction.currency.upper() == "USD":
        amount_rub *= USD_TO_RUB

    if amount_rub < 10000:
        risk_level = "low"
    elif amount_rub <= 50000:
        risk_level = "medium"
    else:
        risk_level = "high"

    logging.info(
        f"Calculated risk: {risk_level}, amount_rub={amount_rub}"
    )

    return {"risk_level": risk_level}