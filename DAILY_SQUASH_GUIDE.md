# 每日 Git 提交合并方案

## 核心目标

- 每天 23:00 自动运行
- 将当天所有提交压缩为一个，提交信息格式：`YYYY-MM-DD - 每日提交汇总`
- 安全推送至远程仓库，避免意外覆盖
- 保留手动操作能力，方便临时调整

## 方案：Bash 脚本 + Cron 定时任务

### 1. 脚本文件

已创建 `daily-squash.sh`，包含以下功能：

- ✅ 检查当前目录是否为 Git 仓库
- ✅ 获取当天日期范围（UTC 时间）
- ✅ 检查当天是否有提交需要合并
- ✅ 使用 rebase 压缩当天所有提交
- ✅ 自动生成统一的提交信息
- ✅ 安全推送（先拉取，再强制推送）

### 2. 配置步骤

#### 步骤 1：设置脚本执行权限

```bash
chmod +x daily-squash.sh
```

#### 步骤 2：测试脚本

```bash
# 测试运行（不会实际推送）
./daily-squash.sh

# 如果需要指定其他仓库目录
./daily-squash.sh /path/to/your/repo
```

#### 步骤 3：配置 Git 认证（避免每次输入密码）

**推荐方案：使用 SSH 密钥**

```bash
# 检查是否已有 SSH 密钥
ls ~/.ssh/id_rsa.pub

# 如果没有，生成新密钥
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# 将公钥添加到 GitHub
cat ~/.ssh/id_rsa.pub
```

**备选方案：使用 Git 凭据存储**

```bash
# 配置 Git 凭据缓存
git config --global credential.helper cache
git config --global credential.helper 'cache --timeout=86400'  # 缓存一天
```

#### 步骤 4：设置 Cron 定时任务

```bash
# 编辑 crontab
crontab -e

# 添加以下内容（每天 UTC 时间 23:00 执行，北京时间 07:00）
0 23 * * * /path/to/daily-squash.sh /path/to/your/repo >> /var/log/daily-squash.log 2>&1

# 或者北京时间 23:00（UTC 15:00）
0 15 * * * /path/to/daily-squash.sh /path/to/your/repo >> /var/log/daily-squash.log 2>&1
```

#### 步骤 5：验证 Cron 配置

```bash
# 查看当前 crontab
crontab -l

# 检查日志
tail -f /var/log/daily-squash.log
```

### 3. 手动运行命令

```bash
# 手动执行合并
./daily-squash.sh

# 指定仓库目录
./daily-squash.sh /path/to/your/repo

# 仅预览（不实际执行）
./daily-squash.sh --dry-run
```

### 4. 脚本配置参数

脚本开头可以修改以下参数：

```bash
REPO_DIR="."                              # 仓库目录
REMOTE_NAME="origin"                      # 远程仓库名称
BRANCH_NAME="master"                      # 分支名称
COMMIT_MESSAGE_PREFIX="每日提交汇总"       # 提交信息前缀
```

### 5. 安全注意事项

1. **备份重要数据**：脚本会重写 Git 历史，首次使用前建议备份
2. **强制推送警告**：使用 `--force-with-lease` 安全强制推送
3. **冲突处理**：如果 rebase 失败，脚本会自动中止并退出
4. **日志记录**：建议将输出重定向到日志文件

### 6. 测试确保功能正常

```bash
# 1. 创建测试提交
echo "test" > test.txt
git add test.txt
git commit -m "测试提交 1"

echo "test2" >> test.txt
git add test.txt
git commit -m "测试提交 2"

# 2. 运行脚本
./daily-squash.sh

# 3. 验证结果
git log --oneline -3
# 应该只看到一个提交：YYYY-MM-DD - 每日提交汇总
```

## 工作流程

```
┌─────────────────────────────────────────────────────────────┐
│                    每日提交合并流程                          │
├─────────────────────────────────────────────────────────────┤
│  1. 获取当天日期范围（UTC 00:00 至 24:00）                  │
│                         ↓                                   │
│  2. 检查当天是否有提交需要合并                               │
│                         ↓                                   │
│  3. 如果没有提交，直接退出                                   │
│                         ↓                                   │
│  4. 使用 rebase -i 压缩当天所有提交                          │
│                         ↓                                   │
│  5. 修改提交信息为：YYYY-MM-DD - 每日提交汇总                 │
│                         ↓                                   │
│  6. 安全推送至远程仓库（--force-with-lease）                 │
│                         ↓                                   │
│  7. 记录日志                                                │
└─────────────────────────────────────────────────────────────┘
```

## 注意事项

- **仅适用于个人项目**：强制推送会重写历史，不适合团队协作分支
- **时区设置**：Cron 使用系统时区，注意调整时间
- **日志监控**：建议定期检查日志确保脚本正常运行
- **手动干预**：如果脚本失败（如冲突），需要手动处理