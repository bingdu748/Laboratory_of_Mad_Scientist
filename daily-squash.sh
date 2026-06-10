#!/bin/bash

# ============================================
# 每日 Git 提交合并脚本
# 功能：将当天所有提交压缩为一个整洁的提交
# 提交信息格式：YYYY-MM-DD - 每日提交汇总
# ============================================

set -euo pipefail

# 配置参数
REPO_DIR="."                              # 仓库目录（当前目录）
REMOTE_NAME="origin"                      # 远程仓库名称
BRANCH_NAME="master"                      # 分支名称
COMMIT_MESSAGE_PREFIX="每日提交汇总"       # 提交信息前缀

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查是否在 Git 仓库中
check_git_repo() {
    if ! git rev-parse --is-inside-work-tree &>/dev/null; then
        log_error "当前目录不是 Git 仓库"
        exit 1
    fi
    log_info "确认在 Git 仓库中"
}

# 获取当天的日期范围（UTC时间）
get_today_range() {
    # 今天 00:00:00 UTC
    TODAY_START=$(date -u -d "today" +"%Y-%m-%dT00:00:00Z")
    # 明天 00:00:00 UTC（即今天结束）
    TODAY_END=$(date -u -d "tomorrow" +"%Y-%m-%dT00:00:00Z")
    log_info "日期范围: $TODAY_START 至 $TODAY_END"
}

# 检查当天是否有提交
has_today_commits() {
    # 获取当天的提交数量
    local commit_count
    commit_count=$(git log --oneline --since="$TODAY_START" --until="$TODAY_END" --count 2>/dev/null || echo 0)
    
    if [ "$commit_count" -eq 0 ]; then
        log_info "当天没有提交，无需合并"
        return 1
    fi
    
    log_info "当天有 $commit_count 个提交需要合并"
    return 0
}

# 获取当前分支
get_current_branch() {
    local branch
    branch=$(git rev-parse --abbrev-ref HEAD)
    echo "$branch"
}

# 压缩当天的提交
squash_commits() {
    local current_branch=$(get_current_branch)
    local today_date=$(date +"%Y-%m-%d")
    local commit_message="$today_date - $COMMIT_MESSAGE_PREFIX"
    
    log_info "当前分支: $current_branch"
    log_info "目标提交信息: $commit_message"
    
    # 获取当天第一个提交的父提交
    local first_commit
    first_commit=$(git log --reverse --since="$TODAY_START" --until="$TODAY_END" --format="%H" | head -1)
    
    if [ -z "$first_commit" ]; then
        log_error "无法找到当天的第一个提交"
        exit 1
    fi
    
    # 获取第一个提交的父提交
    local parent_commit
    parent_commit=$(git rev-parse "$first_commit^" 2>/dev/null || git rev-list --max-parents=0 HEAD)
    
    log_info "从 $parent_commit 开始压缩到 HEAD"
    
    # 执行交互式 rebase 并自动 squash
    # 使用环境变量设置编辑器为 sed 自动修改提交信息
    GIT_SEQUENCE_EDITOR="sed -i '2,\$s/^pick/squash/'" \
    GIT_EDITOR="cat > /dev/null" \
    git rebase -i "$parent_commit" || {
        log_error "Rebase 失败，可能存在冲突"
        # 尝试中止 rebase
        git rebase --abort 2>/dev/null || true
        exit 1
    }
    
    # 修改最终提交信息
    git commit --amend -m "$commit_message"
    log_info "提交压缩完成"
}

# 安全推送
safe_push() {
    log_info "开始安全推送..."
    
    # 先获取远程最新更改
    git fetch "$REMOTE_NAME" "$BRANCH_NAME"
    
    # 检查是否有冲突
    if git merge-base --is-ancestor "HEAD" "$REMOTE_NAME/$BRANCH_NAME"; then
        # 本地落后于远程，需要先拉取
        log_warn "本地分支落后于远程，执行安全拉取"
        git pull "$REMOTE_NAME" "$BRANCH_NAME" --strategy-option=ours
    fi
    
    # 强制推送（因为我们重写了历史）
    log_info "推送压缩后的提交..."
    git push "$REMOTE_NAME" "$BRANCH_NAME" --force-with-lease
    
    if [ $? -eq 0 ]; then
        log_info "推送成功！"
    else
        log_error "推送失败"
        exit 1
    fi
}

# 主函数
main() {
    log_info "========== 每日 Git 提交合并脚本 =========="
    
    # 切换到仓库目录
    cd "$REPO_DIR" || {
        log_error "无法切换到目录: $REPO_DIR"
        exit 1
    }
    
    # 检查是否在 Git 仓库中
    check_git_repo
    
    # 获取当天日期范围
    get_today_range
    
    # 检查当天是否有提交
    if ! has_today_commits; then
        exit 0
    fi
    
    # 压缩提交
    squash_commits
    
    # 安全推送
    safe_push
    
    log_info "========== 脚本执行完成 =========="
}

# 执行主函数
main "$@"