# -*- coding: utf-8 -*-
"""
README 更新模块
生成 README.md、feed.xml，统计字数/图片/更新时间
"""

import os
import sys
# 将项目根目录加入 sys.path，使脚本可直接 python scripts/xxx.py 运行
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
from datetime import datetime, timedelta, timezone

from scripts.utils import (
    logger, login, get_repo, get_me, is_me, format_time,
    get_issue_word_count, get_issue_image_count, load_metadata,
    TOP_ISSUES_LABELS, TODO_ISSUES_LABELS, IGNORE_LABELS,
    RECENT_ISSUE_LIMIT, BEIJING_TZ
)


def get_todo_issues(repo):
    """获取待办issue"""
    try:
        return repo.get_issues(state='all', labels=TODO_ISSUES_LABELS)
    except Exception as e:
        logger.error(f"获取待办文章失败: {str(e)}")
        return []


def get_top_issues(repo):
    """获取置顶issue"""
    try:
        return repo.get_issues(state='all', labels=TOP_ISSUES_LABELS)
    except Exception as e:
        logger.error(f"获取置顶文章失败: {str(e)}")
        return []


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
        return repo.get_issues(state='all', labels=(label,))
    except Exception as e:
        logger.error(f"获取标签issue失败: {str(e)}")
        return []


def add_issue_info(issue, md):
    """添加issue信息到Markdown文件"""
    try:
        time = format_time(issue.updated_at)
        md.write(f"- [{issue.title}]({issue.html_url})--{time}\n")
    except Exception as e:
        logger.error(f"添加issue信息失败 #{issue.number}: {str(e)}")


def add_md_todo(repo, md, me):
    """添加待办事项到Markdown文件"""
    try:
        todo_issues = list(get_todo_issues(repo))
        if not TODO_ISSUES_LABELS or not todo_issues:
            logger.debug("没有找到待办标签或待办文章")
            return
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


def add_md_top(repo, md, me):
    """添加置顶文章到Markdown文件"""
    try:
        top_issues = list(get_top_issues(repo))
        if not TOP_ISSUES_LABELS or not top_issues:
            logger.debug("没有找到Top标签或置顶文章")
            return
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
    """添加文章列表到Markdown文件"""
    try:
        count = 0
        with open(md, "a+", encoding="utf-8") as md_file:
            try:
                md_file.write("## 文章列表\n")
                md_file.write("| 序号 | 文章标题 | 更新时间 | 字数统计 | 插图统计 |\n")
                md_file.write("|:------:|:------------------:|:------------------:|:------:|:------:|\n")
                logger.debug("获取所有issue并按更新时间排序...")
                all_issues = sorted(repo.get_issues(state='all'), key=lambda x: x.updated_at, reverse=True)
                logger.debug(f"获取到 {len(all_issues)} 个issue")

                # 加载元数据（含生成 .md 文件时计算的完整字数/图片数）
                metadata = load_metadata()

                for issue in all_issues:
                    if is_me(issue, me):
                        time = format_time(issue.updated_at)

                        # 优先从元数据读取（含评论），回退到仅统计 issue.body
                        issue_key = str(issue.number)
                        if issue_key in metadata and "word_count" in metadata[issue_key]:
                            word_count = metadata[issue_key]["word_count"]
                            image_count = metadata[issue_key].get("image_count", 0)
                        else:
                            word_count = get_issue_word_count(issue)
                            image_count = get_issue_image_count(issue)

                        md_file.write(
                            f"| {count + 1} | [{issue.title}]({issue.html_url}) "
                            f"| {time} | {word_count} | {image_count} |\n"
                        )
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
                if label.name in IGNORE_LABELS:
                    continue

                issues = get_issues_from_label(repo, label)
                issues_list = list(issues)
                if not issues_list:
                    continue

                md_file.write(f"## {label.name}\n")
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
                    md_file.write("\n")
    except Exception as e:
        logger.error(f"添加标签分类部分失败: {str(e)}")
        raise


def add_md_firends(repo, md, me):
    """添加友链文章到Markdown文件"""
    try:
        with open(md, "a+", encoding="utf-8") as md_file:
            try:
                issues = list(repo.get_issues(state='all'))
                friend_issues = [issue for issue in issues if not is_me(issue, me)]
                friend_issues = sorted(friend_issues, key=lambda x: x.updated_at, reverse=True)

                if friend_issues:
                    logger.debug(f"找到 {len(friend_issues)} 个友链文章")
                    md_file.write("## 友链文章\n")
                    for issue in friend_issues:
                        add_issue_info(issue, md_file)
                else:
                    logger.debug("没有找到友链文章")
            except Exception as e:
                logger.error(f"添加友链文章时发生异常: {str(e)}")
    except Exception as e:
        logger.error(f"添加友链文章部分失败: {str(e)}")
        raise


def generate_rss_feed(repo, me):
    """生成RSS feed文件"""
    try:
        all_issues = sorted(
            [issue for issue in repo.get_issues(state='all') if is_me(issue, me)],
            key=lambda x: x.updated_at, reverse=True
        )

        rss_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
    <title>{repo.name} Blog</title>
    <link>{repo.html_url}</link>
    <description>Blog generated from GitHub issues</description>
    <language>zh-CN</language>
    <lastBuildDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')}</lastBuildDate>
"""

        for issue in all_issues[:RECENT_ISSUE_LIMIT]:
            pub_date = issue.updated_at.strftime('%a, %d %b %Y %H:%M:%S GMT')
            body = issue.body or ""
            description = (body[:200] + '...') if len(body) > 200 else body
            rss_content += f"""
    <item>
        <title>{issue.title}</title>
        <link>{issue.html_url}</link>
        <description>{description}</description>
        <pubDate>{pub_date}</pubDate>
        <guid>{issue.html_url}</guid>
    </item>
"""

        rss_content += """
</channel>
</rss>
"""

        with open("feed.xml", "w", encoding="utf-8") as f:
            f.write(rss_content)

        logger.info("RSS feed生成成功")
    except Exception as e:
        logger.error(f"生成RSS feed失败: {str(e)}")
        raise


def ensure_readme_exists():
    """确保README.md文件存在"""
    if os.path.exists("README.md"):
        return
    logger.warning("README.md文件不存在，创建默认README.md")
    try:
        default_content = """# My GitHub Blog

欢迎访问我的GitHub Blog！本博客基于GitHub Issues构建。

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
    """重新生成README.md文件"""
    try:
        logger.info("开始重新生成README.md...")

        # 清空 README.md
        with open("README.md", "w", encoding="utf-8") as f:
            f.write("")

        # 添加各模块
        add_md_top(repo, "README.md", me)
        add_md_todo(repo, "README.md", me)
        add_md_label(repo, "README.md", me)
        add_md_recent(repo, "README.md", me)
        add_md_firends(repo, "README.md", me)

        # 统计信息
        beijing_now = datetime.now(BEIJING_TZ)
        update_time = beijing_now.strftime("%Y-%m-%d %H:%M:%S")

        all_issues = list(repo.get_issues(state='all'))
        my_issues = [issue for issue in all_issues if is_me(issue, me)]
        total_articles = len(my_issues)

        # 优先从元数据读取（含评论），回退到仅统计 issue.body
        metadata = load_metadata()
        total_word_count = 0
        total_image_count = 0
        for issue in my_issues:
            issue_key = str(issue.number)
            if issue_key in metadata and "word_count" in metadata[issue_key]:
                total_word_count += metadata[issue_key]["word_count"]
                total_image_count += metadata[issue_key].get("image_count", 0)
            else:
                total_word_count += get_issue_word_count(issue)
                total_image_count += get_issue_image_count(issue)

        # 最近24小时内的新增和更新
        recent_threshold = beijing_now - timedelta(hours=24)
        recent_updated = [
            issue for issue in my_issues
            if issue.updated_at.replace(tzinfo=timezone.utc).astimezone(BEIJING_TZ) > recent_threshold
        ]
        recent_created = [
            issue for issue in my_issues
            if issue.created_at.replace(tzinfo=timezone.utc).astimezone(BEIJING_TZ) > recent_threshold
        ]

        with open("README.md", "a+", encoding="utf-8") as f:
            f.write("\n\n## 博客统计\n")
            f.write(f"- 最后更新: {update_time}\n")
            f.write(f"- 总文章数: {total_articles}\n")
            f.write(f"- 新增文章: {len(recent_created)}\n")
            f.write(f"- 更新文章: {len(recent_updated)}\n")
            f.write(f"- 总字数: {total_word_count}\n")
            f.write(f"- 总插图数: {total_image_count}\n")

        logger.info("README.md 重新生成完成")
    except Exception as e:
        logger.error(f"重新生成README.md失败: {str(e)}")
        raise


def main():
    """主入口：生成 README.md 和 feed.xml"""
    import argparse

    parser = argparse.ArgumentParser(description="更新 README.md 和 feed.xml")
    parser.add_argument("token", help="GitHub Personal Access Token")
    parser.add_argument("repo_name", help="仓库名称 (owner/repo)")
    args = parser.parse_args()

    logger.info("=" * 50)
    logger.info("开始更新 README.md 和 feed.xml")

    # 登录
    user = login(args.token)
    me = get_me(user)
    logger.info(f"登录成功: {me}")

    # 获取仓库
    repo = get_repo(user, args.repo_name)

    # 确保 README.md 存在
    ensure_readme_exists()

    # 重新生成 README.md
    regenerate_readme(repo, args.repo_name, me)

    # 生成 RSS feed
    generate_rss_feed(repo, me)

    logger.info("README.md 和 feed.xml 更新完成")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()