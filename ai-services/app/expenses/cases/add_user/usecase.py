from .request import AddUserRequest
from .response import AddUserResponse
from ...domain.entities import UserCreation
from ...domain.repositories import UserRepository


class AddUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(self, request: AddUserRequest) -> AddUserResponse:
        stored_user = await self.user_repository.get_by_external_id(request.external_id)
        if stored_user:
            return AddUserResponse(id=stored_user.id, external_id=stored_user.external_id)

        user = UserCreation(external_id=request.external_id)
        created_user = await self.user_repository.bulk_insert([user])
        return AddUserResponse(
            id=created_user[0].id, external_id=created_user[0].external_id
        )
