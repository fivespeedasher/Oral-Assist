from volcenginesdkarkruntime import Ark
import os
import dotenv


# 加载环境变量
dotenv.load_dotenv(".env") 


# 从环境变量中获取模型 ID
model_id = os.getenv("ENDPOINT_ID")


client = Ark() # 初始化客户端
 
 
print("----- standard request -----")
completion = client.chat.completions.create(
    model = model_id,
    messages = [
        {"role": "system", "content": "你是一个谈话内容梳理助手。可以针对一个话题写一个类似TED演讲的2分钟内容。"},
        {"role": "user", "content": "我们应当如何成长？"},
    ],
)
 
print(completion.choices[0].message.content)