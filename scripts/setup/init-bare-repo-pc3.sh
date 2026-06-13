#!/bin/bash
# ============================================================
# AI-CRM v3.1.0 — 中央 Git 仓库搭建脚本
# 执行位置: PC3 (192.168.0.170, macOS)
# 用途: 创建 bare repo，作为全团队的 push/pull 中心
# ============================================================
set -e

REPO_PATH="$HOME/git/ai-crm.git"

echo "=== Step 1: 创建裸仓库 ==="
mkdir -p "$HOME/git"
git init --bare "$REPO_PATH"
echo "裸仓库创建于: $REPO_PATH"

echo ""
echo "=== Step 2: 允许推送到当前分支 ==="
# 允许其他人 push 到已 checkout 的分支（bare repo 不需要此设置，但以防万一）
git -C "$REPO_PATH" config receive.denyCurrentBranch ignore

echo ""
echo "=== Step 3: 获取本机 IP 确认 ==="
echo "PC3 IP: $(ifconfig | grep 'inet ' | grep -v 127.0.0.1 | awk '{print $2}' | head -1)"
echo ""
echo "============================================================"
echo "✅ PC3 裸仓库搭建完成！"
echo ""
echo "其他机器执行以下命令克隆："
echo "  PC1/PC2/PC4/PC5:"
echo "    git clone ssh://$(whoami)@192.168.0.170/~/git/ai-crm.git"
echo ""
echo "  或已有本地仓库添加 remote："
echo "    git remote add origin ssh://$(whoami)@192.168.0.170/~/git/ai-crm.git"
echo "    git push -u origin --all"
echo "============================================================"
