# GitBlog - 基于GitHub Issues的博客系统

## 项目介绍

GitBlog是一个基于GitHub Issues和GitHub Actions的个人博客系统，灵感来源于[yihong0618/2025](https://github.com/yihong0618/2025)。它允许你利用GitHub的现有功能，轻松搭建属于自己的博客平台，无需额外的服务器和数据库。

## 核心功能

- 📝 **通过GitHub Issues编写博客** - 简单方便，无需学习复杂的博客系统
- 🤖 **自动生成README.md** - 包含博客目录、分类和最近更新
- 📋 **自动备份Issues内容** - 所有Issues内容会自动备份到本地
- 📡 **生成RSS Feed** - 方便订阅和获取最新内容
- ⚡ **自动化部署** - 使用GitHub Actions自动更新博客内容

## 快速开始

### 1. 准备工作

- 注册GitHub账号
- 创建一个新的GitHub仓库
- 生成GitHub Personal Access Token（需要有repo权限）
- 安装Python 3.7+和Git

### 2. 克隆项目

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置GitHub Actions

将以下内容保存为`.github/workflows/generate_readme.yml`：

```yaml
name: Generate README

on:
  issues:
    types: [opened, edited, deleted, transferred, pinned, unpinned, closed, reopened, assigned, unassigned, labeled, unlabeled, locked, unlocked, milestoned, demilestoned]
  issue_comment:
    types: [created, edited, deleted]
  push:
    branches:
      - master
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run script
        env:
          GITHUB_NAME: ${{ github.actor }}
          GITHUB_EMAIL: ${{ github.actor }}@users.noreply.github.com
        run: |
          if [[ "${{ github.event_name }}" == "issues" || "${{ github.event_name }}" == "issue_comment" ]]; then
            if [[ -n "${{ github.event.issue.number }}" ]]; then
              python -u blog_generator.py "${{ secrets.GITHUB_TOKEN || secrets.C_P }}" "${{ github.repository }}" --issue_number '${{ github.event.issue.number }}' 2>&1 | tee blog_generator.py.log
            else
              python -u blog_generator.py "${{ secrets.GITHUB_TOKEN || secrets.C_P }}" "${{ github.repository }}" 2>&1 | tee blog_generator.py.log
            fi
          else
            python -u blog_generator.py "${{ secrets.GITHUB_TOKEN || secrets.C_P }}" "${{ github.repository }}" 2>&1 | tee blog_generator.py.log
          fi
      - name: Check files
        run: |
          ls -la
          cat README.md | head -10
      - name: Push README and changes
        run: |
          git config --global user.name "${{ github.actor }}"
          git config --global user.email "${{ github.actor }}@users.noreply.github.com"
          git add BACKUP/*.md README.md feed.xml
          git status
          git commit -m "Update README and backup files by GitHub Actions - ${{ github.event_name }}" || echo "No changes to commit"
          git push origin HEAD:master || git push origin HEAD:master --force
```

### 5. 手动运行（可选）

如果你想在本地测试或手动更新博客，可以使用以下命令：

```bash
python blog_generator.py YOUR_GITHUB_TOKEN YOUR_GITHUB_USERNAME/YOUR_REPO_NAME
```

## 使用指南

### 编写博客

1. 在你的GitHub仓库中创建一个新的Issue
2. 为Issue添加适当的标题和内容（支持Markdown格式）
3. 可以添加标签（如"技术"、"生活"等）来分类博客
4. 保存Issue，GitHub Actions会自动更新博客

### 特殊标签

- **Top** - 标记为置顶文章
- **TODO** - 标记为待办事项列表
- **Friends** - 友情链接相关内容
- **About** - 关于博主的信息

### 友情链接格式

在标记为"Friends"的Issue中，使用以下格式添加友情链接：

```
名字：博客名称
链接：博客网址
描述：简短描述
```

## 项目结构

```
├── .github/workflows/   # GitHub Actions工作流配置
│   └── generate_readme.yml
├── BACKUP/              # Issues内容备份目录
├── blog_generator.py    # 主程序文件
├── test_blog_generator.py # 测试文件
├── requirements.txt     # 项目依赖
└── README.md            # 自动生成的博客首页
```

## 配置项

你可以在`blog_generator.py`中修改以下配置项：

- `RECENT_ISSUE_LIMIT` - 最近更新显示的数量（默认：5）
- `MAX_SUMMARY_LINES` - 内容摘要显示的行数（默认：3）
- `MAX_SUMMARY_LENGTH` - 每行摘要的最大长度（默认：50）
- `ANCHOR_NUMBER` - 分类下显示的文章数量上限（超过会折叠）

## 常见问题

### Q: 为什么我的博客没有更新？
A: 请检查以下几点：
   1. GitHub Actions是否成功运行
   2. GitHub Token是否有足够的权限
   3. 你的Issue是否符合条件（由你创建且没有被关闭）

### Q: 如何自定义博客样式？
A: 可以修改`blog_generator.py`中的`MD_HEAD`变量来自定义博客头部，或者修改各个`add_md_*`方法来自定义内容格式。

### Q: 如何增加新的功能？
A: 可以参考现有的代码结构，添加新的方法来实现所需功能，然后在`run`方法中调用它。

## 贡献指南

欢迎提交Issue和Pull Request来改进这个项目！

## License

MIT License

---

由[GitBlog](https://github.com/bingdu748/c_d-project)生成