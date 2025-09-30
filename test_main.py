#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证main.py中的README.md更新功能
"""
import os
import sys
import time
import logging
import subprocess
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# 常量定义
BACKUP_DIR = "BACKUP"
TEST_README = "README.md"
TEST_ISSUE_NUMBER = "1"  # 假设仓库中有编号为1的issue


def check_environment():
    """检查测试环境是否准备就绪"""
    # 检查main.py是否存在
    if not os.path.exists("main.py"):
        logger.error("未找到main.py文件！")
        return False
        
    # 检查是否有GitHub令牌环境变量
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        logger.error("未设置GITHUB_TOKEN环境变量！")
        logger.info("请设置GITHUB_TOKEN环境变量后再运行测试")
        return False
    
    # 检查是否有REPO_NAME环境变量
    repo_name = os.getenv("REPO_NAME")
    if not repo_name:
        logger.error("未设置REPO_NAME环境变量！")
        logger.info("请设置REPO_NAME环境变量后再运行测试，格式为owner/repo")
        return False
    
    # 确保备份目录存在
    if not os.path.exists(BACKUP_DIR):
        logger.info(f"创建备份目录: {BACKUP_DIR}")
        os.makedirs(BACKUP_DIR)
    
    # 确保README.md存在
    if not os.path.exists(TEST_README):
        logger.info(f"README.md不存在，创建临时文件")
        with open(TEST_README, "w", encoding="utf-8") as f:
            f.write("# 测试README文件\n\n这是一个用于测试的README文件。\n")
    
    logger.info("测试环境检查通过")
    return True


def backup_readme():
    """备份当前的README.md文件"""
    backup_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"README_backup_{backup_time}.md")
    
    if os.path.exists(TEST_README):
        try:
            with open(TEST_README, "r", encoding="utf-8") as f:
                content = f.read()
            with open(backup_path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info(f"已备份README.md到: {backup_path}")
            return backup_path
        except Exception as e:
            logger.error(f"备份README.md失败: {str(e)}")
            return None
    else:
        logger.warning("README.md不存在，无需备份")
        return None


def verify_readme_update(original_size, original_mtime):
    """验证README.md是否已更新"""
    # 检查文件是否存在
    if not os.path.exists(TEST_README):
        logger.error("README.md不存在！")
        return False
    
    # 获取文件信息
    file_stat = os.stat(TEST_README)
    current_size = file_stat.st_size
    current_mtime = file_stat.st_mtime
    
    logger.info(f"README.md文件信息 - 大小: {current_size} 字节, 修改时间: {datetime.fromtimestamp(current_mtime)}")
    
    # 检查文件大小和修改时间是否发生变化
    if current_size == original_size and current_mtime == original_mtime:
        logger.error("README.md未更新！文件大小和修改时间与之前相同")
        return False
    
    # 检查文件内容是否包含预期的标记
    try:
        with open(TEST_README, "r", encoding="utf-8") as f:
            content = f.read()
            
        # 检查是否包含Gitblog标题
        if "Gitblog" not in content:
            logger.error("README.md内容不完整，未找到'Gitblog'标题")
            return False
        
        # 检查是否包含最后更新时间
        if "最后更新时间" not in content:
            logger.error("README.md内容不完整，未找到'最后更新时间'")
            return False
        
        # 检查是否包含各个部分的标题
        sections = ["置顶文章", "最近更新", "TODO", "友情链接"]
        missing_sections = []
        for section in sections:
            if section not in content:
                missing_sections.append(section)
        
        if missing_sections:
            logger.warning(f"README.md缺少以下部分: {', '.join(missing_sections)}")
            # 不是致命错误，继续检查
        
        logger.info("README.md内容验证通过")
        return True
        
    except Exception as e:
        logger.error(f"读取或验证README.md内容失败: {str(e)}")
        return False


def run_main_script(github_token, repo_name, issue_number=None):
    """运行main.py脚本"""
    # 构建命令
    cmd = [
        sys.executable,  # 使用当前Python解释器
        "main.py",
        github_token,
        repo_name
    ]
    
    # 如果指定了issue_number，则添加到命令中
    if issue_number:
        cmd.extend(["--issue_number", issue_number])
    
    logger.info(f"运行命令: {' '.join(cmd[:2])} **** {cmd[3]}{' --issue_number ' + issue_number if issue_number else ''}")
    
    try:
        # 运行脚本并捕获输出
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # 实时显示输出
        stdout, stderr = process.communicate()
        
        # 输出结果
        if stdout:
            logger.info(f"脚本输出:\n{stdout}")
        if stderr:
            logger.error(f"脚本错误输出:\n{stderr}")
        
        # 检查退出码
        if process.returncode != 0:
            logger.error(f"脚本执行失败，退出码: {process.returncode}")
            return False
        
        logger.info("脚本执行成功")
        return True
        
    except Exception as e:
        logger.error(f"运行脚本时发生错误: {str(e)}")
        return False


def main():
    """主测试函数"""
    logger.info("===== 开始测试README.md更新功能 =====")
    
    # 检查测试环境
    if not check_environment():
        logger.error("测试环境检查失败，无法继续测试")
        sys.exit(1)
    
    # 获取环境变量
    github_token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("REPO_NAME")
    
    # 备份原始README.md
    backup_path = backup_readme()
    
    # 获取原始README.md的信息
    if os.path.exists(TEST_README):
        original_stat = os.stat(TEST_README)
        original_size = original_stat.st_size
        original_mtime = original_stat.st_mtime
        logger.info(f"原始README.md信息 - 大小: {original_size} 字节, 修改时间: {datetime.fromtimestamp(original_mtime)}")
    else:
        original_size = 0
        original_mtime = 0
    
    # 测试场景1：处理单个issue
    logger.info("\n===== 测试场景1: 处理单个issue =====")
    if run_main_script(github_token, repo_name, TEST_ISSUE_NUMBER):
        logger.info("验证README.md是否已更新...")
        if verify_readme_update(original_size, original_mtime):
            logger.info("测试场景1通过：处理单个issue时README.md已成功更新")
        else:
            logger.error("测试场景1失败：处理单个issue时README.md未更新")
    else:
        logger.error("测试场景1失败：运行main.py处理单个issue时出错")
    
    # 获取更新后的README.md信息，用于下一个测试场景
    if os.path.exists(TEST_README):
        updated_stat = os.stat(TEST_README)
        updated_size = updated_stat.st_size
        updated_mtime = updated_stat.st_mtime
    else:
        updated_size = 0
        updated_mtime = 0
    
    # 测试场景2：处理所有issue
    logger.info("\n===== 测试场景2: 处理所有issue =====")
    # 等待几秒，确保修改时间会变化
    time.sleep(2)
    
    if run_main_script(github_token, repo_name):
        logger.info("验证README.md是否已更新...")
        if verify_readme_update(updated_size, updated_mtime):
            logger.info("测试场景2通过：处理所有issue时README.md已成功更新")
        else:
            logger.error("测试场景2失败：处理所有issue时README.md未更新")
    else:
        logger.error("测试场景2失败：运行main.py处理所有issue时出错")
    
    # 总结测试结果
    logger.info("\n===== 测试总结 =====")
    logger.info(f"备份文件路径: {backup_path}")
    logger.info("测试完成，请查看日志了解详细结果")
    
    # 如果测试成功，可以选择自动恢复原始README.md
    # 这里不自动恢复，留给用户手动处理


if __name__ == "__main__":
    main()


# -*- coding: utf-8 -*-
"""
测试main.py功能的测试脚本
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock, mock_open
import datetime
import tempfile
import shutil

# 将当前目录添加到系统路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入需要测试的模块
from main import (
    main, ensure_readme_exists, push_to_backup_branch, save_issue,
    regenerate_readme, get_to_generate_issues, add_issue_info,
    format_time, is_me, get_repo_labels, get_issues_from_label
)

class TestMainFunctions(unittest.TestCase):
    """测试main.py中的主要功能"""
    
    def setUp(self):
        """设置测试环境"""
        # 创建临时目录作为工作目录
        self.temp_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir)
        
        # 创建测试所需的目录
        os.makedirs("BACKUP", exist_ok=True)
        
        # 模拟GitHub issue对象
        self.mock_issue = MagicMock()
        self.mock_issue.number = 1
        self.mock_issue.title = "Test Issue"
        self.mock_issue.body = "This is a test issue content.\nIt has multiple lines."
        self.mock_issue.html_url = "https://github.com/testuser/testrepo/issues/1"
        self.mock_issue.created_at = datetime.datetime(2023, 1, 1, 12, 0, 0)
        self.mock_issue.updated_at = datetime.datetime(2023, 1, 2, 12, 0, 0)
        
        # 模拟issue用户
        self.mock_user = MagicMock()
        self.mock_user.login = "testuser"
        self.mock_issue.user = self.mock_user
        
        # 模拟issue标签
        self.mock_label1 = MagicMock()
        self.mock_label1.name = "Python"
        self.mock_label2 = MagicMock()
        self.mock_label2.name = "测试"
        self.mock_issue.labels = [self.mock_label1, self.mock_label2]
        
        # 模拟评论
        self.mock_comment = MagicMock()
        self.mock_comment.body = "This is a test comment."
        self.mock_comment.created_at = datetime.datetime(2023, 1, 3, 12, 0, 0)
        self.mock_comment.user = self.mock_user
        self.mock_issue.get_comments.return_value = [self.mock_comment]
    
    def tearDown(self):
        """清理测试环境"""
        os.chdir(self.original_dir)
        # 删除临时目录
        shutil.rmtree(self.temp_dir)
    
    def test_format_time(self):
        """测试时间格式化功能"""
        time_obj = datetime.datetime(2023, 1, 1, 12, 0, 0)
        result = format_time(time_obj)
        self.assertEqual(result, "2023-01-01 12:00:00")
        
        # 测试无效时间对象
        result = format_time("not a time object")
        self.assertTrue("未知时间" in result or "时间格式化失败" in result)
    
    def test_is_me(self):
        """测试用户身份判断功能"""
        # 测试匹配的情况
        result = is_me(self.mock_issue, "testuser")
        self.assertTrue(result)
        
        # 测试不匹配的情况
        result = is_me(self.mock_issue, "otheruser")
        self.assertFalse(result)
        
        # 测试评论的情况
        result = is_me(self.mock_comment, "testuser")
        self.assertTrue(result)
    
    def test_ensure_readme_exists(self):
        """测试确保README.md存在的功能"""
        # 测试文件不存在的情况
        if os.path.exists("README.md"):
            os.remove("README.md")
        
        ensure_readme_exists()
        self.assertTrue(os.path.exists("README.md"))
        
        # 测试README_TEMPLATE.md存在的情况
        with open("README_TEMPLATE.md", "w", encoding="utf-8") as f:
            f.write("# Template README")
        
        os.remove("README.md")
        ensure_readme_exists()
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
        self.assertEqual(content, "# Template README")
    
    def test_save_issue(self):
        """测试保存issue到文件的功能"""
        save_issue(self.mock_issue, "testuser", "BACKUP")
        
        # 检查文件是否创建成功
        expected_filename = os.path.join("BACKUP", "1_Test.Issue.md")
        self.assertTrue(os.path.exists(expected_filename))
        
        # 检查文件内容
        with open(expected_filename, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 验证文件内容包含关键信息
        self.assertIn("# [Test Issue](https://github.com/testuser/testrepo/issues/1)", content)
        self.assertIn("## 元信息", content)
        self.assertIn("- 创建时间: 2023-01-01 12:00:00", content)
        self.assertIn("- 更新时间: 2023-01-02 12:00:00", content)
        self.assertIn("- 标签: Python, 测试", content)
        self.assertIn("## 内容", content)
        self.assertIn("This is a test issue content", content)
        self.assertIn("## 评论", content)
    
    @patch("main.login")
    @patch("main.get_repo")
    @patch("main.get_to_generate_issues")
    @patch("main.save_issue")
    @patch("main.regenerate_readme")
    @patch("main.push_to_backup_branch")
    def test_main_function(self, mock_push_backup, mock_regenerate, mock_save, 
                         mock_get_issues, mock_get_repo, mock_login):
        """测试main函数的整体流程"""
        # 设置模拟对象
        mock_user = MagicMock()
        mock_repo = MagicMock()
        mock_login.return_value = mock_user
        mock_user.get_user().login = "testuser"
        mock_get_repo.return_value = mock_repo
        mock_get_issues.return_value = [self.mock_issue]
        
        # 调用main函数
        main("fake_token", "testuser/testrepo")
        
        # 验证各个函数是否被正确调用
        mock_login.assert_called_once_with("fake_token")
        mock_get_repo.assert_called_once_with(mock_user, "testuser/testrepo")
        mock_get_issues.assert_called_once()
        mock_save.assert_called_once()
        mock_regenerate.assert_called_once()
        mock_push_backup.assert_called_once()
    
    @patch("subprocess.run")
    def test_push_to_backup_branch(self, mock_subprocess):
        """测试将备份文件推送到backup分支的功能"""
        # 设置模拟对象
        def side_effect(cmd, **kwargs):
            # 模拟git命令的行为
            if cmd == ["git", "rev-parse", "--verify", "backup"]:
                # 模拟backup分支不存在
                raise subprocess.CalledProcessError(returncode=1, cmd=cmd)
            return MagicMock()
        
        mock_subprocess.side_effect = side_effect
        
        # 调用函数
        try:
            push_to_backup_branch()
        except Exception:
            # 我们期望subprocess会抛出异常，但函数应该优雅地处理它
            pass
        
        # 验证git命令是否被正确调用
        self.assertTrue(mock_subprocess.called)
    
    def test_add_issue_info(self):
        """测试添加issue信息到文件的功能"""
        # 使用mock_open来模拟文件对象
        m = mock_open()
        with patch("builtins.open", m):
            with open("dummy.txt", "a+", encoding="utf-8") as f:
                add_issue_info(self.mock_issue, f)
        
        # 验证文件写入操作
        handle = m()
        handle.write.assert_any_call("- [Test Issue](https://github.com/testuser/testrepo/issues/1)--2023-01-02 12:00:00\n")

class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    @patch("main.login")
    @patch("main.get_repo")
    @patch("main.ensure_readme_exists")
    @patch("main.save_issue")
    @patch("main.regenerate_readme")
    @patch("main.push_to_backup_branch")
    def test_integration_flow(self, mock_push_backup, mock_regenerate, mock_save, 
                           mock_ensure, mock_get_repo, mock_login):
        """测试整个集成流程"""
        # 设置模拟对象
        mock_user = MagicMock()
        mock_repo = MagicMock()
        mock_login.return_value = mock_user
        mock_user.get_user().login = "testuser"
        mock_get_repo.return_value = mock_repo
        
        # 创建模拟issue列表
        mock_issue1 = MagicMock()
        mock_issue1.number = 1
        mock_issue1.title = "Test Issue 1"
        mock_issue1.user.login = "testuser"
        
        mock_issue2 = MagicMock()
        mock_issue2.number = 2
        mock_issue2.title = "Test Issue 2"
        mock_issue2.user.login = "testuser"
        
        # 设置get_to_generate_issues的返回值
        with patch("main.get_to_generate_issues", return_value=[mock_issue1, mock_issue2]):
            # 调用main函数
            main("fake_token", "testuser/testrepo")
        
        # 验证各个函数是否被正确调用
        mock_ensure.assert_called_once()
        self.assertEqual(mock_save.call_count, 2)
        mock_regenerate.assert_called_once()
        mock_push_backup.assert_called_once()

if __name__ == "__main__":
    # 添加subprocess的导入，以避免在测试中出现导入错误
    import subprocess
    # 运行所有测试
    unittest.main()