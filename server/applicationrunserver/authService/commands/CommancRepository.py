from authService.models import UserServer



class UserCommandRepository:
    """
    Repository class for querying user data.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        pass

    def createUser(self, 
        username: str, 
        password: str, 
        email: str, 
        phone: str, 
        name: str, 
        lastname: str) -> bool:
        """
        Creates a user with the specified username, password, email, first name, and last name.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.
            email (str): The email of the user.
            firstName (str): The first name of the user.
            lastName (str): The last name of the user.
        """
        try:
            user = UserServer(
                    username=username, 
                    password=password, 
                    email=email, 
                    name=name, 
                    phone=phone,
                    lastname=lastname
                    )
            user.save()
            return True
        except Exception as e:
            print(e)
            return False

    def deleteUser(self, username: str) -> None:
        """
        Deletes a user with the specified username.

        Args:
            username (str): The username of the user.
        """
        user = UserServer.objects.get(username=username)
        user.delete()

    def updateUser(self, username: str, password: str, email: str, firstName: str, lastName: str) -> None:
        """
        Updates a user with the specified username, password, email, first name, and last name.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.
            email (str): The email of the user.
            firstName (str): The first name of the user.
            lastName (str): The last name of the user.
        """
        user = UserServer.objects.get(username=username)
        user.password = password
        user.email = email

    def activateUser(self, username: str, activate: bool) -> bool:
        """
        Activates or deactivates a user with the specified username.

        Args:
            username (str): The username of the user.
            activate (bool): True to activate the user, False to deactivate the user.

        Returns:
            bool: True if the user has been activated, False otherwise.
        """
        try:
            user = UserServer.objects.get(username=username)
            user.is_active = activate
            user.save()
            return True
        except UserServer.DoesNotExist:
            return False


    def updateUser(self, username: str, password: str, email: str, firstName: str, lastName: str) -> None:
        """
        Updates a user with the specified username, password, email, first name, and last name.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.
            email (str): The email of the user.
            firstName (str): The first name of the user.
            lastName (str): The last name of the user.
        """
        user = UserServer.objects.get(username=username)
        user.password = password
        user.email = email
    