from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from datetime import datetime, timedelta

from models.models import Contact  
from schemas.schemas import ContactCreate


def add_contact(db: Session, contact: ContactCreate):
    db_contact = Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact



def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()

# def get_contacts(db: Session, skip: int = 0, limit: int = 10):
#     return db.query(Contact).offset(skip).limit(limit).all()

def get_contacts(db: Session, skip: int = 0, limit: int = 10, query: str = None):
    if query:
        return db.query(Contact).filter(
            or_(
                Contact.first_name.ilike(f"%{query}%"),
                Contact.last_name.ilike(f"%{query}%"),
                Contact.email.ilike(f"%{query}%")
            )
        ).offset(skip).limit(limit).all()
    return db.query(Contact).offset(skip).limit(limit).all()


def refresh_contact(db: Session, contact_id: int, contact: ContactCreate):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    for key, value in contact.model_dump().items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def remove_contact(db: Session, contact_id: int):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    db.delete(db_contact)
    db.commit()
    return db_contact


def get_upcoming_birthdays(db: Session):
    today = datetime.now()
    end_date = today + timedelta(days=7)
    return db.query(Contact).filter(
        func.extract('month', Contact.birthday) == end_date.month,
        func.extract('day', Contact.birthday) >= today.day,
        func.extract('day', Contact.birthday) <= (end_date).day
    ).all()