from plugins import register, Plugin, Event, EventContext, EventAction
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from config import conf
import logging
import os
import json
from .services.qq_music import QQMusicService

logger = logging.getLogger(__name__)

@register(
    name="MusicPlugin",
    desc="支持QQ音乐、网易云音乐和酷狗音乐点歌",
    version="1.0",
    author="User",
    desire_priority=10,
)
class MusicPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.handle_context
        self.config = conf()  # 加载全局配置
        self.services = self.load_services()
        logger.info("[MusicPlugin] Initialized")

    def load_services(self):
        # 加载服务配置
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        if not os.path.exists(config_path):
            raise FileNotFoundError("Config file not found: config.json")
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        return {
            "qq": QQMusicService(config.get("qq_music", {})),
        }

    def handle_context(self, e_context: EventContext):
        """处理上下文中的点歌指令"""
        context = e_context["context"]
        if context.type != ContextType.TEXT:
            return

        # 判断是否为点歌指令
        content = context.content.strip().lower()
        if content.startswith("点歌 "):  # 处理点歌指令
            parts = content.split(" ", 1)
            if len(parts) < 2:
                e_context["reply"] = Reply(ReplyType.ERROR, "格式错误，请使用：点歌 [关键词]")
                e_context.action = EventAction.BREAK_PASS
                return

            keyword = parts[1]
            service = self.services.get("qq")  # 使用 QQ 音乐服务
            result = service.search_song(keyword)
            if result:
                reply_content = f"🎵 找到歌曲：{result['name']} - {result['artist']}\n👉 [播放链接]({result['url']})"
                e_context["reply"] = Reply(ReplyType.TEXT, reply_content)
            else:
                e_context["reply"] = Reply(ReplyType.INFO, "未找到相关歌曲，请尝试其他关键词。")
            e_context.action = EventAction.BREAK_PASS