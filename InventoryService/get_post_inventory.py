from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
import json

app = FastAPI()

class Product(BaseModel):
    'merchantId' = int
    'productName' = str
    'price' = float
    'quantity' = int



class InventoryManagement:
    def __init__(self) -> None:
        self.FILE_PATH = 'inventory_repo.json'

    def get_all_inventory(self):
        with open(self.FILE_PATH, 'r') as file:
            return json.load(file)
    
    def save_inventory(self, inventory):
        with open(self.FILE_PATH, 'w') as file:
            json.dump(file, inventory, indent=4)

    def add_product(self, product: Product):
        inventory = self.get_all_inventory()
        inventory.append(product.dict())
        self.save_inventory(inventory)
        