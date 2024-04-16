import hashlib
from get_fields_from_proto_data import get_fields_from_proto_data
from utils import get_str_from_unknown_field_set


class Friend:
    def __init__(self, user_id: str, big_avatar: str, remark_name: str, nick_name: str, user_name: str) -> None:
        # user_id 正常来说总是等于 user_name ，后者是数据库查出来的微信用户 ID
        self.user_id = user_id
        self.user_id_hash = hashlib.md5(user_id.encode(encoding='utf-8')).hexdigest()
        self.big_avatar = big_avatar
        self.remark_name = remark_name
        self.nick_name = nick_name
        self.user_name = user_name
        self.display_name = remark_name or nick_name

    def __str__(self) -> str:
        return f'Friend(user_id={self.user_id}, display_name={self.display_name})'


class LoginUser(Friend):
    def __init__(self, user_id: str, big_avatar: str, remark_name: str, nick_name: str, user_name: str, phone: str) -> None:
        super().__init__(user_id, big_avatar, remark_name, nick_name, user_name)
        self.phone = phone

    def __str__(self) -> str:
        return f'LoginUser(user_id={self.user_id}, display_name={self.display_name}, phone={self.phone})'


def get_friend_from_raw_info(db_contact_head_image, db_contact_remark, user_name) -> Friend:
    db_contact_head_image_ufs = get_fields_from_proto_data(db_contact_head_image)
    big_avatar = get_str_from_unknown_field_set(db_contact_head_image_ufs, 2)

    db_contact_remark_ufs = get_fields_from_proto_data(db_contact_remark)
    remark_name = get_str_from_unknown_field_set(db_contact_remark_ufs, 2)
    nick_name = get_str_from_unknown_field_set(db_contact_remark_ufs, 0)

    return Friend(user_name, big_avatar, remark_name, nick_name, user_name)
