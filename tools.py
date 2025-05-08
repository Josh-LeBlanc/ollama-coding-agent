import os

class Tool:
    def __init__(self, name, function, definition):
        self.name = name
        self.function = function
        self.definition = definition

tool_list = []

# read file tool
def read_file(path):
    content = ""
    with open(path, "r") as file:
        content = file.read()

    return content

read_file_definition = {
        'type': 'function',
        'function': {
            'name': 'read_file',
            'description': "Read the contents of a given relative file path. Use this when you want to see what's inside a file. Do not use this with directory names.",
            'parameters': {
                'type': 'object',
                'properties': {
                    'path': {
                        'type': 'string',
                        'description': 'relative path of a file in the working directory',
                        },
                    },
                'required': ['path'],
                },
            },
        }

read_file_tool = Tool(read_file_definition['function']['name'], read_file, read_file_definition)
tool_list.append(read_file_tool)

# list files tool definition
def list_files(path="."):
    files = os.listdir(path)
    for file in files:
        if os.path.isdir(file):
            files.remove(file)
            file += "/"
            files.insert(0, file)
    return ", ".join(files)

list_files_definition = {
        'type': 'function',
        'function': {
            'name': 'list_files',
            'description': "List files and directories at a given path. If no path is provided, lists files in the current directory.",
            'parameters': {
                'type': 'object',
                'properties': {
                    'path': {
                        'type': 'string',
                        'description': 'Optional relative path to list files from. Defaults to current directory if not provided.',
                        },
                    },
                },
            },
        }
list_files_tool = Tool(list_files_definition['function']['name'], list_files, list_files_definition)
tool_list.append(list_files_tool)

# other tool definitions

tools = {}
for tool in tool_list:
    tools[tool.name] = tool
