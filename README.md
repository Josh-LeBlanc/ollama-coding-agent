# ollama coding agent
code editing agent powered by ollama with tool calling powers :)
# usage
1. make sure that you have [ollama](https://ollama.com/) installed
2. pull an ollama model with `ollama pull <model name>`, and set the model name to the `model` field on the Agent in `agent.py`
    - the model is set to `qwen3` which uses the 8b parameter model by default, so if you would like to use that one just pull that model and you can leave the agent file as is.
3. create a venv and pip install `requirements.txt`
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
4. chat with the model:
```bash
python main.py
```
