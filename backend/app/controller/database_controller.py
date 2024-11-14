from fastapi import FastAPI, HTTPException
import asyncpg
class DatabaseController():
    def __init__(self):
        self.DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/postgres"
        self.CREATE_TABLE_QUERY: str = """
            CREATE TABLE IF NOT EXISTS colors (
            id SERIAL PRIMARY KEY,
            color_name VARCHAR(50) NOT NULL,
            color_code VARCHAR(200) NOT NULL
        );
        """
    def set_app(self, app: FastAPI):
        self.app = app


    async def startup(self):
        # アプリケーション起動時に接続プールを作成
        print('きどうしたーーーー')
        self.app.state.db_pool = await asyncpg.create_pool(dsn=self.DATABASE_URL)
        # テーブル作成
        async with self.app.state.db_pool.acquire() as connection:
            await connection.execute(self.CREATE_TABLE_QUERY)


    async def shutdown(self):
        # アプリケーション終了時に接続プールを閉じる
        await self.app.state.db_pool.close()


    async def add_color_data(self, color_name: str, color_codes: list):
        check_query = "SELECT COUNT(*) FROM colors WHERE color_name = $1"
        insert_query = "INSERT INTO colors (color_name, color_code) VALUES ($1, $2)"
        
        try:
            color_codes_str = ",".join(color_codes)
            
            # 接続プールからコネクションを取得
            async with self.app.state.db_pool.acquire() as connection:
                # 既存のcolor_nameを確認
                count = await connection.fetchval(check_query, color_name)
                
                # データが存在しない場合のみ挿入処理
                if count == 0:
                    await connection.execute(insert_query, color_name, color_codes_str)
                    return {"message": "Data inserted successfully"}
                else:
                    return {"message": "Data already exists, skipping insertion"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # DBから色コードを取得する関数
    async def get_colors_from_db(self, query: str):
        # データベースから色コードを取得する処理を実装
        # データが見つかればリスト形式で返し、見つからなければ None を返す
        try:
            async with self.app.state.db_pool.acquire() as connection:
                colors = await connection.fetchval("SELECT color_code FROM colors WHERE color_name = $1", query)
                if colors:
                    return colors.split(",")  # データベース内に保存された色コードをリスト形式に変換
        except Exception as e:
            print(f"データベースエラー: {e}")
        return None