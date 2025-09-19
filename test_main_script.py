#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：用于验证main.py是否能正常更新README.md文件
"""

import os
import sys
import logging
import subprocess
import time
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)


def backup_readme():
    """备份当前的README.md文件"""
    if os.path.exists('README.md'):
        backup_dir = 'BACKUP_TEST'
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # 创建带时间戳的备份文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(backup_dir, f'README_backup_{timestamp}.md')
        
        # 复制文件内容
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f'已备份README.md到: {backup_file}')
        return backup_file
    else:
        logger.warning('README.md文件不存在，无法备份')
        return None


def get_file_timestamp(file_path):
    """获取文件的最后修改时间"""
    if os.path.exists(file_path):
        return os.path.getmtime(file_path)
    return None


def verify_readme_update(original_timestamp):
    """验证README.md是否已更新"""
    current_timestamp = get_file_timestamp('README.md')
    
    if current_timestamp is None:
        logger.error('README.md文件不存在！')
        return False
    
    if original_timestamp is None:
        logger.info('README.md是新创建的文件')
        return True
    
    if current_timestamp > original_timestamp:
        logger.info('README.md已成功更新！')
        # 读取更新后的文件内容，检查最后更新时间
        try:
            with open('README.md', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找最后更新时间行
            for line in content.split('\n'):
                if '最后更新时间' in line:
                    logger.info(f'更新后的时间戳: {line}')
                    break
        except Exception as e:
            logger.error(f'读取README.md内容失败: {str(e)}')
        
        return True
    else:
        logger.error('README.md未更新！')
        return False


def run_main_script(github_token, repo_name):
    """运行main.py脚本"""
    try:
        # 备份原始README.md
        backup_file = backup_readme()
        
        # 记录原始时间戳
        original_timestamp = get_file_timestamp('README.md')
        if original_timestamp:
            logger.info(f'原始README.md修改时间: {datetime.fromtimestamp(original_timestamp)}')
        
        # 运行main.py脚本
        logger.info(f'开始运行main.py脚本...')
        start_time = time.time()
        
        # 构建命令
        cmd = [
            sys.executable,  # 使用当前Python解释器
            'main.py',
            github_token,
            repo_name
        ]
        
        # 执行命令
        result = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        end_time = time.time()
        logger.info(f'main.py脚本执行完成，耗时: {end_time - start_time:.2f}秒')
        
        # 输出执行结果
        logger.debug(f'标准输出:\n{result.stdout}')
        if result.stderr:
            logger.warning(f'标准错误:\n{result.stderr}')
        
        # 验证README.md是否已更新
        updated = verify_readme_update(original_timestamp)
        
        return updated
        
    except subprocess.CalledProcessError as e:
        logger.error(f'main.py脚本执行失败，返回码: {e.returncode}')
        logger.error(f'错误输出:\n{e.stderr}')
        return False
    except Exception as e:
        logger.error(f'运行测试时发生异常: {str(e)}')
        return False


def main():
    """主函数"""
    # 从环境变量或命令行参数获取GitHub Token和仓库名称
    github_token = os.getenv('GITHUB_TOKEN')
    repo_name = os.getenv('REPO_NAME', 'bingdu748/c_d-project')  # 默认使用用户的仓库名称
    
    # 如果没有提供Token，可以要求用户输入
    if not github_token:
        logger.warning('环境变量GITHUB_TOKEN未设置，测试可能无法正常运行')
        # 注意：在实际使用中，不应该在控制台明文输入Token
        # 这里为了测试方便，允许用户选择是否继续
        choice = input('没有提供GitHub Token，是否继续测试？(y/n): ')
        if choice.lower() != 'y':
            logger.info('测试已取消')
            sys.exit(0)
    
    # 运行测试
    success = run_main_script(github_token, repo_name)
    
    if success:
        logger.info('测试成功！main.py能够正常更新README.md文件')
        sys.exit(0)
    else:
        logger.error('测试失败！main.py未能正常更新README.md文件')
        sys.exit(1)


if __name__ == '__main__':
    main()