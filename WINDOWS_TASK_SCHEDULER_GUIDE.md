# Windows 任务计划程序配置指南

## 前提条件

1. **安装 Git for Windows**
   - 下载地址：https://git-scm.com/download/win
   - 安装时确保选择 "Add Git to PATH" 选项

2. **配置 Git SSH 密钥**（避免每次输入密码）
   ```bash
   # 在 Git Bash 中执行
   ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
   # 将 ~/.ssh/id_rsa.pub 内容添加到 GitHub
   ```

## 配置步骤

### 步骤 1：测试脚本

1. 双击运行 `daily-squash.bat`
2. 检查是否有错误提示
3. 查看日志文件 `daily-squash.log`

### 步骤 2：打开任务计划程序

1. 按下 Win + R，输入 `taskschd.msc`，回车
2. 或者在开始菜单搜索 "任务计划程序"

### 步骤 3：创建任务

1. 在右侧点击 **创建任务...**

#### 常规选项卡
- **名称**：每日 Git 提交合并
- **描述**：每天自动合并 Git 提交
- **安全选项**：勾选 "使用最高权限运行"

#### 触发器选项卡
1. 点击 **新建...**
2. **设置**：每天
3. **开始时间**：23:00:00
4. **重复任务间隔**：1 天
5. **持续时间**：无限期
6. 点击 **确定**

#### 操作选项卡
1. 点击 **新建...**
2. **操作**：启动程序
3. **程序或脚本**：浏览选择 `daily-squash.bat` 文件
4. **起始于**：输入脚本所在目录（如 `D:\Laboratory_of_Mad_Scientist`）
5. 点击 **确定**

#### 条件选项卡
- 根据需要调整电源选项（建议取消 "唤醒计算机运行此任务"）

#### 设置选项卡
- 勾选 "允许按需运行任务"
- 勾选 "错过计划的任务时立即运行"
- 其他选项保持默认

### 步骤 4：测试任务

1. 在任务列表中找到刚创建的任务
2. 右键点击，选择 **运行**
3. 等待执行完成
4. 检查日志文件和 Git 提交记录

## 手动运行

```cmd
# 方法1：双击 daily-squash.bat
# 方法2：在命令提示符中
cd D:\Laboratory_of_Mad_Scientist
daily-squash.bat
```

## 日志查看

日志文件位于：`D:\Laboratory_of_Mad_Scientist\daily-squash.log`

```cmd
# 查看日志
type daily-squash.log

# 实时查看日志
tail -f daily-squash.log  # 需要在 Git Bash 中运行
```

## 常见问题

### 问题1：Git Bash 路径不正确

**现象**：脚本提示 "Git Bash not found"

**解决方案**：
1. 查找 Git Bash 实际安装路径
2. 通常在 `C:\Program Files\Git\bin\bash.exe` 或 `C:\Program Files (x86)\Git\bin\bash.exe`
3. 修改 `daily-squash.bat` 中的 `GIT_BASH_PATH`

### 问题2：SSH 密钥未配置

**现象**：脚本运行时提示输入密码

**解决方案**：
1. 在 Git Bash 中生成 SSH 密钥
2. 将公钥添加到 GitHub
3. 测试 SSH 连接：`ssh -T git@github.com`

### 问题3：脚本执行失败

**现象**：日志中显示错误信息

**解决方案**：
1. 检查日志文件中的错误信息
2. 手动运行脚本查看详细错误
3. 确保仓库目录正确

## 脚本配置说明

`daily-squash.bat` 中的可配置参数：

```batch
set "REPO_DIR=%SCRIPT_DIR%"      # 仓库目录（默认脚本所在目录）
set "LOG_FILE=%SCRIPT_DIR%daily-squash.log"  # 日志文件路径
set "GIT_BASH_PATH=C:\Program Files\Git\bin\bash.exe"  # Git Bash 路径
```

## 任务计划程序高级配置

### 设置多个触发器

1. 打开任务属性
2. 切换到触发器选项卡
3. 点击 **新建...** 添加新的触发时间

### 设置任务执行时间限制

1. 打开任务属性
2. 切换到设置选项卡
3. 设置 "最长运行时间"

### 查看任务历史

1. 在任务计划程序中
2. 右键点击任务
3. 选择 **查看历史记录**

## 卸载任务

1. 打开任务计划程序
2. 在任务列表中找到任务
3. 右键点击，选择 **删除**