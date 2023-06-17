from __future__ import annotations

from typing import Any

import httpx
from fastapi import HTTPException
from jose import JWTError, jwt


class AuthClient:
    def __init__(self, auth_app_url: str, secret_key: str, algorithm: str = 'HS256', app_path: str = '/api/v1/users'):
        self.auth_app_url = auth_app_url + app_path
        self.secret_key = secret_key
        self.algorithm = algorithm

    async def authenticate(self, username: str, password: str) -> Any:
        async with httpx.AsyncClient() as client:
            data = {
                'username': username,
                'password': password
            }
            response = await client.post(f'{self.auth_app_url}/token', data=data)
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(401, 'Ошибка аутентификации')

    async def refresh_token(self, refresh_token: str) -> Any:
        async with httpx.AsyncClient() as client:
            headers = {
                'Authorization': f'Bearer {refresh_token}'
            }
            response = await client.post(f"{self.auth_app_url}/refresh_token", headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(400, 'Ошибка обновления токена')

    async def get_access_token(self, username: str, password: str) -> str:
        auth_response = await self.authenticate(username, password)
        return auth_response['access_token']

    async def get_user_data(self, access_token: str) -> dict:
        try:
            data = jwt.decode(access_token, self.secret_key, algorithms=[self.algorithm])
        except JWTError:
            raise HTTPException(401, 'Некорректный токен')
        return data
