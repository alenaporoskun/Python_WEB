from libgravatar import Gravatar
from sqlalchemy.orm import Session

from models.models import User
from schemas.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
    Get user by email.

    Retrieves a user from the database based on the provided email address.

    :param email: The email address of the user to retrieve.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: The user with the specified email address.
    :rtype: User
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    Create user.

    Creates a new user in the database with the provided user data.
    Generates an avatar image URL based on the user's email using Gravatar.
    If Gravatar image retrieval fails, prints the exception.
    Commits the new user to the database and returns the created user.

    :param body: The user data for creating the new user.
    :type body: UserModel
    :param db: The database session.
    :type db: Session
    :return: The created user.
    :rtype: User
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    Update user token.

    Updates the refresh token for the specified user in the database.

    :param user: The user whose token needs to be updated.
    :type user: User
    :param token: The new refresh token.
    :type token: str or None
    :param db: The database session.
    :type db: Session
    :return: None
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    Confirm user email.

    Marks the user with the specified email address as confirmed in the database.

    :param email: The email address of the user to confirm.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()


async def update_avatar(email: str, url: str, db: Session) -> User:
    """
    Update user avatar.

    Updates the avatar URL for the user with the specified email address in the database.

    :param email: The email address of the user whose avatar URL needs to be updated.
    :type email: str
    :param url: The new avatar URL.
    :type url: str
    :param db: The database session.
    :type db: Session
    :return: The updated user.
    :rtype: User
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
