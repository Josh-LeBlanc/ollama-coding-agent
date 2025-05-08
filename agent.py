import ollama
from ansi_codes import *
from tools import *

class Agent:
    model = "qwen3"
    tools = []

    def __init__(self, client: ollama.Client, get_user_message):
        self.client = client
        self.get_user_message = get_user_message
        for tool in tools.values():
            self.tools.append(tool.definition)

    def run(self):
        conversation = []
        # system prompt
        conversation.append({
            "role": "system",
            "content": "respond succinctly"
            })

        print("Chat with " + self.model + " (use ctrl-c to quit)")

        while True:
            print(ANSI_BLUE + "You" + ANSI_END + ": ", end="")
            user_input = self.get_user_message()

            conversation.append({
                "role": "user",
                "content": user_input
                })

            message = self.run_inference(conversation)
            conversation.append({
                "role": "assistant",
                "content": message
                })

            print(ANSI_ORANGE + "Model" + ANSI_END + ": ", end="")
            print(message)

    def run_inference(self, conversation):
        response =  self.client.chat(
                model=self.model,
                messages=conversation,
                tools=self.tools
                )
        if not response:
            return "Error getting response."
        if response.message.tool_calls:
            for tool_call in response.message.tool_calls:
                self.execute_tool(tool_call)
        content = response.message.content
        if not content:
            return "Error getting content."
        if "<think>" in content:
            if not content:
                return "Error getting response."
            parts = content.split("</think>\n\n")
            think = parts[0][8:-1]
            content = parts[1]
        return content

    def execute_tool(self, tool_call):
        if tool_call.function.name not in tools.keys():
            print(ANSI_GREEN + "Tool: " + ANSI_END + "tool not found: " + tool_call.function.name)
            return
        tool_response = globals()[tool_call.function.name](**tool_call.function.arguments)
        print(ANSI_GREEN + "Tool: " + ANSI_END + str(tool_call.function.name) + str(tool_call.function.arguments))
        print(ANSI_GREEN + "Tool Response: " + ANSI_END + tool_response)

