<template>
  <div id="app">
    <div class="py-5">
      <div class="container">
        <div class="row">
          <div class="col-md-12">
            <h1 class="text-center shadow-none"><b class="" style="    font-weight: bold;">HDU排行榜</b></h1>
          </div>
        </div>
      </div>
    </div>
    <div class="py-2">
      <div class="container">
        <div class="row">
          <div class="col-md-12">
            <div class="table-responsive">
              <table class="table">
                <caption>状态：<span id="status">{{crawlStatus}}
                  <i :class="'fa d-inline fa-circle'+crawlStatusClass"></i>
                  <template v-if="isAdmin">
                      <b-button @click="beginCrawl" variant="link" v-if="crawlStatus==='stopped'">启动</b-button>
                    <b-button @click="stopCrawl" variant="link" v-else>停止</b-button>
                  </template>
                </span></caption>
                <thead>
                <tr>
                  <th>#</th>
                  <th>姓名</th>
                  <th>账号</th>
                  <th>格言</th>
                  <th>题数</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="(user,index) in users" v-bind:key="user['id']">
                  <td>{{index+1}}
                    <i class="fa d-inline fa-lg fa-times text-danger" v-if="isAdmin"
                       @click="removeUser(user['id'])"></i>
                  </td>
                  <td>{{user['name']}}</td>
                  <td>{{user['account']}}</td>
                  <td>{{user['motto']}}</td>
                  <td>
                    <template v-if="user['status']==='unchecked'">
                      <span class="text-warning">待确认</span>
                      <i class="fa d-inline fa-lg fa-check text-success" @click="confirmUser(user['id'])"
                         v-if="isAdmin"></i>
                    </template>
                    <template v-else>{{user['solved_num']}}</template>
                  </td>
                </tr>
                </tbody>
              </table>
              <div>
                <b-button variant="link" @click="addUserModalShow = true">
                  <i class="fa fa-plus fa-fw fa-lg py-1"></i>
                  <span style="font-size:110%">添加账号</span></b-button>
              </div>
              <div v-if="isAdmin">
                <b-button variant="link" @click="addNoticeModalShow = true">
                  <i class="fa fa-plus fa-fw fa-lg py-1"></i>
                  <span style="font-size:110%">添加公告</span></b-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- 公告 -->
    <div class="py-2">
      <div class="container">
        <div class="row">
          <div class="col-md-12">
            <vue-markdown :source="notice"></vue-markdown>
            <!--            <p class="lead">-->
            <!--              <span style="font-size: x-large;font-weight: bold; word-wrap:break-word" v-html="notice">-->
            <!--              </span>-->

            <!--            </p>-->
          </div>
        </div>
      </div>
    </div>
    <div class="py-3">
      <div class="container">
        <div class="row">
          <div class="col-md-12 text-center">
            <p class="mb-0">Writed By 雪靡. All rights reserved |
              <b-button variant="link" v-if="!isAdmin" @click="adminLoginModalShow = true">管理员登录</b-button>
              <b-button variant="link" v-else @click="adminLogout">管理员退出</b-button>
              | Open Source on <a href="https://github.com/736248591/hdu_rank" target="_blank">GitHub</a>
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加用户 -->
    <b-modal id="addUserModal" title="添加用户" ok-title="确认" cancel-title="取消" @ok="addUser"
             :ok-disabled="addUserModalOkDisabled" v-model="addUserModalShow">
      <b-form @submit="addUser">
        <b-form-group
          label="姓名：">
          <b-form-input
            :state="formUserNameState"
            aria-describedby="formUserNameFeedback"
            placeholder="请在这里输入您的姓名。"
            required
            trim
            type="text"
            v-model="formUserName">
          </b-form-input>
          <b-form-invalid-feedback id="formUserNameFeedback">
            姓名长度应该在2-16之间。
          </b-form-invalid-feedback>
        </b-form-group>
        <b-form-group
          label="账号：">
          <b-form-input
            :state="formAccountState && formAccountAvailable"
            placeholder="请在这里输入您的杭电的账号名。"
            v-model="formAccount"
            required
            trim
            @blur="validateFormAccount"></b-form-input>
        </b-form-group>
        <b-form-invalid-feedback :state="formAccountState">
          账号长度应该在1-64之间。
        </b-form-invalid-feedback>
        <b-form-invalid-feedback :state="formAccountAvailable">
          {{formAccountServerFeedbackString}}
        </b-form-invalid-feedback>
        <b-form-group
          label="格言：">
          <b-form-textarea
            :state="formMottoState"
            v-model="formMotto"
            rows="3"
            aria-describedby="formMottoFeedback"></b-form-textarea>
          <b-form-invalid-feedback id="formMottoFeedback">格言长度不应该大于255。</b-form-invalid-feedback>
        </b-form-group>
        <!--        <div class="form-group row"><label for="user_name" class="col-2 col-form-label">姓名</label>-->
        <!--          <div class="col-10">-->
        <!--            <input type="text" class="form-control" id="user_name" placeholder="请在这里输入您的姓名。" v-model="formUserName">-->
        <!--          </div>-->
        <!--        </div>-->
        <!--        <div class="form-group row"><label for="account" class="col-2 col-form-label">账号</label>-->
        <!--          <div class="col-10">-->
        <!--            <input type="text" class="form-control" id="account" placeholder="请在这里输入您的杭电的账号名。" v-model="formAccount">-->
        <!--          </div>-->
        <!--          <div class="text-right col-12 inline form-text" style="margin:0;font-size:12px">-->
        <!--            <small class="text-right text-danger"> 注意：这里填写的是您杭电的登录账号，不是用户名，请注意！</small>-->
        <!--          </div>-->
        <!--        </div>-->
        <!--        <div class="form-group row"><label class="col-2 col-form-label">格言</label>-->
        <!--          <div class="col-10">-->

        <!--          </div>-->
        <!--        </div>-->
      </b-form>
      <!--      <b-form-textarea v-model="formMotto" rows="3"></b-form-textarea>-->
    </b-modal>
    <!-- 管理员登录弹窗 -->
    <b-modal id="adminLoginModal" title="管理员登录" ok-title="确认" cancel-title="取消" @ok="adminLogin"
             v-model="adminLoginModalShow">
      <b-form @submit="adminLogin">
        <b-form-group
          label="密码：">
          <b-form-input
            v-model="adminPwd"
            type="password"
            required
            placeholder="请在这里输入管理员密码。">

          </b-form-input>
        </b-form-group>
        <!--        <div class="form-group"><label for="admin_password">密码</label>-->
        <!--          <input id="admin_password"-->
        <!--                 type="password"-->
        <!--                 class="form-control"-->
        <!--                 placeholder="请在这里输入管理员密码。"-->
        <!--                 v-model="adminPwd">-->
        <!--        </div>-->
      </b-form>
    </b-modal>
    <!-- 消息弹窗 -->
    <b-modal id="msgModal" size="sm" :title="msgTitle" ok-title="确认" cancel-title="取消" @ok="msgOkCallback"
             @cancel="msgCancelCallback" :ok-only="msgOkOnly" v-model="msgVisible">
      <p :class="msgClass" v-html="msg"></p>
    </b-modal>
    <!-- 添加公告 -->
    <b-modal id="addNoticeModal" title="添加公告" ok-title="确认" cancel-title="取消" @ok="addNotice" size="xl"
             v-model="addNoticeModalShow">
      <form @submit="addNotice">
        <b-form-textarea v-model="newNotice" rows="8"></b-form-textarea>
        <hr/>
        <vue-markdown :source="newNotice"></vue-markdown>
      </form>
    </b-modal>
  </div>
</template>

<script>
  import VueMarkdown from 'vue-markdown'

  let SHA = require('jssha')

  export default {
    components: { VueMarkdown },
    name: 'app',
    data () {
      return {
        crawlStatus: '',
        isAdmin: false,
        users: [],
        formUserName: '',
        formAccount: '',
        formAccountAvailable: false,
        formAccountServerFeedbackString: '当失去焦点时将验证账号',
        formMotto: '',
        msg: '',
        msgClass: '',
        msgTitle: '',
        msgOkCallback: function () {
        },
        msgCancelCallback: function () {
        },
        msgOkOnly: false,
        msgVisible: false,
        adminPwd: '',
        adminLoginModalShow: false,
        addUserModalShow: false,
        notice: '',
        newNotice: '',
        addNoticeModalShow: false
      }
    },
    methods: {
      getRank () {
        this.$ajax.get('/get_rank').then((resp) => {
          console.log(resp)
          if (resp['status']) {
            this.users = resp['users']
            this.newNotice = this.notice = resp['notice']
          }
        })
      },
      validateFormAccount () {
        this.formAccountServerFeedbackString = '检测中……'
        let params = {
          account: this.formAccount
        }
        this.$ajax.get('/validate_user', { params }).then(resp => {
          if (!resp.status) {
            this.formAccountServerFeedbackString = resp.msg
            this.formAccountAvailable = false
          } else {
            this.formAccountAvailable = true
          }
        })
      },
      addUser () {
        let params = {
          name: this.formUserName,
          account: this.formAccount,
          motto: this.formMotto
        }
        this.$ajax.get('/add', { params }).then(resp => {
          if (resp.status) {
            this.showMsgModal('提示', '操作成功！', () => {
              this.formUserName = ''
              this.formAccount = ''
              this.formMotto = ''
              this.getRank()
            })
          } else {
            this.showMsgModal('错误', resp.msg)
          }
        })
      },
      removeUser (id) {
        this.showMsgModal('提示', '是否确认删除？', () => {
          this.$ajax.get('/remove', { params: { id } }).then(resp => {
            if (resp.status) {
              this.getRank()
            } else {
              this.showMsgModal('错误', resp.msg)
            }
          })
        }, function () {
        }, false)
      },
      confirmUser (id) {
        this.$ajax.get('/confirm', { params: { id } }).then(resp => {
          if (resp.status) {
            this.getRank()
          } else {
            this.showMsgModal('错误', resp.msg)
          }
        })
      },
      adminLogin (event) {
        event.preventDefault()
        let sha = new SHA('SHA3-512', 'TEXT')
        let timeToken = Math.floor((new Date()).getTime() / 10000)
        console.log('time:' + timeToken)
        sha.update(timeToken + this.adminPwd + timeToken)
        let pwd = sha.getHash('HEX')
        console.log('token:' + pwd)
        this.$ajax.get('/login_admin', { params: { pwd } }).then(resp => {
          if (resp.status) {
            this.adminPwd = ''
            this.getLoginInfo()
            this.adminLoginModalShow = false
          } else {
            this.showMsgModal('错误', resp['msg'])
          }
        })
      },
      adminLogout () {
        this.$ajax.get('/logout_admin').then(resp => {
          if (resp.status) {
            this.getLoginInfo()
          } else {
            this.showMsgModal('错误', resp.msg)
          }
        })
      },
      getLoginInfo () {
        this.$ajax.get('/get_login_info').then(resp => {
          if (resp.status) {
            this.isAdmin = resp['is_admin']
          } else {
            this.showMsgModal('错误', resp['msg'])
          }
        })
      },
      beginCrawl () {
        this.$ajax.get('/crawl_start').then(resp => {
          if (resp.status) {
            this.getCrawlStatus()
          } else {
            this.showMsgModal('错误', resp['msg'])
          }
        })
      },
      stopCrawl () {
        this.$ajax.get('/crawl_stop').then(resp => {
          if (resp.status) {
            this.getCrawlStatus()
          } else {
            this.showMsgModal('错误', resp['msg'])
          }
        })
      },
      getCrawlStatus () {
        this.$ajax.get('/crawl_status').then(resp => {
          if (resp.status) {
            this.crawlStatus = resp['crawl_status']
          } else {
            this.showMsgModal('错误', resp['msg'])
          }
        })
      },
      showMsgModal (title, content, okCallback = function () {
      }, cancelCallback = function () {
      }, onlyOk = true) {
        this.msgTitle = title
        this.msg = content
        this.msgOkCallback = okCallback
        this.msgCancelCallback = cancelCallback
        this.msgOkOnly = onlyOk
        this.msgVisible = true
      },
      addNotice () {
        let params = { notice: this.newNotice }
        this.$ajax.get('/add_notice', { params }).then(resp => {
          if (resp.status) {
            this.showMsgModal('提示', '操作成功！', () => {
              this.getRank()
            })
          } else {
            this.showMsgModal('错误', resp['msg'])
          }
        })
      }
    },
    computed: {
      crawlStatusClass () {
        return this.crawlStatus === 'stopped' ? 'text-primary' : 'text-danger'
      },
      formUserNameState () {
        return this.formUserName.length > 1 && this.formUserName.length <= 16
      },
      formAccountState () {
        return this.formAccount.length >= 1 && this.formAccount.length <= 64
      },
      formMottoState () {
        return this.formMotto.length <= 255
      },
      addUserModalOkDisabled () {
        return !(this.formUserNameState && this.formAccountState && this.formMottoState && this.formAccountAvailable)
      }
    },
    mounted () {
      this.getRank()
      this.getLoginInfo()
      this.getCrawlStatus()
    },
    beforeDestroy () {
      this.formMotto.destroy()
    }
  }
</script>
<style lang="scss">
  @import "./assets/css/style.scss";
  @import "./assets/css/editor.scss";
</style>
