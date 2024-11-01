import re
import json

# 入力データ
with open('rawcolors_data.txt', 'r', encoding='utf-8') as file:
    data = file.read()

# データを整形する
pattern = r"([^\s]+)\n?#([0-9a-fA-F]{6})"
matches = re.findall(pattern, data)

# 整形されたデータをJSON形式で保存
colors = {}
for name, hex_code in matches:
    # RGBに変換
    rgb = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
    colors[name.strip()] = rgb

# JSONファイルに書き出す
with open('colors.json', 'w', encoding='utf-8') as f:
    json.dump(colors, f, ensure_ascii=False, indent=4)

print("colors.jsonにRGBデータを書き出しました。")

# 整形されたデータを表示（任意）
formatted_data = ""
for name, hex_code in matches:
    formatted_data += f"{name}\n#{hex_code}\n\n"

print("整形されたデータ:")
print(formatted_data)
