# -*- coding: utf-8 -*-
"""
单元测试：验证 issue 过滤逻辑
测试场景覆盖：
1. PR 应被正确识别并排除
2. closed 状态 issue 应被排除
3. 字数为 0 的 issue 应被排除
4. 图片数量异常的 issue 应被排除
5. 正常 open issue 应通过过滤
"""

import sys
import os
import unittest
from unittest.mock import MagicMock

# 确保可以导入 scripts 模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.utils import (
    is_pull_request,
    should_include_issue,
    _clean_markdown,
    _count_words,
    get_content_word_count,
    get_content_image_count,
)


def _make_mock_issue(number, title, state, body, pull_request=None, user_login="test_user"):
    """辅助函数：创建模拟的 GitHub Issue 对象"""
    issue = MagicMock()
    issue.number = number
    issue.title = title
    issue.state = state
    issue.body = body
    issue.user.login = user_login

    if pull_request is True:
        pr_mock = MagicMock()
        issue.pull_request = pr_mock
    elif pull_request is False:
        issue.pull_request = None
    # else: leave pull_request as MagicMock (will raise on is not None check)

    return issue


class TestIsPullRequest(unittest.TestCase):
    """测试 is_pull_request 函数"""

    def test_pull_request_detected(self):
        """有 pull_request 属性的对象应被识别为 PR"""
        issue = _make_mock_issue(12, "test", "open", "test body", pull_request=True)
        self.assertTrue(is_pull_request(issue))

    def test_regular_issue_not_pr(self):
        """无 pull_request 属性的对象不应被识别为 PR"""
        issue = _make_mock_issue(1, "test", "open", "test body", pull_request=False)
        self.assertFalse(is_pull_request(issue))

    def test_pull_request_none_attribute(self):
        """pull_request 为 None 时不应被识别为 PR"""
        issue = _make_mock_issue(1, "test", "open", "test body", pull_request=False)
        self.assertFalse(is_pull_request(issue))

    def test_pull_request_attribute_error(self):
        """pull_request 属性访问异常时应返回 False"""
        issue = MagicMock()
        issue.number = 1
        issue.title = "test"
        issue.state = "open"
        issue.body = "test"
        del issue.pull_request  # 确保没有这个属性
        # 当属性不存在时，访问 issue.pull_request 会创建新的 MagicMock (not None)
        # 所以我们需要模拟属性错误
        type(issue).pull_request = property(lambda self: (_ for _ in ()).throw(AttributeError("no attribute")))
        self.assertFalse(is_pull_request(issue))


class TestShouldIncludeIssue(unittest.TestCase):
    """测试 should_include_issue 函数"""

    def test_pull_request_excluded(self):
        """PR 应被排除"""
        issue = _make_mock_issue(12, "合并远程更改", "open", "content", pull_request=True)
        self.assertFalse(should_include_issue(issue))

    def test_closed_issue_excluded(self):
        """已关闭的 issue 应被排除"""
        issue = _make_mock_issue(1, "test", "closed", "有内容的文章正文", pull_request=False)
        self.assertFalse(should_include_issue(issue))

    def test_zero_word_count_excluded(self):
        """字数为 0 的 issue 应被排除"""
        issue = _make_mock_issue(1, "test", "open", "", pull_request=False)
        self.assertFalse(should_include_issue(issue))

    def test_zero_word_count_from_metadata_excluded(self):
        """元数据中字数 <= 0 的 issue 应被排除"""
        issue = _make_mock_issue(1, "test", "open", "some content", pull_request=False)
        metadata = {"1": {"word_count": 0, "image_count": 0}}
        self.assertFalse(should_include_issue(issue, metadata))

    def test_negative_image_count_excluded(self):
        """插图数量为负数的 issue 应被排除"""
        issue = _make_mock_issue(1, "test", "open", "content", pull_request=False)
        metadata = {"1": {"word_count": 10, "image_count": -1}}
        self.assertFalse(should_include_issue(issue, metadata))

    def test_valid_open_issue_included(self):
        """正常 open issue 应通过过滤"""
        issue = _make_mock_issue(1, "About Diary", "open", "这是一个关于日记的介绍文章", pull_request=False)
        self.assertTrue(should_include_issue(issue))

    def test_valid_issue_with_metadata_included(self):
        """元数据中有有效数据的 issue 应通过过滤"""
        issue = _make_mock_issue(16, "Diary 2006", "open", "", pull_request=False)
        metadata = {"16": {"word_count": 100, "image_count": 3}}
        self.assertTrue(should_include_issue(issue, metadata))

    def test_issue_with_zero_images_included(self):
        """插图数量为 0 的正常 issue 应通过过滤（0 是有效值）"""
        issue = _make_mock_issue(1, "test", "open", "有内容的文章", pull_request=False)
        self.assertTrue(should_include_issue(issue))

    def test_issue_with_zero_images_in_metadata_included(self):
        """元数据中插图数量为 0 的正常 issue 应通过过滤"""
        issue = _make_mock_issue(1, "test", "open", "", pull_request=False)
        metadata = {"1": {"word_count": 50, "image_count": 0}}
        self.assertTrue(should_include_issue(issue, metadata))

    def test_issue_without_metadata_uses_body(self):
        """无元数据时回退到 issue.body 统计"""
        # body 为空 → 字数为 0 → 应被排除
        issue = _make_mock_issue(1, "test", "open", "", pull_request=False)
        self.assertFalse(should_include_issue(issue))

    def test_multiple_rejections_first_wins(self):
        """多个条件不满足时，按优先级返回 False"""
        # PR + closed + 零字数 → is_pull_request 先命中，返回 False
        issue = _make_mock_issue(12, "test", "closed", "", pull_request=True)
        self.assertFalse(should_include_issue(issue))


class TestCleanMarkdown(unittest.TestCase):
    """测试 _clean_markdown 函数"""

    def test_remove_html_comments(self):
        result = _clean_markdown("<!-- comment -->text")
        self.assertEqual(result, "text")

    def test_remove_code_blocks(self):
        result = _clean_markdown("text```python\ncode\n```more")
        self.assertNotIn("code", result)
        self.assertIn("text", result)
        self.assertIn("more", result)

    def test_remove_images(self):
        result = _clean_markdown("text ![alt](url) more")
        self.assertEqual(result, "text more")  # 图片被移除，多余空格被合并

    def test_remove_links_keep_text(self):
        result = _clean_markdown("[link text](url)")
        self.assertEqual(result, "link text")

    def test_remove_html_tags(self):
        result = _clean_markdown("<div>text</div>")
        self.assertEqual(result, "text")

    def test_handle_none(self):
        result = _clean_markdown(None)
        self.assertEqual(result, "")

    def test_handle_empty(self):
        result = _clean_markdown("")
        self.assertEqual(result, "")


class TestCountWords(unittest.TestCase):
    """测试 _count_words 函数"""

    def test_chinese_characters(self):
        result = _count_words("你好世界")
        self.assertEqual(result, 4)

    def test_english_words(self):
        result = _count_words("hello world test")
        self.assertEqual(result, 3)

    def test_mixed_chinese_english(self):
        result = _count_words("hello 世界 test")
        self.assertEqual(result, 4)  # 2 Chinese chars + 2 English words

    def test_numbers(self):
        result = _count_words("this is 2026")
        self.assertEqual(result, 3)  # 2 words + 1 number

    def test_empty_string(self):
        result = _count_words("")
        self.assertEqual(result, 0)

    def test_none_string(self):
        result = _count_words(None)
        self.assertEqual(result, 0)


class TestContentWordCount(unittest.TestCase):
    """测试 get_content_word_count 函数"""

    def test_markdown_content(self):
        content = "# 标题\n\n这是一段**加粗**的文本，包含[链接](url)和图片![img](url)"
        result = get_content_word_count(content)
        # "标题" (2) + "这是一段加粗的文本，包含链接和图片" (14 + some)
        self.assertGreater(result, 0)

    def test_empty_content(self):
        result = get_content_word_count("")
        self.assertEqual(result, 0)

    def test_none_content(self):
        result = get_content_word_count(None)
        self.assertEqual(result, 0)


class TestContentImageCount(unittest.TestCase):
    """测试 get_content_image_count 函数"""

    def test_markdown_images(self):
        result = get_content_image_count("text![img1](url1) more ![img2](url2)")
        self.assertEqual(result, 2)

    def test_html_images(self):
        result = get_content_image_count('<img src="url"> text <IMG src="url2">')
        self.assertEqual(result, 2)  # should be case insensitive for regex

    def test_no_images(self):
        result = get_content_image_count("plain text without images")
        self.assertEqual(result, 0)

    def test_empty_content(self):
        result = get_content_image_count("")
        self.assertEqual(result, 0)

    def test_none_content(self):
        result = get_content_image_count(None)
        self.assertEqual(result, 0)


if __name__ == "__main__":
    unittest.main()