import numpy as np
import pandas as pd
import json
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# JSONファイルからデータを読み込む
with open('colors.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# JSONから読み込んだデータをテキストと色のリストに変換
text_data = list(json_data.keys())
color_data = [tuple(color) for color in json_data.values()]

# 既存のデータセット
original_data = {
    'text': ['ハート', '青空', '夕日', '草原', '海', '火'],
    'color': [(255, 0, 0), (135, 206, 235), (255, 69, 0), (34, 139, 34), (0, 0, 255), (255, 69, 0)]
}

# データを結合
combined_text = original_data['text'] + text_data
combined_color = original_data['color'] + color_data

# データフレームに変換
df = pd.DataFrame({'text': combined_text, 'color': combined_color})

# テキストのトークン化
tokenizer = Tokenizer()
tokenizer.fit_on_texts(df['text'])
sequences = tokenizer.texts_to_sequences(df['text'])

# パディング
max_len = max(len(x) for x in sequences)
X = pad_sequences(sequences, maxlen=max_len)

# 色データのスケーリング
y = np.array([np.array(color) / 255.0 for color in df['color']])  # RGBを0-1の範囲にスケーリング

# モデルの構築
model = Sequential()
model.add(Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=16, input_length=max_len))
model.add(LSTM(32, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(16))
model.add(Dense(16, activation='relu'))
model.add(Dense(3, activation='sigmoid'))  # RGB値を予測するため、3ユニットでsigmoidを使用

model.compile(optimizer='adam', loss='mean_absolute_error')
model.summary()

# トレーニングとテストの分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# モデルのトレーニング
model.fit(X_train, y_train, epochs=200, validation_data=(X_test, y_test), batch_size=2)

# 予測関数
def predict_color(text):
    sequence = tokenizer.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequence, maxlen=max_len)
    predicted_rgb = model.predict(padded_sequence)[0] * 255  # スケーリングを元に戻す
    return tuple(int(x) for x in predicted_rgb)

# 例: ハートの色を予測
predicted_color = predict_color('ハート')
print(f"Predicted color for 'ハート': {predicted_color}")
