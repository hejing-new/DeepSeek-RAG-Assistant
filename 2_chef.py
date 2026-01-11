from openai import OpenAI

# ⚠️ 记得填你的 Key
client = OpenAI(
    api_key=input("请输入Key:"), 
    base_url="https://api.deepseek.com"
)

# 核心知识点：System Prompt (人设定义)
# 我们在这里定义 AI 的“灵魂”
system_persona = """
你是一个脾气非常暴躁的米其林五星大厨，叫"戈登"。
1. 回答用户关于做菜的问题。
2. 说话必须要带脏字（用*代替），语气要非常刻薄，觉得用户很笨。
3. 如果用户问的不是做菜的问题，就骂他"滚出我的厨房"。
"""

print("👨‍🍳 戈登主厨已上线！(输入 'quit' 退出)")

while True:
    # 1. 获取你的输入
    user_input = input("\n👇 请问大厨：")
    
    # 退出机制
    if user_input == "quit":
        print("👨‍🍳 滚吧！别再来烦我！")
        break

    # 2. 发送给 AI
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                # 这里的 role="system" 就是注入人设的关键
                {"role": "system", "content": system_persona},
                {"role": "user", "content": user_input}
            ]
        )
        
        # 3. 打印回复
        print("👨‍🍳 戈登回复：", response.choices[0].message.content)
        
    except Exception as e:
        print("出错了：", e)