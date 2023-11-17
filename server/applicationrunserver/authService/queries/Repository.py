from authService.models import UserServer
from typing import List
from asgiref.sync import async_to_sync, sync_to_async
import asyncio


class FindByFieldInput():
    """
    Represents the input parameters for finding a user by a specific field.
    """

    def __init__(self, field, value):
        self.field = field
        self.value = value


class FindByFieldOutput():
    """
    Represents the output of finding a user by a specific field.
    """

    def __init__(self, field, data):
        self.data = data
        self.field = field

    def isDataFound(self):
        """
        Checks if data is found for the specified field.
        """
        return self.data is not None
    
    def __str__(self):
        """
        Returns a string representation of the FindByFieldOutput object.
        """
        return f"Field: {self.field} - Data: {self.data}"


class UserQueryRepository:
    """
    Repository class for querying user data.
    """

    def __init__(self):
        pass

    async def findUserByField(self, input: List[FindByFieldInput]) -> List[FindByFieldOutput]:
        """
        Finds users by the specified fields.

        Args:
            input (List[FindByFieldInput]): The list of FindByFieldInput objects representing the fields to search for.

        Returns:
            List[FindByFieldOutput]: The list of FindByFieldOutput objects representing the search results.
        """
        tasks = []
        for item in input:
            task = asyncio.create_task(self.findUser(item))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        return results
    
    async def findUser(self, input: FindByFieldInput) -> FindByFieldOutput:
        """
        Finds a user by the specified field.

        Args:
            input (FindByFieldInput): The FindByFieldInput object representing the field to search for.

        Returns:
            FindByFieldOutput: The FindByFieldOutput object representing the search result.
        """
        try:
            user = await sync_to_async(UserServer.objects.get)(**{input.field: input.value})
            return FindByFieldOutput(input.field, user)
        except UserServer.DoesNotExist:
            return FindByFieldOutput(input.field, None)

            


    

    
