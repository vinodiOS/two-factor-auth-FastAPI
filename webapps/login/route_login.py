from core.hashing import Hasher
from core.otp import OTP
from database.models.users import User
from database.repository.users import get_user_by_email
from database.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from webapps.login.forms import LoginForm


templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/login/")
def login(request: Request):
    return templates.TemplateResponse("login/login.html", {"request": request})


@router.post("/login/")
async def login(request: Request, db: Session = Depends(get_db)):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            user: User = get_user_by_email(form.email, db=db)
            if user is None or not Hasher.verify_password(form.password, user.hashed_password) or \
                not OTP.verify_otp(user.secret, form.token):
                form.__dict__.get("errors").append("Incorrect Credentails")
                return templates.TemplateResponse("login/login.html", form.__dict__)
            
            
            return templates.TemplateResponse("home/index.html", {"request": request, "email":user.email})
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("login/login.html", form.__dict__)
    return templates.TemplateResponse("login/login.html", form.__dict__)