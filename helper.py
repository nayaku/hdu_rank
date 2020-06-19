#!/usr/bin/python3
import hashlib
import pymysql

from my_setting import DB_NAME, DB_ADDR

print(
    '''\
    +---------------------------------------------------------------------------+
    |                            欢迎使用杭电排行榜！                           |
    +---------------------------------------------------------------------------+
    | 本项目是一款基于基于Flask和BootstrapVue的杭电刷题排行榜前后端分离的网站。 |
    |    Github：https://github.com/736248591/hdu_rank, Written by 雪靡         |
    +---------------------------------------------------------------------------+
    '''
)

db_root_pwd = input("请输入root账号密码：\n")
con = pymysql.connect(host=DB_ADDR, user='root', password=db_root_pwd, autocommit=True)

with con:
    sql = "show databases like '%s'" % DB_NAME
    with con.cursor() as cursor:
        cursor.execute(sql)
        row = cursor.fetchone()
        if row:
            is_continue = input("已经存在%s数据库，是否确定重建？\n注意原有的数据会丢失！\n[y/n]" % DB_NAME)
            is_continue = is_continue.lower()
            if is_continue == 'y':
                sql = 'DROP DATABASE %s' % DB_NAME
                cursor.execute(sql)
            else:
                exit(1)

        sql = "CREATE DATABASE `%s` CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_unicode_ci';" % DB_NAME
        cursor.execute(sql)

    con.select_db(DB_NAME)
    with con.cursor() as cursor:
        create_admins = '''
        CREATE TABLE `admins`  (
        `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
        `uid` char(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
        `is_super` tinyint(1) NOT NULL DEFAULT 0,
        `pwd` char(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
        PRIMARY KEY (`id`) USING BTREE,
        UNIQUE INDEX `uid`(`uid`) USING BTREE
        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;'''
        create_server_infos = '''
        CREATE TABLE `server_infos`  (
        `id` int(10) UNSIGNED NOT NULL,
        `notice` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
        PRIMARY KEY (`id`) USING BTREE
        ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;'''
        create_users = '''
        CREATE TABLE `users`  (
        `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '用户唯一标识',
        `uid` char(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
        `pwd` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
        `class_name` char(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
        `name` char(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '姓名',
        `motto` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '格言',
        `account` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '账号',
        `solved_num` int(10) UNSIGNED NULL DEFAULT NULL COMMENT '解决题数',
        `status` enum('unchecked','fetching','active') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'unchecked' COMMENT '状态',
        `html` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
        PRIMARY KEY (`id`) USING BTREE,
        UNIQUE INDEX `uid`(`uid`) USING BTREE
        ) ENGINE = MyISAM CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;'''
        cursor.execute(create_admins)
        cursor.execute(create_server_infos)
        cursor.execute(create_users)

        sql = "DROP USER IF EXISTS `hr`@`localhost`"
        cursor.execute(sql)

        sql = "CREATE USER `hr`@`localhost` IDENTIFIED BY 'hr@hr';"
        cursor.execute(sql)
        sql = 'GRANT ALL ON `%s`.* TO `hr`@`localhost`;' % DB_NAME.replace('_', '\\_')
        cursor.execute(sql)

        sql = "INSERT INTO server_infos(id,notice) VALUES(1, '')"
        cursor.execute(sql)

        admin_uid = input('请输入超级管理员账号名：\n')
        admin_pwd = input('请输入超级管理员密码：\n')
        admin_pwd = admin_pwd.encode('utf-8')
        for i in range(0, 6):
            s = hashlib.sha3_512()
            s.update(admin_pwd)
            admin_pwd = s.hexdigest().encode('utf-8')
        sql = "INSERT INTO admins(uid,is_super,pwd) VALUES(%s,1,%s)"
        cursor.execute(sql, (admin_uid, admin_pwd))

print('============================== 配置成功 ==============================')
