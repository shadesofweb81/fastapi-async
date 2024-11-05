# app/main.py
import asyncio
from fastapi import FastAPI, Depends, HTTPException
import psycopg
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models import Item, SQLModel
from database import engine, get_session
from routes import itemcurd
import uvicorn
import sys

app = FastAPI()

# Register the router
app.include_router(itemcurd.router)

# Create tables on startup
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def main():

    async with await psycopg.AsyncConnection.connect("dbname=db1 user=postgres password=password host=127.0.0.1 port=5432") as con:
        async with con.cursor() as cur:
            print(await (await cur.execute('select 1 a')).fetchall())

if __name__ == '__main__':

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())

if __name__ == "__main__":    
    uvicorn.run(app, host="0.0.0.0", port=8001)