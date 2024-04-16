import sqlite3
import os
from typing import Callable
from utils import singleton
from pathlib import Path

home_path = Path.home()
ITUNES_BAK_PATH = os.path.join(home_path, r'AppData\Roaming\Apple Computer\MobileSync\Backup\00008020-001424E62123002E')  # TODO: 去除硬编码
ITUNES_BAK_MANIFEST_PATH = os.path.join(ITUNES_BAK_PATH, 'Manifest.db')


def get_file_bak_path(file_ID: str):
    return os.path.join(ITUNES_BAK_PATH, file_ID[:2], file_ID)


@singleton
class ITunesBakFinder:
    def __init__(self):
        self.itunes_bak_manifest_conn = sqlite3.connect(ITUNES_BAK_MANIFEST_PATH)
        self.itunes_bak_manifest_cursor = self.itunes_bak_manifest_conn.cursor()
        all_files_query_sql = 'SELECT fileID, relativePath, domain FROM Files'
        self.itunes_bak_manifest_cursor.execute(all_files_query_sql)
        all_files_query_result = self.itunes_bak_manifest_cursor.fetchall()
        self.file_bak_raw_infos = all_files_query_result

    def find_file_bak_infos_by_relative_path(self, relative_path_substr: str, mode='in'):
        res = []
        for file_ID, relative_path, _ in self.file_bak_raw_infos:
            if (mode == 'pre' and relative_path.startswith(relative_path_substr)) or (
                    mode == 'in' and relative_path_substr in relative_path) or (mode == 'suf' and relative_path.endswith(relative_path_substr)):
                file_bak_path = get_file_bak_path(file_ID)
                res.append((file_bak_path, relative_path))
        return res

    def find_file_bak_infos_by_fn(self, fn: Callable[[str, str, str], bool]):
        res = []
        for file_ID, relative_path, domain in self.file_bak_raw_infos:
            if fn(file_ID, relative_path, domain):
                file_bak_path = get_file_bak_path(file_ID)
                res.append((file_bak_path, relative_path))
        return res

    def __del__(self):
        self.itunes_bak_manifest_cursor.close()
        self.itunes_bak_manifest_conn.close()


def main():
    iTunes_bak_finder = ITunesBakFinder()
    res1 = iTunes_bak_finder.find_file_bak_infos_by_relative_path('message')
    print(len(res1), res1[0])  # 1565

    def wechat_dbs_query_condition(_: str, relative_path: str, domain: str):
        return domain.endswith('com.tencent.xin') and '/DB/' in relative_path and relative_path.endswith('.sqlite')
    res2 = iTunes_bak_finder.find_file_bak_infos_by_fn(wechat_dbs_query_condition)
    print(len(res2), res2)  # 8


if __name__ == '__main__':
    main()
