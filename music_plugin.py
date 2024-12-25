import os
import json
from plugins import register, Plugin, Event, EventContext, EventAction
from .services.qq_music import QQMusicService
from .services.netease_music import NeteaseMusicService
from .services.kugou_music import KugouMusicService
from enum import Enum

# 定义消息和回复类型
class ContextType(Enum):
    TEXT = 1
    VOICE = 2
    IMAGE_CREATE = 3

class ReplyType(Enum):
    TEXT = 1
    INFO = 9
    ERROR = 10

class Reply:
    def __init__(self, type: ReplyType, content: str):
        self.type = type
        self.content = content

@register(name="MusicPlugin", desc="支持QQ音乐、网易云音乐和酷狗音乐点歌", version="1.0", author="User", desire_priority=10)
class MusicPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.handle_context
        self.config_path = "config.json"
        self.services = self.load_services()

    def load_services(self):
        # 加载配置并初始化服务
        if not os.path.exists(self.config_path):
            raise FileNotFoundError("Config file not found: config.json")
        with open(self.config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        return {
            "qq": QQMusicService(config.get("qq_music", {})),
            "netease": NeteaseMusicService(config.get("netease_music", {})),
            "kugou": KugouMusicService(config.get("kugou_music", {})),
        }

    def handle_context(self, e_context: EventContext):
        context = e_context["context"]
        if context.type != ContextType.TEXT:
            return

        content = context.content.strip().lower()
        if content.startswith("点歌 "):  # 处理点歌指令
            parts = content.split(" ", 2)
            if len(parts) < 3:
                e_context["reply"] = Reply(ReplyType.ERROR, "格式错误，请使用：点歌 [平台] [关键词]")
                e_context.action = EventAction.BREAK_PASS
                return

            platform, keyword = parts[1], parts[2]
            service = self.services.get(platform)
            if not service:
                e_context["reply"] = Reply(ReplyType.ERROR, f"不支持的平台：{platform}")
                e_context.action = EventAction.BREAK_PASS
                return

            result = service.search_song(keyword)
            if result:
                reply_content = f"找到歌曲：{result['name']} - {result['artist']}\n播放地址：{result['url']}"
                e_context["reply"] = Reply(ReplyType.TEXT, reply_content)
            else:
                e_context["reply"] = Reply(ReplyType.INFO, "未找到相关歌曲，请尝试其他关键词。")
            e_context.action = EventAction.BREAK_PASS