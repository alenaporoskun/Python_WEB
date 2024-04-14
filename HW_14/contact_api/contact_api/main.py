from fastapi import FastAPI, Depends, HTTPException
from fastapi import APIRouter, status, Security, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import APIRouter, Security, BackgroundTasks, Request
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from typing import List

from database.database import engine, get_db
from schemas.schemas import ContactCreate, Contact, UserDb
from schemas.schemas import UserModel, UserResponse, TokenModel, RequestEmail
#from crud import add_contact, get_contacts, get_contact, refresh_contact
#from crud import remove_contact, get_upcoming_birthdays
from repository import users as repository_users
from services.auth import auth_service
from models.models import Base, User
from services.email import send_email
from conf.config import settings

import redis.asyncio as redis
import cloudinary
import cloudinary.uploader


# Initializing FastAPI instance.
# This creates the main application instance for handling HTTP requests and responses.
app = FastAPI()

# Setting up CORS (Cross-Origin Resource Sharing) Middleware to allow requests from all origins.
# CORSMiddleware adds CORS headers to server responses to allow requests from other domains.
# In this case, it allows requests from any origin (origins = ["*"]),
# allows sending user credentials, permitted HTTP methods, and headers.
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialising the HTTPBearer object to provide authentication using Bearer tokens.
security = HTTPBearer()

# Initialising the database
Base.metadata.create_all(bind=engine)

async def startup_event():
    """
    Initialize FastAPILimiter on application startup.

    This function connects to Redis using the provided host, port, and encoding settings from the application settings.
    It then initializes FastAPILimiter using the established Redis connection.

    :return: None
    """
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)

# Adding an event handler for the "startup" event.
# This event handler executes the startup_event function when the application starts.
app.add_event_handler("startup", startup_event)


@app.post("/contacts/", response_model=Contact, status_code=status.HTTP_201_CREATED,
          dependencies=[Depends(RateLimiter(times=10, seconds=60))])
def create_contact(
    contact: ContactCreate, db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
):
    """
    Create a new contact with a speed limit.

    :param contact: The contact information to be created.
    :type contact: ContactCreate
    :param db: The database session.
    :type db: Session, optional
    :param current_user: The current authenticated user.
    :type current_user: User, optional
    :return: The newly created contact.
    :rtype: Contact
    :raises HTTPException: If the rate limit is exceeded.
    """
    return add_contact(db=db, contact=contact, user=current_user)


@app.get("/contacts/", response_model=List[Contact], description='No more than 10 requests per minute',
         dependencies=[Depends(RateLimiter(times=10, seconds=60))])
def read_contacts(
    skip: int = 0, limit: int = 10, query: str = None, db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
):
    """
    Read contacts with a speed limit.

    :param skip: The number of contacts to skip. Defaults to 0.
    :type skip: int, optional
    :param limit: The maximum number of contacts to return. Defaults to 10.
    :type limit: int, optional
    :param query: The query string to filter contacts. Defaults to None.
    :type query: str, optional
    :param db: The database session.
    :type db: Session, optional
    :param current_user: The current authenticated user.
    :type current_user: User, optional
    :return: A list of contacts.
    :rtype: List[Contact]
    """
    return get_contacts(db=db, skip=skip, limit=limit, query=query, user=current_user)


@app.get("/contacts/{contact_id}", response_model=Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db), 
                 current_user: User = Depends(auth_service.get_current_user)):
    """
    Read contact by ID.

    Retrieves a contact with the specified ID from the database.
    Requires authentication. Returns the contact if found, otherwise raises a 404 HTTPException.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param db: The database session.
    :type db: Session, optional
    :param current_user: The current authenticated user.
    :type current_user: User, optional
    :return: The contact with the specified ID.
    :rtype: Contact
    :raises HTTPException: If the contact with the specified ID is not found (HTTP status code 404).
    """
    db_contact = get_contact(db=db, contact_id=contact_id, user=current_user)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@app.put("/contacts/{contact_id}", response_model=Contact)
def update_contact(contact_id: int, contact: ContactCreate, db: Session = Depends(get_db),
                   current_user: User = Depends(auth_service.get_current_user)):
    """
    Update contact by ID.

    Updates the contact with the specified ID in the database with the provided contact data.
    Requires authentication. Returns the updated contact if found, otherwise raises a 404 HTTPException.

    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param contact: The updated contact information.
    :type contact: ContactCreate
    :param db: The database session.
    :type db: Session, optional
    :param current_user: The current authenticated user.
    :type current_user: User, optional
    :return: The updated contact.
    :rtype: Contact
    :raises HTTPException: If the contact with the specified ID is not found (HTTP status code 404).
    """
    db_contact = get_contact(db=db, contact_id=contact_id, user=current_user)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return refresh_contact(db=db, contact_id=contact_id, contact=contact, user=current_user)


@app.delete("/contacts/{contact_id}", response_model=Contact)
def delete_contact(contact_id: int, db: Session = Depends(get_db),
                   current_user: User = Depends(auth_service.get_current_user)):
    """
    Delete contact by ID.

    Deletes the contact with the specified ID from the database.
    Requires authentication. Returns the deleted contact if found, otherwise raises a 404 HTTPException.

    :param contact_id: The ID of the contact to delete.
    :type contact_id: int
    :param db: The database session.
    :type db: Session, optional
    :param current_user: The current authenticated user.
    :type current_user: User, optional
    :return: The deleted contact.
    :rtype: Contact
    :raises HTTPException: If the contact with the specified ID is not found (HTTP status code 404).
    """
    db_contact = get_contact(db=db, contact_id=contact_id, user=current_user)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return remove_contact(db=db, contact_id=contact_id, user=current_user)


@app.get("/contacts/upcoming_birthdays/", response_model=List[Contact])
def get_upcoming_birthdays_list(db: Session = Depends(get_db),
                                current_user: User = Depends(auth_service.get_current_user)):
    """
    Get contacts with upcoming birthdays.

    Retrieves a list of contacts from the database that have upcoming birthdays.
    Requires authentication. Returns the list of contacts with upcoming birthdays.

    :param db: The database session.
    :type db: Session, optional
    :param current_user: The current authenticated user.
    :type current_user: User, optional
    :return: A list of contacts with upcoming birthdays.
    :rtype: List[Contact]
    """
    return get_upcoming_birthdays(db=db, user=current_user)


@app.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserModel, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    """
    Sign up a new user.

    Creates a new user account with the provided user data.
    If the email address already exists in the database, raises a 409 Conflict HTTPException.
    Upon successful creation of the user account, sends a confirmation email and returns the new user details.

    :param body: The user data for creating a new account.
    :type body: UserModel
    :param background_tasks: The background tasks queue.
    :type background_tasks: BackgroundTasks
    :param request: The incoming request.
    :type request: Request
    :param db: The database session.
    :type db: Session, optional
    :return: The new user details and a confirmation message.
    :rtype: UserResponse
    :raises HTTPException: If the email address already exists in the database (HTTP status code 409).
    """
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)
    background_tasks.add_task(send_email, new_user.email, new_user.username, request.base_url)
    return {"user": new_user, "detail": "User successfully created. Check your email for confirmation."}


@app.post("/login", response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    User login.

    Authenticates the user with the provided credentials (email and password).
    If the email is not found in the database, raises a 401 Unauthorized HTTPException with "Invalid email" detail.
    If the email is not confirmed, raises a 401 Unauthorized HTTPException with "Email not confirmed" detail.
    If the password is incorrect, raises a 401 Unauthorized HTTPException with "Invalid password" detail.
    Upon successful authentication, generates and returns JWT access and refresh tokens.

    :param body: The OAuth2PasswordRequestForm containing user credentials.
    :type body: OAuth2PasswordRequestForm
    :param db: The database session.
    :type db: Session, optional
    :return: JWT access and refresh tokens.
    :rtype: TokenModel
    :raises HTTPException: If the provided email or password is invalid (HTTP status code 401).
    """
    user = await repository_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not user.confirmed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@app.get('/refresh_token', response_model=TokenModel)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    """
    Refresh access token.

    Validates the refresh token provided in the authorization header.
    If the refresh token is invalid or expired, raises a 401 Unauthorized HTTPException.
    If the refresh token is valid, generates a new access token and refresh token,
    updates the user's refresh token in the database, and returns the new tokens.

    :param credentials: The HTTPAuthorizationCredentials containing the refresh token.
    :type credentials: HTTPAuthorizationCredentials
    :param db: The database session.
    :type db: Session, optional
    :return: New access and refresh tokens.
    :rtype: TokenModel
    :raises HTTPException: If the provided refresh token is invalid or expired (HTTP status code 401).
    """
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@app.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserModel, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    """
    User sign-up.

    Creates a new user account with the provided user data.
    If the email address already exists in the database, raises a 409 Conflict HTTPException.
    Upon successful creation of the user account, sends a confirmation email and returns the new user details.

    :param body: The user data for creating a new account.
    :type body: UserModel
    :param background_tasks: The background tasks queue.
    :type background_tasks: BackgroundTasks
    :param request: The incoming request.
    :type request: Request
    :param db: The database session.
    :type db: Session, optional
    :return: The new user details and a confirmation message.
    :rtype: UserResponse
    :raises HTTPException: If the email address already exists in the database (HTTP status code 409).
    """
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)
    background_tasks.add_task(send_email, new_user.email, new_user.username, request.base_url)
    return {"user": new_user, "detail": "User successfully created. Check your email for confirmation."}


@app.get('/confirmed_email/{token}')
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    """
    Confirm email.

    Verifies the email confirmation token and confirms the associated user's email address in the database.
    If the token is invalid or the user does not exist, raises a 400 Bad Request HTTPException.
    If the user's email is already confirmed, returns a message indicating so.
    Upon successful confirmation of the email, updates the user's record in the database and returns a success message.

    :param token: The email confirmation token.
    :type token: str
    :param db: The database session.
    :type db: Session, optional
    :return: A message indicating the result of the email confirmation.
    :rtype: dict
    :raises HTTPException: If the token is invalid or the user does not exist (HTTP status code 400).
    """
    email = await auth_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await repository_users.confirmed_email(email, db)
    return {"message": "Email confirmed"}


@app.post('/request_email')
async def request_email(body: RequestEmail, background_tasks: BackgroundTasks, request: Request,
                        db: Session = Depends(get_db)):
    """
    Request email confirmation.

    Sends an email confirmation request to the provided email address.
    If the email address is already confirmed, returns a message indicating so.
    If the email address exists in the database, sends a confirmation email.
    If the email address does not exist in the database, returns a success message without sending an email.

    :param body: The request body containing the email address.
    :type body: RequestEmail
    :param background_tasks: The background tasks queue.
    :type background_tasks: BackgroundTasks
    :param request: The incoming request.
    :type request: Request
    :param db: The database session.
    :type db: Session, optional
    :return: A message indicating the result of the email confirmation request.
    :rtype: dict
    """
    user = await repository_users.get_user_by_email(body.email, db)

    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(send_email, user.email, user.username, request.base_url)
    return {"message": "Check your email for confirmation."}


@app.get("/users/me/", response_model=UserDb)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    """
    Read current user.

    Retrieves the details of the currently authenticated user.
    Requires authentication. Returns the details of the current user.

    :param current_user: The current authenticated user.
    :type current_user: User
    :return: The details of the current user.
    :rtype: UserDb
    """
    return current_user


@app.patch('/users/avatar', response_model=UserDb)
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    """
    Update user avatar.

    Uploads a new avatar image file for the current authenticated user.
    Requires authentication. Returns the updated user details including the new avatar URL.

    :param file: The avatar image file to upload.
    :type file: UploadFile
    :param current_user: The current authenticated user.
    :type current_user: User
    :param db: The database session.
    :type db: Session, optional
    :return: The updated user details including the new avatar URL.
    :rtype: UserDb
    """
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )

    r = cloudinary.uploader.upload(file.file, public_id=f'{current_user.username}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'{current_user.username}')\
                        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user