import abc
import typing
from ..entities.user import User


class UserRepository(abc.ABC):
    @abc.abstractmethod
    async def get_by(self, **kwargs) -> typing.Optional[User]:
        """
        Get user by query parameters

        Args:
          **kwargs: The query parameters

        Returns:
          User: The user

        """
