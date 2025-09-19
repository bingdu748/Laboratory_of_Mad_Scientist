import os
import sys
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# 常量定义
MD_HEAD = """My personal blog（[About Me](https://github.com/bingdu748/c_d-project/issues/7)）using issues and GitHub Actions (随意转载，无需署名)
[RSS Feed](https://raw.githubusercontent.com/bingdu748/c_d-project/master/feed.xml)
"""

BACKUP_DIR = "BACKUP"

# 模拟的issue数据
mock_issues = [
    {
        'number': 9,
        'title': '测试更新的文章',
        'html_url': 'https://github.com/bingdu748/c_d-project/issues/9',
        'updated_at': datetime.now(),
        'labels': ['测试', '更新']
    },
    {
        'number': 8,
        'title': '「Diary」2024·July',
        'html_url': 'https://github.com/bingdu748/c_d-project/issues/8',
        'updated_at': datetime(2024, 7, 9),
        'labels': ['日记']
    },
    {
        'number': 7,
        'title': 'About Me',
        'html_url': 'https://github.com/bingdu748/c_d-project/issues/7',
        'updated_at': datetime(2024, 4, 15),
        'labels': ['关于']
    }
]

# 模拟格式化时间函数
def format_time(time_obj):
    return time_obj.strftime('%Y-%m-%d')

# 模拟添加README头部
def add_md_header(filename, repo_name):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(MD_HEAD)
            # 添加最后更新时间
            f.write(f"\n**最后更新时间：** {format_time(datetime.now())}\n\n")
        logger.info(f"README头部已添加到 {filename}")
    except Exception as e:
        logger.error(f"添加README头部失败: {str(e)}")
        raise

# 模拟添加最近更新部分
def add_md_recent(mock_issues, filename):
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write("## 最近更新\n")
            # 按更新时间排序
            sorted_issues = sorted(mock_issues, key=lambda x: x['updated_at'], reverse=True)
            for issue in sorted_issues[:5]:  # 只显示最近5篇
                f.write(f"- [{issue['title']}]({issue['html_url']})--{format_time(issue['updated_at'])}\n")
            f.write("\n")
        logger.info(f"最近更新部分已添加到 {filename}")
    except Exception as e:
        logger.error(f"添加最近更新部分失败: {str(e)}")
        raise

# 模拟添加标签分类部分
def add_md_label(mock_issues, filename):
    try:
        # 按标签分组
        label_dict = {}
        for issue in mock_issues:
            for label in issue['labels']:
                if label not in label_dict:
                    label_dict[label] = []
                label_dict[label].append(issue)
                
        with open(filename, 'a', encoding='utf-8') as f:
            for label_name, issues in label_dict.items():
                f.write(f"## {label_name}系列\n")
                for issue in issues:
                    f.write(f"- [{issue['title']}]({issue['html_url']})--{format_time(issue['updated_at'])}\n")
                f.write("\n")
        logger.info(f"标签分类部分已添加到 {filename}")
    except Exception as e:
        logger.error(f"添加标签分类部分失败: {str(e)}")
        raise

# 主函数
def main():
    try:
        logger.info("开始测试更新README.md")
        
        # 检查备份目录是否存在
        if not os.path.exists(BACKUP_DIR):
            logger.info(f"创建备份目录: {BACKUP_DIR}")
            os.makedirs(BACKUP_DIR)
            
        # 备份当前README.md
        if os.path.exists("README.md"):
            backup_path = os.path.join(BACKUP_DIR, f"README_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
            with open("README.md", 'r', encoding='utf-8') as f:
                content = f.read()
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"已备份当前README.md到 {backup_path}")
            
        # 更新README.md
        add_md_header("README.md", "bingdu748/c_d-project")
        add_md_recent(mock_issues, "README.md")
        add_md_label(mock_issues, "README.md")
        
        logger.info("README.md更新测试完成")
        
        # 显示更新后的README.md内容
        with open("README.md", 'r', encoding='utf-8') as f:
            content = f.read()
        print("\n更新后的README.md内容:")
        print("=" * 50)
        print(content)
        print("=" * 50)
        
    except Exception as e:
        logger.error(f"测试过程中发生错误: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()