from fastapi import FastAPI, HTTPException
from PaymentService.src.card_validation import CreditCard
import json
import os

app = FastAPI()
FILE_PATH = 'card_validations.json'

@app.post('/card_validations', response_model=str)
async def create_payment(credit_card: CreditCard):
    with open(FILE_PATH, 'w') as f:
        pass

