# AI-CRM v3.1.0 - PC1 OpenSSH Server Setup
# Run as Administrator in PowerShell
# Usage: .\enable-sshd-pc1.ps1

Write-Host "--- Installing OpenSSH Server ---"
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

Write-Host "--- Starting sshd ---"
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'

Write-Host "--- Configuring Firewall ---"
New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (SSH)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22

Write-Host "--- Verifying ---"
Get-Service sshd | Format-List Name,Status,StartType
ssh localhost "echo SSH_OK"

Write-Host ""
Write-Host "=========================================="
Write-Host "OpenSSH Server is now running!"
Write-Host "Clone URL: git clone ssh://$env:USERNAME@192.168.0.168/~/git/ai-crm.git"
Write-Host "=========================================="
