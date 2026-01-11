# backend/src/routes/auth_routes.py
from fastapi import APIRouter, Request, Depends, status, Form
from controllers import auth_controller
from models.user_model import UserCreate, Token, UserLoginRequest
from utils.security import oauth
from utils.dependencies import get_current_user, get_current_teacher # Added these

router = APIRouter(prefix="/auth", tags=["Authentication"])

# --- PUBLIC ROUTES ---

@router.post("/signup")
async def signup(user: UserCreate):
    return await auth_controller.register_user(user)

@router.post("/signin", response_model=Token) 
async def signin(username: str = Form(...), password: str = Form(...)):
    """
    Using Form(...) manually avoids the Pydantic 'FieldInfo' bug 
    while still supporting the Swagger Authorize popup.
    """
    login_data = UserLoginRequest(
        username=username, 
        password=password
    )
    return await auth_controller.login_user(login_data)

# --- PROTECTED ROUTES ---

@router.get("/me")
async def get_my_profile(current_user: dict = Depends(get_current_user)):
    """
    Returns the profile of the currently logged-in user.
    Requires a valid 'Authorization: Bearer <token>' header.
    """
    return {
        "status": "success",
        "user": {
            "email": current_user["email"],
            "name": current_user["name"],
            "role": current_user["role"],
            "id": str(current_user.get("_id") or current_user.get("id"))
        }
    }

@router.get("/teacher-only-test")
async def test_teacher_access(teacher: dict = Depends(get_current_teacher)):
    """
    A test route that will return 403 Forbidden if a Student tries to access it.
    """
    return {
        "message": f"Access granted. Hello, {teacher['name']}. You are verified as a teacher."
    }

# --- GOOGLE AUTH ROUTES ---

@router.get("/google")
async def google_login(request: Request):
    redirect_uri = request.url_for('google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/callback", name="google_callback")
async def google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get('userinfo')
    return await auth_controller.handle_google_login(user_info)