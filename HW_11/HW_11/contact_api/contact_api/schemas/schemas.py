from pydantic import BaseModel, EmailStr, constr
from datetime import date
from typing import Optional

class ContactBase(BaseModel):
    first_name: constr(max_length=50)
    last_name: constr(max_length=50)
    email: EmailStr
    phone_number: constr(max_length=15)
    birthday: date
    additional_data: Optional[str]

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    id: int

    class Config:
        orm_mode = True
