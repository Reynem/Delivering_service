from functools import wraps

from fastapi import APIRouter, HTTPException, Form, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from dishes.database import get_dishes
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


@router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(
    request: Request,
    admin: Admin = Depends(get_current_admin)
):
    dishes = await get_dishes()
    serialized_dishes = [dish.serialize() for dish in dishes]
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "dishes": serialized_dishes}
    )