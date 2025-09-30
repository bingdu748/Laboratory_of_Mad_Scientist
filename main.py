# -*- coding: utf-8 -*-
"""
GitBlog README和备份生成器
将GitHub issue转换为Markdown文件并更新README.md
"""

import os
import sys
import logging
import argparse
import traceback
from datetime import datetime

import github

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# 常量定义
TOP_ISSUES_LABELS = ["Top", "置顶"]
TODO_ISSUES_LABELS = ["TODO", "待办"]
IGNORE_LABELS = TOP_ISSUES_LABELS + TODO_ISSUES_LABELS + ["bug", "enhancement"]
BACKUP_DIR = "BACKUP"
RECENT_ISSUE_LIMIT = 20  # 最近更新显示数量
MAX_SUMMARY_LINES = 3    # 摘要显示行数
MAX_SUMMARY_LENGTH = 100  # 摘要行最大长度

def get_me(user):
    """获取当前用户信息"""
    try:
        # 检查是否在GitHub Actions环境中
        if os.getenv("GITHUB_ACTIONS") == "true":
            # 在GitHub Actions环境中，使用环境变量获取仓库所有者作为用户名
            # 或者直接返回一个默认值，因为在Actions环境中用户信息不是必需的
            repo_name = os.getenv("GITHUB_REPOSITORY", "")
            if repo_name and '/' in repo_name:
                owner = repo_name.split('/')[0]
                logger.info(f"在GitHub Actions环境中，使用仓库所有者作为用户名: {owner}")
                return owner
            logger.info("在GitHub Actions环境中，使用默认用户名")
            return "github-actions"
        
        # 非GitHub Actions环境，正常获取用户信息
        return user.get_user().login
    except Exception as e:
        logger.warning(f"获取当前用户信息失败，使用默认值: {str(e)}")
        # 返回一个默认值，避免程序因用户信息获取失败而崩溃
        return "unknown_user"

def is_me(issue_or_comment, me):
    """判断issue或评论是否属于自己"""
    try:
        return issue_or_comment.user.login == me
    except Exception as e:
        logger.error(f"判断用户身份失败: {str(e)}")
        return False

def login(token):
    """登录GitHub"""
    try:
        # 使用新的认证方法
        try:
            import github.Auth
            auth = github.Auth.Token(token)
            return github.Github(auth=auth)
        except ImportError:
            # 如果Auth模块不存在（旧版本PyGithub），则回退到旧方法
            logger.warning("使用旧版本的PyGithub认证方法")
            return github.Github(token)
    except Exception as e:
        logger.error(f"登录GitHub失败: {str(e)}")
        raise

def get_repo(user, repo_name):
    """获取GitHub仓库"""
    try:
        return user.get_repo(repo_name)
    except Exception as e:
        logger.error(f"获取仓库失败: {str(e)}")
        raise

def format_time(time_obj):
    """格式化时间"""
    try:
        return time_obj.strftime("%Y-%m-%d %H:%M:%S") if hasattr(time_obj, 'strftime') else "未知时间"
    except Exception as e:
        logger.error(f"格式化时间失败: {str(e)}")
        return "时间格式化失败"

def get_repo_labels(repo):
    """获取仓库所有标签"""
    try:
        return list(repo.get_labels())
    except Exception as e:
        logger.error(f"获取仓库标签失败: {str(e)}")
        return []

def get_issues_from_label(repo, label):
    """获取特定标签的issue"""
    try:
        return repo.get_issues(labels=(label,))
    except Exception as e:
        logger.error(f"获取标签issue失败: {str(e)}")
        return []

def get_todo_issues(repo):
    """获取待办issue"""
    try:
        issues = repo.get_issues(labels=TODO_ISSUES_LABELS)
        logger.debug(f"获取待办文章数量: {issues.totalCount}")
        return issues
    except Exception as e:
        logger.error(f"获取待办文章失败: {str(e)}")
        return []

def add_md_todo(repo, md, me):
    """添加待办事项到Markdown文件"""
    try:
        todo_issues = list(get_todo_issues(repo))
        if not TODO_ISSUES_LABELS or not todo_issues:
            logger.debug("没有找到待办标签或待办文章")
            return
        # 按更新时间排序
        todo_issues = sorted(todo_issues, key=lambda x: x.updated_at, reverse=True)
        logger.debug(f"找到 {len(todo_issues)} 个待办文章")
        
        with open(md, "a+", encoding="utf-8") as md_file:
            md_file.write("## 待办事项\n")
            for issue in todo_issues:
                if is_me(issue, me):
                    add_issue_info(issue, md_file)
    except Exception as e:
        logger.error(f"添加待办事项部分失败: {str(e)}")
        raise

def get_top_issues(repo):
    """获取置顶issue"""
    try:
        issues = repo.get_issues(labels=TOP_ISSUES_LABELS)
        logger.debug(f"获取置顶文章数量: {issues.totalCount}")
        return issues
    except Exception as e:
        logger.error(f"获取置顶文章失败: {str(e)}")
        return []

def add_issue_info(issue, md):
    """添加issue信息到Markdown文件"""
    try:
        time = format_time(issue.updated_at)  # 使用更新时间而不是创建时间
        logger.debug(f"添加issue信息: #{issue.number} - {issue.title} - {time}")
        
        # 只添加issue标题和链接，不添加内容摘要
        md.write(f"- [{issue.title}]({issue.html_url})--{time}\n")
        
    except Exception as e:
        logger.error(f"添加issue信息失败 #{issue.number}: {str(e)}")

def add_md_firends(repo, md, me):
    """添加朋友的issue到Markdown文件"""
    try:
        with open(md, "a+", encoding="utf-8") as md_file:
            try:
                # 获取所有issue
                issues = list(repo.get_issues())
                logger.debug(f"获取朋友的issue总数: {len(issues)}")
                
                # 筛选出不属于自己的issue
                friend_issues = [issue for issue in issues if not is_me(issue, me)]
                
                # 按更新时间排序
                friend_issues = sorted(friend_issues, key=lambda x: x.updated_at, reverse=True)
                
                if friend_issues:
                    logger.debug(f"找到 {len(friend_issues)} 个朋友的issue")
                    md_file.write("## 朋友的文章\n")
                    for issue in friend_issues:
                        add_issue_info(issue, md_file)
                else:
                    logger.debug("没有找到朋友的issue")
            except Exception as e:
                logger.error(f"添加朋友的文章时发生异常: {str(e)}")
    except Exception as e:
        logger.error(f"添加朋友的文章部分失败: {str(e)}")
        raise

def add_md_top(repo, md, me):
    """添加置顶文章到Markdown文件"""
    try:
        top_issues = list(get_top_issues(repo))
        if not TOP_ISSUES_LABELS or not top_issues:
            logger.debug("没有找到Top标签或置顶文章")
            return
        # 按更新时间排序
        top_issues = sorted(top_issues, key=lambda x: x.updated_at, reverse=True)
        logger.debug(f"找到 {len(top_issues)} 个置顶文章")
        
        with open(md, "a+", encoding="utf-8") as md_file:
            md_file.write("## 置顶文章\n")
            for issue in top_issues:
                if is_me(issue, me):
                    add_issue_info(issue, md_file)
    except Exception as e:
        logger.error(f"添加置顶文章部分失败: {str(e)}")
        raise

def add_md_recent(repo, md, me, limit=RECENT_ISSUE_LIMIT):
    """添加最近更新到Markdown文件"""
    try:
        count = 0
        with open(md, "a+", encoding="utf-8") as md_file:
            # one the issue that only one issue and delete (pyGitHub raise an exception)
            try:
                md_file.write("## 最近更新\n")
                # 按更新时间排序，确保最新更新的issue在最前面
                logger.debug("获取所有issue并按更新时间排序...")
                all_issues = sorted(repo.get_issues(), key=lambda x: x.updated_at, reverse=True)
                logger.debug(f"获取到 {len(all_issues)} 个issue")
                
                for issue in all_issues:
                    if is_me(issue, me):
                        add_issue_info(issue, md_file)
                        count += 1
                        if count >= limit:
                            break
                logger.debug(f"已添加 {count} 个最近更新的issue")
            except Exception as e:
                logger.error(f"添加最近更新部分时发生异常: {str(e)}")
    except Exception as e:
        logger.error(f"添加最近更新部分失败: {str(e)}")
        raise

def add_md_label(repo, md, me):
    """添加标签分类的issue到Markdown文件"""
    try:
        labels = get_repo_labels(repo)
        
        # sort lables by description info if it exists, otherwise sort by name,
        # for example, we can let the description start with a number (1#Java, 2#Docker, 3#K8s, etc.)
        labels = sorted(
            labels,
            key=lambda x: (
                x.description is None,
                x.description == "",
                x.description,
                x.name,
            ),
        )
        
        with open(md, "a+", encoding="utf-8") as md_file:
            for label in labels:
                # we don't need add top label again
                if label.name in IGNORE_LABELS:
                    logger.debug(f"跳过忽略的标签: {label.name}")
                    continue
                
                issues = get_issues_from_label(repo, label)
                
                # 处理issues，无论是GitHub API对象还是列表
                issues_list = list(issues)  # 转换为列表以确保可排序
                
                if issues_list:  # 检查列表是否非空
                    md_file.write(f"## {label.name}\n")
                    # 按更新时间排序，确保最新更新的issue在最前面
                    issues_list = sorted(issues_list, key=lambda x: x.updated_at, reverse=True)
                    logger.debug(f"标签 '{label.name}' 下有 {len(issues_list)} 个issue")
                i = 0
                for issue in issues_list:
                    if not issue:
                        continue
                    if is_me(issue, me):
                        add_issue_info(issue, md_file)
                        i += 1
                if i > 0:
                    md_file.write("\n")  # 添加空行分隔不同标签
    except Exception as e:
        logger.error(f"添加标签分类部分失败: {str(e)}")
        raise

def get_to_generate_issues(repo, dir_name, issue_number=None):
    """获取需要生成的issue列表"""
    try:
        # 首先获取所有issue
        all_issues = list(repo.get_issues())
        logger.debug(f"获取所有issue数量: {len(all_issues)}")
        
        # 如果提供了issue_number，只处理指定的issue
        if issue_number:
            logger.info(f"指定了issue_number: {issue_number}，将只处理该issue")
            try:
                target_issue = repo.get_issue(int(issue_number))
                return [target_issue]
            except Exception as e:
                logger.error(f"获取指定issue失败: {str(e)}")
                return []
        
        # 如果没有提供issue_number，处理所有issue
        logger.info(f"未指定issue_number，将处理所有issue")
        return all_issues
    except Exception as e:
        logger.error(f"获取待生成的issues失败: {str(e)}")
        return []

def generate_rss_feed(repo, me):
    """生成RSS feed文件"""
    try:
        # 获取所有自己的issue
        all_issues = sorted(
            [issue for issue in repo.get_issues() if is_me(issue, me)],
            key=lambda x: x.updated_at, reverse=True
        )
        
        # 生成RSS内容
        rss_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
    <title>{repo.name} Blog</title>
    <link>{repo.html_url}</link>
    <description>Blog generated from GitHub issues</description>
    <language>zh-CN</language>
    <lastBuildDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')}</lastBuildDate>
"""
        
        # 添加每个issue作为一个条目
        for issue in all_issues[:RECENT_ISSUE_LIMIT]:  # 只添加最近的20个
            pub_date = issue.updated_at.strftime('%a, %d %b %Y %H:%M:%S GMT')
            rss_content += f"""
    <item>
        <title>{issue.title}</title>
        <link>{issue.html_url}</link>
        <description>{issue.body[:200] + '...' if len(issue.body) > 200 else issue.body}</description>
        <pubDate>{pub_date}</pubDate>
        <guid>{issue.html_url}</guid>
    </item>
"""
        
        rss_content += """
</channel>
</rss>
"""
        
        # 写入feed.xml文件
        with open("feed.xml", "w", encoding="utf-8") as f:
            f.write(rss_content)
        
        logger.info("RSS feed生成成功")
    except Exception as e:
        logger.error(f"生成RSS feed失败: {str(e)}")
        raise

def ensure_readme_exists():
    """确保README.md文件存在"""
    if not os.path.exists("README.md"):
        logger.warning("README.md文件不存在，将创建一个默认的README.md")
        try:
            # 检查是否有README模板
            if os.path.exists("README_TEMPLATE.md"):
                with open("README_TEMPLATE.md", "r", encoding="utf-8") as f:
                    template_content = f.read()
                with open("README.md", "w", encoding="utf-8") as f:
                    f.write(template_content)
                logger.info("已使用README_TEMPLATE.md创建README.md")
            else:
                # 创建默认的README
                default_content = """
# My GitHub Blog

欢迎访问我的GitHub Blog！本博客基于GitHub Issues构建。

[RSS Feed](https://raw.githubusercontent.com/{owner}/{repo}/master/feed.xml)

## 最近更新

（暂无内容，请创建Issue）
"""
                with open("README.md", "w", encoding="utf-8") as f:
                    f.write(default_content)
                logger.info("已创建默认的README.md")
        except Exception as e:
            logger.error(f"创建README.md失败: {str(e)}")
            raise

def regenerate_readme(repo, repo_name, me):
    """重新生成README.md文件，按照标签分类更新所有issue链接"""
    try:
        logger.info("开始重新生成README.md...")
        
        # 备份当前README.md
        backup_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(BACKUP_DIR, f"README_backup_{backup_time}.md")
        if os.path.exists("README.md"):
            try:
                with open("README.md", "r", encoding="utf-8") as f:
                    content = f.read()
                with open(backup_path, "w", encoding="utf-8") as f:
                    f.write(content)
                logger.info(f"已备份README.md到: {backup_path}")
            except Exception as e:
                logger.error(f"备份README.md失败: {str(e)}")
        
        # 创建新的README.md
        # 从仓库名提取所有者和仓库名
        parts = repo_name.split("/")
        owner = parts[0] if len(parts) > 1 else ""
        repo_short_name = parts[1] if len(parts) > 1 else parts[0]
        
        # 创建新的README内容
        new_content = f"""My personal blog（[About Me](https://github.com/{owner}/{repo_short_name}/issues/7)）using issues and GitHub Actions (随意转载，无需署名)
[RSS Feed](https://raw.githubusercontent.com/{owner}/{repo_short_name}/master/feed.xml)

"""
        
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(new_content)
        
        # 添加置顶文章
        add_md_top(repo, "README.md", me)
        
        # 添加待办事项
        add_md_todo(repo, "README.md", me)
        
        # 根据标签分类添加issue链接（主要功能）
        add_md_label(repo, "README.md", me)
        
        # 添加最近更新
        add_md_recent(repo, "README.md", me)
        
        # 添加朋友的文章
        add_md_firends(repo, "README.md", me)
        
        # 更新最后更新时间
        update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("README.md", "a+", encoding="utf-8") as f:
            f.write(f"\n\n## 更新日志\n")
            f.write(f"- 最后更新: {update_time}\n")
        
        logger.info("README.md重新生成成功")
        
        # 生成RSS feed
        generate_rss_feed(repo, me)
        
    except Exception as e:
        logger.error(f"重新生成README.md失败: {str(e)}")
        raise

def push_to_backup_branch(dir_name=BACKUP_DIR):
    """将备份文件推送到backup分支
    在GitHub Actions环境中，这个功能由工作流处理，避免重复操作
    只推送md文件到分支根目录，不创建文件夹
    """
    try:
        # 检查是否在GitHub Actions环境中运行
        is_github_actions = os.getenv("GITHUB_ACTIONS") == "true"
        
        if is_github_actions:
            logger.info("在GitHub Actions环境中运行，跳过备份分支推送操作（由工作流处理）")
            return
        
        # 检查是否有git命令可用
        import subprocess
        try:
            subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("git命令不可用，跳过备份分支推送操作")
            return
        
        logger.info("开始将备份文件推送到backup分支...")
        
        # 检查backup分支是否存在，如果不存在则创建
        try:
            subprocess.run(["git", "rev-parse", "--verify", "backup"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logger.info("backup分支已存在")
        except subprocess.CalledProcessError:
            logger.info("backup分支不存在，正在创建...")
            subprocess.run(["git", "branch", "backup"], check=True)
        
        # 切换到backup分支
        logger.info("切换到backup分支...")
        subprocess.run(["git", "checkout", "backup"], check=True)
        
        # 清理旧的备份文件（只保留当前备份的md文件）
        logger.info("清理旧的备份文件...")
        import glob
        import shutil
        
        # 创建临时目录存放当前md文件
        temp_dir = os.path.join(os.getcwd(), "temp_backup")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        
        # 复制当前备份目录中的md文件到临时目录
        md_files = glob.glob(os.path.join(dir_name, "*.md"))
        for md_file in md_files:
            shutil.copy2(md_file, temp_dir)
        
        # 清理backup分支上的所有文件（保留.git目录）
        logger.info("彻底清理backup分支上的所有文件...")
        for item in os.listdir():
            # 跳过.git目录和README.md
            if item == ".git" or item == "README.md":
                continue
            
            item_path = os.path.join(os.getcwd(), item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        
        # 将临时目录中的md文件复制到根目录
        temp_md_files = glob.glob(os.path.join(temp_dir, "*.md"))
        for md_file in temp_md_files:
            shutil.copy2(md_file, os.getcwd())
        
        # 清理临时目录
        shutil.rmtree(temp_dir)
        
        # 添加根目录中的md文件
        logger.info("添加md文件到根目录...")
        subprocess.run(["git", "add", "*.md"], check=True)
        
        # 提交更改
        commit_message = f"备份issue文件 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        logger.info(f"提交更改: {commit_message}")
        try:
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
        except subprocess.CalledProcessError:
            logger.info("没有需要提交的更改")
        
        # 推送分支
        logger.info("推送到backup分支...")
        subprocess.run(["git", "push", "origin", "backup"], check=True)
        
        # 切换回原来的分支（通常是master）
        logger.info("切换回master分支...")
        subprocess.run(["git", "checkout", "master"], check=True)
        
        logger.info("备份文件已成功推送到backup分支")
    except Exception as e:
        logger.error(f"将备份文件推送到backup分支失败: {str(e)}")
        # 尝试切换回master分支，避免影响后续操作
        try:
            import subprocess
            subprocess.run(["git", "checkout", "master"], check=True)
        except:
            pass
        raise

def save_issue(issue, me, dir_name=BACKUP_DIR):
    # 生成文件名，替换可能导致问题的字符
    safe_title = issue.title.replace('/', '-').replace(' ', '.').replace('\\', '-')
    # 移除其他可能导致文件名问题的字符
    safe_title = ''.join(c for c in safe_title if c.isalnum() or c in '.-_')
    md_name = os.path.join(dir_name, f"{issue.number}_{safe_title}.md")
    
    # 检查文件是否已存在
    file_existed = os.path.exists(md_name)
    
    try:
        with open(md_name, "w", encoding="utf-8") as f:
            # 写入issue标题和链接
            f.write(f"# [{issue.title}]({issue.html_url})\n\n")
            
            # 写入issue创建时间和更新时间
            f.write(f"## 元信息\n\n")
            f.write(f"- 创建时间: {format_time(issue.created_at)}\n")
            f.write(f"- 更新时间: {format_time(issue.updated_at)}\n")
            
            # 写入issue标签信息
            labels = [label.name for label in issue.labels]
            if labels:
                f.write(f"- 标签: {', '.join(labels)}\n")
            f.write("\n")
            
            # 写入issue内容
            f.write("## 内容\n\n")
            f.write(issue.body or "(无内容)")
            
            # 写入评论（如果有）
            comments = list(issue.get_comments())
            if comments:
                logger.info(f"处理issue #{issue.number} 的 {len(comments)} 条评论")
                f.write("\n\n## 评论\n\n")
                
                for c in comments:
                    # 只保存自己的评论
                    if is_me(c, me):
                        comment_time = format_time(c.created_at)
                        f.write(f"### 评论 ({comment_time})\n\n")
                        f.write(c.body or "(无评论内容)")
                        f.write("\n\n---\n\n")
    
        # 记录文件保存状态
        if file_existed:
            logger.info(f"更新已存在的issue文件: {md_name}")
        else:
            logger.info(f"创建新的issue文件: {md_name}")
            
    except Exception as e:
        logger.error(f"保存issue #{issue.number} 到 {md_name} 失败: {str(e)}")
        raise

# 运行测试脚本验证README更新功能

def main(token, repo_name, issue_number=None, dir_name=BACKUP_DIR):
    try:
        # 输出环境信息
        logger.debug(f"当前工作目录: {os.getcwd()}")
        logger.debug(f"Python版本: {sys.version}")
        logger.debug(f"环境变量: {dict(os.environ)}")
        
        logger.info(f"开始执行main函数，仓库: {repo_name}, issue_number: {issue_number}")
        
        # 确保README.md存在
        ensure_readme_exists()
        
        # 检查备份目录是否存在
        if not os.path.exists(dir_name):
            logger.info(f"创建备份目录: {dir_name}")
            os.makedirs(dir_name)
        
        # 登录GitHub
        logger.info("正在登录GitHub...")
        user = login(token)
        me = get_me(user)
        logger.info(f"登录成功，用户: {me}")
        
        # 获取仓库
        logger.info(f"正在获取仓库: {repo_name}")
        repo = get_repo(user, repo_name)
        logger.info(f"获取仓库成功: {repo.full_name}")
        
        # 处理issue_number
        logger.info(f"处理issue_number: {issue_number}")
        # 更健壮的issue_number处理
        if issue_number == '' or issue_number is None:
            issue_number = None
            logger.info("issue_number为空字符串或None，将处理所有issue")
        else:
            # 尝试转换为整数，确保输入有效
            try:
                issue_number = int(issue_number)
                logger.info(f"已转换issue_number为整数: {issue_number}")
            except ValueError:
                logger.error(f"无效的issue_number: {issue_number}，将处理所有issue")
                issue_number = None
        
        # 获取待生成的issues
        logger.info("获取待生成的issues...")
        to_generate_issues = get_to_generate_issues(repo, dir_name, issue_number)
        logger.info(f"找到{len(to_generate_issues)}个待生成的issue")
        
        # 保存issue到备份文件夹
        logger.info("开始保存issue到备份文件夹...")
        for issue in to_generate_issues:
            logger.info(f"保存issue: #{issue.number} - {issue.title}")
            save_issue(issue, me, dir_name)
        
        # 主要修改：无论是否指定了issue_number，都重新生成整个README.md
        # 这样在GitHub Actions触发时，即使只处理单个issue，也能更新README
        regenerate_readme(repo, repo_name, me)
        
        # 将备份文件推送到backup分支
        # 注意：在GitHub Actions环境中，此操作会被push_to_backup_branch函数跳过，由工作流处理
        try:
            push_to_backup_branch(dir_name)
        except Exception as e:
            logger.warning(f"备份分支推送失败，但这不影响主要功能: {str(e)}")
        
        logger.info("main函数执行完成")
        
        # 验证README.md是否已更新
        if os.path.exists("README.md"):
            file_stat = os.stat("README.md")
            logger.info(f"README.md文件状态 - 大小: {file_stat.st_size} 字节, 修改时间: {datetime.fromtimestamp(file_stat.st_mtime)}")
        else:
            logger.error("README.md文件不存在！")
            
    except Exception as e:
        logger.error(f"main函数执行失败: {str(e)}")
        logger.error(traceback.format_exc())
        raise

if __name__ == "__main__":
    try:
        # 确保BACKUP_DIR存在
        if not os.path.exists(BACKUP_DIR):
            logger.info(f"创建备份目录: {BACKUP_DIR}")
            os.makedirs(BACKUP_DIR)
            
        # 解析命令行参数
        parser = argparse.ArgumentParser(description='生成GitBlog README和备份文件')
        parser.add_argument("github_token", help="GitHub访问令牌")
        parser.add_argument("repo_name", help="GitHub仓库名称，格式为owner/repo")
        parser.add_argument(
            "--issue_number", help="指定要处理的issue编号（可选）", default=None, required=False
        )
        parser.add_argument(
            "--dir_name", help="备份目录名称（可选）", default=BACKUP_DIR, required=False
        )
        
        options = parser.parse_args()
        logger.info(f"解析命令行参数完成: {options}")
        
        # 执行主函数
        main(options.github_token, options.repo_name, options.issue_number, options.dir_name)
        
    except argparse.ArgumentError as e:
        logger.error(f"参数解析错误: {str(e)}")
        parser.print_help()
        sys.exit(1)
    except Exception as e:
        logger.error(f"程序执行失败: {str(e)}")
        logger.error(traceback.format_exc())
        sys.exit(1)
