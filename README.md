# AI-CRM 企业级政企大B客户管理系统

## 系统简介
基于 DeepSeek V4 AI 的企业级客户关系管理系统，面向政府机关、事业单位、
国有企业、大型集团等政企大B客户。覆盖6大基础业务模块 + 7大AI赋能模块
+ 5大行业应用 + LTC全链路，共115+项功能。

## 技术架构
- 后端：Spring Cloud / Go / Python（自主选型）
- 前端：Vue3 + Element Plus / Ant Design Vue / Vben5（自主选型）
- 数据库：PostgreSQL 15+ + PGVector（向量检索）
- 缓存：Redis 7.x
- AI引擎：DeepSeek V4（主）+ 通义千问（备）+ RAG知识库
- 工作流：Flowable（BPM）
- 协作：SSH + Git + Claude Code Agent

## 团队角色（5机集群）
- PC1 (192.168.0.168): CEO指挥中心 · 三级审查终审者
- PC2 (192.168.0.169): PM + 前端开发 + UI/UX
- PC3 (192.168.0.170): 后端架构师 + DevOps
- PC4 (192.168.0.171): 安全审计 + 技术文档 · 一级审查
- PC5 (192.168.0.253): QA测试(专任) · 二级审查
