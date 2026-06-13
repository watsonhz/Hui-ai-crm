# Remote SSH key setup script v2 - replaces old key with new one

$pubkey = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFWf+nNBm8QLlGy70xktgxlo4i2M1jjlR+LzU1zXNKEB pc1-ceo@aicrm"

# 1. User's authorized_keys - replace old key, add new
$userSshDir = "$env:USERPROFILE\.ssh"
$userAuthFile = "$userSshDir\authorized_keys"

if (-not (Test-Path $userSshDir)) {
    New-Item -ItemType Directory -Path $userSshDir -Force
}

$existing = @()
if (Test-Path $userAuthFile) {
    $existing = Get-Content $userAuthFile | Where-Object { $_ -notmatch "pc1-ceo@aicrm" }
}
$existing += $pubkey
Set-Content -Path $userAuthFile -Value $existing -Encoding ASCII
icacls $userAuthFile /inheritance:r /grant "${env:USERNAME}:(R)" /grant "SYSTEM:(R)" 2>&1 | Out-Null
Write-Host "USER_KEY_UPDATED"

# 2. Administrators authorized_keys
$adminAuthFile = "$env:ProgramData\ssh\administrators_authorized_keys"
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if ($isAdmin) {
    if (-not (Test-Path "$env:ProgramData\ssh")) {
        New-Item -ItemType Directory -Path "$env:ProgramData\ssh" -Force
    }
    $adminExisting = @()
    if (Test-Path $adminAuthFile) {
        $adminExisting = Get-Content $adminAuthFile | Where-Object { $_ -notmatch "pc1-ceo@aicrm" }
    }
    $adminExisting += $pubkey
    Set-Content -Path $adminAuthFile -Value $adminExisting -Encoding ASCII
    icacls $adminAuthFile /inheritance:r /grant "BUILTIN\Administrators:(R)" /grant "SYSTEM:(R)" 2>&1 | Out-Null
    Write-Host "ADMIN_KEY_UPDATED"
}

Write-Host "DONE"
