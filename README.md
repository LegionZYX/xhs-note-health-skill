# XHS Note Health Checker Skill

小红书笔记健康检测 AI Agent Skill。

## 功能

- Level 状态解读（4 到 -102）
- 敏感词检测（AI/自动化、极限词、虚假承诺、医疗功效、引流、诱导互动等）
- 标签数量检测（>5 警告）
- 优化建议生成

## 安装

将 `xhs-note-health.skill` 文件导入到你的 AI Agent 工具中。

## 使用

```bash
python scripts/xhs_health.py "<标题>" <level> [标签数]
```

示例：
```bash
python scripts/xhs_health.py "我的日常vlog" 2 4
```

## Level 含义

| Level | 状态 | 说明 |
|-------|------|------|
| 4 | 正常推荐 | 笔记正常分发 |
| 2 | 基本正常 | 轻微受限 |
| 1 | 新帖初始 | 刚发布，等待审核 |
| -1 | 轻度限流 | 推荐量明显下降 |
| -5 | 中度限流 | 几乎无推荐 |
| -102 | 严重限流 | 不可逆，需删除重发 |

## License

MIT
