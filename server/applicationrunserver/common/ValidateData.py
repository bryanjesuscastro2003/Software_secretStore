from typing import List


class FieldValue():
    """
    Represents a field value with its name, value, and state.

    Attributes:
        nameField (str): The name of the field.
        value: The value of the field.
        state (bool): The state of the field.
    """

    def __init__(self, nameField: str, value, state: bool):
        self.nameField = nameField
        self.value = value
        self.state = state

    def to_json(self):
        return {
            "nameField": self.nameField,
            "value": self.value,
            "state": self.state
        }
    def __str__(self):
        return {
            "nameField": self.nameField,
            "value": self.value,
            "state": self.state
        }

class ValidateDataOutput():
    """
    Represents the output of the data validation process.
  
    Attributes:
        status (List[FieldValue]): The list of field values with their states.
        message: The message indicating the completion of data validation.
    """

    def __init__(self, status: List[FieldValue], message, ok):
        self.ok = ok
        self.status = status
        self.message = message
    
    def __str__(self):
        return f"ok: {self.ok}, status: {self.status}, message: {self.message}"

class ValidateDataInput():
    """
    Represents the input for the data validation process.

    Attributes:
        nameAction: The name of the action.
        data: The data to be validated.
    """

    def __init__(self, nameAction, data):
        self.nameAction = nameAction
        self.data = data

def validate_data(data: ValidateDataInput) -> ValidateDataOutput:
    """
    Validates the given data.

    Args:
        data (ValidateDataInput): The input data to be validated.

    Returns:
        ValidateDataOutput: The output of the data validation process.
    """
    status = []
    anyError = False
    
    # Validate name field
    if 'name' in data.data:
        name = data.data['name']
        if not isinstance(name, str) or len(name) < 4 or len(name) > 30:
            status.append(FieldValue('name', name, False))
            anyError = True
        else:
            status.append(FieldValue('name', name, True))
    
    # Validate lastname field
    if 'lastname' in data.data:
        lastname = data.data['lastname']
        if not isinstance(lastname, str) or len(lastname) < 4 or len(lastname) > 30:
            status.append(FieldValue('lastname', lastname, False))
            anyError = True
        else:
            status.append(FieldValue('lastname', lastname, True))
    
    # Validate username field
    if 'username' in data.data:
        username = data.data['username']
        if not isinstance(username, str) or len(username) < 4 or len(username) > 30:
            status.append(FieldValue('username', username, False))
            anyError = True
        else:
            status.append(FieldValue('username', username, True))
    
    # Validate password field
    if 'password' in data.data:
        password = data.data['password']
        if not isinstance(password, str) or len(password) < 4 or len(password) > 30:
            status.append(FieldValue('password', password, False))
            anyError = True
        else:
            status.append(FieldValue('password', password, True))
    
    # Validate email field
    if 'email' in data.data:
        email = data.data['email']
        if not isinstance(email, str) or len(email) < 4 or len(email) > 30:
            status.append(FieldValue('email', email, False))
            anyError = True
        else:
            status.append(FieldValue('email', email, True))
    
    # Validate phone field
    if 'phone' in data.data:
        phone = data.data['phone']
        if not isinstance(phone, str) or len(phone) < 4 or len(phone) > 30:
            status.append(FieldValue('phone', phone, False))
            anyError = True
        else:
            status.append(FieldValue('phone', phone, True))
    
    message = f"{data.nameAction} -> Data validation Done. "
    if anyError:
        message += " Sintax data validation Error : Please verify your data."
    return ValidateDataOutput(status, message, not anyError)
