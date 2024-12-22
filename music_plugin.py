from plugins import register, Plugin, Event, EventContext, EventAction, ContextType, ReplyType, Reply
from services.qq_music import QQMusicService
from services.netease_music import NeteaseMusicService
from services.kugou_music import KugouMusicService
import json
import logging

logger = logging.getLogger(__name__)

@register(name="MusicPlugin", desc="支持QQ音乐、网易云音乐和酷狗音乐点歌", version="1.0", author="User", desire_priority=1)
class MusicPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.handle_context
        with open("config.json", "r") as f:
            config = json.load(f)
        self.services = {
            "qq": QQMusicService(config["qq_music"]),
            "netease": NeteaseMusicService(config["netease_music"]),
            "kugou": KugouMusicService(config["kugou_music"]),
        }
        logger.info("[MusicPlugin] Initialized")

    def handle_context(self, e_context: EventContext):
        context = e_context["context"]
        if context.type != ContextType.TEXT:
            return

        content = context.content.strip().lower()
        if content.startswith("点歌 "):  # 例如：点歌 keyword
            platform, *keywords = content.split(" ", 2)
            if len(keywords) < 2:
                reply = Reply(type=ReplyType.TEXT, content="格式错误，请使用：点歌 [平台] [关键词]")
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS
                return

            platform, keyword = keywords[0], keywords[1]
            if platform not in self.services:
                reply = Reply(type=ReplyType.TEXT, content=f"不支持的平台：{platform}")
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS
                return

            service = self.services[platform]
            result = service.search_song(keyword)
            if result:
                reply_content = f"找到歌曲：{result['name']} - {result['artist']}\n播放地址：{result['url']}"
            else:
                reply_content = "未找到相关歌曲，请尝试其他关键词。"

            reply = Reply(type=ReplyType.TEXT, content=reply_content)
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS