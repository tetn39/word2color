import asyncio
import aiohttp
from PIL import Image
from io import BytesIO
from colorthief import ColorThief
import os
from serpapi import GoogleSearch
from dotenv import load_dotenv

# Google検索用APIのキー（SerpAPI）
load_dotenv()
API_KEY = os.getenv("SERP_API_KEY")

COLOR_LIMIT = 10
COLOR_GET_NUM = 5

# 非同期で画像検索を行い、10枚の画像URLを取得する関数
async def fetch_image_urls(query: str) -> list:
    params = {
        "q": query,
        "tbm": "isch",  # 画像検索
        "ijn": "0",  # ページインデックス
        "api_key": API_KEY,
    }
    async with aiohttp.ClientSession() as session:
        search = GoogleSearch(params)
        results = search.get_dict()
        images_results = results.get("images_results", [])
        print(f"Found {len(images_results)} images.")
        image_urls = [img["original"] for img in images_results[:10]]  # 最大10枚を取得
        return image_urls

# 非同期で画像URLから主要な色を抽出する関数
async def extract_colors_from_image(image_url: str) -> list:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                if response.status != 200:
                    print(f"画像のダウンロードに失敗しました: {response.status}")
                    return []

                # 画像の取得
                img_data = await response.read()
                img = Image.open(BytesIO(img_data))

                if img.mode != "RGB":
                    img = img.convert("RGB")

                # 一時ファイルに保存
                img_path = "temp_image.jpg"
                img.save(img_path)

                # 主要な色を抽出
                color_thief = ColorThief(img_path)
                dominant_colors = color_thief.get_palette(color_count=COLOR_GET_NUM)  # 5色のパレットを抽出

                # 一時ファイルを削除
                os.remove(img_path)

                return dominant_colors

    except Exception as e:
        print(f"画像の処理中にエラーが発生しました: {e}")
        return []

# 16進カラーコードに変換する関数
def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

# メイン処理を非同期にして並列化
async def get_color_code(query: str) -> list:

    # 画像URLの取得
    print(f"'{query}'の画像を検索しています...")
    image_urls = await fetch_image_urls(query)

    if not image_urls:
        print("画像が見つかりませんでした。")
        return []

    # 画像ごとに色を非同期に抽出
    tasks = []
    for url in image_urls:
        tasks.append(extract_colors_from_image(url))

    # 色抽出処理を並行して実行
    all_colors = await asyncio.gather(*tasks)

    # 取得した色を16進数形式に変換
    all_colors_hex = []
    color_cnt = 0
    for colors in all_colors:
        for color in colors:
            all_colors_hex.append(rgb_to_hex(color))
            color_cnt += 1
        if color_cnt >= COLOR_LIMIT:
            break

    return all_colors_hex
