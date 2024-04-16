import sqlite3
from typing import List
from friend import Friend, get_friend_from_raw_info
from message import WechatMessage, Session
from ctx import context
from write_messages import write_messages
from write_friends import write_friends
from get_login_info import get_login_info


def get_wechat_db_file_infos():
    def wechat_dbs_query_condition(_: str, relative_path: str, domain: str):
        return domain.endswith('com.tencent.xin') and '/DB/' in relative_path and relative_path.endswith('.sqlite')
    wechat_dbs_bak_infos = context.iTunes_bak_finder.find_file_bak_infos_by_fn(wechat_dbs_query_condition)

    wechat_db_file_infos = []
    message_db_paths = []
    mm_sqlite_db_path = ''
    for file_bak_path, relative_path in wechat_dbs_bak_infos:
        if 'message' in relative_path:
            message_db_paths.append(file_bak_path)
        if 'WCDB_Contact' in relative_path:
            mm_sqlite_db_path = file_bak_path
        wechat_db_file_infos.append((file_bak_path, relative_path))
    return wechat_db_file_infos, message_db_paths, mm_sqlite_db_path


def watch_tables(wechat_db_file_infos):  # unused dbg
    for file_bak_path, relative_path in wechat_db_file_infos:
        with sqlite3.connect(file_bak_path) as conn:
            cursor = conn.cursor()
            sql = "SELECT name FROM sqlite_master WHERE type='table' order by name"
            cursor.execute(sql)
            print(relative_path, file_bak_path, cursor.fetchall())
            cursor.close()


def get_friend_by_user_id(user_id: str):
    db_contact_head_image, db_contact_remark, user_name = context.friend_finder.query_record_by_user_id(user_id)
    friend = get_friend_from_raw_info(db_contact_head_image, db_contact_remark, user_name)
    return friend


def get_session_by_user_id(friend: Friend, message_db_paths: List[str]):
    chat_table_name = 'Chat_' + friend.user_id_hash
    for message_db_path in message_db_paths:
        with sqlite3.connect(message_db_path) as conn:
            cursor = conn.cursor()
            table_exist_jdg_sql = "SELECT COUNT(*) FROM sqlite_master WHERE type='table' and name=?"
            cursor.execute(table_exist_jdg_sql, (chat_table_name,))
            table_count = cursor.fetchone()[0]
            if table_count == 0:
                cursor.close()
                continue
            message_query_sql = f'SELECT CreateTime, Message, Des, Type, MesLocalID FROM {chat_table_name}'
            cursor.execute(message_query_sql)
            chat_records = cursor.fetchall()
            messages = [WechatMessage(chat_record, friend.user_id_hash) for chat_record in chat_records]
            cursor.close()
            return Session(messages, friend)
    return []


def main():
    _, message_db_paths, mm_sqlite_db_path = get_wechat_db_file_infos()
    login_users = get_login_info()
    context.defer_init(mm_sqlite_db_path, login_users)

    write_friends()

    export_user_id = input('plz input user_id to export chat data: ')
    friend = get_friend_by_user_id(export_user_id)
    print(friend)  # dbg

    session = get_session_by_user_id(friend, message_db_paths)
    write_messages(session)


if __name__ == '__main__':
    main()
