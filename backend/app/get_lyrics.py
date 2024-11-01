import os
import re
from janome.tokenizer import Tokenizer
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import lyricsgenius
import requests


class Lyrics():
    def __init__(self, title):

        self.tokenizer = Tokenizer()
        # dotenvから取得
        load_dotenv()
        self.ID = os.getenv("GENIUS_API_ID")
        self.SECRET = os.getenv("GENIUS_API_SECRET")
        self.GENIUS_API_ACCESS_TOKEN = os.getenv("GENIUS_API_ACCESS_TOKEN")
        self.genius = lyricsgenius.Genius(self.GENIUS_API_ACCESS_TOKEN)

        self.title = title
        self.lyrics = self.get_lyrics()

    def search_song(self) -> str:
        base_url = "https://api.genius.com"
        headers = {'Authorization': 'Bearer ' + self.GENIUS_API_ACCESS_TOKEN}
        search_url = base_url + "/search"
        data = {'q': self.title}
        res = requests.get(search_url, params=data, headers=headers)
        json_response = res.json()

        # 歌詞が見つかった場合、その曲の詳細ページURLを取得
        song_url = None
        if json_response['response']['hits']:
            song_url = json_response['response']['hits'][0]['result']['url']
        
        return song_url
    
    def get_lyrics(self) -> list:
        # 曲の詳細ページURLを取得
        song_url = self.search_song()

        if song_url:
            # 歌詞ページから歌詞をスクレイピング
            page = requests.get(song_url)
            html = BeautifulSoup(page.text, 'html.parser')
            # 英語ページから日本語ページへ
            japanese_url = html.find('ul', class_='clLDPR') # MEMO: ここが変わるから注意
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
        
        return ["歌詞が取得できませんでした"]
    

    # 歌詞から名詞を抽出する関数
    def extract_nouns(self, lyrics: list) -> list:
        tokens = [token.surface for token in self.tokenizer.tokenize(lyrics) if token.part_of_speech.split(',')[0] == '名詞']
        # none なら[]を返す
        if tokens == None:
            return []
        return tokens