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