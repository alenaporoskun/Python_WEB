from sqlalchemy.orm import Session
import models
from schemas.schemas import ContactCreate


def create_contact(db: Session, contact: ContactCreate):
    db_contact = models.Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact
