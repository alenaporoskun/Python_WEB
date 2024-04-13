from typing import Optional
import pytz

from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import redis, pickle

from database.database import get_db
from repository import users as repository_users
from conf.config import settings

class Auth:
    """
    Authentication utilities.

    Provides methods for password hashing, token generation and validation,
    and retrieving the current authenticated user.
    """

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")  # /api/auth/login
    r = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)

    def verify_password(self, plain_password, hashed_password):
        """
        Verify password.

        Compares a plain password with its hashed counterpart to verify their match.

        :param plain_password: The plain text password.
        :type plain_password: str
        :param hashed_password: The hashed password.
        :type hashed_password: str
        :return: True if the passwords match, False otherwise.
        :rtype: bool
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        """
        Get password hash.

        Hashes a plain text password using bcrypt.

        :param password: The plain text password.
        :type password: str
        :return: The hashed password.
        :rtype: str
        """
        return self.pwd_context.hash(password)

    async def create_access_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        Create access token.

        Generates a new access token JWT.

        :param data: The data to be included in the token payload.
        :type data: dict
        :param expires_delta: Optional expiration time delta in seconds.
        :type expires_delta: float, optional
        :return: The encoded access token.
        :rtype: str
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(pytz.utc) + timedelta(seconds=expires_delta)
        else:
            expire = datetime.now(pytz.utc) + timedelta(minutes=15)
        to_encode.update({"iat": datetime.now(pytz.utc), "exp": expire, "scope": "access_token"})
        encoded_access_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_access_token

    # define a function to generate a new refresh token
    async def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        Create refresh token.

        Generates a new refresh token JWT.

        :param data: The data to be included in the token payload.
        :type data: dict
        :param expires_delta: Optional expiration time delta in seconds.
        :type expires_delta: float, optional
        :return: The encoded refresh token.
        :rtype: str
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(pytz.utc) + timedelta(seconds=expires_delta)
        else:
            expire = datetime.now(pytz.utc) + timedelta(days=7)
        to_encode.update({"iat": datetime.now(pytz.utc), "exp": expire, "scope": "refresh_token"})
        encoded_refresh_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_refresh_token

    async def decode_refresh_token(self, refresh_token: str):
        """
        Decode refresh token.

        Decodes and verifies a refresh token JWT.

        :param refresh_token: The refresh token to decode.
        :type refresh_token: str
        :return: The email address extracted from the token payload.
        :rtype: str
        :raises HTTPException: If the token is invalid or unauthorized.
        """
        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'refresh_token':
                email = payload['sub']
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')

    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        """
        Get current user.

        Retrieves the current authenticated user based on the provided access token.

        :param token: The access token.
        :type token: str
        :param db: The database session.
        :type db: Session
        :return: The current authenticated user.
        :rtype: User
        :raises HTTPException: If the token is invalid or unauthorized.
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            # Decode JWT
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'access_token':
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as e:
            raise credentials_exception
        user = self.r.get(f"user:{email}")
        if user is None:
            user = await repository_users.get_user_by_email(email, db)
            if user is None:
                raise credentials_exception
            self.r.set(f"user:{email}", pickle.dumps(user))
            self.r.expire(f"user:{email}", 900)
        else:
            user = pickle.loads(user)
        return user

    def create_email_token(self, data: dict):
        """
        Create email verification token.

        Generates a new JWT for email verification.

        :param data: The data to be included in the token payload.
        :type data: dict
        :return: The encoded email verification token.
        :rtype: str
        """
        to_encode = data.copy()
        expire = datetime.now(pytz.utc) + timedelta(days=7)
        to_encode.update({"iat": datetime.now(pytz.utc), "exp": expire})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token
    

    async def get_email_from_token(self, token: str):
        """
        Get email from token.

        Decodes and extracts the email address from the provided JWT token.

        :param token: The JWT token.
        :type token: str
        :return: The email address extracted from the token payload.
        :rtype: str
        :raises HTTPException: If the token is invalid or cannot be processed.
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email = payload["sub"]
            return email
        except JWTError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Invalid token for email verification")

# Initialize authentication service
auth_service = Auth()
