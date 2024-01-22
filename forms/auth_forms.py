from fastapi import Request
from typing import Optional

class LoginForm:
    def __init__(self,request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def create_oauth_form(self):
        form = await self.request.form()
        self.username = form["email"]
        self.password = form["password"]