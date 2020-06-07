<template>
  <div id="app">
    <!-- 导航栏  -->
    <b-navbar toggleable="lg" type="dark" variant="primary">
      <b-navbar-brand>HDU排行榜</b-navbar-brand>
      <b-navbar-brand>
        <small>
          <a href="https://github.com/736248591/hdu_rank" style="color: rgba(255,255,255,0.4)">GitHub地址</a>
        </small>
      </b-navbar-brand>
      <b-navbar-nav class="ml-auto">
        <b-nav-item-dropdown text="用户" right>
          <template v-if="!user&&!admin">
            <b-dropdown-item>登录</b-dropdown-item>
            <b-dropdown-item>注册</b-dropdown-item>
          </template>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-navbar>

    <!-- 公告 -->
    <div class="py-4">
      <b-container>
        <b-row>
          <vue-markdown :source="notice"></vue-markdown>
        </b-row>
      </b-container>
    </div>
    <!-- 排行榜 -->
    <div class="py-2">
      <b-container>
        <b-row>
          <b-table :items="users" :fields="user_fields">
            <template v-slot:cell(index)="data">
              {{data.index +1 }}
            </template>
          </b-table>
        </b-row>
      </b-container>
    </div>

    <div class="py-3">
      <div class="container">
        <div class="row">
          <div class="col-md-12 text-center">
            <p class="mb-0">Writed By 雪靡. All rights reserved | Open Source on <a
              href="https://github.com/736248591/hdu_rank" target="_blank">GitHub</a>
            </p>
          </div>
        </div>
      </div>
    </div>
    <b-modal v-model="loginModalShow" title="登录" ok-title="确认" cancel-title="取消" @ok

    <!-- 注册 -->
    <b-modal id="addUserModal" title="注册" ok-title="确认" cancel-title="取消" @ok="addUser"
             :ok-disabled="addUserModalOkDisabled" v-model="addUserModalShow">
      <b-form @submit="addUser">
        <b-form-group
          label="登录账号">
          <b-form-input
            :state="formUidState"
            required
            trim
            type="text"
            v-model="formUid">
          </b-form-input>
          <b-form-invalid-feedback id="formUidFeedback">
            {{formUidServerFeedbackString}}
          </b-form-invalid-feedback>
        </b-form-group>
        <b-form-group
          label="密码">
          <b-form-input
            :state="formPwdState"
            aria-describedby="formPwdFeedback"
            placeholder="请在这里输入密码！"
            required
            trim
            type="password"
            v-model="formPwd"></b-form-input>
        </b-form-group>
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
        user_fields: [
          {
            key: 'index',
            label: ' '
          },
          {
            key: 'class_name',
            label: '班级',
            sortable: true
          },
          {
            key: 'name',
            label: '姓名',
            sortable: true
          },
          {
            key: 'motto',
            label: '格言'
          },
          {
            key: 'solved_num',
            label: '题数'
          }
        ],
        users: [],
        user: null,
        admin: null,
        formUid: '',
        formUidAvailable: false,
        formUidServerFeedbackString: '当失去焦点时将验证账号',
        formPwd: '',
        formConfirmPwd: '',
        formClassName: '',
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
        loginModalShow: false,
        addUserModalShow: false,
        notice: '',
        newNotice: '',
        addNoticeModalShow: false
      }
    },
    methods: {
      getRank () {
        this.$ajax.get('/get_rank').then((resp) => {
          this.users = resp['users']
          this.newNotice = this.notice = resp['notice']
          this.user = resp['user']
          this.admin = resp['admin']
        })
      },
      validateFormUid () {
        this.formUidServerFeedbackString = '检测中……'
        let params = {
          field: 'uid',
          value: this.formUid
        }
        this.$ajax.get('/validate_user', { params }).then(resp => {
          this.formAccountAvailable = resp.status
          if (!resp.status) {
            this.formUidServerFeedbackString = resp.msg
          }
        })
      },
      validateFormAccount () {
        this.formAccountServerFeedbackString = '检测中……'
        let params = {
          account: this.formAccount
        }
        this.$ajax.get('/validate_user', { params }).then(resp => {
          this.formAccountAvailable = resp.status
          if (!resp.status) {
            this.formAccountServerFeedbackString = resp.msg
          }
        })
      },
      formReset () {
        this.formUid = ''
        this.formUidAvailable = false
        this.formUidServerFeedbackString = '当失去焦点时将验证账号'
        this.formPwd = ''
        this.formConfirmPwd = ''
        this.formClassName = ''
        this.formUserName = ''
        this.formAccount = ''
        this.formAccountAvailable = false
        this.formAccountServerFeedbackString = '当失去焦点时将验证账号'
        this.formMotto = ''
      },
      addUser () {
        let sha = new SHA('SHA3-512', 'TEXT', { encoding: 'UTF8', numRounds: 6 })
        let pwd = this.formPwd
        sha.update(this.formPwd)
        pwd = sha.getHash('HEX')
        let params = {
          uid: this.formUid,
          pwd: pwd,
          class_name: this.formClassName,
          name: this.formUserName,
          account: this.formAccount,
          motto: this.formMotto
        }
        this.$ajax.post('/put_user', { params }).then(resp => {
          if (resp.status) {
            this.showMsgModal('提示', '操作成功！', () => {
              this.formReset()
              this.getRank()
            })
          } else {
            this.showMsgModal('错误', resp.msg)
          }
        })
      },
      login () {
        let sha = new SHA('SHA3-512', 'TEXT', { encoding: 'UTF8', numRounds: 6 })
        let pwd = this.formPwd
        sha.update(this.formPwd)
        pwd = sha.getHash('HEX')
        let params = {
          uid: this.formUid,
          pwd: pwd
        }
        this.$ajax.post('/login', { params }).then(resp => {
          if (resp.status) {
            this.formReset()
            this.getRank()
          } else {
            this.showMsgModal('错误', resp.msg)
          }
        })
      },
      logout () {
        this.$ajax.get('/logout').then(resp => {
          this.getRank()
        })
      },
      removeUser (id) {
        this.showMsgModal('提示', '是否确认删除？', () => {
          this.$ajax.get('/remove_user', { params: { id } }).then(resp => {
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
        this.$ajax.get('/login').then(resp => {
          if (resp.status) {
            this.isAdmin = resp['is_admin']
          } else {
            // this.showMsgModal('错误', resp['msg'])
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
      formUidState () {
        return this.formUid.length > 1 && this.formUid.length <= 16
      },
      formPwdState () {
        let regNumber = /\d+/
        let regAlpha = /[a-zA-Z]+/
        return this.formPwd.length > 3 && regNumber.test(this.formPwd) && regAlpha.test(this.formPwd)
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
    created () {
      // 添加响应拦截器
      this.$ajax.interceptors.response.use(resp => resp.data, error => {
        console.error(error)
        this.showMsgModal('服务器错误', error)
        return Promise.reject(error)
      })
    },
    mounted () {
      this.getRank()
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

  // 表单的可换行的文字
  .table-text-wrap {
    word-wrap: break-word;
    word-break: break-all;
  }
</style>
