import base64
from io import BytesIO
import os
from database.repository.users import create_new_user
from database.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi.templating import Jinja2Templates
from schemas.users import UserCreate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from webapps.signup.forms import UserCreateForm
import pyqrcode
import png


templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/signup/")
def register(request: Request):
    return templates.TemplateResponse("signup/signup.html", {"request": request})

@router.get("/qrcode")
def register(request: Request):
    return templates.TemplateResponse("qrcode/qrcode.html", {"request": request})

@router.post("/signup/")
async def register(request: Request, db: Session = Depends(get_db)):
    form = UserCreateForm(request)
    await form.load_data()
    if await form.is_valid():
        user = UserCreate(
            email=form.email, password=form.password, secret=base64.b32encode(os.urandom(10)).decode('utf-8')
        )
        try:
            user = create_new_user(user=user, db=db)
            data = 'otpauth://totp/FastAPI-2FA:{0}?secret={1}&issuer=FastAPI-2FA' \
            .format(user.email, user.secret)
            url = pyqrcode.create(data)
            stream = BytesIO()
            url.png(stream, scale=3)
            return templates.TemplateResponse("qrcode/qrcode.html", {"request": request, "data": base64.b64encode(stream.getvalue()).decode('utf-8')})
            #
        except IntegrityError:
            form.__dict__.get("errors").append("Duplicate username or email")
            return templates.TemplateResponse("signup/signup.html", form.__dict__)
    return templates.TemplateResponse("signup/signup.html", form.__dict__)