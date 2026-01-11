import sys
import os
import getpass
import openai
import datetime
import random

def retrieve_api_key():
    """ Prompt user for API key or read it from file """
    base_dir = os.path.split(os.path.dirname(__file__))[0]
    key_file = os.path.join(base_dir, "api_key.txt")
    if os.path.isfile(key_file):
        with open(key_file, "r") as f:
            key = f.read()
    else:
        print(f"Please enter API key (will be stored in {key_file})")
        key = getpass.getpass("API key: ")
        with open(key_file, "w") as f:
            f.write(key)
    return key


class Wrapper:
    """ Wrapper around model object for bookkeeping """
    def __init__(self, config, model, system_prompt = None):
        self.config = config
        if model is None:
            # Dry run
            self.model = None
        else:
            self.model = self.config["models"][model]
            self.client = openai.OpenAI(api_key=retrieve_api_key(), base_url=self.config["API_ENDPOINT"])
        self.messages = []
        if system_prompt is not None:
            self.add_message("system", system_prompt)
    
    def add_message(self, role, content):
        """ Add message to conversation history """
        self.messages.append({
            "role": role,
            "content": content
        })

    def query(self, prompt):
        """ Prompt the model """
        self.add_message("user", prompt)
        return self._do_query()

    def _do_query(self):
        """ Actually query the model """
        assert self.messages[-1]["role"] == "user"

        if self.model is None:
            response = "random response " + str(random.randint(1000,9999))
            self.add_message("assistant", response)
            result = dict()
            result["model_response"] = response
            result["completion_tokens"] = 42
            result["timestamp"] = datetime.datetime.now().isoformat()
            result["latency_ms"] = 1234
            return result

        for i in range(1,self.config["API_RETRIES"]+1):
            try:
                t0 = datetime.datetime.now()
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.messages,
                    timeout=self.config["API_TIMEOUT"],
                    **self.config["query_config"]
                )
                t1 = datetime.datetime.now()
                break
            except openai.APITimeoutError:
                if i < self.config["API_RETRIES"]:
                    print("API timed out. Trying again")
                else:
                    print("Giving up")
                    raise Exception("API timed out")

        response = completion.choices[0].message.content
        self.add_message("assistant", response)
        result = dict()
        result["model_response"] = response
        result["completion_tokens"] = completion.usage.completion_tokens
        result["timestamp"] = datetime.datetime.fromtimestamp(completion.created).isoformat()
        result["latency_ms"] = int((t1-t0).total_seconds()*1000)

        return result
