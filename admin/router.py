from fastapi import APIRouter, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from models import Admin
from users.encryption import verify_password

router = APIRouter(prefix="/admin", tags=["Admin"])
templates = Jinja2Templates(directory="templates/admin")

admin_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login")


async def get_current_admin(request: Request):
    admin = request.session.get("admin")
    if not admin:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return admin


@router.get("/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def admin_login_api(
        request: Request,
        username: str = Form(...),
        password: str = Form(...)
):
    admin = await Admin.get_admin(username)
    if not admin or not verify_password(password, admin.password):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid credentials"}
        )

    request.session["admin"] = admin.username
    return RedirectResponse(url="/admin/dashboard", status_code=303)


