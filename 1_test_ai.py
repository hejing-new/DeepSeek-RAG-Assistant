from openai import OpenAI

# 填入你的 Key
my_key = input("请输入Key:")

client = OpenAI(
    api_key=my_key,
    base_url="https://api.deepseek.com"  # 代码里通常不需要 v1，如果不行再加
)

try:
    print("正在发送请求...")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": "你好，能听到我说话吗？"}
        ]
    )
    print("AI回复成功：")
    print(response.choices[0].message.content)
except Exception as e:
    print("出错了：", e)