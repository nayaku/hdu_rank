[![MIT](https://img.shields.io/github/license/736248591/TSF-TypeLib)](LICENSE)

# 说明

本项目是一款基于Flask和BootstrapVue的杭电刷题排行榜前后端分离的网站。

![add_notice](demo_img/add_notice.png)

![admin_index](demo_img/admin_index.png)

![admin_list](demo_img/admin_list.png)

![index](demo_img/index.jpg)

![login](demo_img/login.png)

![register](demo_img/register.png)

![user_index](demo_img/user_index.png)



### 3.0 我们添加了什么？

- [x] 用户登录、修改、注册
- [x] 用户自定义网页代码
- [x] 管理员添加与删除
- [x] 管理员管理员用户以及其他管理员
- [x] 一键初始化和运行
- [x] 可以在Windows和Linux上运行
- [x] 多进程、高并发
- [ ] 使用pip直接安装

### 2.0原有的功能

- [x] 添加用户
- [x] 爬取用户题数
- [x] 显示公告
- [x] 管理员登录
- [x] 管理员管理用户
- [x] 爬虫状态管理



# 环境需求

操作系统：Windows或者Linux均可。
python3.x	pip3	MySQL8.x

# 快速入门

## 安装所需的运行环境
``` sh
# 安装所需的PIP库
pip3 install flask pymysql requests flask_cors
# 国内用户可以使用在pip安装时候添加参数，如：
pip3 install -i https://mirrors.ustc.edu.cn/pypi/web/simple/ flask pymysql requests flask_cors
# 克隆项目
git clone https://github.com/736248591/hdu_rank.git
# 进入项目
cd hdu_rank
# 运行安装助手
python3 helper.py
# 启动爬虫进程
python3 hdu_crawl.py &
```

注：以下方式二选一即可

## 1. 独立运行

<font color='#CC0033'>注意在windows下tornado无法以多进程运行。</font>

```shell
# 注意：编译安装Python前请确安装了libffi-devel，否则这里pip3 install会出错。
# 安装所需的PIP库
pip3 install tornado
# 国内用户可以使用以下命令来替换上面命令
pip3 install -i https://mirrors.ustc.edu.cn/pypi/web/simple/ tornado
cd hdu_rank
# 启动tornado
python3 run_tornado.py
```

## 2. 在NGINX下运行
```sh
# 注意：编译安装Python前请确安装了libffi-devel，否则这里pip3 install会出错。
# 安装所需的PIP库
pip3 install uWSGI
# 增加hdurank的用户名和组
/usr/sbin/groupadd hdurank
/usr/sbin/useradd -g hdurank hdurank
# 新建域名
lnmp vhost add
# 按照提示填写你的域名和项目本地存放的地址。注意，网站的根目录填写的是hdu_rank/static
```
![vhost_add](vhost_add.jpg)
```shell
# 编辑NGINX的配置
vim /usr/local/nginx/conf/vhost/你的域名.conf
# 在server的子级location的同级加入以下内容。
location ~* /api/{
    include  uwsgi_params;
    uwsgi_pass  127.0.0.1:5007;
}
# 重启nginx服务器
lnmp nginx reload
# 开启新的一个screen，这样在关闭终端以后程序不会被关闭
screen -R hdu_rank
# 启动uwsgi服务器
uwsgi --ini uwsgi.ini 
```

## 3. mod_wsgi(Apache)、其他独立WSGI容器、FastCGI、CGI

这些方式可以查看[Flask官方中文文档](http://docs.jinkan.org/docs/flask/)，这里不再赘述。


# 进阶开发

## 数据库逻辑表

| 表名            | 列名          | 说明         | 数据类型                                   | 长度  | 默认值       | 约束      |
|---------------|-------------|------------|----------------------------------------|-----|-----------|---------|
| users         | id          | 用户唯一标识     | uint                                   | 10  |           | 主键、自动递增 |
|               | uid         | 登录账号       | char                                   | 16  |           | 不为空，唯一  |
|               | pwd         | 密码         | char                                   | 128 |           | 不为空     |
|               | class\_name | 班级名        | char                                   | 24  |           |         |
|               | name        | 姓名         | char                                   | 16  |           | 不为空     |
|               | motto       | 格言         | varchar                                | 255 |           |         |
|               | account     | 杭电账号       | varchar                                | 64  |           | 不为空     |
|               | solved\_num | 解决题数       | unit                                   |     |           |         |
|               | status      | 状态         | "enum 'unchecked','fetching','active'" |     | unchecked |         |
|               | html        | 自定义页面代码    | longtext                               |     |           |         |
|               |             |            |                                        |     |           |         |
| admins        | id          | 管理员唯一标识    | uint                                   | 10  |           | 主键、自动递增 |
|               | uid         | 管理员登录账号    | char                                   | 16  |           | 不为空，唯一  |
|               | is\_super   | 是否可以管理其他用户 | tinyint                                | 1   | FALSE     | 不为空     |
|               | pwd         | 密码         | char                                   | 128 |           | 不为空     |
|               |             |            |                                        |     |           |         |
| server\_infos | id          |            | uint                                   |     |           | 主键、自动递增 |
|               | notice      | 公告         | longtext                               |     |           |         |




## API接口

- ### /api/get_rank 获取排行榜
**参数：** （无）
**响应数据：**
```
  {
      status: 操作状态 Boolean,
      notice: 公告 string,
      crawl_status: 爬虫状态 union("runnable","running","sleeping","stopped")
      users: 用户列表（当状态为True时，拥有这个字段）
      [
          {
              id: 用户ID unsigned int,
              uid 登录账号 string,
              class_name 班级 string,
              name 姓名 string,
              motto 格言 string,
              account 账号 string,
              solved_num 题数 int,
              status 状态 union("unchecked","fetching","active","disconnect")
          }
      ],
      user:{
          id 用户ID unsigned int,
          uid 登录账号 string,
          class 班级 string,
          name 姓名 string,
          motto 格言 string,
          account 账号 string,
          solved_num 题数 int,
          status 状态 union("unchecked","fetching","active"),
          html 自定义页面代码 string
      },
      admin:{
          id: 管理员ID int,
          uid: 管理员 string,
          is_super: 是否可以管理其他用户 bool,
      }
  }
```

- ### /api/login 用户登录 
**说明：**  不填写任何信息的时候，则返回当前登录信息。
**参数：**
| 字段名 | 数据类型 | 默认值 |  描   述   |
| :----: | :------: | :----: | :--------: |
| uid	 | string(16) |        | 账号  |
| pwd	 | string(16) |    ""  | 密码，sha3-512(原始密码)，重复加密6次 |
**响应数据：**

```
  {
      status: 操作状态 Boolean,
      mgs: 错误原因 (当状态为false时，拥有这个字段）string，
      // 当登录成功时候显示以下信息
      user:{
          id 用户ID unsigned int,
          uid 登录账号 string,
          class 班级 string,
          name 姓名 string,
          motto 格言 string,
          account 账号 string,
          solved_num 题数 int,
          status 状态 union("unchecked","fetching","active"),
          html 自定义页面代码 string
      },
      admin:{
          id: 管理员ID int,
          uid: 管理员 string,
          is_super: 是否可以管理其他用户 bool,
      }
  }
```

- ### /api/put_user 添加或者修改用户
**说明：**  修改时候，只需提交ID和修改的字段即可。添加用户时候，不需要id。
**参数：**
| 字段名 | 数据类型 | 默认值 |  描   述   |
| :----: | :------: | :----: | :--------: |
| id	 | int |        | 用户唯一标识  |
| uid	 | string(16) |        | 登录账号  |
| pwd	 | string(16) |    ""  | 密码，sha3-512(原始密码)，重复加密6次 |
| class_name	 | string(24) |    ""    | 班级 |
| name	 | string(16) |        | 姓名  |
| account |  string(64)  |        |  杭电账号  |
|  motto | string(255) |        |   格言   |
|  status | 'unchecked','fetching','active' |        |   状态，只有管理层才能修改   |
|  html | string |        |   自定义代码   |
**响应数据：**
```
  {
      status: 操作状态 Boolean,
      mgs: 错误原因 (当状态为false时，拥有这个字段）string
  }
```

- ### /api/validate_user 验证字段
**说明：**  注册的时候用来验证字段。
**参数：**
| 字段名 | 数据类型 | 默认值 |  描   述   |
| :----: | :------: | :----: | :--------: |
|  field | string |        |   字段   |
|  value | string |        |  数值   |
  **响应数据：**
```
  {
      status: 操作状态 Boolean,
      mgs: 错误原因 (当状态为false时，拥有这个字段）string
  }
```

- ### /api/logout 登出  用户和管理员均可使用。
**参数：** (无)
**响应数据：**
```
  {
      status: 操作状态 Boolean
  }
```


- ### /api/remove_user 删除用户
**说明：** 必须先登录才能使用该接口。用户只能删除自己，只有管理员可以删除任意用户。
**参数：**
| 字段名 | 数据类型 | 默认值 |  描   述   |
| :----: | :------: | :----: | :--------: |
| id	 |   unsigned int |        | 用户ID  |
**响应数据：**
```
  {
      status: 操作状态 Boolean,
      mgs: 错误原因 (当状态为false时，拥有这个字段）string
  }
```

- ### /api/login_admin 管理员登录
**说明：**  不填写任何信息的时候，则返回当前登录信息。
**参数：**
| 字段名 | 数据类型 | 默认值 |  描   述   |
| :----: | :------: | :----: | :--------: |
| uid	 |   unsigned int |        | 管理员ID  |
| pwd	 |   string |        | 密码，sha3-512(原始密码)，重复加密6次 |
**响应数据：**
```
  {
      status: 操作状态 Boolean,
      mgs: 错误原因 (当状态为false时，拥有这个字段）string,
      admin:{
          id: 管理员ID int,
          uid: 管理员 string,
          is_super: 是否可以管理其他用户 bool,
      }
  }
```

- ### /api/list_admin 管理员列表
**参数：** (无)
**响应数据：**
```
  {
      status: 操作状态 Boolean,
      mgs: 错误原因 (当状态为false时，拥有这个字段）string,
      admins:[
      	{
            id: 管理员ID int,
            uid: 管理员登录账号 int,
            is_super: 是否可以管理其他管理员 bool
        }
      ]
  }
```

- ### /api/validate_admin 验证管理员字段
**说明：**  添加管理员的时候用来验证字段。
**参数：**
| 字段名 | 数据类型 | 默认值 |  描   述   |
| :----: | :------: | :----: | :--------: |
|  field | string |        |   字段   |
|  value | string |        |  数值   |
  **响应数据：**
```
  {
      status: 操作状态 Boolean,
      mgs: 错误原因 (当状态为false时，拥有这个字段）string
  }
```

- ### /api/put_admin 添加或修改管理员
**说明：**  修改时候，只需提交ID和修改的字段即可。
**参数：**
| 字段名 | 数据类型 | 默认值 |  描   述   |
| :----: | :------: | :----: | :--------: |
| id	 |   unsigned int |        | ID  |
| uid	 |   string(16) |        | 管理员ID  |
| is_super	 |   bool |        | 是否可以管理其他用户  |
| pwd	 |   string(128) |        | 密码，sha3-512(原始密码)，重复加密6次  |
**响应数据：**
```
  {
      status: 操作状态 Boolean,
      mgs: 错误原因 (当状态为false时，拥有这个字段）string,
  }
```

- ### /api/remove_admin  删除管理员
**说明：** 必须先登录才能使用该接口。只有超级管理员才能删除其他管理员。
**参数：**
| 字段名 | 数据类型 | 默认值 |  描   述   |
| :----: | :------: | :----: | :--------: |
| id	 |   unsigned int |        | 用户ID  |
**响应数据：**
```
  {
      status: 操作状态 Boolean,
      mgs: 错误原因 (当状态为false时，拥有这个字段）string
  }
```

- ### /api/crawl_start 开始滚版
**说明：** 只有管理员才能使用该接口。
**参数：**（无）
**响应数据：**
```
  {
      status: 操作状态 Boolean,
      mgs: 错误原因 (当状态为false时，拥有这个字段）string
  }
```

- ### /api/crawl_stop 停止滚榜
**说明：** 只有管理员才能使用该接口。
**参数：**（无）
**响应数据：**
```
  {
      status: 操作状态 Boolean,
      mgs: 错误原因 (当状态为false时，拥有这个字段）string
  }
```


- ### /api/add_notice 添加通知
**说明：** 只有管理员才能使用该接口。
**参数：**
| 字段名 | 数据类型 | 默认值 |  描   述   |
| :----: | :------: | :----: | :--------: |
| notice	 |   string |        | 通知  |
**响应数据：**
```
  {
      status: 操作状态 Boolean,
      mgs: 错误原因 (当状态为false时，拥有这个字段）string
  }

```



## 手动编译客户端

安装Node.js和Yarn

```shell
cd hdu_rank
yarn global add @vue/cli
yarn install
yarn build
```

## 更新日记

### 2021年5月21日

修正PyMysql升级后造成的错误

更新@vue/cli-service到4.x

### 2021年5月16日

更新依赖

### 2021年5月7日

更新依赖

### 2020年11月10日

修正题数未从高到底排序的BUG。

### 2020年11月8日

更新依赖

### 2020年10月13日

更新依赖

### 2020年9月19日

更新依赖

### 2020年9月10日

更新依赖

### 2020年8月8日

更新依赖并重新编译客户端。

### 2020年7月17日

- 更新并重新编译客户端。

### 2020年6月18日（3.0）

- 大幅度修改和重构前端和后端代码。
- 增加了用户登录、修改、注册功能。
- 增加了用户自定义网页代码功能。
- 增加了管理员添加与删除、管理员用户以及其他管理员功能
- 一键初始化和运行
- 可以在Windows和Linux上运行
- 多进程、高并发

### 2020年3月17日

- 更新客户端依赖库并重新编译客户端。

### 2019年12月27日

- 更新库。
- 删除fibers依赖。

### 2019年10月22日

- 增大爬虫重试连接次数。
- 更新并重新编译客户端。

### 2019年9月27日

- 修改uwsgi服务器配置。

- 修正了爬虫连接的一些问题。

### 2019年9月25日

- 删除了没用的右上角丝带，github地址添加到页脚，避免移动端的页面变得很恶心。
- 修改页面语言标签的错误。
- 在账号合法性判断之前，添加了对杭电OJ连接的判断。
- 改善移动端的显示体验。

### 2019年9月23日

- 修改数据库Users表中name字段大小，从长度为8改为16。
- 在添加账号之前，先对账号进行验证。
- 修正了无法写入日记的错误。日记写入位置为/tmp/uwsgi.pid
- 更新了依赖包，重新编译网页客户端。

### 2019年9月3日

- 修改设定的备注，并且修改主循环默认为30分钟循环一次。

### 2019年9月2日

- 更新了依赖包，重新编译网页客户端。

#### 2019年7月28日

- 修正输入管理员密码回车时候，不登录而刷新页面的操作。
- 公告支持Markdown语法高亮。
- 更新了所有组件。
- 右上角添加了包含github项目链接的丝带。
- 修正添加用户成功以后，用户信息仍然存在表单中的问题。
- 修正管理员登录以后，密码仍然储存在表单中问题。
- 修正重新开启网页以后，公告不可以修改，只能新建的问题。
- 删除产品模式下的所有console.log输出。


#### 2019年5月31日

- 更新所有组件，移除安全隐患。
- 移除了富文本编辑器。
- 增加了添加公告功能。
- 修复长时间不使用的时候，MySQL连接掉线问题。

#### 2019年5月31日

- 更新AXIOS到0.19.0使得修复其安全漏洞。
- 顺带更新一下其他的组件。

#### 2019年5月26日

- 升级了依赖包的版本，解决安全隐患。

- 修复了数据库文件导入的BUG。

- 添加了说明文档中python3.7需要的依赖。

- 未创建管理员密码错误。

- 添加了网站的图标和标题。

#### 2019年4月24日
- 当密码不存在的时候会自动生成新密码保存在admin.key文件里面。

#### 2019年4月9日 

1.0 初次发布

```

```