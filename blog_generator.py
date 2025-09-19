import argparse
import os
import re
import sys
import traceback
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

import markdown
from feedgen.feed import FeedGenerator
from github import Github
from lxml.etree import CDATA
from marko.ext.gfm import gfm as marko

# 配置常量
MD_HEAD = """## [Gitblog](https://github.com/bingdu748/c_d-project)
My personal blog using issues and GitHub Actions (随意转载，无需署名)
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

class BlogGenerator:
    """博客生成器类，封装所有功能"""
    def __init__(self, token, repo_name, issue_number=None, dir_name=BACKUP_DIR):
        self.token = token
        self.repo_name = repo_name
        self.issue_number = issue_number
        self.dir_name = dir_name
        self.user = None
        self.me = None
        self.repo = None
        
    def initialize(self):
        """初始化GitHub连接和仓库"""
        # 检查备份目录是否存在
        if not os.path.exists(self.dir_name):
            logger.info(f"创建备份目录: {self.dir_name}")
            os.makedirs(self.dir_name)
            
        # 登录GitHub
        logger.info("正在登录GitHub...")
        self.user = self.login(self.token)
        self.me = self.get_me(self.user)
        logger.info(f"登录成功，用户: {self.me}")
        
        # 获取仓库
        logger.info(f"正在获取仓库: {self.repo_name}")
        self.repo = self.get_repo(self.user, self.repo_name)
        logger.info(f"获取仓库成功: {self.repo.full_name}")
        
    @staticmethod
    def login(token):
        """登录GitHub"""
        return Github(token)
        
    @staticmethod
    def get_me(user):
        """获取当前用户信息"""
        return user.get_user().login
        
    @staticmethod
    def get_repo(user, repo):
        """获取仓库对象"""
        return user.get_repo(repo)
        
    @staticmethod
    def is_me(issue, me):
        """判断issue是否属于当前用户"""
        return issue.user.login == me
        
    @staticmethod
    def is_hearted_by_me(comment, me):
        """判断评论是否被当前用户点赞"""
        reactions = list(comment.get_reactions())
        for r in reactions:
            if r.content == "heart" and r.user.login == me:
                return True
        return False
        
    @staticmethod
    def _valid_xml_char_ordinal(c):
        """检查字符是否为有效的XML字符"""
        codepoint = ord(c)
        return (
            0x20 <= codepoint <= 0xD7FF
            or codepoint in (0x9, 0xA, 0xD)
            or 0xE000 <= codepoint <= 0xFFFD
            or 0x10000 <= codepoint <= 0x10FFFF
        )
        
    @staticmethod
    def format_time(time):
        """格式化时间"""
        return str(time)[:10]
        
    def parse_TODO(self, issue):
        """解析TODO类型的issue"""
        body = issue.body.splitlines()
        todo_undone = [l for l in body if l.startswith("- [ ] ")]
        todo_done = [l for l in body if l.startswith("- [x] ")]
        # 全部完成的情况
        if not todo_undone:
            return f"[{issue.title}]({issue.html_url}) all done", []
        return (
            f"[{issue.title}]({issue.html_url})--{len(todo_undone)} jobs to do--{len(todo_done)} jobs done",
            todo_done + todo_undone,
        )
        
    def get_top_issues(self):
        """获取置顶issue"""
        return self.repo.get_issues(labels=TOP_ISSUES_LABELS)
        
    def get_todo_issues(self):
        """获取TODO类型的issue"""
        return self.repo.get_issues(labels=TODO_ISSUES_LABELS)
        
    def get_repo_labels(self):
        """获取仓库所有标签"""
        return [l for l in self.repo.get_labels()]
        
    def get_issues_from_label(self, label):
        """获取特定标签的issue"""
        return self.repo.get_issues(labels=(label,))
        
    def add_issue_info(self, issue, md_file):
        """添加issue信息到Markdown文件"""
        time = self.format_time(issue.updated_at)  # 使用更新时间而不是创建时间
        
        # 添加issue标题和链接
        md_file.write(f"- [{issue.title}]({issue.html_url})--{time}\n")
        
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
                    md_file.write(f"  - {line}\n")
                md_file.write("\n")  # 添加空行分隔
        
    def add_md_todo(self, md_filename):
        """添加TODO部分到Markdown文件"""
        todo_issues = list(self.get_todo_issues())
        if not TODO_ISSUES_LABELS or not todo_issues:
            return
        # 按更新时间排序
        todo_issues = sorted(todo_issues, key=lambda x: x.updated_at, reverse=True)
        with open(md_filename, "a+", encoding="utf-8") as md:
            md.write("## TODO\n")
            for issue in todo_issues:
                if self.is_me(issue, self.me):
                    todo_title, todo_list = self.parse_TODO(issue)
                    md.write("TODO list from " + todo_title + "\n")
                    for t in todo_list:
                        md.write(t + "\n")
                    # new line
                    md.write("\n")
        
    def add_md_top(self, md_filename):
        """添加置顶文章到Markdown文件"""
        top_issues = list(self.get_top_issues())
        if not TOP_ISSUES_LABELS or not top_issues:
            return
        # 按更新时间排序
        top_issues = sorted(top_issues, key=lambda x: x.updated_at, reverse=True)
        with open(md_filename, "a+", encoding="utf-8") as md:
            md.write("## 置顶文章\n")
            for issue in top_issues:
                if self.is_me(issue, self.me):
                    self.add_issue_info(issue, md)
        
    def _make_friend_table_string(self, s):
        """生成友情链接表格字符串"""
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
            print(str(e))
            return
        
    def add_md_firends(self, md_filename):
        """添加友情链接到Markdown文件"""
        s = FRIENDS_TABLE_HEAD
        friends_issues = list(self.repo.get_issues(labels=FRIENDS_LABELS))
        if not FRIENDS_LABELS or not friends_issues:
            return
        friends_issue_number = friends_issues[0].number
        for issue in friends_issues:
            for comment in issue.get_comments():
                if self.is_hearted_by_me(comment, self.me):
                    try:
                        s += self._make_friend_table_string(comment.body or "")
                    except Exception as e:
                        print(str(e))
                        pass
        s = markdown.markdown(s, output_format="html", extensions=["extra"])
        with open(md_filename, "a+", encoding="utf-8") as md:
            md.write(
                f"## [友情链接](https://github.com/{str(self.me)}/gitblog/issues/{friends_issue_number})\n"
            )
            md.write("<details><summary>显示</summary>\n")
            md.write(s)
            md.write("</details>\n")
            md.write("\n\n")
        
    def add_md_recent(self, md_filename, limit=RECENT_ISSUE_LIMIT):
        """添加最近更新到Markdown文件"""
        count = 0
        with open(md_filename, "a+", encoding="utf-8") as md:
            # one the issue that only one issue and delete (pyGitHub raise an exception)
            try:
                md.write("## 最近更新\n")
                # 按更新时间排序，确保最新更新的issue在最前面
                all_issues = sorted(self.repo.get_issues(), key=lambda x: x.updated_at, reverse=True)
                for issue in all_issues:
                    if self.is_me(issue, self.me):
                        self.add_issue_info(issue, md)
                        count += 1
                        if count >= limit:
                            break
            except Exception as e:
                print(str(e))
        
    def add_md_header(self, md_filename):
        """添加Markdown文件头部"""
        # 获取当前时间作为更新时间戳
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(md_filename, "w", encoding="utf-8") as md:
            md.write(MD_HEAD.format(repo_name=self.repo_name))
            # 添加最后更新时间
            md.write(f"**最后更新时间**: {current_time}\n\n")
        
    def add_md_label(self, md_filename):
        """添加标签分类的issue到Markdown文件"""
        labels = self.get_repo_labels()
        
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
        
        with open(md_filename, "a+", encoding="utf-8") as md:
            for label in labels:
                # we don't need add top label again
                if label.name in IGNORE_LABELS:
                    continue
                
                issues = self.get_issues_from_label(label)
                if issues.totalCount:
                    md.write("## " + label.name + "\n")
                    # 按更新时间排序，确保最新更新的issue在最前面
                    issues = sorted(issues, key=lambda x: x.updated_at, reverse=True)
                i = 0
                for issue in issues:
                    if not issue:
                        continue
                    if self.is_me(issue, self.me):
                        if i == ANCHOR_NUMBER:
                            md.write("<details><summary>显示更多</summary>\n")
                            md.write("\n")
                        self.add_issue_info(issue, md)
                        i += 1
                if i > ANCHOR_NUMBER:
                    md.write("</details>\n")
                    md.write("\n")
        
    def get_to_generate_issues(self):
        """获取需要生成的issue列表"""
        # 首先获取所有issue
        all_issues = list(self.repo.get_issues())
        
        # 如果提供了issue_number，只处理指定的issue
        if self.issue_number:
            logger.info(f"指定了issue_number: {self.issue_number}，将只处理该issue")
            try:
                target_issue = self.repo.get_issue(int(self.issue_number))
                return [target_issue]
            except Exception as e:
                logger.error(f"获取指定issue失败: {str(e)}")
                return []
        
        # 如果没有提供issue_number，处理所有issue
        logger.info(f"未指定issue_number，将处理所有issue")
        return all_issues
        
    def generate_rss_feed(self, filename="feed.xml"):
        """生成RSS feed"""
        generator = FeedGenerator()
        generator.id(self.repo.html_url)
        generator.title(f"RSS feed of {self.repo.owner.login}'s {self.repo.name}")
        generator.author(
            {"name": os.getenv("GITHUB_NAME"), "email": os.getenv("GITHUB_EMAIL")}
        )
        generator.link(href=self.repo.html_url)
        generator.link(
            href=f"https://raw.githubusercontent.com/{self.repo.full_name}/master/{filename}",
            rel="self",
        )
        # 按更新时间排序
        sorted_issues = sorted(self.repo.get_issues(), key=lambda x: x.updated_at, reverse=True)
        for issue in sorted_issues:
            if not issue.body or not self.is_me(issue, self.me) or issue.pull_request:
                continue
            item = generator.add_entry(order="append")
            item.id(issue.html_url)
            item.link(href=issue.html_url)
            item.title(issue.title)
            item.published(issue.created_at.strftime("%Y-%m-%dT%H:%M:%SZ"))
            for label in issue.labels:
                item.category({"term": label.name})
            body = "".join(c for c in issue.body if self._valid_xml_char_ordinal(c))
            item.content(CDATA(marko.convert(body)), type="html")
        generator.atom_file(filename)
        
    def save_issue(self, issue):
        """保存issue到本地文件"""
        # 生成文件名，替换可能导致问题的字符
        safe_title = issue.title.replace('/', '-').replace(' ', '.').replace('\\', '-')
        md_name = os.path.join(self.dir_name, f"{issue.number}_{safe_title}.md")
        
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
                        if self.is_me(c, self.me):
                            comment_time = self.format_time(c.created_at)
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
            
    def run(self):
        """运行博客生成器"""
        try:
            # 初始化
            self.initialize()
            
            # 添加README头部
            logger.info("正在生成README.md头部...")
            self.add_md_header("README.md")
            
            # 添加各个部分
            functions = [self.add_md_firends, self.add_md_top, self.add_md_recent, self.add_md_label, self.add_md_todo]
            for func in functions:
                # 安全地获取函数名称
                func_name = getattr(func, "__name__", str(func))
                logger.info(f"正在执行: {func_name}")
                func("README.md")
            
            # 生成RSS feed
            logger.info("正在生成RSS feed...")
            self.generate_rss_feed("feed.xml")
            
            # 处理issue_number
            logger.info(f"处理issue_number: {self.issue_number}")
            if self.issue_number == '':
                self.issue_number = None
                logger.info("issue_number为空字符串，已设置为None")
            
            # 获取待生成的issues
            logger.info("获取待生成的issues...")
            to_generate_issues = self.get_to_generate_issues()
            logger.info(f"找到{len(to_generate_issues)}个待生成的issue")
            
            # 保存issue到备份文件夹
            logger.info("开始保存issue到备份文件夹...")
            for issue in to_generate_issues:
                logger.info(f"保存issue: #{issue.number} - {issue.title}")
                self.save_issue(issue)
            
            logger.info("博客生成器执行完成")
            
        except Exception as e:
            logger.error(f"执行过程中发生错误: {str(e)}")
            logger.error(traceback.format_exc())
            # 重新抛出异常，以便GitHub Actions能够捕获到错误
            raise


# 命令行入口
if __name__ == "__main__":
    try:
        # 确保BACKUP_DIR存在
        if not os.path.exists(BACKUP_DIR):
            logger.info(f"创建备份目录: {BACKUP_DIR}")
            os.makedirs(BACKUP_DIR)
            
        # 解析命令行参数
        parser = argparse.ArgumentParser(description='GitBlog生成器 - 基于GitHub Issues的博客系统')
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
        
        # 创建博客生成器并运行
        blog_generator = BlogGenerator(options.github_token, options.repo_name, options.issue_number, options.dir_name)
        blog_generator.run()
        
    except argparse.ArgumentError as e:
        logger.error(f"参数解析错误: {str(e)}")
        parser.print_help()
        sys.exit(1)
    except Exception as e:
        logger.error(f"程序执行失败: {str(e)}")
        logger.error(traceback.format_exc())
        sys.exit(1)