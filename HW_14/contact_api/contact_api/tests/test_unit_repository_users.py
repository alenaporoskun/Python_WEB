import unittest
from unittest.mock import MagicMock, AsyncMock, patch

from sqlalchemy.orm import Session

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.models import User
from schemas.schemas import UserModel
from repository.users import get_user_by_email, create_user, update_token, confirmed_email, update_avatar


class TestUsers(unittest.IsolatedAsyncioTestCase):

    async def test_get_user_by_email(self):
        email = "test@example.com"
        user = User(email=email)  # Assuming User model has an email attribute
        session = AsyncMock(spec=Session)
        session.query(User).filter.return_value.first.return_value = user

        retrieved_user = await get_user_by_email(email, session)

        self.assertEqual(retrieved_user, user)

    async def test_create_user(self):
        user_data = UserModel(username="test_user", password="test_pwd", email="test@example.com")
        session = AsyncMock(spec=Session)

        with patch("repository.users.Gravatar") as mock_gravatar:
            mock_gravatar.return_value.get_image.return_value = "http://example.com/avatar.jpg"
            
            created_user = await create_user(user_data, session)

            self.assertIsNotNone(created_user)
            self.assertEqual(created_user.email, user_data.email)
            self.assertEqual(created_user.avatar, "http://example.com/avatar.jpg")

    async def test_update_token(self):
        user = User()
        token = "test_token"
        session = AsyncMock(spec=Session)

        await update_token(user, token, session)

        self.assertEqual(user.refresh_token, token)
        session.commit.assert_called_once()

    async def test_confirmed_email(self):
        email = "test@example.com"
        user = User(email=email)
        session = AsyncMock(spec=Session)
        session.commit = AsyncMock()

        with patch("repository.users.get_user_by_email", return_value=user):
            await confirmed_email(email, session)

            self.assertTrue(user.confirmed)
            session.commit.assert_called_once()

    async def test_update_avatar(self):
        email = "test@example.com"
        url = "http://example.com/avatar.jpg"
        user = User(email=email)
        session = MagicMock(spec=Session)
        session.commit = MagicMock()  # Замінюємо на MagicMock

        with patch("repository.users.get_user_by_email", return_value=user):
            updated_user = await update_avatar(email, url, session)

            self.assertEqual(updated_user.avatar, url)
            session.commit.assert_called_once()  # Перевіряємо виклик методу commit()



if __name__ == "__main__":
    unittest.main()
