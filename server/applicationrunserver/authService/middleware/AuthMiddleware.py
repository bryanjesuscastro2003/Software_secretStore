from django.shortcuts import redirect
from common.Codes import generate_jwt, validate_jwt
from django.conf import settings
from django.contrib.auth import logout


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        current_path = request.path
        session_secure = request.COOKIES.get('session_secure')
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return response
            # Callback for google auth
            if current_path == "/" and request.user.name == "":
                return redirect('/auth/accounts/inactive/')
            if "auth/logout" in current_path:
                response.delete_cookie("session_secure")  
                logout(request)
                return redirect('/auth/signIn')
            if session_secure is None:
                jwt = generate_jwt(
                    {"username": request.user.username}, settings.SECRET_TEXT_FOR_JWT, 5)  
                response.set_cookie('session_secure', jwt)
            else:
                jwtValid, payload = validate_jwt(session_secure, settings.SECRET_TEXT_FOR_JWT)
                if not jwtValid:
                    jwt = generate_jwt(
                        {"username": request.user.username}, settings.SECRET_TEXT_FOR_JWT, 5)  
                    response.set_cookie('session_secure', jwt)
            if "auth" in current_path:
                return redirect('/dashboard/')
        else:
            if "dashboard" in current_path or "auth/logout" in current_path:
                return redirect('/auth/signIn/')
            if session_secure:
                response.delete_cookie("session_secure")

        return response
    

    