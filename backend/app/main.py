from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from get_lyrics import Lyrics
from get_word_img import get_color_code

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,   
    allow_methods=["*"],      
    allow_headers=["*"],
    expose_headers=["Access-Control-Allow-Origin"]
)


@app.get("/")
def read_root() -> dict:
    return {"Hello": "World"}

@app.get("/lyrics")
def get_lyrics(title: str = None) -> dict:
    song_title = title
    l = Lyrics(song_title)
    song_lyrics = l.get_lyrics()
    nouns = l.extract_nouns(song_lyrics)
    # 不要な文字をリストから削除
    for char in [',', '、', '。', '(', ')', "'"]:
        if char in nouns:
            nouns.remove(char)
    # ひらがな1文字を削除
    nouns = [noun for noun in nouns if not (len(noun) == 1 and '\u3040' <= noun <= '\u309F')]
    song_lyrics = song_lyrics.split('\n')
    nouns = list(set(nouns))
    # jsonにしてreturn

    return {"lyrics": song_lyrics, "tokens": nouns}

@app.get("/word2img")
def word_to_color(word: str) -> dict:
    dominant_color = get_color_code(word)
    # print(dominant_color)
    return {"word":word, "color_codes": dominant_color}

# 起動したときに実行
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)

