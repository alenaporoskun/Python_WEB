from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database.database import engine, get_db
from schemas.schemas import ContactCreate, Contact
from crud import add_contact, get_contacts, get_contact, refresh_contact
from crud import remove_contact, get_upcoming_birthdays
from models.models import Base  

app = FastAPI()

# Ініціалізація бази даних
Base.metadata.create_all(bind=engine)

# Create contact
@app.post("/contacts/", response_model=Contact)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    return add_contact(db=db, contact=contact)

# # Read contacts
# @app.get("/contacts/", response_model=List[Contact])
# def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     contacts = get_contacts(db=db, skip=skip, limit=limit)
#     return contacts

# Read contacts
@app.get("/contacts/", response_model=List[Contact])
def read_contacts(
    skip: int = 0, limit: int = 10, query: str = None, db: Session = Depends(get_db)
):
    return get_contacts(db=db, skip=skip, limit=limit, query=query)

# Read contact by ID
@app.get("/contacts/{contact_id}", response_model=Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = get_contact(db=db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

# Update contact
@app.put("/contacts/{contact_id}", response_model=Contact)
def update_contact(contact_id: int, contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = get_contact(db=db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return refresh_contact(db=db, contact_id=contact_id, contact=contact)

# Delete contact
@app.delete("/contacts/{contact_id}", response_model=Contact)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = get_contact(db=db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return remove_contact(db=db, contact_id=contact_id)

# Get contacts with upcoming birthdays
@app.get("/contacts/upcoming_birthdays/", response_model=List[Contact])
def get_upcoming_birthdays_list(db: Session = Depends(get_db)):
    return get_upcoming_birthdays(db=db)