import sqlite3
from utils import singleton
from friend import get_friend_from_raw_info


@singleton
class FriendFinder:
    def __init__(self, mm_sqlite_db_path: str) -> None:
        self.mm_sqlite_db_conn = sqlite3.connect(mm_sqlite_db_path)
        self.mm_sqlite_db_cursor = self.mm_sqlite_db_conn.cursor()
        all_friends_query_sql = 'SELECT dbContactHeadImage, dbContactRemark, userName FROM Friend'
        self.mm_sqlite_db_cursor.execute(all_friends_query_sql)
        all_friends_query_result = self.mm_sqlite_db_cursor.fetchall()
        self.all_friends_raw_infos = all_friends_query_result
        self.all_friends = [
            get_friend_from_raw_info(db_contact_head_image, db_contact_remark, user_name)
            for db_contact_head_image, db_contact_remark, user_name in self.all_friends_raw_infos
        ]

    def query_record_by_user_id(self, user_id: str):
        query_record_sql = 'SELECT dbContactHeadImage, dbContactRemark, userName FROM Friend WHERE userName=?'
        self.mm_sqlite_db_cursor.execute(query_record_sql, (user_id,))
        res = self.mm_sqlite_db_cursor.fetchone()
        if not res:
            raise Exception(f'Friend(userName={user_id}) record not found')
        return res

    def __del__(self):
        self.mm_sqlite_db_cursor.close()
        self.mm_sqlite_db_conn.close()
