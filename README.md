# Music Plugin

## 插件简介

Music Plugin 是一个插件化的点歌工具，支持 QQ 音乐、网易云音乐和酷狗音乐三大音乐平台。用户可以通过简单的指令搜索歌曲，并返回对应的播放链接。

---

## 功能特性

- **支持多平台**：支持 QQ 音乐、网易云音乐、酷狗音乐的歌曲搜索和播放链接获取。
- **插件化设计**：符合标准的插件化结构，便于扩展和维护。
- **用户交互简单**：使用自然语言命令即可点歌，例如：`点歌 qq keyword`。
- **易于配置**：通过 JSON 文件管理 API 地址，方便修改。

---

## 安装方法

1. **准备工作**：
   - 确保安装了 Python 3.7 及以上版本。
   - 安装必要依赖：`pip install -r requirements.txt`。

2. **放置插件**：
   - 将 `plugin_music-master` 文件夹放入你的插件目录中。
   - 按照以下目录结构组织文件：
     ```
     plugin_music-master/
     │
     ├── __init__.py
     ├── requirements.txt
     ├── config.json.template
     ├── music_plugin.py
     ├── services/
     │   ├── __init__.py
     │   ├── qq_music.py
     │   ├── netease_music.py
     │   └── kugou_music.py
     └── README.md
     ```

3. **配置 API**：
   - 复制 `config.json.template` 并重命名为 `config.json`。
   - 填写 QQ 音乐、网易云音乐、酷狗音乐的 API 地址。例如：
     ```json
     {
         "qq_music": {
             "api_url": "https://api.qqmusic.com"
         },
         "netease_music": {
             "api_url": "https://api.netease.com"
         },
         "kugou_music": {
             "api_url": "https://api.kugou.com"
         }
     }
     ```

4. **启动插件**：
   - 按照主程序的插件加载方式，扫描并启动插件。

---

## 使用方法

1. 在聊天中输入以下命令以搜索歌曲：

使用方法

点歌 [平台] [关键词]

示例：

点歌 qq 稻香
点歌 netease 南山南
点歌 kugou 浪子回头


2. 插件会返回找到的歌曲名称、艺术家和播放链接。

---

## 文件说明

- `__init__.py`：插件入口逻辑，加载主程序的 `MusicPlugin`。
- `music_plugin.py`：插件的核心功能逻辑，包括事件处理和服务调用。
- `services/`：各音乐平台的实现，支持扩展更多平台。
- `qq_music.py`：QQ 音乐平台的搜索和播放链接获取。
- `netease_music.py`：网易云音乐平台的实现。
- `kugou_music.py`：酷狗音乐平台的实现。
- `config.json.template`：配置模板文件，需重命名为 `config.json` 并填写 API 地址。
- `requirements.txt`：插件所需的 Python 依赖。
- `README.md`：插件文档。

---

## 注意事项

1. 确保 API 地址有效，否则无法返回结果。
2. 插件对每个平台返回的数据结构有所依赖，如需调整，请修改对应的服务文件。
3. 插件事件处理基于 `ON_HANDLE_CONTEXT`，优先级默认为 `1`，可根据需求调整。

---

## 未来计划

- 添加更多音乐平台支持，如 Spotify、Apple Music。
- 增强搜索功能，支持多条件查询（例如艺术家、专辑等）。
- 增加播放列表支持，实现多首歌曲返回。

---

如需帮助或反馈问题，请随时联系开发者！