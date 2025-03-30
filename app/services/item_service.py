from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.database import ItemDB
from app.models.item import ItemCreate, ItemUpdate

def get_items(db: Session) -> List[ItemDB]:
  return db.query(ItemDB).all()

def get_item(db: Session, item_id: int) -> Optional[ItemDB]:
  return db.query(ItemDB).filter(ItemDB.id == item_id).first()

def create_item(db: Session, item: ItemCreate) -> ItemDB:
  db_item = ItemDB(**item.model_dump())
  db.add(db_item)
  db.commit()
  db.refresh(db_item)
  return db_item

def update_item(db: Session, item_id: int, item: ItemUpdate) -> Optional[ItemDB]:
  db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
  if db_item is None:
    return None
  
  update_data = item.model_dump(exclude_unset=True)
  for key, value in update_data.items():
    setattr(db_item, key, value)

  db.commit()
  db.refresh(db_item)
  return db_item

def delete_item(db: Session, item_id: int) -> bool:
  db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
  if db_item is None:
    return False
  
  db.delete(db_item)
  db.commit()
  return True