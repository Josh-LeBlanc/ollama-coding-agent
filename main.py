from agent import *

def get_user_message():
    return input()

def main():
    client = ollama.Client(host='http://localhost:11434')
    agent = Agent(client, get_user_message)
    agent.run()

if __name__ == "__main__":
    main()
