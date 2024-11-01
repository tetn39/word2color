from flask import Flask, request, render_template
import requests
from janome.tokenizer import Tokenizer
from bs4 import BeautifulSoup
import lyricsgenius
import re

app = Flask(__name__)

# Janomeトークナイザのインスタンスを作成
tokenizer = Tokenizer()

# Genius APIのアクセストークン
ID = "jR-bv8ka_cH9wrt7IyZyYaqKw6zHbIGxjaL2Pf4-SVQGRyWMraaCeR6VPoBHSM2f"
SECRET = "IMOL9EXp8j8g7JyOWY0CuJEi7A8Ft6VtzIEXzSGyXatNy_8V3aY61SVgoP3JvaYVJkilA57Ks9lHgM6Ll0cUVw"

GENIUS_API_ACCESS_TOKEN = '1uXwHCjRkGvdGa8Gm3lfXZ-Z2POeAO_vO_DojDcGteWIrt-mYdwyZHgIKS2r1EaR'
genius = lyricsgenius.Genius(GENIUS_API_ACCESS_TOKEN)
# Genius APIを使用して曲の歌詞を取得する関数
def search_song(song_title):
    base_url = "https://api.genius.com"
    headers = {'Authorization': 'Bearer ' + GENIUS_API_ACCESS_TOKEN}
    search_url = base_url + "/search"
    data = {'q': song_title}
    res = requests.get(search_url, params=data, headers=headers)
    json_response = res.json()

    # 歌詞が見つかった場合、その曲の詳細ページURLを取得
    song_url = None
    if json_response['response']['hits']:
        song_url = json_response['response']['hits'][0]['result']['url']
    
    return song_url

def get_lyrics(song_title):
    # 曲の詳細ページURLを取得
    song_url = search_song(song_title)

    if song_url:
        # 歌詞ページから歌詞をスクレイピング
        page = requests.get(song_url)
        html = BeautifulSoup(page.text, 'html.parser')
        
        # 英語ページから日本語ページへ
        japanese_url = html.find('ul', class_='fSmeGU')
        if japanese_url:
            # この中のdivのtextが「日本語」のdivの親のaタグのhrefを取得 
            japanese_url = japanese_url.find('div', text='日本語')
            if japanese_url:
                japanese_url = japanese_url.parent['href']
                page = requests.get(japanese_url)
                html = BeautifulSoup(page.text, 'html.parser')




        lyrics_element = html.find('div', class_='kUgSbL')
        if lyrics_element:

            for br in lyrics_element.find_all('br'):
                br.replace_with('\n')
            # divの中をすべて取得   
            lyrics = lyrics_element.get_text()
            # []に囲まれた部分は除外する
            lyrics = re.sub(r'\[.*?\]', '', lyrics)
            
            return lyrics
    
    return "歌詞が取得できませんでした"


@app.route('/', methods=['GET', 'POST'])
def index():
    lyrics = ""
    nouns = []
    lyrics_ls = []
    if request.method == 'POST':
        song_title = request.form['song_title']
        lyrics = get_lyrics(song_title)
        nouns = extract_nouns(lyrics)
        # 不要な文字をリストから削除
        for char in [',', '、', '。', '(', ')', "'"]:
            if char in nouns:
                nouns.remove(char)
        # ひらがな1文字を削除
        nouns = [noun for noun in nouns if not (len(noun) == 1 and '\u3040' <= noun <= '\u309F')]
        nouns = ', '.join(nouns)
        lyrics_ls = lyrics.split('\n')
    return render_template('index.html', lyrics_ls=lyrics_ls, tokens=nouns)


# 歌詞を単語に分割する関数
def tokenize_lyrics(lyrics):
    tokens = [token.surface for token in tokenizer.tokenize(lyrics)]
    return tokens

@app.route('/kasiBunkatu', methods=['GET', 'POST'])
def kasiBunkatu():
    tokens = []
    if request.method == 'POST':
        lyrics = request.form['lyrics']
        lyrics = lyrics.replace('\n', '')
        lyrics = lyrics.replace('\r', '')
        lyrics = lyrics.replace(' ', '')
        tokens = tokenize_lyrics(lyrics)
    return render_template('kasiBunkatu.html', tokens=tokens)


# 歌詞から名詞を抽出する関数
def extract_nouns(lyrics):
    tokens = [token.surface for token in tokenizer.tokenize(lyrics) if token.part_of_speech.split(',')[0] == '名詞']
    # none なら[]を返す
    if tokens == None:
        return []
    return tokens

@app.route('/kasiMeisi', methods=['GET', 'POST'])
def kasiMeisi():
    nouns = []
    if request.method == 'POST':
        lyrics = request.form['lyrics']
        nouns = extract_nouns(lyrics)
    return render_template('kasiMeisi.html', tokens=nouns)

if __name__ == '__main__':
    app.run(debug=True)
