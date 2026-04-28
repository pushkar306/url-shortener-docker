import os
import random
import string
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel, HttpUrl

# 1. DB Configurantion

DATABASE_URL = os.getenv("DATABASE_URL","postgresql://user:password@db:5432/shortener")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()

# 2. DB Model

class URLItem(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_id = Column(String, unique=True, index=True, nullable=False)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortner API")

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

class URLCreate(BaseModel):
    url : HttpUrl

def generate_short_id(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

# API Endpoints

@app.post("/shorten")
def create_short_url(item:URLCreate, db: Session = Depends(get_db)):
    short_id = generate_short_id()

    while db.query(URLItem).filter(URLItem.short_id==short_id).first():
        short_id = generate_short_id()  

    db_url = URLItem(original_url = str(item.url) , short_id=short_id)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    return {
        "short_url": f"http://localhost:8000/{short_id}",
        "original_url": str(item.url)
    }

@app.get("/{short_id}")
def redirect_to_url(short_id: str, db: Session = Depends(get_db)):
    db_url = db.query(URLItem).filter(URLItem.short_id == short_id).first()
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url=str(db_url.original_url))