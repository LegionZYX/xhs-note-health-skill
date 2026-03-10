#!/usr/bin/env python3
"""小红书笔记健康检测脚本"""

import re
from dataclasses import dataclass
from typing import Optional

SENSITIVE_WORDS = [
    "AI生成", "AI自动", "AI创作", "自动化", "自动发布", "自动工作流",
    "全自动", "批量", "内容工厂", "矩阵号",
    "最好", "最佳", "最强", "最便宜", "最低价", "全网最低",
    "第一", "NO.1", "TOP1", "唯一", "顶级", "极致", "巅峰",
    "独一无二", "全国第一", "世界级", "国家级",
    "包过", "稳赚不赔", "零风险", "永久", "万能", "100%",
    "根治", "特效", "一次见效", "立竿见影", "秒变",
    "一洗白", "一抹就瘦", "防脱发", "改善睡眠",
    "微信", "加V", "+V", "VX", "wx",
    "互粉", "互关", "求关注", "求点赞", "求收藏", "一键三连",
    "秒杀", "抢疯了", "再不抢就没了", "随时涨价",
    "招财进宝", "旺夫"
]

LEVEL_META = {
    4: {"label": "L4 正常", "emoji": "🟢", "desc": "正常推荐"},
    2: {"label": "L2 基本", "emoji": "🟡", "desc": "基本正常"},
    1: {"label": "L1 新帖", "emoji": "⚪", "desc": "新帖初始"},
    -1: {"label": "L-1 限流", "emoji": "🔴", "desc": "轻度限流"},
    -5: {"label": "L-5 中度", "emoji": "🔴🔴", "desc": "中度限流"},
    -102: {"label": "L-102 严重", "emoji": "⛔", "desc": "严重限流"},
}

@dataclass
class NoteHealth:
    title: str
    level: int
    tag_count: int
    sensitive_hits: list[str]
    
    @property
    def level_meta(self) -> dict:
        if self.level <= -102:
            return LEVEL_META[-102]
        if self.level <= -5:
            return {"label": f"L{self.level} 中度", "emoji": "🔴🔴", "desc": "中度限流"}
        if self.level <= -1:
            return LEVEL_META[-1]
        if self.level >= 4:
            return LEVEL_META[4]
        if self.level >= 2:
            return {"label": f"L{self.level} 基本", "emoji": "🟡", "desc": "基本正常"}
        return {"label": f"L{self.level}", "emoji": "⚪", "desc": "未知状态"}
    
    @property
    def is_healthy(self) -> bool:
        return self.level >= 1 and len(self.sensitive_hits) == 0 and self.tag_count <= 5
    
    @property
    def tag_warning(self) -> bool:
        return self.tag_count > 5

def check_sensitive(title: str) -> list[str]:
    return [w for w in SENSITIVE_WORDS if w in title]

def analyze_note(title: str, level: int, tag_count: int = 0) -> NoteHealth:
    return NoteHealth(
        title=title,
        level=level,
        tag_count=tag_count,
        sensitive_hits=check_sensitive(title)
    )

def format_report(health: NoteHealth) -> str:
    meta = health.level_meta
    lines = [
        "## 笔记健康报告",
        "",
        f"**Level 状态**: {meta['label']} {meta['emoji']}",
        f"**标题**: {health.title}",
        "",
        "### 检测结果",
    ]
    
    if health.sensitive_hits:
        lines.append(f"- ⚠️ **敏感词检测**: 命中 {len(health.sensitive_hits)} 个 - {', '.join(health.sensitive_hits)}")
    else:
        lines.append("- ✅ **敏感词检测**: 未命中")
    
    if health.tag_warning:
        lines.append(f"- ⚠️ **标签数量**: {health.tag_count} 个（建议不超过5个）")
    else:
        lines.append(f"- ✅ **标签数量**: {health.tag_count} 个")
    
    lines.append("")
    lines.append("### 优化建议")
    
    suggestions = []
    
    if health.level < 1:
        if health.level == -102:
            suggestions.append("严重限流不可逆，建议删除后使用全新图片重新发布")
        elif health.level <= -5:
            suggestions.append("中度限流，检查内容是否违规，考虑修改或删除重发")
        else:
            suggestions.append("轻度限流，检查敏感词和内容质量，可尝试编辑优化")
    
    if health.sensitive_hits:
        suggestions.append(f"替换或删除敏感词：{', '.join(health.sensitive_hits)}")
    
    if health.tag_warning:
        suggestions.append(f"减少标签数量，保留最相关的 {min(5, health.tag_count)} 个")
    
    if not suggestions:
        suggestions.append("笔记状态良好，继续保持优质内容输出")
    
    for i, s in enumerate(suggestions, 1):
        lines.append(f"{i}. {s}")
    
    return "\n".join(lines)

if __name__ == "__main__":
    import sys
    import io
    
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    if len(sys.argv) < 3:
        print("用法: python xhs_health.py <标题> <level> [标签数]")
        print("示例: python xhs_health.py '我的笔记标题' -1 6")
        sys.exit(1)
    
    title = sys.argv[1]
    level = int(sys.argv[2])
    tag_count = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    
    health = analyze_note(title, level, tag_count)
    print(format_report(health))
