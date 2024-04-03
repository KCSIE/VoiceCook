from openai import OpenAI
from langchain.agents import load_tools
from langchain.agents import Tool
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor, create_json_chat_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from .tools.time import GetTime, SetTimer
from .tools.recipe import RecipeGen, RecipeSearch

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
Always remember if you use GetTime() to get current time then just answer the time.
Always remember if you use RecipeGen() to generate the recipe then keep the original result of RecipeGen() as the final answer.
Always remember if you use RecipeSearch() to search the recipe, when there are two or more recipe options then just list the options' titles.
Markdown code snippet formatted in the following schema:
```json
{{
    "action": "Final Answer",
    "action_input": string \\ You should put what you want to return to use here. Always remember if you are ask anything about current time then just answer the time despite of the context. If you use RecipeGen() or RecipeSearch(), summarize them rather than use numbered lists.
}}
```

USER'S INPUT
--------------------
Here is the user's input (remember to respond with a markdown code snippet of a json blob with a single action, and NOTHING else):
{input}'''

class ChefAgent:
    def __init__(self, openai_api_key, proxy_url, system_pmt, human_pmt):
        self.openai_api_key = openai_api_key
        self.proxy_url = proxy_url
        self.tools = load_tools(["wikipedia"]) + [
            GetTime(),
            SetTimer(),
            RecipeGen(),
            RecipeSearch(),
        ]
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_pmt),
                MessagesPlaceholder("chat_history", optional=True),
                ("human", human_pmt),
                MessagesPlaceholder("agent_scratchpad"),
            ]
        )
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.llm = ChatOpenAI(temperature=0.3,  model="gpt-3.5-turbo", openai_api_key=self.openai_api_key, openai_api_base=self.proxy_url)
        self.agent = create_json_chat_agent(self.llm, self.tools, self.prompt)
        self.agent_exe = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True, memory=self.memory)

    def chat_with_agent(self, text):
        print(f'ChatGPT Query:{text}')
        reply = self.agent_exe.invoke({"input": text})
        return reply

if __name__ == '__main__':
    test = ChefAgent(OPENAI_API_KEY, proxy_url, system_prompt, human_prompt)
    print(test.chat_with_agent("How are you?"))
    # print(test.chat_with_agent("Can you say it again?"))
    # print(test.chat_with_agent("What time is it?"))
    # print(test.chat_with_agent("Call me after 15 seconds."))
    # print(test.chat_with_agent("I got some wings, garlic, honey, salt. What should I cook?"))
    # print(test.chat_with_agent("Oh, how much should I prepare for each ingredient"))
    # print(test.chat_with_agent("I want to eat wings. Do you know any recipe?"))
    # print(test.chat_with_agent("Oh, I want to cook the Habanero Spiced Buffalo Wings. Tell me more about it."))
    # print(test.chat_with_agent("What cuisine does it belongs to?"))