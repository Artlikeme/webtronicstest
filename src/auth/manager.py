from typing import Optional

import httpx
from fastapi import Depends, Request, HTTPException
from fastapi_users import BaseUserManager, IntegerIDMixin
from sqlalchemy import update

from .models import User
from .utils import get_user_db
from src.config import SECRET_PASS, HUNTER_API_KEY, CLEARBIT_KEY
from src.database import async_session_maker

SECRET = SECRET_PASS


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    @staticmethod
    async def clearbit_fio_add(user):
        clearbit_url = f'https://person.clearbit.com/v1/people/email/{user.email}'
        async with httpx.AsyncClient(
                headers={'API-Version': '2019-12-19', 'Authorization': f'Bearer {CLEARBIT_KEY}'}) as client:
            response_clearbit = await client.get(clearbit_url)
            response_clearbit = response_clearbit.json()
        try:
            if response_clearbit['name'] is None:
                raise HTTPException(status_code=404, detail="User not found")
        except KeyError:
            raise HTTPException(status_code=404, detail="User not found")

        user_fio = response_clearbit['name']
        user_fio_string = f"{user_fio['givenName']} {user_fio['familyName']} {user_fio['fullName']}"
        async with async_session_maker() as session:
            stmt = update(User).where(User.id == user.id).values(fio=user_fio_string)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def hunter_email_filter(user):
        url = f"https://api.hunter.io/v2/email-verifier?email={user.email}&api_key={HUNTER_API_KEY}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            data = response.json()
        try:
            if data['data']['status'] != 'valid':
                raise HTTPException(status_code=400, detail="Invalid email")
        except KeyError:
            raise HTTPException(status_code=400, detail="Invalid email")

    async def on_after_register(self,
                                user: User,
                                request: Optional[Request] = None):

        # await self.hunter_email_filter(user)
        await self.clearbit_fio_add(user)

        return {"status": "success"}


async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
):
    print(f"User {user.id} has forgot their password. Reset token: {token}")


async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
):
    print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
