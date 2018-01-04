# Temproom -SE project
#### 使用方法：下载所有文件到同一个文件夹中，运行w1.py即可。程序需要pyqt5,pyaudio,pymysql,qdarkstyle,pyqtgraph,matplotlib，scipy数个模块的支持，与数据库相关的函数都可以使用

### 更新日志
##### 17.12.08更新  V0.0.1
数据库与界面整合完成，等待二次测试，网络部分优化中
 
 
##### 17.12.17更新  V0.0.2
1.上传了mysignal.py与changevoice.py两个文件，删除了ip.py文件

2.现在点击上方退出程序按钮有提示啦！并且退出后数据库也会反应~


##### 17.12.18更新 V0.0.3
1.修复了（用户名/密码/房间号/密钥）可以为空的bug,现在注册时长度须大于四位

2.完善下线按钮功能，现在下线按钮等同于上方退出按钮


##### 17.12.18第二次更新 V0.0.4
修复了多个客户端可以登录同一个用户的bug~


##### 17.12.18第三次更新 V0.0.5
找到了个很酷的主题装上去了~并且改动了一些细微的地方
[主题地址](https://github.com/ColinDuquesnoy/QDarkStyleSheet)
 
 
##### 17.12.19更新 V0.0.6
1.修改了大量交互细节~

2.修复了进入房间时输入不正确导致的程序崩溃问题

3.添加了程序图标


##### 17.12.19第二次更新 V0.0.7
1.修改了字体和细微布局

2.密码输入框内容隐藏


##### 17.12.20更新 V0.0.8
在线用户同步啦！虽然用的方法很蠢，试过了各种方式，QT还是复杂


##### 17.12.20第二次更新 V0.0.9
双向网络测试通过


##### 17.12.22更新 V0.1
1.通话功能上线，待调试

2.加入了音频处理接口

3.修复了用户登录中文字符导致的bug

##### 18.1.1更新 V0.2
改进了交互逻辑
1.自动分配房间号码，设置4位数口令
2.增加了独立的注册界面