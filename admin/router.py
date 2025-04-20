
from fastapi import APIRouter, HTTPException, Form, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from dishes.database import get_dishes
from models import Admin, User
from users.encryption import verify_password

router = APIRouter(prefix="/admin", tags=["Admin"])
templates = Jinja2Templates(directory="templates/admin")


async def get_current_admin(request: Request):
    admin = request.session.get("admin")
    if not admin:
        raise HTTPException(status_code=401, detail="Not authenticated")

    admin = await Admin.get_admin(admin)
    if not admin:
        request.session.pop("admin", None)
        raise HTTPException(status_code=401, detail="Admin not found or deactivated")
    return admin


async def get_users(admin: Admin = Depends(get_current_admin)):
    return await User.find({}).to_list()


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


@router.get("/users", response_class=HTMLResponse)
async def admin_users(
        request: Request,
        admin: Admin = Depends(get_current_admin)
):
    users = await get_users()
    serialized_users = [user.serialize() for user in users]
    return templates.TemplateResponse(
        "admin_users.html",
        {"request": request, "users": serialized_users}
    )


@router.delete("/users/delete/{email}")
async def admin_delete_user(
        email: str,
        admin: Admin = Depends(get_current_admin),
):
    print(email)
    try:
        await User.find_one(User.email == email).delete()
    except Exception as e:
        return {"status": 400, "detail": e}
    return {"status": 200, "detail": "User is deleted"}
