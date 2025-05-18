
import uuid
import requests
import json

def simple_chatglm_request(prompt):
    device_id = str(uuid.uuid4()).replace('-', '')
    headers = {
        'Accept-Language': 'en-US,en;q=0.9',
        'App-Name': 'chatglm',
        'Authorization': 'undefined',
        'Content-Type': 'application/json',
        'Origin': 'https://chatglm.cn',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'X-App-Platform': 'pc',
        'X-App-Version': '0.0.1',
        'X-Device-Id': device_id,
        'Accept': 'text/event-stream'
    }

    data = {
        "assistant_id": "65940acff94777010aa6b796",
        "conversation_id": "",
        "meta_data": {
            "if_plus_model": False,
            "is_test": False,
            "input_question_type": "general",
            "channel": "",
            "draft_id": "",
            "quote_log_id": "",
            "platform": "pc"
        },
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    }

    response = requests.post(
        'https://chatglm.cn/chatglm/mainchat-api/guest/stream',
        headers=headers,
        data=json.dumps(data),
        stream=True
    )

    print("🤖 ChatGLM says:\n")
    for line in response.iter_lines():
        if line:
            decoded = line.decode('utf-8')
            if decoded.startswith("data: "):
                try:
                    json_data = json.loads(decoded[6:])
                    parts = json_data.get('parts', [])
                    if parts:
                        content = parts[0].get('content', [])
                        if content:
                            text = content[0].get('text', '')
                            print(text, end='', flush=True)
                    if json_data.get('status') == 'finish':
                        print("\n[✔ Conversation finished]")
                        break
                except json.JSONDecodeError:
                    continue

if __name__ == "__main__":
    user_input = input("👤 You: ")
    simple_chatglm_request(user_input)
