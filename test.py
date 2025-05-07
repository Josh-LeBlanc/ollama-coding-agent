import ollama
import requests

def read_file(path):
    content = ""
    with open(path, "r") as file:
        content = file.read()

    return content

response = ollama.chat(
    model='qwen3',
    messages=[{'role': 'user', 'content':
        'what is in the file main.py?'}],

		# provide a weather checking tool to the model
    tools=[{
      'type': 'function',
      'function': {
        'name': 'read_file',
        'description': "Read the contents of a given relative file path. Use this when you want to see what's inside a file. Do not use this with directory names.",
        'parameters': {
          'type': 'object',
          'properties': {
            'path': {
              'type': 'string',
              'description': 'relative path to the file to be read',
            },
          },
          'required': ['path'],
        },
      },
    },
  ],
)

print(response['message']['tool_calls'])
print("\n\nresponse:")
print(response['message'])
print("\n\ntool call result:")
for tool_call in response['message']['tool_calls']:
    print(globals()[tool_call.function.name](**tool_call.function.arguments))
