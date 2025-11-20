
from fastapi import APIRouter, Request
from .service import calculate_income, calculate_percent

router = APIRouter(prefix="/sales_commission/v1", tags=["sales_commission"])

@router.get("/health")
async def health():
    return {"ok":True,"tiers":5}

@router.get("/percent/{count}")
async def percent(count:int):
    return {"percent": calculate_percent(count)}

@router.post("/calc")
async def calc(req:Request):
    data = await req.json()
    sales = int(data.get("sales",0))
    price = float(data.get("price",0.0))
    return calculate_income(sales, price)
