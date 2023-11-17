from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from common.ValidateData import *
from .queries.Repository import FindByFieldInput, UserQueryRepository 
import json
import asyncio

def signUpService(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')  # Decode the request body
        # Process the body as needed
        # Example: Extract data from JSON body
        data = json.loads(body)
        username = data.get('name')
        response_data = {
            "ok": True,
            "okValidationDataSintax": True, 
            "statusSintaxDataVaidation": [], 
            "statusValidationDataSintax": "",
            "okValidationDataUnavailable": True, 
            "statusUnavailableDataVaidation": [], 
            "statusValidationDataUnavailable": ""
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
        return JsonResponse(response_data, status=200)

    return render(request, 'auth/signUpService.html', {"is_authenticated": False})



