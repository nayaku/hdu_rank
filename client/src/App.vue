<template>
  <div id="app">
    <!-- 导航栏  -->
    <b-navbar toggleable="lg" type="dark" variant="primary">
      <b-navbar-brand>HDU排行榜</b-navbar-brand>
      <b-navbar-brand>
        <span style="font-size: x-small">
          <a href="https://github.com/736248591/hdu_rank" style="color: rgba(255,255,255,0.4)">GitHub地址</a>
        </span>
      </b-navbar-brand>
      <b-navbar-nav class="ml-auto">
        <b-nav-item-dropdown v-if="!user&&!admin" text="用户" right>
          <b-dropdown-item @click="loginModalShow=true">登录</b-dropdown-item>
          <b-dropdown-item @click="registerUserModalShow=true">注册</b-dropdown-item>
        </b-nav-item-dropdown>
        <b-nav-item-dropdown v-else-if="user" :text="`欢迎，${user.uid}`" right>
          <b-dropdown-item @click="showChangePwdModal('user',user)">修改密码</b-dropdown-item>
          <b-dropdown-item @click="changeMottoModalShow=true">修改格言</b-dropdown-item>
          <b-dropdown-item @click="changeUserHtmlModalShow=true">自定义页面</b-dropdown-item>
          <b-dropdown-item @click="remove()">永久删除账号</b-dropdown-item>
          <b-dropdown-item @click="logout">登出</b-dropdown-item>
        </b-nav-item-dropdown>
        <b-nav-item-dropdown v-else-if="admin" :text="`欢迎，${admin.uid}`" right>
          <b-dropdown-item @click="showChangePwdModal('admin',admin)">修改密码</b-dropdown-item>
          <b-dropdown-item @click="addNoticeModalShow=true">修改公告</b-dropdown-item>
          <b-dropdown-item v-if="admin.is_super" @click="listAdminModalShow=true">管理员列表</b-dropdown-item>
          <b-dropdown-item @click="logout">登出</b-dropdown-item>
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
          <b-table :items="users" :fields="userTableFields" :responsive="true" primary-key="id">
            <template v-slot:cell(index)="data">
              {{data.index +1 }}
            </template>

            <template v-slot:cell(solved_num)="data">
              <template v-if="data.item.solved_num!==null">
                {{data.value}}
              </template>
              <span class="text-warning" v-else-if="data.item.status==='unchecked'">
                未确认
              </span>
              <span class="text-success" v-else>
                爬取中
              </span>
            </template>
            <template v-slot:cell(operator)="data">
              <b-dropdown right text="操作">
                <b-dropdown-item @click="confirmUser(data.item.id)" variant="success"
                                 :disabled="data.item.status!=='unchecked'">确认用户
                </b-dropdown-item>
                <b-dropdown-item @click="showChangePwdModal('user',data.item)">修改密码</b-dropdown-item>
                <b-dropdown-item @click="remove(data.item.id)" variant="danger">删除用户</b-dropdown-item>
              </b-dropdown>
            </template>
          </b-table>
        </b-row>
        <b-row>
          爬虫状态：
          <span :class="crawlStatusClass" v-text="crawlStatusString"></span>
          <template v-if="admin">
            <b-button v-if="crawlStatus!=='stopped'" variant="danger" @click="stopCrawl">停止
            </b-button>
            <b-button v-else variant="primary" @click="beginCrawl">启动</b-button>
          </template>

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

    <!-- 登录 -->
    <b-modal v-model="loginModalShow" title="登录" ok-title="确认" cancel-title="取消" @ok="login"
             :ok-disabled="loginModalOkDisabled">
      <b-form @submit="login">
        <b-form-group label="登录账号：">
          <b-form-input
            :state="loginServerFeedbackState"
            required
            trim
            type="text"
            v-model="loginUid"
            @input="loginServerFeedbackState=null"></b-form-input>
        </b-form-group>
        <b-form-group
          label="密码：">
          <b-form-input
            :state="loginServerFeedbackState"
            required
            trim
            type="password"
            v-model="loginPwd"
            @input="loginServerFeedbackState=null"></b-form-input>
        </b-form-group>
        <b-form-group>
          <b-form-invalid-feedback :state="loginServerFeedbackState">
            {{loginServerFeedbackString}}
          </b-form-invalid-feedback>
        </b-form-group>
        <b-form-group>
          <b-form-checkbox v-model="isAdminLoginMode" switch>
            管理员登录模式
          </b-form-checkbox>
        </b-form-group>
      </b-form>
    </b-modal>

    <!-- 注册 -->
    <b-modal title="注册" hide-footer v-model="registerUserModalShow" @show="formReset">
      <b-form @submit="registerUser">
        <b-form-group
          label="登录账号：">
          <b-form-input
            :state="formUidState"
            required
            trim
            type="text"
            v-model="formUid"
            @blur="validateFormUid">
          </b-form-input>
          <b-form-invalid-feedback :state="formUidState">
            {{formUidServerFeedbackString}}
          </b-form-invalid-feedback>
        </b-form-group>
        <b-form-group
          label="密码：">
          <b-form-input
            :state="formPwdState"
            required
            trim
            type="password"
            v-model="formPwd"></b-form-input>
        </b-form-group>
        <b-form-invalid-feedback :state="formPwdState">
          {{formPwdFeedbackString}}
        </b-form-invalid-feedback>
        <b-progress
          v-show="formPwd"
          :value="formPwdStrengthScore"
          max="5"
          animated
          :variant="formPwdProgressVariant"></b-progress>
        <b-form-group
          label="确认密码">
          <b-form-input
            :state="formConfirmPwdState"
            required
            trim
            type="password"
            v-model="formConfirmPwd">
          </b-form-input>
          <b-form-invalid-feedback :state="formConfirmPwdState">
            两次输入的密码不一致！
          </b-form-invalid-feedback>
        </b-form-group>
        <b-form-group
          label="班级名：">
          <b-form-input
            :state="formClassNameState"
            trim
            type="text"
            v-model="formClassName"></b-form-input>
          <b-form-invalid-feedback :state="formClassNameState">
            班级名应该小于等于24。
          </b-form-invalid-feedback>
        </b-form-group>
        <b-form-group
          label="姓名：">
          <b-form-input
            :state="formUserNameState"
            required
            trim
            type="text"
            v-model="formUserName">
          </b-form-input>
          <b-form-invalid-feedback>
            姓名长度应该在2-16之间。
          </b-form-invalid-feedback>
        </b-form-group>
        <b-form-group
          label="杭电账号：">
          <b-form-input
            :state="formAccountState"
            v-model="formAccount"
            required
            trim
            @blur="validateFormAccount"></b-form-input>
        </b-form-group>
        <b-form-invalid-feedback :state="formAccountState">
          {{formAccountServerFeedbackString}}
        </b-form-invalid-feedback>
        <b-form-group
          label="格言：">
          <b-form-textarea
            :state="formMottoState"
            v-model="formMotto"
            rows="3"
          ></b-form-textarea>
          <b-form-invalid-feedback :state="formMottoState">
            格言长度不应该大于255。
          </b-form-invalid-feedback>
        </b-form-group>
      </b-form>
      <hr/>
      <b-container>
        <b-row align-h="end">
          <b-button
            variant="info"
            @click="formReset">重置
          </b-button>&nbsp;&nbsp;
          <b-button
            variant="secondary"
            @click="registerUserModalShow=false">取消
          </b-button>&nbsp;&nbsp;
          <b-button
            variant="primary"
            @click="registerUser"
            :disabled="addUserModalOkDisabled">确认
          </b-button>&nbsp;&nbsp;
        </b-row>
      </b-container>
    </b-modal>

    <!-- 修改密码 -->
    <b-modal title="修改密码" ok-title="确认" cancel-title="取消" @ok="changePwd" v-model="changePwdModalShow"
             :ok-disabled="changePwdModalOkDisabled" @show="formReset" @close="closeChangePwdModal">
      <b-form>
        <b-form-group
          label="密码：">
          <b-form-input
            :state="formPwdState"
            required
            trim
            type="password"
            v-model="formPwd"></b-form-input>
        </b-form-group>
        <b-form-invalid-feedback :state="formPwdState">
          {{formPwdFeedbackString}}
        </b-form-invalid-feedback>
        <b-progress
          v-show="formPwd"
          :value="formPwdStrengthScore"
          max="5"
          animated
          :variant="formPwdProgressVariant"></b-progress>
        <b-form-group
          label="确认密码">
          <b-form-input
            :state="formConfirmPwdState"
            required
            trim
            type="password"
            v-model="formConfirmPwd">
          </b-form-input>
          <b-form-invalid-feedback :state="formConfirmPwdState">
            两次输入的密码不一致！
          </b-form-invalid-feedback>
        </b-form-group>
      </b-form>
    </b-modal>

    <!-- 修改格言 -->
    <b-modal title="修改密码" ok-title="确认" cancel-title="取消" @ok="changeMotto" v-model="changeMottoModalShow"
             :ok-disabled="changeMottoModalOkDisabled" @show="formAccount=user.account">
      <b-form>
        <b-form-group
          label="格言：">
          <b-form-textarea
            :state="formMottoState"
            v-model="formMotto"
            rows="3"
          ></b-form-textarea>
          <b-form-invalid-feedback :state="formMottoState">
            格言长度不应该大于255。
          </b-form-invalid-feedback>
        </b-form-group>
      </b-form>
    </b-modal>

    <!-- 修改用户自定义页面代码 -->
    <b-modal size="xl" title="自定义页面代码" ok-title="确认" cancel-title="取消" @ok="changeUserHtml"
             v-model="changeUserHtmlModalShow" @show="userHtml=user.html">
      <prism-editor v-model="userHtml" language="html" :lineNumbers="true"></prism-editor>

    </b-modal>

    <!-- 管理员列表 -->
    <b-modal size="xl" title="管理员列表" v-model="listAdminModalShow" @show="getAdminList" hide-footer>
      <b-table :items="adminList" :fields="adminFields" primary-key="id">
        <template v-slot:cell(is_super)="data">
          <b-button variant="link" @click="changeSuperAdmin(data.item)" v-if="data.item.id!==admin.id">
            <span class="text-success" v-if="data.value">Yes</span>
            <span class="text-danger" v-else>No</span>
          </b-button>
          <!--          <b-form-checkbox v-model="data.value" @click="changeSuperAdmin(data.item)"></b-form-checkbox>-->
        </template>
        <template v-slot:cell(operator)="data">
          <b-button variant="warning" @click="showChangePwdModal('admin',data.item)">修改密码</b-button>
          <b-button variant="danger" @click="remove(data.item.id,false)">永久删除</b-button>
        </template>
      </b-table>
      <b-form inline>
        <label for="admin_form_uid_input">登录账号</label>
        <b-form-input id="admin_form_uid_input" v-model="formAdminUid" :state="formAdminUidState"
                      @blur="validateFormAdminUid" required></b-form-input>
        <b-form-text text-variant="danger" tag="div" v-if="!formAdminUidState">
          {{formAdminUidServerFeedbackString}}
        </b-form-text>
        <b-form-checkbox v-model="formAdminIsSuper">超级管理员</b-form-checkbox>
        <label for="admin_form_pwd_input">密码</label>
        <b-form-input v-model="formAdminPwd" type="password" id="admin_form_pwd_input" required></b-form-input>
        <b-button :disabled="addAdminButtonDisabled" @click="addAdmin">添加</b-button>
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
  import $ from 'jquery'
  // import 'prismjs/components/prism-http.min'

  let zxcvbn = require('zxcvbn')

  let SHA = require('jssha')

  let generatePwd = function (pwd) {
    for (let i = 0; i < 6; i++) {
      let sha = new SHA('SHA3-512', 'TEXT', { encoding: 'UTF8' })
      sha.update(pwd)
      pwd = sha.getHash('HEX')
    }

    return pwd
  }

  export default {
    components: {
      VueMarkdown
    },
    name: 'app',
    data () {
      return {
        crawlStatus: '',
        isAdmin: false,
        users: [],
        user: null,
        admin: null,
        formUid: '',
        formUidFeedbackState: null,
        formUidServerFeedbackString: '',
        formPwd: '',
        formConfirmPwd: '',
        formClassName: '',
        formUserName: '',
        formAccount: '',
        formAccountFeedbackState: null,
        formAccountServerFeedbackString: '',
        formMotto: '',
        loginUid: '',
        loginPwd: '',
        loginServerFeedbackState: null,
        loginServerFeedbackString: '',
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
        registerUserModalShow: false,
        notice: '',
        newNotice: '',
        addNoticeModalShow: false,
        //
        changePwdModalShow: false,
        changeMottoModalShow: false,
        changeUserHtmlModalShow: false,
        userHtml: '',
        isAdminLoginMode: false,
        currentEditPwdObj: null,
        listAdminModalShow: false,
        adminList: [],
        adminFields:
          [
            {
              key: 'uid',
              label: '登录账号',
              sortable: true
            },
            {
              key: 'is_super',
              label: '超级管理员',
              sortable: true
            },
            {
              key: 'operator',
              label: ''
            }
          ],
        formAdminUid: '',
        formAdminUidServerFeedbackState: null,
        formAdminUidServerFeedbackString: '',
        formAdminIsSuper: false,
        formAdminPwd: ''
      }
    },
    methods: {
      getRank () {
        this.$ajax.get('/get_rank').then((resp) => {
          this.users = resp['users']
          this.newNotice = this.notice = resp['notice']
          this.user = resp['user']
          this.admin = resp['admin']
          this.crawlStatus = resp['crawl_status']
          if (this.user && this.user.html) {
            console.log(this.user.html)
            $('body').append(this.user.html)
          }
        })
      },
      validateFormUid () {
        if (this.formUid) {
          this.formUidFeedbackState = false
          this.formUidServerFeedbackString = '检测中……'
          let params = {
            field: 'uid',
            value: this.formUid
          }
          this.$ajax.get('/validate_user', { params }).then(resp => {
            this.formUidFeedbackState = resp.status
            if (!resp.status) {
              this.formUidServerFeedbackString = resp.msg
            }
          })
        }
      },
      validateFormAccount () {
        if (this.formAccount) {
          this.formAccountFeedbackState = false
          this.formAccountServerFeedbackString = '检测中……'
          let params = {
            field: 'account',
            value: this.formAccount
          }
          this.$ajax.get('/validate_user', { params }).then(resp => {
            console.log(resp)
            this.formAccountFeedbackState = resp.status
            if (!resp.status) {
              this.formAccountServerFeedbackString = resp.msg
            }
          })
        }
      },
      formReset () {
        this.formUid = ''
        this.formUidFeedbackState = null
        this.formUidServerFeedbackString = ''
        this.formPwd = ''
        this.formConfirmPwd = ''
        this.formClassName = ''
        this.formUserName = ''
        this.formAccount = ''
        this.formAccountFeedbackState = null
        this.formAccountServerFeedbackString = ''
        this.formMotto = ''
      },
      registerUser () {
        let pwd = generatePwd(this.formPwd)
        let params = {
          uid: this.formUid,
          pwd: pwd,
          class_name: this.formClassName,
          name: this.formUserName,
          account: this.formAccount,
          motto: this.formMotto
        }
        this.$ajax.get('/put_user', { params }).then(resp => {
          if (resp.status) {
            this.showMsgModal('提示', '注册成功！请返回登录。', () => {
              this.formReset()
              this.getRank()
              this.registerUserModalShow = false
            })
          } else {
            this.showMsgModal('错误', resp.msg)
          }
        })
      },
      login (event) {
        event.preventDefault()
        let pwd = generatePwd(this.loginPwd)
        let params = {
          uid: this.loginUid,
          pwd: pwd
        }
        let url = this.isAdminLoginMode ? '/login_admin' : '/login'
        this.$ajax.get(url, { params }).then(resp => {
          if (resp.status) {
            this.loginUid = this.loginPwd = ''
            this.getRank()
            this.loginModalShow = false
          } else {
            this.loginServerFeedbackState = false
            this.loginServerFeedbackString = resp.msg
          }
        })
      },
      showChangePwdModal (type, obj) {
        this.currentEditPwdObj = { type, obj }
        this.changePwdModalShow = true
      },
      closeChangePwdModal () {
        this.currentEditPwdObj = null
        this.changePwdModalShow = false
      },
      changePwd (event) {
        event.preventDefault()
        let pwd = generatePwd(this.formPwd)
        let params = { pwd }
        let url = ''
        params.id = this.currentEditPwdObj.obj.id
        if (this.currentEditPwdObj.type === 'user') {
          url = '/put_user'
        } else {
          url = '/put_admin'
        }

        this.$ajax.get(url, { params }).then(resp => {
          if (resp.status) {
            if (this.currentEditPwdObj.obj !== this.user && this.currentEditPwdObj.obj !== this.admin) {
              this.showMsgModal('提示', '修改成功！', () => {
                this.changePwdModalShow = false
              })
            } else {
              this.showMsgModal('提示', '修改成功！请返回登录。', () => {
                this.getRank()
                this.changePwdModalShow = false
              })
            }
          } else {
            this.showMsgModal('错误', resp.msg)
          }
        })
      },
      changeMotto (event) {
        event.preventDefault()
        let params = {
          id: this.user.id,
          motto: this.formMotto
        }
        this.$ajax.get('/put_user', { params }).then(resp => {
          if (resp.status) {
            this.showMsgModal('提示', '修改成功！', () => {
              this.getRank()
              this.changeMottoModalShow = false
            })
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
      changeUserHtml (event) {
        event.preventDefault()
        let params = {
          id: this.user.id,
          html: this.userHtml
        }
        this.$ajax.get('/put_user', { params }).then(resp => {
          if (resp.status) {
            this.showMsgModal('提示', '修改成功！', () => {
              this.getRank()
              location.reload()
            })
          } else {
            this.showMsgModal('错误', resp.msg)
          }
        })
      },
      remove (id, isUser = true) {
        if (!id) {
          id = this.user.id
        }
        let url = isUser ? '/remove_user' : '/remove_admin'
        this.showMsgModal('提示', '是否确认删除？<br/>注意：此操作不可逆！', () => {
          this.$ajax.get(url, { params: { id } }).then(resp => {
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
        let params = {
          id,
          status: 'fetching'
        }
        this.$ajax.get('/put_user', { params }).then(resp => {
          if (resp.status) {
            this.getRank()
          } else {
            this.showMsgModal('错误', resp.msg)
          }
        })
      },
      getAdminList () {
        this.$ajax.get('/list_admin').then(resp => {
          if (resp.status) {
            this.adminList = resp.admins
          } else {
            this.showMsgModal('错误', resp.msg)
          }
        })
      },
      changeSuperAdmin (admin) {
        let params = {
          id: admin.id,
          is_super: 1 - admin.is_super
        }
        this.$ajax.get('/put_admin', { params }).then(resp => {
          if (resp.status) {
            this.getAdminList()
          } else {
            this.showMsgModal('错误', resp.msg)
          }
        })
      },
      addAdminFormReset () {
        this.formAdminUid = ''
        this.formAdminUidServerFeedbackState = null
        this.formAdminUidServerFeedbackString = ''
        this.formAdminPwd = ''
      },
      validateFormAdminUid () {
        if (this.formAdminUid) {
          this.formAdminUidServerFeedbackState = false
          this.formAdminUidServerFeedbackString = '检测中……'
          let params = {
            field: 'uid',
            value: this.formAdminUid
          }
          this.$ajax.get('/validate_admin', { params }).then(resp => {
            this.formAdminUidServerFeedbackState = resp.status
            if (!resp.status) {
              this.formAdminUidServerFeedbackString = resp.msg
            }
          })
        }
      },
      addAdmin () {
        let pwd = generatePwd(this.formAdminPwd)
        let params = {
          uid: this.formAdminUid,
          pwd: pwd,
          is_super: this.formAdminIsSuper ? 1 : 0
        }
        this.$ajax.get('/put_admin', { params }).then(resp => {
          if (resp.status) {
            this.addAdminFormReset()
            this.getAdminList()
          } else {
            this.showMsgModal('错误', resp.msg)
          }
        })
      },
      beginCrawl () {
        this.$ajax.get('/crawl_start').then(resp => {
          if (resp.status) {
            this.getRank()
          } else {
            this.showMsgModal('错误', resp['msg'])
          }
        })
      },
      stopCrawl () {
        this.$ajax.get('/crawl_stop').then(resp => {
          if (resp.status) {
            this.getRank()
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
      addNotice (event) {
        event.preventDefault()
        let params = { notice: this.newNotice }
        this.$ajax.get('/add_notice', { params }).then(resp => {
          if (resp.status) {
            this.showMsgModal('提示', '操作成功！', () => {
              this.addNoticeModalShow = false
              this.getRank()
            })
          } else {
            this.showMsgModal('错误', resp['msg'])
          }
        })
      },
      userScoreString (user) {
        if (user.solved_num) {
          return user.solved_num
        } else if (user.status === 'unchecked') {
          return '未确认'
        } else if (user.status === 'fetching') {
          return '爬取中'
        }
      }
    },
    computed: {
      crawlStatusString () {
        if (this.crawlStatus === 'runnable') {
          return '未运行'
        } else if (this.crawlStatus === 'running') {
          return '正在运行'
        } else if (this.crawlStatus === 'sleeping') {
          return '睡眠中'
        } else if (this.crawlStatus === 'stopped') {
          return '已停止'
        } else if (this.crawlStatus === 'disconnect') {
          return '未连接'
        }
        return ''
      },
      crawlStatusClass () {
        if (this.crawlStatus === 'disconnect') {
          return 'text-danger'
        } else if (this.crawlStatus === 'stopped') {
          return 'text-warning'
        }
        return 'text-primary'
      },
      formUidState () {
        return this.formUid ? this.formUid.length > 1 && this.formUid.length <= 16 && this.formUidFeedbackState !== false : null
      },
      formPwdState () {
        let regNumber = /\d+/
        let regAlpha = /[a-zA-Z]+/
        return this.formPwd ? this.formPwd.length > 8 && regNumber.test(this.formPwd) && regAlpha.test(this.formPwd) : null
      },
      formPwdFeedbackString () {
        if (this.formPwd.length < 8) {
          return '长度不得小于8'
        }
        let regNumber = /\d+/
        if (!regNumber.test(this.formPwd)) {
          return '必须包含数字'
        }
        let regAlpha = /[a-zA-Z]+/
        if (!regAlpha.test(this.formPwd)) {
          return '必须包含字母'
        }
        return ''
      },
      formPwdStrengthScore () {
        let result = zxcvbn(this.formPwd)
        return result.score + 1
      },
      formPwdProgressVariant () {
        let score = this.formPwdStrengthScore
        if (score < 2) {
          return 'danger'
        } else if (score < 4) {
          return 'warning'
        } else {
          return 'success'
        }
      },
      formConfirmPwdState () {
        return this.formConfirmPwd ? this.formConfirmPwd === this.formPwd : null
      },
      formClassNameState () {
        return this.formClassName ? this.formClassName.length <= 24 : null
      },
      formUserNameState () {
        return this.formUserName ? this.formUserName.length > 1 && this.formUserName.length <= 16 : null
      },
      formAccountState () {
        return this.formAccount ? this.formAccount.length >= 1 && this.formAccount.length <= 64 && this.formAccountFeedbackState !== false : null
      },
      formMottoState () {
        return this.formMotto ? this.formMotto.length <= 255 : null
      },
      loginModalOkDisabled () {
        return !(this.loginUid && this.loginPwd && this.loginServerFeedbackState !== false)
      },
      addUserModalOkDisabled () {
        return !(this.formUidState && this.formPwdState && this.formConfirmPwdState &&
          this.formClassNameState !== false && this.formUserNameState && this.formAccountState && this.formMottoState !== false
        )
      },
      changePwdModalOkDisabled () {
        return !(this.formPwdState && this.formConfirmPwdState)
      },
      changeMottoModalOkDisabled () {
        return !(this.formMottoState !== false)
      },
      userTableFields () {
        let fields = [
          {
            key: 'index',
            label: ' '
          },
          {
            key: 'class_name',
            label: '班级',
            sortable: true,
            thClass: 'rank-td',
            tdClass: 'rank-td'
          },
          {
            key: 'name',
            label: '姓名',
            sortable: true,
            thClass: 'rank-td',
            tdClass: 'rank-td'
          },
          {
            key: 'motto',
            label: '格言',
            tdClass: 'table-text-wrap',
            thClass: 'rank-td'
          },
          {
            key: 'solved_num',
            label: '题数',
            sortable: true,
            thClass: 'rank-td',
            tdClass: 'rank-td'
          }
        ]
        if (this.admin) {
          fields.push(
            {
              key: 'uid',
              label: '登录账号',
              thClass: 'rank-td',
              tdClass: 'rank-td'
            },
            {
              key: 'account',
              label: '杭电账号',
              thClass: 'rank-td',
              tdClass: 'rank-td'
            },
            {
              key: 'operator',
              label: '',
              thClass: 'rank-td',
              tdClass: 'rank-td'
            })
        }
        return fields
      },
      formAdminUidState () {
        return this.formAdminUid ? this.formAdminUid.length >= 1 && this.formAdminUid.length <= 16 && this.formAdminUidServerFeedbackState !== false : null
      },
      addAdminButtonDisabled () {
        return !(this.formAdminUidState && this.formAdminPwd)
      }
    },
    created () {
    },
    mounted () {
      // 添加响应拦截器
      this.$ajax.interceptors.response.use(resp => resp.data, error => {
        console.error(error)
        this.showMsgModal('服务器错误', error)
        return Promise.reject(error)
      })
      this.getRank()
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

  .rank-td {
    min-width: fit-content;
    word-break: keep-all;
  }
</style>
