from ninja import Schema


class SUsersGetMeOut(Schema):
    tg_id: int
    is_superuser: bool
