from typing import List
from iTunes_bak_finder import ITunesBakFinder
from friend_finder import FriendFinder
from utils import singleton
from friend import Friend


@singleton
class Context:
    def __init__(self) -> None:
        self.iTunes_bak_finder = ITunesBakFinder()
        self.friend_finder = None
        self.login_users = None
        self.login_user = None

    def defer_init(self, mm_sqlite_db_path: str, login_users: List[Friend]):
        self.init_friend_finder(mm_sqlite_db_path)
        self.init_login_users(login_users)

    def init_friend_finder(self, mm_sqlite_db_path: str):
        self.friend_finder = FriendFinder(mm_sqlite_db_path)

    def init_login_users(self, login_users: List[Friend]):
        self.login_users = login_users
        if login_users:
            self.login_user = login_users[0]


context = Context()
