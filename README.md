PIP库

flask pymysql requests

**解决方案：**

增加用户和组，具体命令如下：

```ini
/usr/sbin/groupadd hdurank

/usr/sbin/useradd -g hdurank hdurank
```

增加了www的用户名和组，之后修改uWsgi配置文件：

```ini
[uwsgi]

uid = hdurank

gid = hdurank
```

# API接口

- ### /api/get_rank 获取排行榜
**参数：** （无）
**响应数据：**
```json
  {
      "status": 操作状态 Boolean,
      "msg": 错误原因 (当状态为false时，拥有这个字段）string,
      "users": 用户列表(当状态为True时，拥有这个字段）
      [
          [
              id 用户ID unsigned int,
              name 姓名 string,
              account 账号 string,
              motto 格言 string,
              solved_num 题数 int,
              status 状态 union("unchecked","fetching","active")
          ]
      ]
  }
```

- ### /api/add 添加用户
  **参数：**
| 字段名 | 数据类型 | 默认值 |  描   述   |
| :----: | :------: | :----: | :--------: |
| name	 | string(8) |        | 姓名  |
| account |  string(64)  |        |  账号  |
|  motto | string(255) |        |   格言   |
**响应数据：**
```json
  {
      "status": 操作状态 Boolean,
      "mgs": 错误原因 (当状态为false时，拥有这个字段）string
  }
```

- ### /api/remove 删除用户
**说明：** 必须先登录才能使用该接口。
**参数：**
| 字段名 | 数据类型 | 默认值 |  描   述   |
| :----: | :------: | :----: | :--------: |
| id	 |   unsigned int |        | 用户ID  |
**响应数据：**
```json
  {
      "status": 操作状态 Boolean,
      "mgs": 错误原因 (当状态为false时，拥有这个字段）string
  }
```

- ### /api/login_admin 管理员登录
**说明：** 登录的token留在Session中。
**参数：**
| 字段名 | 数据类型 | 默认值 |  描   述   |
| :----: | :------: | :----: | :--------: |
| pwd	 |   string |        | 管理员密码<br/>字段=sha3-512(PWD+time%10000+PWD) |
**响应数据：**

```json
  {
      "status": 操作状态 Boolean,
      "mgs": 错误原因 (当状态为false时，拥有这个字段）string
  }
```

- ### /api/logout_admin 管理员登出
**说明：** 清空session。
**参数：** (无)
**响应数据：**
```json
  {
      "status": 操作状态 Boolean,
      "mgs": 错误原因 (当状态为false时，拥有这个字段）string
  }
```

- ### /api/confirm 确认用户

  **说明：** 必须先登录才能使用该接口。
  **参数：**
| 字段名 | 数据类型 | 默认值 |  描   述   |
| :----: | :------: | :----: | :--------: |
| id	 |   unsigned int |        | 用户ID  |
**响应数据：**
```json
  {
      "status": 操作状态 Boolean,
      "mgs": 错误原因 (当状态为false时，拥有这个字段）string
  }
```

- ### /api/get_login_info 获取登录信息
**参数：** （无）
**响应数据：**
```json
  {
      "status": 操作状态 Boolean,
      "mgs": 错误原因 (当状态为false时，拥有这个字段）string,
      "is_admin":是否已经登录管理员权限 Boolean
  }
```

- ### /api/crawl_start 开始滚版
**说明：** 必须先登录才能使用该接口。
**参数：**（无）
**响应数据：**
```json
  {
      "status": 操作状态 Boolean,
      "mgs": 错误原因 (当状态为false时，拥有这个字段）string
  }
```

- ### /api/crawl_stop 停止滚榜
**说明：** 必须先登录才能使用该接口。
**参数：**（无）
**响应数据：**
```json
  {
      "status": 操作状态 Boolean,
      "mgs": 错误原因 (当状态为false时，拥有这个字段）string
  }
```

- ### /api/crawl_status 爬虫状态
**参数：**（无）
**响应数据：**
```json
  {
      "status": 操作状态 Boolean,
      "mgs": 错误原因 (当状态为false时，拥有这个字段）string
      “crawl_status”： 爬虫状态 union("runable","running","sleeping","stopped")
  }
```