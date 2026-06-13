$pass = ConvertTo-SecureString 'A123*a' -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential('administrator', $pass)

$source = 'C:\DevProjects\ai-crm\qa'
$dest = '\\192.168.0.253\c$\DevProjects\ai-crm\qa'

Write-Host "PC2 -> PC5 QA Sync" -ForegroundColor Cyan
Write-Host "Source: $source"
Write-Host "Dest:   $dest"

try {
    New-Item -ItemType Directory -Path $dest -Force -ErrorAction SilentlyContinue
    Copy-Item -Path "$source\*" -Destination $dest -Recurse -Force -Credential $cred -ErrorAction Stop
    Write-Host "DONE: QA files synced to PC5" -ForegroundColor Green
    Get-ChildItem $dest -Recurse | ForEach-Object { Write-Host "  $($_.FullName)" }
} catch {
    Write-Host "ERROR: $_" -ForegroundColor Red
    Write-Host "Try manually: copy \\192.168.0.169\qa\ to C:\DevProjects\ai-crm\qa\" -ForegroundColor Yellow
}
