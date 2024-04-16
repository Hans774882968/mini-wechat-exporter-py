from typing import List
from ctx import context
from get_fields_from_proto_data import get_fields_from_proto_data
from utils import decode_var_int32, get_str_from_ufs_and_target_fn
from friend import LoginUser


def get_login_info() -> List[LoginUser]:
    login_info2_path = 'Documents/LoginInfo2.dat'
    login_info2_bak_infos = context.iTunes_bak_finder.find_file_bak_infos_by_relative_path(login_info2_path)
    if not login_info2_bak_infos:
        raise Exception('Documents/LoginInfo2.dat doesn\'t exist')
    login_info2_file_bak_path, _ = login_info2_bak_infos[0]
    with open(login_info2_file_bak_path, 'rb') as login_info2_f:
        login_info2_data = login_info2_f.read()
        login_info2_ufs = get_fields_from_proto_data(login_info2_data)
        users_data = login_info2_ufs[0].data
        users_data_len = len(users_data)

        login_users: List[LoginUser] = []
        cur_users_data = users_data
        ofs = 0
        while ofs < users_data_len:
            user_buffer_len, var_int_len = decode_var_int32(cur_users_data, ofs)
            tot_len = var_int_len + user_buffer_len
            user_data = users_data[ofs + var_int_len:ofs + tot_len]
            login_info2_user_ufs = get_fields_from_proto_data(user_data)
            user_id = get_str_from_ufs_and_target_fn(login_info2_user_ufs, 1)
            phone = get_str_from_ufs_and_target_fn(login_info2_user_ufs, 2)
            nick_name = get_str_from_ufs_and_target_fn(login_info2_user_ufs, 3)
            login_user = LoginUser(user_id, '', nick_name, nick_name, user_id, phone)
            login_users.append(login_user)
            ofs += tot_len

        return login_users
