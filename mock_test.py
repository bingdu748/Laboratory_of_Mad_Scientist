import unittest
from unittest.mock import patch, MagicMock, mock_open
import sys
import os

# 确保我们可以导入main模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入main模块中的函数
from main import main, add_md_header, add_md_recent, generate_rss_feed, get_to_generate_issues, save_issue

class MockTest(unittest.TestCase):
    @patch('main.login')
    @patch('main.get_me')
    @patch('main.get_repo')
    @patch('builtins.open', new_callable=mock_open)
    @patch('main.add_md_header')
    @patch('main.add_md_firends')
    @patch('main.add_md_top')
    @patch('main.add_md_recent')
    @patch('main.add_md_label')
    @patch('main.add_md_todo')
    @patch('main.generate_rss_feed')
    @patch('main.get_to_generate_issues')
    @patch('main.save_issue')
    def test_main_function(self, mock_save_issue, mock_get_to_generate_issues, 
                          mock_generate_rss_feed, mock_add_md_todo, mock_add_md_label, 
                          mock_add_md_recent, mock_add_md_top, mock_add_md_firends, 
                          mock_add_md_header, mock_open_file, mock_get_repo, 
                          mock_get_me, mock_login):
        """测试main函数的基本流程"""
        # 设置模拟对象
        mock_user = MagicMock()
        mock_login.return_value = mock_user
        mock_get_me.return_value = "test_user"
        mock_repo = MagicMock()
        mock_get_repo.return_value = mock_repo
        
        # 模拟get_to_generate_issues返回空列表
        mock_get_to_generate_issues.return_value = []
        
        # 调用main函数
        main("mock_token", "owner/repo", None, "BACKUP")
        
        # 验证函数调用
        mock_login.assert_called_once_with("mock_token")
        mock_get_me.assert_called_once_with(mock_user)
        mock_get_repo.assert_called_once_with(mock_user, "owner/repo")
        mock_add_md_header.assert_called_once()
        mock_generate_rss_feed.assert_called_once()
        mock_get_to_generate_issues.assert_called_once()
        
    @patch('builtins.open', new_callable=mock_open)
    def test_add_md_header(self, mock_open_file):
        """测试add_md_header函数"""
        add_md_header("README.md", "owner/repo")
        mock_open_file.assert_called_once_with("README.md", "w", encoding="utf-8")
        mock_open_file().write.assert_called()

# 如果直接运行此脚本，则执行测试
if __name__ == '__main__':
    unittest.main()