import csv
import os
from const import EXPORT_DIR_MOCK_NAME
from utils import check_or_mkdir
from ctx import context


def write_login_users():
    login_users_txt_name = 'login_users.txt'
    login_users_txt_path = os.path.join(EXPORT_DIR_MOCK_NAME, login_users_txt_name)
    with open(login_users_txt_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join([str(u) for u in context.login_users]))


def write_friends():
    check_or_mkdir(EXPORT_DIR_MOCK_NAME)
    write_login_users()
    friends_csv_name = f'{context.login_user.display_name}_Contacts.csv'
    friends_csv_path = os.path.join(EXPORT_DIR_MOCK_NAME, friends_csv_name)
    with open(friends_csv_path, 'w', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['user_id', 'remark_name', 'nick_name', 'display_name', 'big_avatar'])

        friend_rows = [(f.user_id, f.remark_name, f.nick_name, f.display_name, f.big_avatar) for f in context.friend_finder.all_friends]
        csv_writer.writerows(friend_rows)
