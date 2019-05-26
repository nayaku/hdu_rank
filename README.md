# 说明

HDU_Rank是一款基于基于Flask、Vue.js和BootstrapVue的杭电刷题排行榜爬虫。

DEMO页面：

![demo_img](demo_img.png)

注意：由于本项目中使用到了Python3的uWSGI库，因此只能运行在Linux平台上面。

# 快速入门

```shell
# 依赖包
yum install libffi-devel -y
# 安装Python3（如果已经安装可以跳过）
wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz
tar -zxvf Python-3.7.3.tgz
cd Python-3.7.3
./configure
make && make install

# 安装LNMP环境（如果已经安装可以跳过）
wget http://soft.vpser.net/lnmp/lnmp1.6beta.tar.gz
tar -zxvf lnmp1.6beta.tar.gz
cd lnmp1.6beta
./install.sh
# 其中MySQL版本建议选择MySQL8，其余根据需求选择

# 安装screen和git（如果已经安装可以跳过）
yum install screen git vim
# 安装所需的PIP库
pip3 install flask pymysql requests uWSGI
# 增加hdurank的用户名和组
/usr/sbin/groupadd hdurank
/usr/sbin/useradd -g hdurank hdurank
# 克隆本项目
git clone https://github.com/736248591/hdu_rank.git
# 建立数据库
cd hdu_rank
mysql -u你的数据库用户名 -p你的数据库密码 < hdu_rank.sql
# 新建域名
lnmp vhost add
# 按照提示填写你的域名和项目本地存放的地址。注意，网站的根目录填写的是hdu_rank/static
# 编辑NGINX的配置
vim /usr/local/nginx/conf/vhost/你的域名.conf
# 在server的子级location的同级加入以下内容。
location ~* /api/{
    include  uwsgi_params;
    uwsgi_pass  127.0.0.1:5007;
    client_max_body_size 35m;
}
# 开启新的一个screen，这样在关闭终端以后程序不会被关闭
screen -R hdu_rank
# 启动服务器
uwsgi --ini uwsgi.ini 
```
# 进阶开发

## API接口

- ### /api/get_rank 获取排行榜
**参数：** （无）
**响应数据：**
```
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
```
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
```
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

```
  {
      "status": 操作状态 Boolean,
      "mgs": 错误原因 (当状态为false时，拥有这个字段）string
  }
```

- ### /api/logout_admin 管理员登出
**说明：** 清空session。
**参数：** (无)
**响应数据：**
```
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
```
  {
      "status": 操作状态 Boolean,
      "mgs": 错误原因 (当状态为false时，拥有这个字段）string
  }
```

- ### /api/get_login_info 获取登录信息
**参数：** （无）
**响应数据：**
```
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
```
  {
      "status": 操作状态 Boolean,
      "mgs": 错误原因 (当状态为false时，拥有这个字段）string
  }
```

- ### /api/crawl_stop 停止滚榜
**说明：** 必须先登录才能使用该接口。
**参数：**（无）
**响应数据：**
```
  {
      "status": 操作状态 Boolean,
      "mgs": 错误原因 (当状态为false时，拥有这个字段）string
  }
```

- ### /api/crawl_status 爬虫状态
**参数：**（无）
**响应数据：**
```
  {
      "status": 操作状态 Boolean,
      "mgs": 错误原因 (当状态为false时，拥有这个字段）string
      "crawl_status": 爬虫状态 union("runable","running","sleeping","stopped")
  }
```
## 手动编译客户端
安装Node.js和Yarn
```shell
cd hdu_rank
yarn
```

## 更新日记

#### 2019年5月26日

升级了依赖包的版本，解决安全隐患。

修复了数据库文件导入的BUG。

添加了说明文档中python3.7需要的依赖。

#### 2019年4月9日 

1.0 初次发布