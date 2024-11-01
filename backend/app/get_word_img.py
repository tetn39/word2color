import requests
from PIL import Image
from io import BytesIO
from colorthief import ColorThief
import os
from serpapi import GoogleSearch
from dotenv import load_dotenv

# Google検索用APIのキー（SerpAPI）
# dotenvから読み込む
load_dotenv()
API_KEY = os.getenv("SERP_API_KEY")

COLOR_LIMIT=10
COLOR_GET_NUM=5

# 画像検索を行い、20枚の画像URLを取得する関数
def fetch_image_urls(query: str) -> list:
    params = {
        "q": query,
        "tbm": "isch",  # 画像検索
        "ijn": "0",  # ページインデックス
        "api_key": API_KEY,
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    images_results = results.get("images_results", [])
    print(len(images_results))
    image_urls = [img["original"] for img in images_results[:10]]
    return image_urls

# 画像URLから主要な色を抽出する関数
def extract_colors_from_image(image_url: str) -> list:
    try:
        response = requests.get(image_url)
        # HTTPステータスコードを確認
        if response.status_code != 200:
            print(f"画像のダウンロードに失敗しました: {response.status_code}")
            return []
        
        # MIMEタイプを確認して画像かどうか判断
        content_type = response.headers['Content-Type']
        if not content_type.startswith('image/'):
            print(f"無効な画像URL: {content_type}")
            return []
        
        # 画像のオープン
        img = Image.open(BytesIO(response.content))

        if img.mode != "RGB":
            img = img.convert("RGB")

        # 一時ファイルに保存
        img_path = "temp_image.jpg"
        img.save(img_path)

        # 主要な色を抽出
        color_thief = ColorThief(img_path)
        dominant_color = color_thief.get_palette(color_count=COLOR_GET_NUM)  # 5色のパレットを抽出

        # 一時ファイルを削除
        os.remove(img_path)

        return dominant_color

    except Exception as e:
        print(f"画像の処理中にエラーが発生しました: {e}")
        return []

# 16進カラーコードに変換する関数
def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

# メイン処理
def get_color_code(query: str) -> list:

    # 画像URLの取得
    print(f"'{query}'の画像を検索しています...")
    image_urls = fetch_image_urls(query)

    if not image_urls:
        print("画像が見つかりませんでした。")
        return

    # 画像ごとに色を抽出
    all_colors = []
    color_cnt = 0
    for idx, url in enumerate(image_urls):
        # print(f"{idx+1}枚目の画像の色を抽出しています: {url}")
        colors = extract_colors_from_image(url)
        if colors:
            all_colors.append(colors)
            color_cnt += COLOR_GET_NUM
        if color_cnt >= COLOR_LIMIT:
            break


    all_colors_hex = []
    # 結果を追加
    for idx, colors in enumerate(all_colors):
        # print(f"{idx+1}枚目の画像の主要な色:")
        for color in colors:
            # print(rgb_to_hex(color))
            all_colors_hex.append(rgb_to_hex(color))

        # print()
    return all_colors_hex

if __name__ == "__main__":
    get_color_code()
