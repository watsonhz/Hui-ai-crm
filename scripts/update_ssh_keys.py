import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')

pubkey = 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFWf+nNBm8QLlGy70xktgxlo4i2M1jjlR+LzU1zXNKEB pc1-ceo@aicrm'

targets = [
    ('PC2', '192.168.0.169', 'Gzzhh', 'Hziot@)@%168', 'gzzhh'),
    ('PC5', '192.168.0.253', 'administrator', 'A123*a', 'Administrator'),
]

for name, host, user, pwd, ssh_user in targets:
    try:
        print(f'=== {name} ===')
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=user, password=pwd, timeout=10)

        user_path = 'C:\\Users\\' + ssh_user + '\\.ssh\\authorized_keys'
        admin_path = 'C:\\ProgramData\\ssh\\administrators_authorized_keys'

        # Reset permissions and write user key
        cmds = [
            'icacls "' + user_path + '" /reset /q 2>&1',
            'echo ' + pubkey + ' > "' + user_path + '" 2>&1',
            'icacls "' + admin_path + '" /reset /q 2>&1',
            'echo ' + pubkey + ' > "' + admin_path + '" 2>&1',
            'icacls "' + user_path + '" /inheritance:r /grant "' + ssh_user + ':(R)" /grant "SYSTEM:(R)" /q 2>&1',
            'icacls "' + admin_path + '" /inheritance:r /grant "Administrators:(R)" /grant "SYSTEM:(R)" /q 2>&1',
        ]

        for cmd in cmds:
            stdin, stdout, stderr = client.exec_command(cmd)
            out = stdout.read().decode('utf-8', errors='replace').strip()
            err = stderr.read().decode('utf-8', errors='replace').strip()
            if out:
                print('  ' + out[:120])
            if err and 'successfully' not in err.lower():
                print('  ERR: ' + err[:120])

        # Verify
        stdin, stdout, stderr = client.exec_command('type "' + user_path + '"')
        content = stdout.read().decode('utf-8', errors='replace')
        if 'IFWf+nNBm8QL' in content:
            print('  [OK] ' + name + ' key updated')
        else:
            print('  [WARN] ' + name + ' key may not be updated. Content length: ' + str(len(content)))

        client.close()
    except Exception as e:
        print('  [ERR] ' + type(e).__name__ + ': ' + str(e))
print('Done.')
