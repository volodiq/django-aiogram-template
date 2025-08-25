from ninja import Router

from core.typedefs import AuthedRequest

from . import schemas


router = Router()


@router.get("/me/", response=schemas.SUsersGetMeOut)
async def get_me(request: AuthedRequest):
    return schemas.SUsersGetMeOut(
        tg_id=request.auth.tg_id,
        is_superuser=request.auth.is_superuser,
    )
