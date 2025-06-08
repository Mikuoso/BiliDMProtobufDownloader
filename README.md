# BiliDanmakuProtobufDownloader Bilibili弹幕获取工具
注：该项目已完成与[ProtobufCSV2XML](https://github.com/Mikuoso/ProtobufCSV2XML)的合并工作！  
现决定停止维护，请移步至[BiliDanmakuDownloader](https://github.com/Mikuoso/BiliDanmakuDownloader)！  

项目本身无使用意义，需搭配另外两个工具使用  
分别是[ProtobufCSV2XML](https://github.com/Mikuoso/ProtobufCSV2XML)与[BiliDanmakuDiff](https://github.com/Mikuoso/BiliDanmakuDiff)。

## 特别声明
本项目开发过程中参考了[SocialSisterYi/bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect)的实现思路，感谢各位大佬的贡献！  
源项目遵循 CC BY-NC 4.0 协议，禁止一切商业使用！！！  
参考文档：[Protobuf弹幕](https://socialsisteryi.github.io/bilibili-API-collect/docs/danmaku/danmaku_proto.html)。  

## 功能描述
本工具基于Python 3.10，用于下载B站视频的完整弹幕数据，支持分P视频选择，输出为包含完整元数据的CSV文件。

### 🚀 核心功能
- **分P选择**：精确获取指定分P的弹幕数据
- **完整元数据**：包含颜色、发送时间、用户哈希等15+个字段
- **分段下载**：自动处理多分段弹幕数据
- **数据压缩处理**：自动解压zlib压缩的Protobuf数据
- **容错机制**：请求重试+异常处理保障稳定性

### 📌 注意事项
- 部分视频在无`Cookie: SESSDATA`时只返回部分弹幕。  
- 只能返回普通弹幕`（pool=1 mode=1-7）`和代码弹幕`（pool=2 mode=8）`。

## 使用说明  
### 📦 依赖安装
```bash
# 安装必要库
pip install requests protobuf
```
### ⚙️ 配置说明
```python
BVID = "BV1VuZ5YjEin"        # 目标视频BV号（必填）
PART_INDEX = 3               # 分P序号（从1开始计数）
COOKIE = "SESSDATA=..."      # 用户身份Cookie（必填）
REQUEST_INTERVAL = 1         # 请求间隔
OUTPUT_FILE = r"C:\path.csv" # 输出文件路径
```  
  

**建议**前往[BAC](https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/grpc_api/bilibili/community/service/dm/v1/dm.proto)获取`dm.proto`，自行生成`dm_pb2.py`与同一目录下  
**生成命令**：`protoc --python_out=. dm.proto`  
或者直接下载项目中提供的`dm_pb2.py`

## 更新计划
本项目最初是为《【高清修复】东方幻想万华镜全集》补档工作而设计，已与[ProtobufCSV2XML](https://github.com/Mikuoso/ProtobufCSV2XML)合并为[BiliDanmakuDownloader](https://github.com/Mikuoso/BiliDanmakuDownloader)，现决定停止维护。
