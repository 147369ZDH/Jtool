import time
import sys, os
import platform
import subprocess
import csv

def resource_path(relative_path):
    """获取用户目录下的配置文件路径"""
    user_home = os.path.expanduser('~')
    config_dir = os.path.join(user_home, '.change_jdk')
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    return os.path.join(config_dir, relative_path)

jdk_path_file = resource_path("jdk_path.csv")

def initialize_csv():
    if not os.path.exists(jdk_path_file) or os.path.getsize(jdk_path_file) == 0:
        with open(jdk_path_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Version', 'Path'])

def jdk_list():
    """列出所有jdk版本"""
    initialize_csv()
    with open(jdk_path_file, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)  # 跳过表头
        print("\n当前配置的JDK列表：")
        print("-" * 50)
        print(f"{'版本'.ljust(15)}{'路径'}")
        print("-" * 50)
        for row in reader:
            print(f"{row[0].ljust(15)}{row[1]}")
        print()

def add_jdk_path(jdk_version: str, jdk_path: str):
    """添加jdk版本和路径"""
    initialize_csv()
    if not os.path.exists(os.path.join(jdk_path, "bin")):
        print("JDK 路径不存在`bin`目录,请检查路径是否正确!")
        return

    rows = []
    updated = False
    with open(jdk_path_file, 'r') as f:
        reader = csv.reader(f)
        rows.append(next(reader))  # 保存表头
        for row in reader:
            if row[0] == jdk_version:
                rows.append([jdk_version, jdk_path])
                updated = True
            else:
                rows.append(row)
    
    if not updated:
        rows.append([jdk_version, jdk_path])
        print(f"Added: {jdk_version} -> {jdk_path}")
    else:
        print(f"Updated: {jdk_version} -> {jdk_path}")

    with open(jdk_path_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def get_jdk_path(jdk_version: str):
    """根据jdk版本获取jdk路径"""
    initialize_csv()
    with open(jdk_path_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # 跳过表头
        for row in reader:
            if row[0] == jdk_version:
                return row[1]
    return None

def delete_jdk_path(jdk_version: str):
    initialize_csv()
    rows = []
    found = False
    with open(jdk_path_file, 'r') as f:
        reader = csv.reader(f)
        rows.append(next(reader))  # 保存表头
        for row in reader:
            if row[0] != jdk_version:
                rows.append(row)
            else:
                found = True

    if found:
        with open(jdk_path_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        print(f"删除: {jdk_version}")
    else:
        print(f"找不到`{jdk_version}`相关配置!")

def change_jdk(jdk_version):
    """
    修改JDK版本并设置系统环境变量
    
    Args:
        jdk_version (str): 要切换的JDK版本号
    """
    initialize_csv()
    jdk_path = get_jdk_path(jdk_version)
    
    if not jdk_path:
        print(f"找不到`{jdk_version}`相关的配置!")
        return
        
    system = platform.system()

    if system == 'Windows':
        _set_windows_env(jdk_path)
    elif system in ['Linux', 'Darwin']:
        _set_unix_env(jdk_path)
    else:
        print(f"不支持的操作系统: {system}")

def _set_windows_env(jdk_path):
    """设置Windows系统的环境变量"""
    try:
        # 设置 JAVA_HOME (使用 /M 参数设置系统环境变量)
        subprocess.run(['setx', '/M', 'JAVA_HOME', jdk_path], check=True)
        print(f"已将JAVA_HOME设置为: {jdk_path}")
        print("请重新打开命令行窗口使环境变量生效")
    except subprocess.CalledProcessError as e:
        print(f"设置环境变量失败: {e}")
        print("请尝试以管理员权限运行此命令")

def _set_unix_env(jdk_path):
    """设置Unix系统(Linux/MacOS)的环境变量"""
    home = os.path.expanduser("~")
    shell_rc = os.path.join(home, '.zshrc' if os.path.exists(os.path.join(home, '.zshrc')) else '.bashrc')

    # 读取现有配置文件
    lines = []
    if os.path.exists(shell_rc):
        with open(shell_rc, 'r') as f:
            lines = f.readlines()

    # 移除旧的JAVA_HOME配置
    lines = [line for line in lines if 'export JAVA_HOME=' not in line]

    # 添加新的JAVA_HOME配置
    lines.extend([
        f'\nexport JAVA_HOME={jdk_path}\n',
        'export PATH=$JAVA_HOME/bin:$PATH\n'
    ])

    # 写入配置文件
    with open(shell_rc, 'w') as f:
        f.writelines(lines)

    print(f"已将JAVA_HOME设置为: {jdk_path}")
    print(f"请运行 'source {shell_rc}' 或重新打开终端使环境变量生效")

def help_info():
    """显示命令行工具的使用帮助信息"""
    print("\n=== JDK 版本管理工具使用指南 ===\n")
    commands = [
        ("list", "查看已配置的JDK列表"),
        ("add <版本> <路径>", "添加或更新JDK配置\n  例如: add jdk8 C:\\Java\\jdk1.8.0"),
        ("use <版本>", "切换到指定的JDK版本\n  例如: use jdk8"),
        ("del <版本>", "删除指定的JDK配置\n  例如: del jdk8")
    ]
    
    for cmd, desc in commands:
        print(f"• {cmd.ljust(20)} {desc}")
    
    print("\n提示：所有命令中的<版本>参数可以自定义，建议使用数字标识，如：8、11、17等\n")


if __name__ == '__main__':
    print(f"参数列表:{sys.argv}")
    arg=sys.argv[1]
    match arg:
        case 'list':
            jdk_list()
        case 'add':
            jdk_version=sys.argv[2]
            jdk_path=sys.argv[3]
            add_jdk_path(jdk_version,jdk_path)
            jdk_list()
        case 'use':
            jdk_version=sys.argv[2]
            change_jdk(jdk_version)
        case 'del':
            jdk_version=sys.argv[2]
            delete_jdk_path(jdk_version)
        case 'help':
            help_info()
        case _:
            print("命令错误!")
            help_info()
            time.sleep(5)

