import sqlite3

# iTunes 备份内容浅析 https://sspai.com/post/79029


def main():
    conn = sqlite3.connect(r'C:\Users\admin\AppData\Roaming\Apple Computer\MobileSync\Backup\00008020-001424E62123002E\Manifest.db')
    cursor = conn.cursor()
    # 已知只有67条记录
    sql1 = "select relativePath, flags from Files where relativePath like '%wechat%' COLLATE utf8_general_ci"
    cursor.execute(sql1)
    result = cursor.fetchall()
    print(result)
    sql2 = "select * from Files where relativePath like '%MM.sqlite'"
    cursor.execute(sql2)
    result = cursor.fetchall()
    print(result)
    conn.close()


if __name__ == '__main__':
    main()
