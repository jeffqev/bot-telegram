import abc
import typing
from ..entities.user import User


class UserRepository(abc.ABC):
    @abc.abstractmethod
    async def get_by_external_id(self, external_id: str) -> typing.Optional[User]:
        """
        Get a user by its external id
        
        Args:
            external_id (str): The external id of the user

        Returns:
            typing.Optional[User]: The user if found, None otherwise
        """
