import os
import json

# 修正导入路径为相对路径
from .services.qq_music import QQMusicService
from .services.netease_music import NeteaseMusicService
from .services.kugou_music import KugouMusicService


class MusicPlugin:
    def __init__(self):
        try:
            self.config = self.load_config()  # 加载配置文件
            self.services = self.load_services()  # 初始化服务
        except Exception as e:
            print(f"[MusicPlugin] Failed to initialize plugin: {e}")
            self.config = {}
            self.services = {}
        print("[MusicPlugin] Initialized")

    def load_config(self):
        """加载配置文件"""
        config_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "config.json")
        if not os.path.exists(config_path):
            raise FileNotFoundError("Configuration file config.json not found")
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_services(self):
        """加载服务实例"""
        services = {}
        config = self.config

        # 验证配置文件中的服务设置
        if not config:
            raise ValueError("Configuration is empty or invalid")

        # 初始化各音乐服务
        if config.get("qq_music"):
            services["qq"] = QQMusicService(config["qq_music"])
        if config.get("netease_music"):
            services["netease"] = NeteaseMusicService(config["netease_music"])
        if config.get("kugou_music"):
            services["kugou"] = KugouMusicService(config["kugou_music"])

        return services

    def handle_context(self, context):
        """处理上下文中的点歌指令"""
        if context.type != "TEXT":
            return

        content = context.content.strip()
        if not content.startswith("点歌 "):
            return

        # 解析指令
        parts = content.split(" ", 2)
        if len(parts) < 3:
            return self.reply("ERROR", "格式错误，请使用：点歌 [平台名称] [关键词]")

        platform_name, keyword = parts[1], parts[2]
        platform_map = {
            "网易云": "netease",
            "QQ": "qq",
            "酷狗": "kugou",
        }
        platform = platform_map.get(platform_name)
        if not platform:
            return self.reply("ERROR", f"不支持的平台：{platform_name}")

        service = self.services.get(platform)
        if not service:
            return self.reply("ERROR", f"未配置服务：{platform_name}")

        try:
            result = service.search_song(keyword)
            if result:
                # 返回卡片消息格式
                return self.reply("CARD", {
                    "type": "music",
                    "title": result["name"],
                    "description": result["artist"],
                    "music_url": result["url"],
                    "hq_music_url": result["url"],
                    "thumb_media_id": result["cover"],
                })
            else:
                return self.reply("INFO", "未找到相关歌曲，请尝试其他关键词。")
        except Exception as e:
            print(f"Error while searching song: {e}")
            return self.reply("ERROR", "搜索歌曲时发生错误，请稍后重试。")

    def reply(self, reply_type, content):
        """封装回复"""
        return {"type": reply_type, "content": content}