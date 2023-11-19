from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from common.ValidateData import *
from common.EmailActions import send_email
from common.Codes import generate_jwt, encrypt_text, validate_jwt
from .queries.Repository import FindByFieldInput, UserQueryRepository 
from .commands.CommancRepository import UserCommandRepository
import json
import asyncio
from django.conf import settings


def signUpService(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')  # Decode the request body
        # Process the body as needed
        # Example: Extract data from JSON body
        data = json.loads(body)
        response_data = {
            "ok": True,
            "okValidationDataSintax": True, 
            "statusSintaxDataVaidation": [], 
            "statusValidationDataSintax": "",
            "okValidationDataUnavailable": True, 
            "statusUnavailableDataVaidation": [], 
            "statusValidationDataUnavailable": "", 
            "userCreated": False, 
            "message": ""
        }
        inputData = {
            "name": data.get('name'),
            "lastname": data.get('lastname'),
            "username": data.get('username'),
            "password": data.get('password'),
            "email": data.get('email'),
            "phone": data.get('phoneNumber') 
        }
        inputForValidation = ValidateDataInput("Logup validation", inputData)
        responseValidation = validate_data(inputForValidation)
        if not responseValidation.ok:
            response_data["okValidationDataSintax"] = False
            response_data["statusSintaxDataVaidation"] = [item.to_json() for item in responseValidation.status]
            response_data["statusValidationDataSintax"] = responseValidation.message                
            return JsonResponse(response_data, status=400)
        inputData = [
            FindByFieldInput("username", data.get('username')),
            FindByFieldInput("email", data.get('email')),
            FindByFieldInput("phone", data.get('phoneNumber'))
        ]
        userQueryRepository = UserQueryRepository()
        responseQueryData = asyncio.run(userQueryRepository.findUserByField(inputData))#await userQueryRepository.findUserByField(inputData)
        error = False
        for item in responseQueryData:
            response_data["okValidationDataUnavailable"] = not item.isDataFound()
            response_data["statusUnavailableDataVaidation"].append({
                "nameField": item.field,
                "state": not item.isDataFound()
            })
            if not error:
                error = item.isDataFound()
        response_data["statusValidationDataUnavailable"] = "The data is already registered" if error else ""
        if not error:
            userCommandRepository = UserCommandRepository()
            dataCreated = userCommandRepository.createUser(
                username=data.get('username'),
                password=encrypt_text(settings.SERET_TEXT_FOR_PASSWORD,data.get('password')),
                email=data.get('email'),
                phone=data.get('phoneNumber'),
                name=data.get('name'),
                lastname=data.get('lastname')
            );
            if dataCreated:
                response_data["userCreated"] = True
                response_data["message"] = "Account created ok but its not active please activate with the email verifier send to your account. "
                if dataCreated:
                    jwt = generate_jwt({
                        "username": data.get('username'),
                    },settings.SECRET_TEXT_FOR_JWT, 1) 
                    send_email("EmailVerifier", 
                            f"Click here to activate your account : \n http://{settings.DOMAIN}/auth/activateAccount/{jwt}/", 
                            data.get('email'))
            else:
                response_data["userCreated"] = False
                response_data["message"] = "Unexpected error creating your account try again later ."

        return JsonResponse(response_data, status=200)

    return render(request, 'auth/signUpService.html')


def activateAccountService(request, token:str):
    ok, payload = validate_jwt(token, settings.SECRET_TEXT_FOR_JWT)
    message = payload if not ok else None
    print(payload)
    if ok:
        userCommandRepository = UserCommandRepository()
        userActivated = userCommandRepository.activateUser(payload.get("username"), True)
        if userActivated:
            message = "Your account has been activated successfully."
        else:
            ok = False
            message = "Unexpected error activating your account try again later ."
    return render(request, 'auth/accountActivatedService.html', {"ok": ok, "message": message})

def resendActivatorService(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        data = json.loads(body)
        inputData = [
            FindByFieldInput("email", data.get('email'))
        ]
        userQueryRepository = UserQueryRepository()
        responseQueryData = asyncio.run(userQueryRepository.findUserByField(inputData))#await userQueryRepository.findUserByField(inputData)
        accountRegistered = False if responseQueryData[0].data is None else True if not responseQueryData[0].data.is_active else False
        jsonResponse = {"ok": False, "message": "The email is not registered in our system or has been already activated."}
        if accountRegistered:
            jwt = generate_jwt({
                "username": responseQueryData[0].data.username,
            },settings.SECRET_TEXT_FOR_JWT, 1) 
            send_email("EmailVerifier", 
                    f"Click here to activate your account : \n http://{settings.DOMAIN}/auth/activateAccount/{jwt}/", 
                    data.get('email'))
            jsonResponse["ok"] = True
            jsonResponse["message"] = "Email sent successfully."
        return JsonResponse(jsonResponse, status=200)
    return render(request, 'auth/resendActivatorService.html')

def signInService(request):
    return render(request, 'auth/signInService.html')
