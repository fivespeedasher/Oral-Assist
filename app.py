from flask import Flask, request, jsonify
from flask_cors import CORS  # 处理跨域请求，这是因为浏览器有安全策略限制，不允许跨域请求
from volcenginesdkarkruntime import Ark
import os
import dotenv
import prompt_info

# 加载环境变量
dotenv.load_dotenv(".env")

# 从环境变量中获取模型 ID
model_id = os.getenv("ENDPOINT_ID")

app = Flask(__name__) 
CORS(app)  # 启用 CORS, 缓存一天

# 初始化 Ark 客户端
client = Ark()

@app.route('/process', methods=['POST']) # 路由(route)用于指定 URL 触发的函数
def process_text():
    user_text = request.json.get('text')
    chinese_speech = speech_ai(user_text)
    english_translation = translation_ai(chinese_speech)
    return jsonify({"chinese": chinese_speech, "english": english_translation}) # 返回 JSON 格式的响应

def speech_ai(user_text):
    completion = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": prompt_info.speech_system_content},
            {"role": "user", "content": user_text},
        ],
    )
    return completion.choices[0].message.content

def translation_ai(user_text):
    completion = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": prompt_info.translation_system_content},
            {"role": "user", "content": user_text},
        ],
    )
    return completion.choices[0].message.content

# 保存音频文件
@app.route('/upload', methods=['POST'])
def upload_audio():
    audio_file = request.files['audio_file']
    save_path = os.path.join("audio", "recording.wav")
    audio_file.save(save_path)
    return "文件已成功保存！", 200

if __name__ == '__main__':
    app.run(debug=True)
