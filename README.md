# BiliDanmakuProtobufDownloader Bilibili弹幕获取工具
项目本身无使用意义，需搭配另外两个工具使用（尚未完善）  
分别是`ProtobufCSV2XML`与`BiliDanmakuDiff`。

## 特别感谢
实现方法来源于[SocialSisterYi/bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect)，感谢各位大佬的贡献！
参考文档：[Protobuf弹幕](https://socialsisteryi.github.io/bilibili-API-collect/docs/danmaku/danmaku_proto.html)。

## 更新计划
本项目最初是为《【高清修复】东方幻想万华镜全集》补档工作而设计，尽管现已结束补档工作，但本项目将继续作为练手作继续练习开发、维护。

## 功能描述
本脚本基于Python 3.10，使用B站新的默认弹幕 API 获取弹幕。  
新的 API 以`6min`为一个单位加载，部分视频在无`Cookie: SESSDATA`时只返回部分弹幕。
只能返回普通弹幕`（pool=1 mode=1-7）`和代码弹幕`（pool=2 mode=8）`。

## 使用说明  
1.安装运行环境`request` `protubuf`
2.下载`BiliDanmakuProtobufDownloader.py`
3.打开`BiliDanmakuProtobufDownloader.py`，填入希望获取的视频信息、COOKIE与输出文件路径  

**建议**前往[BAC](https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/grpc_api/bilibili/community/service/dm/v1/dm.proto)获取`dm.proto`，自行生成`dm_pb2.py`与同一目录下  
或者直接下载项目中提供的`dm_pb2.py`
