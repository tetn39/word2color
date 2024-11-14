from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from get_lyrics import Lyrics
from get_word_img import get_color_code
from contextlib import asynccontextmanager
from controller.database_controller import DatabaseController


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("startup event")
    db_instance.set_app(app)
    await db_instance.startup()
    yield
    print("shutdown event")
    await db_instance.shutdown()

db_instance = DatabaseController()
app = FastAPI(lifespan=lifespan)


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

@app.get("/word2color")
async def word_to_color(word: str) -> dict:
    # dbにあるか確認
    existing_colors = await db_instance.get_colors_from_db(word)
    if existing_colors:
        return {"word":word, "color_codes": existing_colors}
    
    dominant_color = await get_color_code(word)
    # 非同期でdbに追加
    await db_instance.add_color_data(word, dominant_color)

    return {"word":word, "color_codes": dominant_color}

# 起動したときに実行
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)

