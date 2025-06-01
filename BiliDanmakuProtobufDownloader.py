import sys
import zlib
import time
import csv
import requests
from datetime import datetime
import dm_pb2 as Danmaku


# ————————————————————用户配置区————————————————————
BVID = "BV1VuZ5YjEin"  # 替换为要下载的视频BV号
PART_INDEX = 3  # 分P序号（从1开始计数）
COOKIE = ("SESSDATA=YourSESSDATA;"
          "bili_jct=Yourbili_jct")  # 替换为真实Cookie
REQUEST_INTERVAL = 1  # 请求间隔（秒）
MAX_RETRIES = 3  # 失败重试次数
OUTPUT_FILE = fr"C:\output\path\P{PART_INDEX}.csv"  # 输出文件名
# —————————————————————————————————————————————————

def get_video_info(bvid: str) -> dict:
    """获取视频元数据（cid/avid）"""
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": COOKIE
    }

    for _ in range(MAX_RETRIES):
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            data = resp.json()['data']

            # 获取所有分P信息
            pages = data['pages']
            if PART_INDEX > len(pages) or PART_INDEX < 1:
                raise ValueError(f"无效的分P序号，该视频共有 {len(pages)} 个分P")

            # 获取指定分P信息
            selected_page = pages[PART_INDEX - 1]
            return {
                "oid": selected_page['cid'],
                "pid": data['aid'],
                "title": f"{data['title']} - {selected_page['part']}"
            }
        except Exception as e:
            print(f"获取视频信息失败: {e}")
            time.sleep(REQUEST_INTERVAL)
    raise RuntimeError("无法获取视频信息")

def get_all_danmaku(oid: int, pid: int) -> list:
    """获取所有分段的弹幕数据"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Referer": f"https://www.bilibili.com/video/{BVID}",
        "Cookie": COOKIE
    }

    all_danmaku = []
    segment = 1

    while True:
        print(f"正在获取第 {segment} 段弹幕...")
        params = {
            "type": 1,
            "oid": oid,
            "pid": pid,
            "segment_index": segment
        }

        # 请求重试
        for retry in range(MAX_RETRIES):
            try:
                resp = requests.get(
                    "https://api.bilibili.com/x/v2/dm/web/seg.so",
                    params=params,
                    headers=headers,
                    timeout=15
                )
                resp.raise_for_status()
                break
            except Exception as e:
                if retry == MAX_RETRIES - 1:
                    print(f"第 {segment} 段请求失败，终止获取")
                    return all_danmaku
                print(f"请求失败，第 {retry + 1} 次重试...")
                time.sleep(REQUEST_INTERVAL)

        # 处理压缩数据
        try:
            data = zlib.decompress(resp.content)
        except zlib.error:
            data = resp.content

        # 解析Protobuf
        try:
            danmaku_seg = Danmaku.DmSegMobileReply()
            danmaku_seg.ParseFromString(data)
        except Exception as e:
            print(f"解析失败: {e}")
            print("错误数据头部:", data[:16].hex())
            break

        if not danmaku_seg.elems:
            print("已获取所有弹幕分段")
            break

        all_danmaku.extend(danmaku_seg.elems)
        print(f"成功获取 {len(danmaku_seg.elems)} 条弹幕")
        segment += 1
        time.sleep(REQUEST_INTERVAL)

    return all_danmaku


def save_complete_data(danmaku_list: list, filename: str):
    """保存完整弹幕数据到CSV"""
    fields_order = [
        ("id", "弹幕ID"),
        ("progress", "出现时间(毫秒)"),
        ("mode", "模式"),
        ("fontsize", "字体大小"),
        ("color", "颜色"),
        ("midHash", "用户MID哈希"),
        ("content", "内容"),
        ("ctime", "发送时间"),
        ("weight", "权重"),
        ("action", "动作"),
        ("pool", "弹幕池"),
        ("idStr", "弹幕ID字符串"),
        ("attr", "属性"),
        ("animation", "动画")
    ]

    csv_headers = [col for _, col in fields_order]
    proto_fields = [field for field, _ in fields_order]

    with open(filename, "w", encoding="utf-8-sig", newline='') as f:
        writer = csv.writer(f)
        # 写入元数据
        writer.writerow(["视频标题", video_info['title']])
        writer.writerow(["视频BV号", BVID])
        writer.writerow(["分P序号", PART_INDEX])
        writer.writerow(["弹幕总数", len(danmaku_list)])
        writer.writerow(["导出时间", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        writer.writerow([])
        # 写入列标题
        writer.writerow(csv_headers)
        # 写入数据行
        for d in danmaku_list:
            row = []
            for field in proto_fields:
                try:
                    value = getattr(d, field)
                    # 特殊字段处理
                    if field == "color":
                        value = f"#{value:06x}"
                    elif field == "ctime":
                        value = datetime.fromtimestamp(value).strftime("%Y-%m-%d %H:%M:%S")
                    elif field == "weight":
                        value = max(0, min(int(value), 10))
                    elif field == "attr":
                        attr_value = int(value)
                        attributes = []
                        if attr_value & (1 << 0): attributes.append("保护")
                        if attr_value & (1 << 1): attributes.append("直播")
                        if attr_value & (1 << 2): attributes.append("高赞")
                        value = ",".join(attributes) if attributes else "普通"
                    row.append(str(value))
                except AttributeError:
                    row.append("N/A")
            writer.writerow(row)


# ————————————————————主程序————————————————————
if __name__ == "__main__":
    try:
        # 步骤1：获取视频信息
        print("正在获取视频元数据...")
        video_info = get_video_info(BVID)
        print(f"视频标题: {video_info['title']}")
        print(f"cid: {video_info['oid']}, avid: {video_info['pid']}")

        # 步骤2：获取所有弹幕
        print("\n开始获取弹幕...")
        danmaku_list = get_all_danmaku(video_info['oid'], video_info['pid'])

        # 步骤3：保存数据
        print("\n保存数据中...")
        save_complete_data(danmaku_list, OUTPUT_FILE)
        print(f"数据已保存到 {OUTPUT_FILE}")

    except Exception as e:
        print(f"程序运行出错: {str(e)}")
        sys.exit(1)