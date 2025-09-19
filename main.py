# -*- coding: utf-8 -*-
import argparse
import os
import re
import sys
import traceback
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,  # 提高日志级别到DEBUG
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

import markdown
from feedgen.feed import FeedGenerator
from github import Github
from lxml.etree import CDATA
from marko.ext.gfm import gfm as marko

MD_HEAD = """## [Gitblog](https://github.com/bingdu748/c_d-project)
My personal blog（[About Me](https://github.com/yihong0618/gitblog/issues/282)）using issues and GitHub Actions (随意转载，无需署名)
[RSS Feed](https://raw.githubusercontent.com/{repo_name}/master/feed.xml)
"""

BACKUP_DIR = "BACKUP"
ANCHOR_NUMBER = 5
TOP_ISSUES_LABELS = ["Top"]
TODO_ISSUES_LABELS = ["TODO"]
FRIENDS_LABELS = ["Friends"]
ABOUT_LABELS = ["About"]
IGNORE_LABELS = FRIENDS_LABELS + TOP_ISSUES_LABELS + TODO_ISSUES_LABELS + ABOUT_LABELS

FRIENDS_TABLE_HEAD = "| Name | Link | Desc | \n | ---- | ---- | ---- |\n"
FRIENDS_TABLE_TEMPLATE = "| {name} | {link} | {desc} |\n"
FRIENDS_INFO_DICT = {
    "名字": "",
    "链接": "",
    "描述": "",
}

# 新增配置项
RECENT_ISSUE_LIMIT = 5  # 最近更新显示的数量
MAX_SUMMARY_LINES = 3   # 内容摘要显示的行数
MAX_SUMMARY_LENGTH = 50  # 每行摘要的最大长度


# 主要修改：添加一个函数来重新生成整个README.md
# 这样无论是处理单个issue还是所有issue，都能正确更新README

def regenerate_readme(repo, repo_name, me):
    """重新生成整个README.md文件"""
    try:
        logger.info("开始重新生成README.md...")
        
        # 先清空并添加头部
        add_md_header("README.md", repo_name)
        
        # 添加各个部分
        functions = [add_md_firends, add_md_top, add_md_recent, add_md_label, add_md_todo]
        for func in functions:
            # 安全地获取函数名称
            func_name = getattr(func, "__name__", str(func))
            logger.info(f"正在执行: {func_name}")
            func(repo, "README.md", me)
        
        # 生成RSS feed
        logger.info("正在生成RSS feed...")
        generate_rss_feed(repo, "feed.xml", me)
        
        logger.info("README.md重新生成完成")
    except Exception as e:
        logger.error(f"重新生成README.md失败: {str(e)}")
        raise


def get_me(user):
    """获取当前用户信息"""
    try:
        result = user.get_user().login
        logger.debug(f"获取当前用户成功: {result}")
        return result
    except Exception as e:
        logger.error(f"获取当前用户失败: {str(e)}")
        raise


def is_me(issue, me):
    """判断issue是否属于当前用户"""
    result = issue.user.login == me
    logger.debug(f"检查issue #{issue.number} 是否属于当前用户: {result}")
    return result


def is_hearted_by_me(comment, me):
    """判断评论是否被当前用户点赞"""
    try:
        reactions = list(comment.get_reactions())
        logger.debug(f"获取评论 reactions 数量: {len(reactions)}")
        for r in reactions:
            if r.content == "heart" and r.user.login == me:
                logger.debug(f"找到当前用户的 heart 反应")
                return True
        return False
    except Exception as e:
        logger.error(f"检查评论 reactions 失败: {str(e)}")
        return False


# help to covert xml vaild string
def _valid_xml_char_ordinal(c):
    codepoint = ord(c)
    # conditions ordered by presumed frequency
    return (
        0x20 <= codepoint <= 0xD7FF
        or codepoint in (0x9, 0xA, 0xD)
        or 0xE000 <= codepoint <= 0xFFFD
        or 0x10000 <= codepoint <= 0x10FFFF
    )


def format_time(time):
    return str(time)[:10]


def login(token):
    """登录GitHub"""
    try:
        logger.debug("正在创建GitHub连接...")
        result = Github(token)
        # 验证连接是否成功
        user = result.get_user()
        logger.info(f"GitHub登录成功，用户: {user.login}")
        return result
    except Exception as e:
        logger.error(f"GitHub登录失败: {str(e)}")
        raise


def get_repo(user, repo):
    """获取仓库对象"""
    try:
        logger.debug(f"正在获取仓库: {repo}")
        result = user.get_repo(repo)
        logger.info(f"获取仓库成功: {result.full_name}")
        return result
    except Exception as e:
        logger.error(f"获取仓库失败: {str(e)}")
        # 输出更多信息帮助调试
        logger.error(f"尝试获取的仓库: {repo}")
        # 尝试列出用户可访问的仓库（用于调试）
        try:
            repos = user.get_user().get_repos()
            logger.debug(f"用户可访问的仓库数量: {repos.totalCount}")
        except Exception as inner_e:
            logger.debug(f"列出用户仓库失败: {str(inner_e)}")
        raise


def parse_TODO(issue):
    try:
        body = issue.body.splitlines()
        todo_undone = [l for l in body if l.startswith("- [ ] ")]
        todo_done = [l for l in body if l.startswith("- [x] ")]
        # just add info all done
        if not todo_undone:
            return f"[{issue.title}]({issue.html_url}) all done", []
        return (
            f"[{issue.title}]({issue.html_url})--{len(todo_undone)} jobs to do--{len(todo_done)} jobs done",
            todo_done + todo_undone,
        )
    except Exception as e:
        logger.error(f"解析TODO失败: {str(e)}")
        return f"[{issue.title}]({issue.html_url}) (解析失败)", []


def get_top_issues(repo):
    """获取置顶issue"""
    try:
        issues = repo.get_issues(labels=TOP_ISSUES_LABELS)
        logger.debug(f"获取置顶文章数量: {issues.totalCount}")
        return issues
    except Exception as e:
        logger.error(f"获取置顶文章失败: {str(e)}")
        return []


def get_todo_issues(repo):
    """获取TODO类型的issue"""
    try:
        issues = repo.get_issues(labels=TODO_ISSUES_LABELS)
        logger.debug(f"获取TODO文章数量: {issues.totalCount}")
        return issues
    except Exception as e:
        logger.error(f"获取TODO文章失败: {str(e)}")
        return []


def get_repo_labels(repo):
    """获取仓库所有标签"""
    try:
        labels = [l for l in repo.get_labels()]
        logger.debug(f"获取仓库标签数量: {len(labels)}")
        logger.debug(f"仓库标签列表: {[label.name for label in labels]}")
        return labels
    except Exception as e:
        logger.error(f"获取仓库标签失败: {str(e)}")
        return []


def get_issues_from_label(repo, label):
    """获取特定标签的issue"""
    try:
        issues = repo.get_issues(labels=(label,))
        logger.debug(f"获取标签 '{label.name}' 下的文章数量: {issues.totalCount}")
        return issues
    except Exception as e:
        logger.error(f"获取标签 '{label.name}' 下的文章失败: {str(e)}")
        return []


def add_issue_info(issue, md):
    """添加issue信息到Markdown文件"""
    try:
        time = format_time(issue.updated_at)  # 使用更新时间而不是创建时间
        logger.debug(f"添加issue信息: #{issue.number} - {issue.title} - {time}")
        
        # 添加issue标题和链接（修复Markdown格式）
        md.write(f"- [{issue.title}]({issue.html_url})--{time}\n")
        
        # 如果issue有内容且内容不是太长，添加内容摘要
        if issue.body:
            # 获取issue内容的前几行作为摘要
            summary_lines = issue.body.split('\n')[:MAX_SUMMARY_LINES]  # 取前几行
            # 过滤掉空行和太短的行
            summary_lines = [line.strip() for line in summary_lines if line.strip()]
            
            if summary_lines:
                # 简单处理Markdown格式，移除标题标记等
                for line in summary_lines:
                    if line.startswith('#'):
                        # 移除标题标记
                        line = line.lstrip('#').strip()
                    # 限制行长度
                    if len(line) > MAX_SUMMARY_LENGTH:
                        line = line[:MAX_SUMMARY_LENGTH] + '...'
                    # 添加缩进和内容
                    md.write(f"  - {line}\n")
                md.write("\n")  # 添加空行分隔
    except Exception as e:
        logger.error(f"添加issue信息失败 #{issue.number}: {str(e)}")


def add_md_todo(repo, md, me):
    """添加TODO部分到Markdown文件"""
    try:
        todo_issues = list(get_todo_issues(repo))
        if not TODO_ISSUES_LABELS or not todo_issues:
            logger.debug("没有找到TODO标签或TODO文章")
            return
        # 按更新时间排序
        todo_issues = sorted(todo_issues, key=lambda x: x.updated_at, reverse=True)
        logger.debug(f"找到 {len(todo_issues)} 个TODO文章")
        
        with open(md, "a+", encoding="utf-8") as md_file:
            md_file.write("## TODO\n")
            for issue in todo_issues:
                if is_me(issue, me):
                    todo_title, todo_list = parse_TODO(issue)
                    md_file.write("TODO list from " + todo_title + "\n")
                    for t in todo_list:
                        md_file.write(t + "\n")
                    # new line
                    md_file.write("\n")
    except Exception as e:
        logger.error(f"添加TODO部分失败: {str(e)}")
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


def add_md_firends(repo, md, me):
    """添加友情链接到Markdown文件"""
    try:
        s = FRIENDS_TABLE_HEAD
        friends_issues = list(repo.get_issues(labels=FRIENDS_LABELS))
        if not FRIENDS_LABELS or not friends_issues:
            logger.debug("没有找到Friends标签或友情链接文章")
            return
        friends_issue_number = friends_issues[0].number
        logger.debug(f"找到友情链接文章 #{friends_issue_number}")
        
        for issue in friends_issues:
            for comment in issue.get_comments():
                if is_hearted_by_me(comment, me):
                    try:
                        s += _make_friend_table_string(comment.body or "")
                    except Exception as e:
                        logger.error(f"处理友情链接评论失败: {str(e)}")
                        pass
        
        s = markdown.markdown(s, output_format="html", extensions=["extra"])
        with open(md, "a+", encoding="utf-8") as md_file:
            md_file.write(
                f"## [友情链接](https://github.com/{str(me)}/gitblog/issues/{friends_issue_number})\n"
            )
            md_file.write("<details><summary>显示</summary>\n")
            md_file.write(s)
            md_file.write("</details>\n")
            md_file.write("\n\n")
    except Exception as e:
        logger.error(f"添加友情链接部分失败: {str(e)}")
        raise


# help to make friend table string
def _make_friend_table_string(s):
    info_dict = FRIENDS_INFO_DICT.copy()
    try:
        string_list = s.splitlines()
        # drop empty line
        string_list = [l for l in string_list if l and not l.isspace()]
        for l in string_list:
            string_info_list = re.split("：", l)
            if len(string_info_list) < 2:
                continue
            info_dict[string_info_list[0]] = string_info_list[1]
        return FRIENDS_TABLE_TEMPLATE.format(
            name=info_dict["名字"], link=info_dict["链接"], desc=info_dict["描述"]
        )
    except Exception as e:
        logger.error(f"生成友情链接表格字符串失败: {str(e)}")
        return


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


def add_md_header(md, repo_name):
    """添加Markdown文件头部"""
    try:
        # 获取当前时间作为更新时间戳
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"准备添加README头部，当前时间: {current_time}")
        
        # 检查文件是否存在，先读取内容以便备份
        if os.path.exists(md):
            with open(md, "r", encoding="utf-8") as f:
                old_content = f.read()
            logger.debug(f"已读取现有README内容，长度: {len(old_content)} 字符")
            
        with open(md, "w", encoding="utf-8") as md_file:
            md_file.write(MD_HEAD.format(repo_name=repo_name))
            # 添加最后更新时间
            md_file.write(f"**最后更新时间**: {current_time}\n\n")
        logger.info(f"成功添加README头部到文件: {md}")
    except Exception as e:
        logger.error(f"添加README头部失败: {str(e)}")
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
                if issues.totalCount:
                    md_file.write(f"## {label.name}\n")
                    # 按更新时间排序，确保最新更新的issue在最前面
                    issues = sorted(issues, key=lambda x: x.updated_at, reverse=True)
                    logger.debug(f"标签 '{label.name}' 下有 {issues.totalCount} 个issue")
                i = 0
                for issue in issues:
                    if not issue:
                        continue
                    if is_me(issue, me):
                        if i == ANCHOR_NUMBER:
                            md_file.write("<details><summary>显示更多</summary>\n")
                            md_file.write("\n")
                        add_issue_info(issue, md_file)
                        i += 1
                if i > ANCHOR_NUMBER:
                    md_file.write("</details>\n")
                    md_file.write("\n")
                logger.debug(f"已添加标签 '{label.name}' 下的 {i} 个issue")
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


def generate_rss_feed(repo, filename, me):
    """生成RSS feed"""
    try:
        generator = FeedGenerator()
        generator.id(repo.html_url)
        generator.title(f"RSS feed of {repo.owner.login}'s {repo.name}")
        
        # 获取环境变量
        github_name = os.getenv("GITHUB_NAME", "Unknown")
        github_email = os.getenv("GITHUB_EMAIL", "unknown@example.com")
        logger.debug(f"使用的作者信息 - 名称: {github_name}, 邮箱: {github_email}")
        
        generator.author(
            {"name": github_name, "email": github_email}
        )
        generator.link(href=repo.html_url)
        generator.link(
            href=f"https://raw.githubusercontent.com/{repo.full_name}/master/{filename}",
            rel="self",
        )
        # 按更新时间排序
        logger.debug("获取所有issue并按更新时间排序（用于RSS）...")
        sorted_issues = sorted(repo.get_issues(), key=lambda x: x.updated_at, reverse=True)
        
        entry_count = 0
        for issue in sorted_issues:
            if not issue.body or not is_me(issue, me) or issue.pull_request:
                continue
            item = generator.add_entry(order="append")
            item.id(issue.html_url)
            item.link(href=issue.html_url)
            item.title(issue.title)
            item.published(issue.created_at.strftime("%Y-%m-%dT%H:%M:%SZ"))
            for label in issue.labels:
                item.category({"term": label.name})
            body = "".join(c for c in issue.body if _valid_xml_char_ordinal(c))
            item.content(CDATA(marko.convert(body)), type="html")
            entry_count += 1
        
        # 保存RSS feed
        generator.atom_file(filename)
        logger.info(f"成功生成RSS feed，共添加 {entry_count} 个条目到文件: {filename}")
    except Exception as e:
        logger.error(f"生成RSS feed失败: {str(e)}")
        # 为了不影响主要功能，这里不抛出异常


# 检查并修复可能存在的bug
# 1. 添加更健壮的错误处理
# 2. 修复函数名称拼写一致性
# 3. 改进日志记录和输入验证

# 检查是否存在备份文件，如果存在则自动恢复
# 如果README.md不存在，则先创建一个空文件

def ensure_readme_exists():
    """确保README.md文件存在，如果不存在则创建一个空文件"""
    if not os.path.exists("README.md"):
        logger.warning("README.md文件不存在，创建空文件...")
        with open("README.md", "w", encoding="utf-8") as f:
            f.write("# 临时README文件\n")
        return True
    return False


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
        
        logger.info("main函数执行完成")
        
        # 验证README.md是否已更新
        if os.path.exists("README.md"):
            file_stat = os.stat("README.md")
            logger.info(f"README.md文件状态 - 大小: {file_stat.st_size} 字节, 修改时间: {datetime.fromtimestamp(file_stat.st_mtime)}")
        else:
            logger.error("README.md文件不存在！")
            raise FileNotFoundError("README.md文件不存在！")
        
    except Exception as e:
        logger.error(f"执行过程中发生错误: {str(e)}")
        logger.error(traceback.format_exc())
        # 重新抛出异常，以便GitHub Actions能够捕获到错误
        raise


def save_issue(issue, me, dir_name=BACKUP_DIR):
    # 生成文件名，替换可能导致问题的字符
    safe_title = issue.title.replace('/', '-').replace(' ', '.').replace('\\', '-')
    md_name = os.path.join(dir_name, f"{issue.number}_{safe_title}.md")
    
    # 检查文件是否已存在
    file_existed = os.path.exists(md_name)
    
    try:
        with open(md_name, "w", encoding="utf-8") as f:
            # 写入issue标题和链接
            f.write(f"# [{issue.title}]({issue.html_url})\n\n")
            
            # 写入issue内容
            f.write("## 内容\n\n")
            f.write(issue.body or "(无内容)")
            
            # 写入评论（如果有）
            comments = list(issue.get_comments())
            if comments:
                logger.info(f"处理issue #{issue.number} 的 {len(comments)} 条评论")
                f.write("\n\n## 评论\n\n")
                
                for c in comments:
                    # 只保存自己的评论或者所有评论（根据需求）
                    # 这里保留原逻辑，只保存自己的评论
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
