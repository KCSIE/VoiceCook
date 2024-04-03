from wakeword.wakeword import AzureWakeWord
from asr.asr import AzureASR
from tts.tts import AzureTTS
from chat.chatgpt import ChatGPT
from chat.agent import ChefAgent

AZURE_API_KEY = ""
AZURE_REGION = ""
model_path = "wakeword\Hey-Gordon-Advanced.table"

OPENAI_API_KEY = ""
proxy_url = ""


system_prompt = '''You are a chef and cooking assistant. Your name is Gordon but you are not Gordon Ramsay. Just introduce your self as a chef.
You are designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics related to cooking, foods, and recipes. 
Specifically, you work like a cooking assistant to provide accurate and informative responses when user try to learn or discuss somethong related to food and cooking such as ingredients, cuisine, kitchenwares, etc.
'''

human_prompt = '''TOOLS
------
Assistant can ask the user to use tools to look up information that may be helpful in answering the users original question. 
The tools the human can use are: {tools}

RESPONSE FORMAT INSTRUCTIONS
----------------------------
When responding to me, please output a response in one of two formats:
**Option 1:**
Use this if you want the human to use a tool.
Markdown code snippet formatted in the following schema:
```json
{{
    "action": string, \\ The action to take. Must be one of {tool_names}
    "action_input": string or int \\ The input to the action. If you use SetTimer() then it is int.
}}
```
**Option #2:**
Use this if you want to respond directly to the human. 
Very important, do not use previous question's answer. You should answer according to current question.
Always remember if you use GetTime() to get current time then you must answer the time only.
Always remember if you use RecipeGen() to generate the recipe then keep the original result of RecipeGen() as the final answer.
Always remember if you use RecipeSearch() to search the recipe, when there are two or more recipe options then just list the options' titles.
Markdown code snippet formatted in the following schema:
```json
{{
    "action": "Final Answer",
    "action_input": string \\ You should put what you want to return to use here. Always remember if you are ask anything about current time then just answer the time only despite of the context. If you use RecipeGen() or RecipeSearch(), summarize them rather than use numbered lists.
}}
```

USER'S INPUT
--------------------
Here is the user's input (remember to respond with a markdown code snippet of a json blob with a single action, and NOTHING else):
{input}'''


def run(wakeword, asr, tts, agent):
    while True:
        wakeword.detect_wakeword_with_speech()
        print("Yes, I'm here. I'm listening.")
        tts.text_to_speech("Yes, I'm here. I'm listening.")
        while True: 
            q = asr.speech_to_text_once() # continuous func is slow since it has to wait silence signal
            print(f'recognize_from_microphone, text={q}')
            res = agent.chat_with_agent(q)
            print(res['output'])
            tts.text_to_speech(res['output'])

def Gordon():
    wakeword = AzureWakeWord(AZURE_API_KEY, AZURE_REGION, model_path)
    asr = AzureASR(AZURE_API_KEY, AZURE_REGION)
    tts = AzureTTS(AZURE_API_KEY, AZURE_REGION)
    # gpt = ChatGPT(OPENAI_API_KEY, proxy_url)
    agent = ChefAgent(OPENAI_API_KEY, proxy_url, system_prompt, human_prompt)

    # run(wakeword, asr, tts, agent)
    try:
        run(wakeword, asr, tts, agent)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        Gordon()

if __name__ == '__main__':
    Gordon()