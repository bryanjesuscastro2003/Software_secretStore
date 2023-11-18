from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from common.ValidateData import *
from common.EmailActions import send_email
from common.Codes import generate_jwt, encrypt_text
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

    return render(request, 'auth/signUpService.html', {"is_authenticated": False})



