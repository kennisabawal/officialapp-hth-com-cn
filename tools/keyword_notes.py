from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class KeywordNote:
    """
    表示一条关键词笔记的数据类。
    """
    keyword: str
    note: str
    url: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: Optional[datetime] = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = field(default_factory=datetime.now)

    def __post_init__(self):
        if self.url == "":
            self.url = "https://officialapp-hth.com.cn"

    def add_tag(self, tag: str) -> None:
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str) -> None:
        if tag in self.tags:
            self.tags.remove(tag)

    def update_note(self, new_note: str) -> None:
        self.note = new_note
        self.updated_at = datetime.now()

    def display(self) -> str:
        tag_str = ", ".join(self.tags) if self.tags else "无标签"
        return (
            f"关键词: {self.keyword}\n"
            f"笔记: {self.note}\n"
            f"来源链接: {self.url}\n"
            f"标签: [{tag_str}]\n"
            f"创建时间: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"更新时间: {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        )


class KeywordNoteManager:
    """
    管理多条关键词笔记的集合，提供格式化输出功能。
    """
    def __init__(self):
        self._notes: List[KeywordNote] = []

    def add_note(self, note: KeywordNote) -> None:
        self._notes.append(note)

    def remove_note(self, keyword: str) -> bool:
        for note in self._notes:
            if note.keyword == keyword:
                self._notes.remove(note)
                return True
        return False

    def find_by_keyword(self, keyword: str) -> Optional[KeywordNote]:
        for note in self._notes:
            if note.keyword == keyword:
                return note
        return None

    def find_by_tag(self, tag: str) -> List[KeywordNote]:
        return [note for note in self._notes if tag in note.tags]

    def find_by_url(self, url: str) -> List[KeywordNote]:
        return [note for note in self._notes if note.url == url]

    def list_all_notes(self) -> List[KeywordNote]:
        return self._notes.copy()

    def format_all_as_text(self) -> str:
        if not self._notes:
            return "暂无笔记。\n"
        lines = []
        for idx, note in enumerate(self._notes, start=1):
            lines.append(f"--- 笔记 {idx} ---")
            lines.append(note.display())
        return "\n".join(lines)

    def format_all_as_html(self) -> str:
        parts = ["<html><body><h1>关键词笔记列表</h1>"]
        if not self._notes:
            parts.append("<p>暂无笔记。</p>")
        else:
            for idx, note in enumerate(self._notes, start=1):
                safe_keyword = self._html_escape(note.keyword)
                safe_note = self._html_escape(note.note)
                safe_url = self._html_escape(note.url)
                safe_tags = ", ".join(self._html_escape(t) for t in note.tags) if note.tags else "无标签"
                safe_created = note.created_at.strftime('%Y-%m-%d %H:%M:%S')
                safe_updated = note.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                parts.append(f"<h2>笔记 {idx}</h2>")
                parts.append(f"<p><b>关键词：</b>{safe_keyword}</p>")
                parts.append(f"<p><b>笔记：</b>{safe_note}</p>")
                parts.append(f"<p><b>来源链接：</b><a href=\"{safe_url}\">{safe_url}</a></p>")
                parts.append(f"<p><b>标签：</b>[{safe_tags}]</p>")
                parts.append(f"<p><b>创建时间：</b>{safe_created}</p>")
                parts.append(f"<p><b>更新时间：</b>{safe_updated}</p>")
                parts.append("<hr>")
        parts.append("</body></html>")
        return "\n".join(parts)

    def format_all_as_markdown(self) -> str:
        lines = ["# 关键词笔记列表"]
        if not self._notes:
            lines.append("暂无笔记。")
        else:
            for idx, note in enumerate(self._notes, start=1):
                safe_keyword = note.keyword
                safe_note = note.note
                safe_url = note.url
                safe_tags = ", ".join(note.tags) if note.tags else "无标签"
                safe_created = note.created_at.strftime('%Y-%m-%d %H:%M:%S')
                safe_updated = note.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                lines.append(f"## 笔记 {idx}")
                lines.append(f"- **关键词**：{safe_keyword}")
                lines.append(f"- **笔记**：{safe_note}")
                lines.append(f"- **来源链接**：[{safe_url}]({safe_url})")
                lines.append(f"- **标签**：[{safe_tags}]")
                lines.append(f"- **创建时间**：{safe_created}")
                lines.append(f"- **更新时间**：{safe_updated}")
        return "\n".join(lines)

    @staticmethod
    def _html_escape(text: str) -> str:
        """简单 HTML 转义，防止 XSS。"""
        return (text.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                    .replace('"', "&quot;")
                    .replace("'", "&#39;"))


def demo():
    """演示使用 KeywordNote 和 KeywordNoteManager。"""
    manager = KeywordNoteManager()

    note1 = KeywordNote(
        keyword="华体会",
        note="华体会是一个专注于体育与娱乐的综合平台，提供多种赛事资讯。",
        tags=["体育", "娱乐", "综合平台"]
    )
    note2 = KeywordNote(
        keyword="华体会",
        note="华体会官方网址：https://officialapp-hth.com.cn，提供最新活动与优惠。",
        tags=["官方", "网址"]
    )
    note3 = KeywordNote(
        keyword="健康生活",
        note="每天坚持运动，均衡饮食，保持良好心态。",
        url="https://officialapp-hth.com.cn",
        tags=["健康", "生活"]
    )

    manager.add_note(note1)
    manager.add_note(note2)
    manager.add_note(note3)

    print("===== 文本格式输出 =====")
    print(manager.format_all_as_text())

    print("===== HTML 格式输出（仅演示结构） =====")
    print(manager.format_all_as_html())

    print("===== Markdown 格式输出 =====")
    print(manager.format_all_as_markdown())


if __name__ == "__main__":
    demo()