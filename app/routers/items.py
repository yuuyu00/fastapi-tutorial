from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session

from app.models.item import Item, ItemCreate, ItemUpdate
from app.models.database import ItemDB
from app.services import item_service
from app.database import get_db

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Item not found"}},
)

@router.get("/", response_model=List[Item])
async def read_items(db: Session = Depends(get_db)):
    return item_service.get_items(db)

@router.post("/", response_model=Item, status_code=201)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    return item_service.create_item(db, item)

@router.get("/{item_id}", response_model=Item)
async def read_item(item_id: int, db: Session = Depends(get_db)):
    item = item_service.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    updated_item = item_service.update_item(db, item_id, item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    success = item_service.delete_item(db, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")