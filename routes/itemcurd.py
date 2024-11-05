from sqlmodel import  Session, select
from typing import List
from fastapi import  APIRouter, Depends, HTTPException
from models import *
from database import get_session
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

# Create an item
@router.post("/items/", response_model=Item)
async def create_item(item: Item, session: AsyncSession = Depends(get_session)):
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item

# Read all items
@router.get("/items/", response_model=list[Item])
async def read_items(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Item))
    return result.scalars().all()

# Read a single item by ID
@router.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int, session: AsyncSession = Depends(get_session)):
    item = await session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Update an item
@router.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, updated_item: Item, session: AsyncSession = Depends(get_session)):
    item = await session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.name = updated_item.name
    item.description = updated_item.description
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item

# Delete an item
@router.delete("/items/{item_id}")
async def delete_item(item_id: int, session: AsyncSession = Depends(get_session)):
    item = await session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    await session.delete(item)
    await session.commit()
    return {"detail": "Item deleted"}