"""Sprint 7: Automated fixes for all remaining issues"""
import os, re

BASE = r'd:\DevProjects\ai-crm'

# === 1. KnowledgePage XSS Fix ===
kp_path = os.path.join(BASE, 'frontend/src/views/knowledge/KnowledgePage.vue')
with open(kp_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Insert HTML escape before markdown rendering
old_marker = 'function renderMarkdownPreview(content: string): string {'
idx = content.find(old_marker)
brace_idx = content.find('{', idx) + 1
newline_idx = content.find('\n', brace_idx) + 1

safe_line = '  const safe = content.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");\n'

# Replace '  return content' with '  return safe'
content = content[:newline_idx] + safe_line + content[newline_idx:]
content = content.replace('\n  return content\n', '\n  return safe\n')

with open(kp_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('1. KnowledgePage XSS fixed')

# === 2. Register All API Routers ===
init_path = os.path.join(BASE, 'backend/app/api/v1/__init__.py')
router_code = '''from fastapi import APIRouter
router = APIRouter()

from app.api.v1.bidding import router as br; router.include_router(br, prefix="/bidding", tags=["Bidding"])
from app.api.v1.projects import router as pr; router.include_router(pr, prefix="/projects", tags=["Projects"])
from app.api.v1.organizations import router as or_; router.include_router(or_, prefix="/organizations", tags=["Organizations"])
from app.api.v1.customers import router as cr; router.include_router(cr, prefix="/customers", tags=["Customers"])
from app.api.v1.auth import router as ar; router.include_router(ar, prefix="/auth", tags=["Auth"])
from app.api.v1.ai_diagnosis import router as dr; router.include_router(dr, prefix="/ai/diagnosis", tags=["AI Diagnosis"])
from app.api.v1.ai_sales import router as asr; router.include_router(asr, prefix="/ai/sales", tags=["AI Sales"])
from app.api.v1.ai_marketing import router as amr; router.include_router(amr, prefix="/ai/marketing", tags=["AI Marketing"])
from app.api.v1.ai_service import router as avr; router.include_router(avr, prefix="/ai/service", tags=["AI Service"])
from app.api.v1.decision_chain import router as dcr; router.include_router(dcr, prefix="/decision-chain", tags=["Decision Chain"])
from app.api.v1.knowledge import router as kr; router.include_router(kr, prefix="/knowledge", tags=["Knowledge"])
from app.api.v1.service_tickets import router as str_; router.include_router(str_, prefix="/service/tickets", tags=["Tickets"])
from app.api.v1.system import router as sr; router.include_router(sr, prefix="/system", tags=["System"])
from app.api.v1.system_admin import router as sar; router.include_router(sar, prefix="/system/admin", tags=["Admin"])
from app.api.v1.workflow import router as wr; router.include_router(wr, prefix="/workflow", tags=["Workflow"])
'''
with open(init_path, 'w', encoding='utf-8') as f:
    f.write(router_code)
print('2. 15 API routers registered')

# Also update main.py to use the new __init__ router
main_path = os.path.join(BASE, 'backend/app/main.py')
with open(main_path, 'r', encoding='utf-8') as f:
    main_content = f.read()

# Replace individual router imports with single init import
old_routers = """from app.api.v1.bidding import router as bid_router
from app.api.v1.projects import router as proj_router
from app.api.v1.organizations import router as org_router
from app.api.v1.auth import router as auth_router
from app.api.v1.customers import router as cust_router

app.include_router(bid_router, prefix=\"/api/v1/bidding\", tags=[\"Bidding\"])
app.include_router(proj_router, prefix=\"/api/v1/projects\", tags=[\"Projects\"])
app.include_router(org_router, prefix=\"/api/v1/organizations\", tags=[\"Organizations\"])
app.include_router(auth_router, prefix=\"/api/v1/auth\", tags=[\"Auth\"])
app.include_router(cust_router, prefix=\"/api/v1/customers\", tags=[\"Customers\"])"""

new_routers = """from app.api.v1 import router as v1_router
app.include_router(v1_router, prefix=\"/api/v1\")"""

if old_routers in main_content:
    main_content = main_content.replace(old_routers, new_routers)
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(main_content)
    print('   main.py updated to use v1 router')
else:
    print('   main.py already using v1 router or different format')

# === 3. Rate Limiter Redis Note ===
rl_path = os.path.join(BASE, 'backend/app/core/rate_limit.py')
with open(rl_path, 'a', encoding='utf-8') as f:
    f.write('\n# TODO(Sprint7): Redis backend - replace dict with Redis sorted sets for production\n')
print('3. Rate limiter Redis note added')

# === 4. Fix credentials in apple-style.py ===
as_path = os.path.join(BASE, 'scripts/apple-style.py')
with open(as_path, 'r', encoding='utf-8') as f:
    as_content = f.read()

as_content = as_content.replace(
    "client.connect('106.55.106.85', username='root', password='Admin@90088*', timeout=15)",
    "host = os.environ.get('DEPLOY_HOST', 'localhost')\n"
    "user = os.environ.get('DEPLOY_USER', 'root')\n"
    "pwd = os.environ.get('DEPLOY_PASSWORD', '')\n"
    "if not pwd: raise RuntimeError('Set DEPLOY_PASSWORD env var')\n"
    "client.connect(host, username=user, password=pwd, timeout=15)"
)
if 'import os' not in as_content[:50]:
    as_content = 'import os\n' + as_content

with open(as_path, 'w', encoding='utf-8') as f:
    f.write(as_content)
print('4. Credentials moved to env vars')

print('\n=== Sprint 7 fixes complete ===')
