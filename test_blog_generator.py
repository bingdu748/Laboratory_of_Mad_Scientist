import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入需要测试的模块
from blog_generator import BlogGenerator

class TestBlogGenerator(unittest.TestCase):
    
    def setUp(self):
        # 设置测试环境
        self.token = "test_token"
        self.repo_name = "test_user/test_repo"
        self.issue_number = "1"
        self.dir_name = "TEST_BACKUP"
        
        # 创建博客生成器实例
        self.blog_generator = BlogGenerator(self.token, self.repo_name, self.issue_number, self.dir_name)
        
    @patch('blog_generator.Github')
    def test_login(self, mock_github):
        """测试登录功能"""
        # 模拟GitHub登录
        mock_user = MagicMock()
        mock_github.return_value = mock_user
        
        # 调用login方法
        result = self.blog_generator.login(self.token)
        
        # 验证GitHub是否被正确调用
        mock_github.assert_called_once_with(self.token)
        self.assertEqual(result, mock_user)
        
    @patch('blog_generator.Github')
    def test_get_me(self, mock_github):
        """测试获取当前用户信息"""
        # 模拟GitHub用户
        mock_user_instance = MagicMock()
        mock_user_instance.login = "test_user"
        
        mock_user = MagicMock()
        mock_user.get_user.return_value = mock_user_instance
        mock_github.return_value = mock_user
        
        # 调用get_me方法
        result = self.blog_generator.get_me(mock_user)
        
        # 验证结果
        self.assertEqual(result, "test_user")
        mock_user.get_user.assert_called_once()
        
    @patch('blog_generator.Github')
    def test_get_repo(self, mock_github):
        """测试获取仓库信息"""
        # 模拟GitHub仓库
        mock_repo = MagicMock()
        
        mock_user = MagicMock()
        mock_user.get_repo.return_value = mock_repo
        mock_github.return_value = mock_user
        
        # 调用get_repo方法
        result = self.blog_generator.get_repo(mock_user, self.repo_name)
        
        # 验证结果
        self.assertEqual(result, mock_repo)
        mock_user.get_repo.assert_called_once_with(self.repo_name)
        
    def test_format_time(self):
        """测试时间格式化功能"""
        # 模拟时间对象
        class MockTime:
            def __str__(self):
                return "2024-01-01T12:00:00Z"
        
        # 调用format_time方法
        result = self.blog_generator.format_time(MockTime())
        
        # 验证结果
        self.assertEqual(result, "2024-01-01")
        
    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_initialize(self, mock_makedirs, mock_exists):
        """测试初始化功能"""
        # 模拟目录不存在
        mock_exists.return_value = False
        
        # 模拟GitHub登录和仓库获取
        with patch('blog_generator.BlogGenerator.login') as mock_login, \
             patch('blog_generator.BlogGenerator.get_me') as mock_get_me, \
             patch('blog_generator.BlogGenerator.get_repo') as mock_get_repo:
            
            # 设置模拟返回值
            mock_user = MagicMock()
            mock_login.return_value = mock_user
            mock_get_me.return_value = "test_user"
            
            mock_repo = MagicMock()
            mock_repo.full_name = self.repo_name
            mock_get_repo.return_value = mock_repo
            
            # 调用initialize方法
            self.blog_generator.initialize()
            
            # 验证方法调用
            mock_exists.assert_called_once_with(self.dir_name)
            mock_makedirs.assert_called_once_with(self.dir_name)
            mock_login.assert_called_once_with(self.token)
            mock_get_me.assert_called_once_with(mock_user)
            mock_get_repo.assert_called_once_with(mock_user, self.repo_name)
            
            # 验证实例变量设置
            self.assertEqual(self.blog_generator.user, mock_user)
            self.assertEqual(self.blog_generator.me, "test_user")
            self.assertEqual(self.blog_generator.repo, mock_repo)
            
    def tearDown(self):
        # 清理测试环境
        if os.path.exists(self.dir_name):
            import shutil
            shutil.rmtree(self.dir_name)


if __name__ == "__main__":
    unittest.main()