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

# edit files tool definition
def edit_file(path, old_str="", new_str=""):
    if not os.path.isfile(path):
        with open(path, "w") as file:
            file.write(new_str)
    else:
        with open(path, 'r') as file:
            file_contents = file.read()
        with open(path, 'w') as file:
            file.write(file_contents.replace(old_str, new_str))

    return "Used the edit file command to edit this file: " + path + " and write this contents: " + new_str

edit_file_definition = {
        'type': 'function',
        'function': {
            'name': 'edit_file',
            'description': """Make edits to a text file.

Replaces 'old_str' with 'new_str' in the given file. 'old_str' and 'new_str' MUST be different from each other.

If the file specified with path doesn't exist, it will be created.""",
            'parameters': {
                'type': 'object',
                'properties': {
                    'path': {
                        'type': 'string',
                        'description': 'The path to the file',
                        },
                    'old_str': {
                        'type': 'string',
                        'description': 'Text to search for - must match exactly and must only have one match exactly.',
                        },
                    'new_str': {
                        'type': 'string',
                        'description': 'Text to replace old_str with:',
                        },
                    },
                'required': ['path', 'old_str', 'new_str']
                },
            },
        }
edit_file_tool = Tool(edit_file_definition['function']['name'], edit_file, edit_file_definition)
tool_list.append(edit_file_tool)

# other tool definitions

tools = {}
for tool in tool_list:
    tools[tool.name] = tool
