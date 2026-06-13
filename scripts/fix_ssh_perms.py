import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')

pubkey_path = r"C:\Users\watson\.ssh\id_ed25519_aicrm.pub"
with open(pubkey_path) as f:
    pubkey = f.read().strip()

targets = [
    ("PC2", "192.168.0.169", "Gzzhh", "Hziot@)@%168", "gzzhh"),
    ("PC5", "192.168.0.253", "administrator", "A123*a", "Administrator"),
]

for name, host, user, pwd, ssh_user in targets:
    try:
        print(f"=== {name} ===")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=user, password=pwd, timeout=10)

        # Fix permissions using icacls
        cmds = [
            r'icacls "C:\Users\{}\.ssh\authorized_keys" /inheritance:r /grant "{}:(R)" /grant "SYSTEM:(R)"'.format(ssh_user, ssh_user),
            r'icacls "C:\ProgramData\ssh\administrators_authorized_keys" /inheritance:r /grant "Administrators:(R)" /grant "SYSTEM:(R)"',
        ]

        for cmd in cmds:
            stdin, stdout, stderr = client.exec_command(cmd)
            out = stdout.read().decode("utf-8", errors="replace")
            err = stderr.read().decode("utf-8", errors="replace")
            if out.strip():
                print(f"  {out.strip()[:120]}")
            if err.strip():
                print(f"  err: {err.strip()[:120]}")

        client.close()
        print(f"  [OK] {name}")
    except Exception as e:
        print(f"  [ERR] {type(e).__name__}: {e}")
print("Done.")
