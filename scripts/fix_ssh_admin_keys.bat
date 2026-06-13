@echo off
(
echo ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFWf+nNBm8QLlGy70xktgxlo4i2M1jjlR+LzU1zXNKEB pc1-ceo@aicrm
echo ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMxdlAud98xCmgOClizO9FIo2+SlTrYzU1f0u7GoxbNl pc2-pm-frontend@aicrm
echo ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILE+8A8fU/nJgTavaUUDw2BGxib81Tsk/StaBWtGfNE4 pc3-architect@aicrm
echo ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPGzEUtOVbvTY8d1MiWelT7xSxVq4wVdg8p5mQ/LnHfo pc4-security@aicrm
echo ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIeRqgPEvBESuYhuXDWrdB5zvMu0TgAIAwUXW1cwWPF+ pc5-qa@aicrm
) > "C:\ProgramData\ssh\administrators_authorized_keys"
icacls "C:\ProgramData\ssh\administrators_authorized_keys" /inheritance:r /grant "BUILTIN\Administrators:(R)" /grant "NT AUTHORITY\SYSTEM:(R)" /q
echo DONE > D:\DevProjects\ai-crm\scripts\fix_result.txt
