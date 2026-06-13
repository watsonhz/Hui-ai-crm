# Sprint4 安全审查清单 — BPM流程注入 + 登录安全 + 图表XSS

## 1. BPM 工作流注入

### XXE / XML 注入
- [ ] BPMN XML 解析是否禁用外部实体 (resolve_entities=False)
- [ ] 流程定义上传是否校验 XML 格式
- [ ] 是否使用 defusedxml 或安全解析器
- [ ] 流程变量是否直接拼入 SQL/命令执行

### 审批权限
- [ ] 审批动作是否校验用户角色+节点权限
- [ ] 是否有越权审批（非审批人直接调 API）
- [ ] 流程驳回/撤回是否校验操作者身份
- [ ] 代理审批（delegate）是否有权限校验

### 流程变量泄露
- [ ] 流程变量是否跨租户/跨用户可见
- [ ] 审批历史中是否暴露敏感变量

**审计命令**:
```bash
grep -rn "etree\|ElementTree\|lxml\|defusedxml\|xml" backend/ --include="*.py"
grep -rn "approve\|reject\|delegate\|claim\|complete" backend/app/api/v1/
```

---

## 2. 登录认证安全

### JWT 机制
- [ ] 是否支持 Token 刷新 (refresh_token)
- [ ] 是否有 Token 黑名单/撤销机制 (logout)
- [ ] refresh_token 是否一次性使用 (rotation)
- [ ] Token 是否存储在 httpOnly cookie (防 XSS 窃取)

### 暴力破解防护
- [ ] 登录失败是否递增计数
- [ ] 连续失败 N 次后是否锁定 (建议 5 次 / 15 分钟)
- [ ] 是否记录登录失败来源 IP
- [ ] 是否有人机验证 (验证码)

### 短信验证码
- [ ] 发送是否有频率限制 (同一手机号 60s 内不重发)
- [ ] 验证码是否有过期时间 (建议 5 分钟)
- [ ] 验证码是否与手机号+session 绑定
- [ ] 同一手机号每日发送上限

### 微信 OAuth
- [ ] state 参数是否为随机值 + session 绑定
- [ ] 是否校验 redirect_uri 白名单
- [ ] code 是否一次性使用

**审计命令**:
```bash
grep -rn "login\|logout\|refresh\|revoke\|token" backend/app/api/v1/auth.py
grep -rn "sms\|verify_code\|rate_limit\|throttle" backend/ --include="*.py"
grep -rn "wechat\|oauth\|state\|openid" backend/ --include="*.py"
```

---

## 3. 图表 XSS + 数据权限

### ECharts 注入
- [ ] 用户数据是否直接赋给 ECharts option（无转义）
- [ ] 图表 label/formatter 中是否包含用户可控字符串
- [ ] tooltip formatter 自定义函数是否安全
- [ ] 图表数据是否有 XSS 编码

### 驾驶舱权限
- [ ] 驾驶舱数据是否按用户权限过滤
- [ ] 图表 API 是否校验数据归属
- [ ] 导出功能是否有权限校验

**审计命令**:
```bash
grep -rn "setOption\|echarts\|formatter\|tooltip\|label" frontend/src/ --include="*.vue" --include="*.ts"
grep -rn "dangerouslySetInnerHTML\|v-html\|innerHTML" frontend/src/views/dashboard/
grep -rn "dashboard\|chart\|驾驶舱\|报表" frontend/src/ --include="*.vue"
```

---

## 4. 公共检查

- [ ] 所有新端点有 `Depends(get_current_user)`
- [ ] 审批/图表 API 有速率限制
- [ ] 错误信息不泄露内部逻辑

## Sprint4 风险矩阵

| 风险 | 概率 | 影响 | 优先级 |
|------|:--:|:--:|:--:|
| XXE via BPMN XML | 中 | 极高 | **P0** |
| 越权审批 | 高 | 高 | **P0** |
| 暴力破解无锁定 | 高 | 高 | **P0** |
| ECharts XSS | 中 | 高 | **P1** |
| 短信接口被刷 | 高 | 中 | **P1** |
| Token 无撤销 | 中 | 中 | **P2** |
