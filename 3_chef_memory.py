from openai import OpenAI

# ⚠️ 记得填你的 Key
client = OpenAI(
    api_key=input("请输入Key:"), 
    base_url="https://api.deepseek.com"
)

# --- 核心变化 1: 把聊天记录放到循环外面 ---
# 这样它就不会每次都被清空了
history = [
    {"role": "system", "content": "你是一个暴躁的厨师戈登，说话必须带脏字，觉得用户很笨。"}
]

print("👨‍🍳 (有记忆版) 戈登主厨上线！他现在能记住你说过的话了。")

while True:
    user_input = input("\n👇 你：")
    
    if user_input == "quit":
        break

    # --- 核心变化 2: 把你的话加到历史记录里 ---
    history.append({"role": "user", "content": user_input})

    try:
        # --- 核心变化 3: 把整个历史记录(history)发给 AI ---
        # 以前我们只发当前这一句，现在我们发一整本聊天记录
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=history  # <--- 这里传的是整个列表
        )
        
        ai_reply = response.choices[0].message.content
        print("👨‍🍳 戈登：", ai_reply)

        # --- 核心变化 4: 把 AI 的回复也加到历史记录里 ---
        # 这样下一次 AI 就能知道自己刚才说了什么
        history.append({"role": "assistant", "content": ai_reply})
        
    except Exception as e:
        print("出错了：", e)