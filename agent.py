import ollama
from ansi_codes import *
from tools import *

class Agent:
    model = "qwen3"
    tools = []
    conversation = []

    def __init__(self, client: ollama.Client, get_user_message):
        self.client = client
        self.get_user_message = get_user_message
        for tool in tools.values():
            self.tools.append(tool.definition)

    def run(self):
        # system prompt
        self.conversation.append({
            "role": "system",
            "content": "respond succinctly"
            })

        print("Chat with " + self.model + " (use ctrl-c to quit)")

        read_user_input = True

        while True:
            if read_user_input:
                print(ANSI_BLUE + "You" + ANSI_END + ": ", end="")
                user_input = self.get_user_message()

                self.conversation.append({
                    "role": "user",
                    "content": user_input
                    })

            message: ollama.Message = self.run_inference()
            if message.content:
                self.conversation.append({
                    "role": "assistant",
                    "content": message.content
                    })
            
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    self.execute_tool(tool_call)
                    read_user_input = False
            else:
                read_user_input = True

            if read_user_input:
                print(ANSI_ORANGE + "Model" + ANSI_END + ": ", end="")
                print(message.content)

    def run_inference(self):
        response =  self.client.chat(
                model=self.model,
                messages=self.conversation,
                tools=self.tools
                )
        if not response:
            message = ollama.Message(role='assistant')
            message.content = "Error getting response"
            return message
        content = response.message.content
        if not content:
            return response.message
        if "<think>" in content:
            parts = content.split("</think>\n\n")
            think = parts[0][8:-1]
            content = parts[1]
        response.message.content = content
        return response.message

    def execute_tool(self, tool_call):
        if tool_call.function.name not in tools.keys():
            print(ANSI_GREEN + "Tool: " + ANSI_END + "tool not found: " + tool_call.function.name)
            return
        tool_response = globals()[tool_call.function.name](**tool_call.function.arguments)
        print(ANSI_GREEN + "Tool: " + ANSI_END + str(tool_call.function.name) + str(tool_call.function.arguments))
        self.conversation.append({
            'role': 'tool',
            'content': tool_response,
            'name': tool_call.function.name
            })

