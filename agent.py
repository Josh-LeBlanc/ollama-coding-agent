import ollama
from ansi_codes import *

class Agent:
    model = "qwen3"

    def __init__(self, client: ollama.Client, get_user_message):
        self.client = client
        self.get_user_message = get_user_message

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
                )
        content = response.message.content
        if not content:
            return "Error getting response."
        if "<think>" in content:
            if not content:
                return "Error getting response."
            parts = content.split("</think>\n\n")
            think = parts[0][8:-1]
            content = parts[1]
        return content

