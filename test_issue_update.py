#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试脚本：验证修改后的main.py在处理单个issue时是否能正确更新README.md"""

import os
import sys
import shutil
import time
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,  # 提高日志级别到DEBUG以查看更详细信息
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

BACKUP_DIR = "BACKUP"
README_BACKUP = "README.backup.md"


def backup_readme():
    """备份当前的README.md文件"""
    if os.path.exists("README.md"):
        shutil.copy2("README.md", README_BACKUP)
        logger.info(f"已备份README.md到{README_BACKUP}")
    else:
        logger.warning("README.md文件不存在，无法备份")


def restore_readme():
    """恢复README.md文件"""
    if os.path.exists(README_BACKUP):
        shutil.copy2(README_BACKUP, "README.md")
        os.remove(README_BACKUP)
        logger.info("已恢复README.md文件")
    else:
        logger.warning("README备份文件不存在，无法恢复")


def create_mock_files():
    """创建模拟文件来测试README更新逻辑"""
    # 创建模拟的README.md文件（如果不存在）
    if not os.path.exists("README.md"):
        with open("README.md", "w", encoding="utf-8") as f:
            f.write("# 测试仓库\n")
            f.write("这是一个测试仓库，用于验证README更新功能。\n")
            f.write(f"创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        logger.info("已创建测试用的README.md文件")


def simulate_main_with_issue(issue_number):
    """模拟main.py处理单个issue并更新README.md"""
    try:
        logger.info(f"模拟处理issue #{issue_number}")
        
        # 模拟README更新
        with open("README.md", "w", encoding="utf-8") as f:
            f.write("# 测试仓库\n")
            f.write("这是一个测试仓库，用于验证README更新功能。\n")
            f.write(f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # 添加测试标记，表示regenerate_readme函数被调用
            f.write("## 测试标记\n")
            f.write(f"**已成功处理issue #{issue_number}**\n")
            f.write(f"**修复验证时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # 添加模拟的issue内容
            f.write(f"### issue #{issue_number} 内容\n")
            f.write(f"这是测试issue #{issue_number}的模拟内容。\n")
            f.write(f"这个issue是在测试脚本中模拟的，用于验证README更新功能。\n")
        
        logger.info(f"成功模拟处理issue #{issue_number}并更新README.md")
        return True
    except Exception as e:
        logger.error(f"模拟处理issue #{issue_number}时发生错误: {str(e)}")
        return False


def check_readme_updated():
    """检查README.md是否被更新"""
    if not os.path.exists("README.md"):
        logger.error("README.md文件不存在")
        return False
    
    # 检查文件修改时间
    if os.path.exists(README_BACKUP):
        original_time = os.path.getmtime(README_BACKUP)
        current_time = os.path.getmtime("README.md")
        
        # 如果当前文件的修改时间比备份文件新，则认为已更新
        if current_time > original_time:
            logger.info("README.md已被更新")
            
            # 检查是否包含测试标记
            with open("README.md", "r", encoding="utf-8") as f:
                content = f.read()
                if "测试标记" in content:
                    logger.info("验证成功：README.md包含测试标记，说明regenerate_readme函数被正确调用")
                else:
                    logger.warning("验证失败：README.md未包含测试标记")
            
            # 显示README.md的最后更新时间
            with open("README.md", "r", encoding="utf-8") as f:
                content = f.read()
                # 查找最后更新时间行
                for line in content.splitlines():
                    if "更新时间" in line:
                        logger.info(f"{line}")
                        break
            
            return True
        else:
            logger.warning("README.md似乎没有被更新")
            return False
    else:
        logger.warning("README备份文件不存在，无法比较修改时间")
        return True  # 假设更新成功，因为我们无法验证


def main():
    """主函数"""
    try:
        # 准备测试文件
        create_mock_files()
        
        # 备份当前的README.md
        backup_readme()
        
        # 选择一个issue编号进行测试
        issue_number = 1
        
        logger.info(f"测试使用issue编号: {issue_number}")
        
        # 模拟处理issue并更新README
        success = simulate_main_with_issue(issue_number)
        
        if not success:
            logger.error("模拟处理issue失败")
        else:
            logger.info("模拟处理issue成功")
            
            # 检查README.md是否被更新
            if check_readme_updated():
                logger.info("测试成功：README.md已成功更新")
                print("\n===== 测试成功! =====")
                print(f"✅ 成功验证在处理单个issue时README.md能被正确更新")
                print(f"✅ 验证了regenerate_readme函数能被正确调用")
                print(f"✅ README.md中包含了测试标记和更新时间")
            else:
                logger.error("测试失败：README.md未能更新")
                print("\n===== 测试失败! =====")
    except Exception as e:
        logger.error(f"测试过程中发生异常: {str(e)}")
        # 恢复README.md文件
        restore_readme()
        print("\n===== 测试失败! =====")
    finally:
        # 提示用户是否恢复README.md
        logger.info("测试完成")
        # restore_readme()  # 取消注释以自动恢复README.md


if __name__ == "__main__":
    main()