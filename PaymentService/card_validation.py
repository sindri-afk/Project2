'''
Kortanúmer er skipt upp sem
Luhn algorithm notaður til að validate-a PAN
Month expiration þarf að vera 1 - 12
Year expiration þarf að vera 4 stafa tala
CVC ætti að vera þriggja stafa tala
'''
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class CreditCard(BaseModel):
    pass



class CardValidator:
    def __init__(self, cardnumber) -> None:
        self.cardnumber = cardnumber
    
    def validate_card_number(self):

        pan = buyer['cardNumber']