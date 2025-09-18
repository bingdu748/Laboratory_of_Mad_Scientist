import os
import sys
from github import Github

# 这是一个测试脚本，用于检查GitHub连接和权限
# 在实际使用时，需要设置GITHUB_TOKEN环境变量

def test_github_connection():
    try:
        # 获取GitHub令牌
        token = os.environ.get('GITHUB_TOKEN')
        if not token:
            print("错误: 未设置GITHUB_TOKEN环境变量")
            return False
        
        print("正在尝试连接到GitHub...")
        g = Github(token)
        
        # 获取当前用户
        user = g.get_user()
        print(f"登录成功，用户: {user.login}")
        
        # 尝试访问仓库
        repo_name = "bingdu748/Laboratory_of_Mad_Scientist"
        print(f"正在尝试访问仓库: {repo_name}")
        repo = g.get_repo(repo_name)
        print(f"访问仓库成功: {repo.full_name}")
        
        # 尝试获取issues
        print("正在尝试获取issues...")
        issues = list(repo.get_issues(state="open"))
        print(f"获取到 {len(issues)} 个开放的issues")
        
        # 尝试获取labels
        print("正在尝试获取labels...")
        labels = list(repo.get_labels())
        print(f"获取到 {len(labels)} 个labels")
        
        print("所有测试都已成功完成！")
        return True
        
    except Exception as e:
        print(f"测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_github_connection()
    sys.exit(0 if success else 1)