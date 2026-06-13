import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')

pubkey_path = r'C:\Users\watson\.ssh\id_ed25519_aicrm.pub'
with open(pubkey_path) as f:
    pubkey = f.read().strip()

host = '192.168.0.171'
user = 'Administrator'
pwd = '112233'

try:
    print(f'=== PC4 ({user}@{host}) ===')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=pwd, timeout=10)
    print('  Connected OK')

    # Get home directory
    stdin, stdout, stderr = client.exec_command('echo %USERPROFILE%')
    home = stdout.read().decode('utf-8', errors='replace').strip()
    print(f'  HOME: {home}')

    # USER authorized_keys
    user_path = home + '\\.ssh\\authorized_keys'
    user_ssh_dir = home + '\\.ssh'
    print(f'  User path: {user_path}')

    sftp = client.open_sftp()
    try:
        sftp.stat(user_ssh_dir)
    except:
        sftp.mkdir(user_ssh_dir)
        print('  Created .ssh dir')

    existing = ''
    try:
        with sftp.open(user_path, 'r') as f:
            existing = f.read().decode('utf-8')
    except:
        pass

    # Remove old pc1 keys, add new one
    lines = [l for l in existing.split('\n') if 'pc1-ceo@aicrm' not in l and l.strip()]
    lines.append(pubkey)
    with sftp.open(user_path, 'w') as f:
        f.write('\n'.join(lines).encode('utf-8'))
    print(f'  User key written ({len(lines)} keys)')
    sftp.close()

    # ADMINISTRATORS authorized_keys
    admin_path = 'C:\\ProgramData\\ssh\\administrators_authorized_keys'
    admin_dir = 'C:\\ProgramData\\ssh'
    sftp = client.open_sftp()
    try:
        sftp.stat(admin_dir)
    except:
        sftp.mkdir(admin_dir)
        print('  Created ProgramData\\ssh dir')

    admin_existing = ''
    try:
        with sftp.open(admin_path, 'r') as f:
            admin_existing = f.read().decode('utf-8')
    except:
        pass

    admin_lines = [l for l in admin_existing.split('\n') if 'pc1-ceo@aicrm' not in l and l.strip()]
    admin_lines.append(pubkey)
    with sftp.open(admin_path, 'w') as f:
        f.write('\n'.join(admin_lines).encode('utf-8'))
    print(f'  Admin key written ({len(admin_lines)} keys)')
    sftp.close()

    # Fix permissions
    cmds = [
        'icacls "' + user_path + '" /inheritance:r /grant "Administrator:(R)" /grant "SYSTEM:(R)" /q',
        'icacls "' + admin_path + '" /inheritance:r /grant "Administrators:(R)" /grant "SYSTEM:(R)" /q',
    ]
    for cmd in cmds:
        stdin, stdout, stderr = client.exec_command(cmd)
        out = stdout.read().decode('utf-8', errors='replace')
        err = stderr.read().decode('utf-8', errors='replace')
        if out.strip():
            print(f'  perm: {out.strip()[:100]}')

    client.close()
    print('  [OK] PC4 setup complete')

except Exception as e:
    print(f'  [ERR] {type(e).__name__}: {e}')
print('Done.')
