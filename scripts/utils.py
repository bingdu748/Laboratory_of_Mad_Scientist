# -*- coding: utf-8 -*-
"""
公共工具模块
认证、时间格式化、字数统计、图片统计
"""

import os
import re
import sys
import json
import logging
from datetime import datetime, timedelta, timezone

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
POSTS_DIR = "posts"
RECENT_ISSUE_LIMIT = 20
METADATA_FILE = ".temp_metadata.json"

# 北京时区
BEIJING_TZ = timezone(timedelta(hours=8))


def get_me(user):
    """获取当前用户信息"""
    try:
        if os.getenv("GITHUB_ACTIONS") == "true":
            repo_name = os.getenv("GITHUB_REPOSITORY", "")
            if repo_name and '/' in repo_name:
                owner = repo_name.split('/')[0]
                logger.info(f"在GitHub Actions环境中，使用仓库所有者作为用户名: {owner}")
                return owner
            logger.info("在GitHub Actions环境中，使用默认用户名")
            return "github-actions"
        return user.get_user().login
    except Exception as e:
        logger.warning(f"获取当前用户信息失败，使用默认值: {str(e)}")
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
        try:
            import github.Auth
            auth = github.Auth.Token(token)
            return github.Github(auth=auth)
        except ImportError:
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
    """格式化时间为北京时间 (UTC+8)"""
    try:
        if not hasattr(time_obj, 'strftime'):
            return "未知时间"
        if time_obj.tzinfo is None:
            time_obj = time_obj.replace(tzinfo=timezone.utc)
        local_time = time_obj.astimezone(BEIJING_TZ)
        return local_time.strftime("%Y-%m-%d %H:%M")
    except Exception as e:
        logger.error(f"格式化时间失败: {str(e)}")
        return "时间格式化失败"


def get_issue_word_count(issue):
    """获取issue的字数统计（去掉markdown语法后真正显示的字符数）"""
    try:
        body = issue.body or ""

        # 移除 HTML 注释
        body = re.sub(r'<!--.*?-->', '', body, flags=re.DOTALL)
        # 移除代码块
        body = re.sub(r'```.*?```', '', body, flags=re.DOTALL)
        body = re.sub(r'~~~.*?~~~', '', body, flags=re.DOTALL)
        # 移除行内代码
        body = re.sub(r'`[^`]*`', '', body)
        # 移除图片（在移除链接之前处理）
        body = re.sub(r'!\[[^\]]*\]\([^)]+\)', '', body)
        # 移除链接语法，保留链接文本 [text](url) -> text
        body = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', body)
        # 移除 HTML 标签
        body = re.sub(r'<[^>]+>', '', body)
        # 移除 URL（裸链接）
        body = re.sub(r'https?://\S+', '', body)
        # 移除表格分隔线
        body = re.sub(r'^\s*\|?[-:| ]+\|?\s*$', '', body, flags=re.MULTILINE)
        # 移除引用标记、列表标记
        body = re.sub(r'^\s*[>\-*+]\s+', '', body, flags=re.MULTILINE)
        # 移除标题标记
        body = re.sub(r'^#{1,6}\s+', '', body, flags=re.MULTILINE)
        # 移除水平分隔线
        body = re.sub(r'^[-*_]{3,}\s*$', '', body, flags=re.MULTILINE)
        # 移除加粗/斜体标记
        body = re.sub(r'\*\*([^*]+)\*\*', r'\1', body)
        body = re.sub(r'__([^_]+)__', r'\1', body)
        body = re.sub(r'\*([^*]+)\*', r'\1', body)
        body = re.sub(r'_([^_]+)_', r'\1', body)
        # 移除删除线
        body = re.sub(r'~~([^~]+)~~', r'\1', body)
        # 移除表格管道符和多余的空白
        body = re.sub(r'\|', ' ', body)
        # 移除反斜杠转义
        body = re.sub(r'\\(.)', r'\1', body)
        # 合并多余的空白
        body = re.sub(r'\s+', ' ', body).strip()

        # 统计中文字符（包括中文标点）
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]', body))
        # 统计英文单词
        english_words = len(re.findall(r'\b[a-zA-Z]+\b', body))
        # 统计数字（独立数字也算作一个"字"）
        numbers = len(re.findall(r'\b\d+\b', body))

        return chinese_chars + english_words + numbers
    except Exception as e:
        logger.error(f"获取issue字数失败 #{issue.number}: {str(e)}")
        return 0


def get_issue_image_count(issue):
    """获取issue中的图片数量"""
    try:
        body = issue.body or ""
        md_images = len(re.findall(r'!\[[^\]]*\]\([^)]+\)', body))
        html_images = len(re.findall(r'<img[^>]+src=["\'][^"\']+["\']', body, re.IGNORECASE))
        return md_images + html_images
    except Exception as e:
        logger.error(f"获取issue图片数量失败 #{issue.number}: {str(e)}")
        return 0


def load_metadata():
    """加载元数据文件，返回 issue_number -> metadata 的字典"""
    if not os.path.exists(METADATA_FILE):
        return {}
    try:
        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"加载元数据失败: {str(e)}")
        return {}


def save_metadata(metadata):
    """保存元数据到文件"""
    try:
        with open(METADATA_FILE, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"保存元数据失败: {str(e)}")