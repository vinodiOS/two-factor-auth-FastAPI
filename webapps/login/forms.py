from operator import le
from typing import List
from typing import Optional
from fastapi import Request


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.email: Optional[str] = None
        self.password: Optional[str] = None
        self.token: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.email = form.get("email")  
        self.password = form.get("password")
        self.token = form.get("auth_code")

    async def is_valid(self):
        if not self.email or not (self.email.__contains__("@")):
            self.errors.append("Email is required")
        if not self.password or not len(self.password) >= 4:
            self.errors.append("A valid password is required")
        if len(self.token) != 6:
            self.errors.append("Enter valid token")
        if not self.errors:
            return True
        return False