#!/bin/bash
# ============================================================
# AI-CRM v3.1.0 — SSH Key 分发脚本
# 执行位置: PC1 (192.168.0.168)
# 用途: 将 PC1 的 SSH 公钥分发到 PC2-PC5
# ============================================================
set -e

# v3.1.0 IP 分配 (Section 2.3)
declare -A PCS
PCS[pc2]="192.168.0.169"
PCS[pc3]="192.168.0.170"
PCS[pc4]="192.168.0.171"
PCS[pc5]="192.168.0.253"

# 确保密钥存在
if [ ! -f ~/.ssh/id_ed25519.pub ]; then
    echo "生成 SSH Key..."
    ssh-keygen -t ed25519 -C "openclaw-v5" -f ~/.ssh/id_ed25519 -N ""
fi

echo "=== 分发 SSH 公钥到 4 台工作节点 ==="
for name in pc2 pc3 pc4 pc5; do
    ip="${PCS[$name]}"
    echo ""
    echo "--- $name ($ip) ---"
    ssh-copy-id -i ~/.ssh/id_ed25519.pub "$ip" 2>/dev/null && \
        echo "✅ $name OK" || \
        echo "❌ $name FAILED — 请手动操作"
done

echo ""
echo "=== 验证连接 ==="
for name in pc2 pc3 pc4 pc5; do
    ip="${PCS[$name]}"
    echo -n "$name ($ip): "
    ssh -o ConnectTimeout=3 "$ip" "echo \$(hostname) [OK]" 2>/dev/null || echo "UNREACHABLE"
done
echo ""
echo "============================================================"
echo "分发完成。如果某台机器失败，手动执行："
echo "  ssh-copy-id user@<IP>"
echo "============================================================"
