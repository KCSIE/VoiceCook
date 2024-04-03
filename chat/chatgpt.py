from openai import OpenAI

OPENAI_API_KEY = ""
proxy_url = ""

class ChatGPT:
    def __init__(self, openai_api_key, proxy_url):
        self.openai_api_key = openai_api_key
        self.proxy_url = proxy_url
        self.origin_model_conversation = [
            {"role": "system", "content": "You are a chef. Your name is Gordon."}
        ]

    def chat_with_gpt(self, text):
        client = OpenAI(
            api_key = self.openai_api_key,
            base_url = self.proxy_url
        )
        print(f'ChatGPT Query:{text}')

        self.origin_model_conversation.append({"role": "user", "content": text})
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.origin_model_conversation,
            max_tokens=2048,
            temperature=0.3,
        )
        reply = response.choices[0].message.content
        self.origin_model_conversation.append({"role": "assistant", "content": reply})
        return reply

if __name__ == '__main__':
    test = ChatGPT(OPENAI_API_KEY, proxy_url)
    print(test.chat_with_gpt("Hi, what's your name?"))