from bridge.bridge import register, Plugin, Event, EventContext, EventAction
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from config import conf
import logging
import os
import json
from .services.qq_music import QQMusicService
from .services.netease_music import NeteaseMusicService
from .services.kugou_music import KugouMusicService

logger = logging.getLogger(__name__)

@register(
    name="MusicPlugin",
    desc="支持QQ音乐、网易云音乐和酷狗音乐点歌",
    version="1.0",
    author="User",
    desire_priority=10,
)
def validate_config(config):
    """验证配置文件的必要参数"""
    required_platforms = ["qq_music", "netease_music", "kugou_music"]
    for platform in required_platforms:
        if platform not in config:
            logger.warning(f"[MusicPlugin] {platform} configuration missing")

class MusicPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.handle_context
        self.config = conf()  # 加载全局配置
        try:
            self.services = self.load_services()
        except Exception as e:
            logger.error(f"[MusicPlugin] Failed to initialize services: {str(e)}")
            self.services = {}
        logger.info("[MusicPlugin] Initialized")
def validate_config(config):
    """验证配置文件的必要参数"""
    required_platforms = ["qq_music", "netease_music", "kugou_music"]
def load_services(self):
        """加载音乐服务配置"""
        services = {}
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
        
        # 如果配置文件不存在，尝试使用模板文件
        if not os.path.exists(config_path):
            template_path = config_path + ".template"
            if os.path.exists(template_path):
                config_path = template_path
            else:
                raise FileNotFoundError("Neither config.json nor config.json.template found")
        
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            
        validate_config(config)
        
        if config.get("qq_music"):
            services["qq"] = QQMusicService(config["qq_music"])
        if config.get("netease_music"):
            services["netease"] = NeteaseMusicService(config["netease_music"])
        if config.get("kugou_music"):
            services["kugou"] = KugouMusicService(config["kugou_music"])
        
        return services
    with open(config_path, "r", encoding="utf-8")
        config = json.load(f)
        
    validate_config(config)
    
    if config.get("qq_music"):
        services["qq"] = QQMusicService(config["qq_music"])
    if config.get("netease_music"):
        services["netease"] = NeteaseMusicService(config["netease_music"])
    if config.get("kugou_music"):
        services["kugou"] = KugouMusicService(config["kugou_music"])
    
    return services
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.handle_context
        self.config = conf()  # 加载全局配置
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
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
            "netease": NeteaseMusicService(config.get("netease_music", {})),
            "kugou": KugouMusicService(config.get("kugou_music", {})),
        }

    def handle_context(self, e_context: EventContext):
        """处理上下文中的点歌指令"""
        context = e_context["context"]
        if context.type != ContextType.TEXT:
            return

        # 判断是否为点歌指令
        content = context.content.strip()
        if content.startswith("点歌 "):  # 处理点歌指令
            parts = content.split(" ", 2)
            if len(parts) < 3:
                e_context["reply"] = Reply(ReplyType.ERROR, "格式错误，请使用：点歌 [平台名称] [关键词]")
                e_context.action = EventAction.BREAK_PASS
                return

            # 获取平台名称和关键词
            platform_name = parts[1]
            keyword = parts[2]

            # 将中文平台名称映射为内部服务名称
            platform_map = {
                "网易云": "netease",
                "QQ": "qq",
                "酷狗": "kugou",
            }
            platform = platform_map.get(platform_name)

            if not platform:
                e_context["reply"] = Reply(ReplyType.ERROR, f"不支持的平台：{platform_name}")
                e_context.action = EventAction.BREAK_PASS
                return

            # 调用对应平台服务
            service = self.services.get(platform)
            if not service:
                e_context["reply"] = Reply(ReplyType.ERROR, f"未配置服务：{platform_name}")
                e_context.action = EventAction.BREAK_PASS
                return

            try:
                # 调用服务搜索歌曲
                result = service.search_song(keyword)
                if result:
                    # 构造音乐卡片格式
                    card_message = {
                        "type": "music",
                        "title": result["name"],
                        "description": result["artist"],
                        "music_url": result["url"],  # 播放链接
                        "hq_music_url": result["url"],  # 高品质链接
                        "thumb_media_id": result["cover"],  # 封面图片
                    }
                    e_context["reply"] = Reply(ReplyType.CARD, card_message)
                else:
                    e_context["reply"] = Reply(ReplyType.INFO, "未找到相关歌曲，请尝试其他关键词。")
            except Exception as e:
                logger.error(f"Error while searching song: {e}")
                e_context["reply"] = Reply(ReplyType.ERROR, "搜索歌曲时发生错误，请稍后重试。")
            e_context.action = EventAction.BREAK_PASS
