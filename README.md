## Jtool
### 针对Windows系统的JDK版本切换工具

## 基本使用
### 下载好`jtool.exe`程序之后，将其所在目录添加到系统环境变量Path中,使用管理员权限打开CMD命令行</br>

### 基本命令：</br>
### jtool list, 查看已配置的JDK列表</br>
### jtool add <版本> <路径>, 添加或更新JDK配置  例如: jtool add jdk8 C:\\Java\\jdk1.8.0</br>
### jtool use <版本>, 切换到指定的JDK版本  例如: jtool use jdk8</br>
### jtool del <版本>, 删除指定的JDK配置  例如: jtool del jdk8</br>
### jtool help, 查看命令帮助
### 切换成功后需要关闭当前命令行重新打开输入：java -version检查版本是否已经更改完成</br>


