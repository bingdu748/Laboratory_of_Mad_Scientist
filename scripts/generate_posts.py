# -*- coding: utf-8 -*-
"""
文章生成模块
从 GitHub Issues 拉取数据，生成 .md 文件到 posts/ 目录
按标签分目录，无标签放 no-label/
"""

import os
import sys
# 将项目根目录加入 sys.path，使脚本可直接 python scripts/xxx.py 运行
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import glob
import logging
from scripts.utils import (
    logger, login, get_repo, get_me, is_me, format_time,
    POSTS_DIR, IGNORE_LABELS, METADATA_FILE, load_metadata, save_metadata
)


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


def get_to_generate_issues(repo, me, issue_number=None):
    """获取需要生成的issue列表"""
    try:
        if issue_number:
            logger.info(f"指定了issue_number: {issue_number}，将只处理该issue")
            try:
                return [repo.get_issue(int(issue_number))]
            except Exception as e:
                logger.error(f"获取指定issue失败: {str(e)}")
                return []

        logger.info("未指定issue_number，将处理所有issue")
        return list(repo.get_issues())
    except Exception as e:
        logger.error(f"获取待生成的issues失败: {str(e)}")
        return []


def sanitize_filename(title):
    """将标题转换为安全的文件名"""
    safe = title.replace('/', '-').replace('\\', '-').replace(' ', '.')
    safe = ''.join(c for c in safe if c.isalnum() or c in '.-_')
    return safe


def get_label_dir(issue):
    """获取 issue 应存放的标签目录名"""
    labels = [label.name for label in issue.labels]
    content_labels = [l for l in labels if l not in IGNORE_LABELS]
    return content_labels[0] if content_labels else "no-label"


def save_issue(issue, me):
    """保存 issue 为 .md 文件到 posts/ 目录下"""
    label_dir = get_label_dir(issue)
    dir_path = os.path.join(POSTS_DIR, label_dir)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        logger.info(f"创建标签目录: {dir_path}")

    safe_title = sanitize_filename(issue.title)
    md_path = os.path.join(dir_path, f"{safe_title}.md")

    labels = [label.name for label in issue.labels]

    try:
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# [{issue.title}]({issue.html_url})\n\n")
            f.write(f"## 元信息\n\n")
            f.write(f"- 创建时间: {format_time(issue.created_at)}\n")
            f.write(f"- 更新时间: {format_time(issue.updated_at)}\n")
            if labels:
                f.write(f"- 标签: {', '.join(labels)}\n")
            f.write("\n")
            f.write("## 内容\n\n")
            f.write(issue.body or "(无内容)")

            # 写入评论
            comments = list(issue.get_comments())
            if comments:
                logger.info(f"处理issue #{issue.number} 的 {len(comments)} 条评论")
                f.write("\n\n## 评论\n\n")
                for c in comments:
                    if is_me(c, me):
                        f.write(f"### 评论 ({format_time(c.created_at)})\n\n")
                        f.write(c.body or "(无评论内容)")
                        f.write("\n\n---\n\n")

        logger.info(f"保存issue文件: {md_path}")

        # 更新元数据
        metadata = load_metadata()
        metadata[str(issue.number)] = {
            "title": issue.title,
            "filename": safe_title,
            "label": label_dir,
            "updated": issue.updated_at.isoformat() if hasattr(issue.updated_at, 'isoformat') else str(issue.updated_at)
        }
        save_metadata(metadata)

        return md_path
    except Exception as e:
        logger.error(f"保存issue #{issue.number} 到 {md_path} 失败: {str(e)}")
        raise


def delete_issue_files(issue):
    """删除指定 issue 的所有 .md 文件"""
    try:
        # 先尝试从元数据中查找
        metadata = load_metadata()
        issue_key = str(issue.number)

        if issue_key in metadata:
            info = metadata[issue_key]
            old_path = os.path.join(POSTS_DIR, info["label"], f"{info['filename']}.md")
            if os.path.exists(old_path):
                os.remove(old_path)
                logger.info(f"删除旧issue文件: {old_path}")

        # 遍历所有目录确保清理干净（处理元数据丢失的情况）
        for root, dirs, files in os.walk(POSTS_DIR):
            for f in files:
                if f.endswith('.md'):
                    filepath = os.path.join(root, f)
                    try:
                        with open(filepath, "r", encoding="utf-8") as fh:
                            first_line = fh.readline()
                            # 通过文件名中的标题匹配（标题已 sanitize）
                            safe_title = sanitize_filename(issue.title)
                            if safe_title in f:
                                os.remove(filepath)
                                logger.info(f"删除旧issue文件(遍历): {filepath}")
                    except Exception:
                        pass

        # 从元数据中移除
        if issue_key in metadata:
            del metadata[issue_key]
            save_metadata(metadata)

        logger.info(f"Issue #{issue.number} 的文件已清理")
    except Exception as e:
        logger.error(f"删除issue文件失败 #{issue.number}: {str(e)}")


def cleanup_empty_dirs():
    """清理 posts/ 下的空目录"""
    try:
        for root, dirs, files in os.walk(POSTS_DIR, topdown=False):
            if root == POSTS_DIR:
                continue
            if not os.listdir(root):
                os.rmdir(root)
                logger.info(f"删除空目录: {root}")
    except Exception as e:
        logger.error(f"清理空目录失败: {str(e)}")


def main():
    """主入口：生成 .md 文件"""
    import argparse

    parser = argparse.ArgumentParser(description="从 GitHub Issues 生成 .md 文件")
    parser.add_argument("token", help="GitHub Personal Access Token")
    parser.add_argument("repo_name", help="仓库名称 (owner/repo)")
    parser.add_argument("--issue_number", type=int, default=None, help="指定 issue 编号")
    args = parser.parse_args()

    logger.info("=" * 50)
    logger.info("开始生成 issue .md 文件")

    # 登录
    user = login(args.token)
    me = get_me(user)
    logger.info(f"登录成功: {me}")

    # 获取仓库
    repo = get_repo(user, args.repo_name)

    # 处理指定 issue（关闭的 issue 执行删除）
    if args.issue_number:
        try:
            issue = repo.get_issue(args.issue_number)
            if issue.state == "closed":
                logger.info(f"Issue #{args.issue_number} 已关闭，删除文件")
                delete_issue_files(issue)
                cleanup_empty_dirs()
                return
        except Exception as e:
            logger.error(f"获取 issue #{args.issue_number} 失败: {str(e)}")

    # 获取需要生成的 issues
    issues = get_to_generate_issues(repo, me, args.issue_number)
    logger.info(f"需要处理 {len(issues)} 个 issue")

    if not issues:
        logger.info("没有需要处理的 issue")
        return

    # 生成 .md 文件
    for issue in issues:
        if not is_me(issue, me):
            logger.debug(f"跳过非自己的 issue: #{issue.number}")
            continue
        try:
            save_issue(issue, me)
        except Exception as e:
            logger.error(f"处理 issue #{issue.number} 失败: {str(e)}")

    cleanup_empty_dirs()
    logger.info("issue .md 文件生成完成")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()