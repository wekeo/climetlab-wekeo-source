import json
import os

import yaml
from climetlab.sources.file import FileSource
from climetlab.sources.prompt import APIKeyPrompt
from hda import Client
from hda.api import bytes_to_string


def assert_query(value):
    try:
        json.dumps(value)
    except TypeError:
        assert False, "query is not a JSON serializable"

    assert isinstance(value, dict), "query is not a dict"
    assert "dataset_id" in value, "missing dataset_id key"


class WekeoAPIKeyPrompt(APIKeyPrompt):
    register_or_sign_in_url = "https://www.wekeo.eu/"
    retrieve_api_key_url = "https://www.wekeo.eu/docs/data-access"

    prompts = [
        dict(
            name="user",
            title="Username",
            validate=r"[^\s]+",
        ),
        dict(
            name="password",
            title="Password",
            hidden=True,
            validate=r"[^\s]+",
        ),
    ]

    rcfile = "~/.hdarc"

    def save(self, input, file):
        yaml.dump(input, file, default_flow_style=False)


def client():
    prompt = WekeoAPIKeyPrompt()
    prompt.check()

    try:
        return Client()
    except Exception as e:
        if ".hdarc" in str(e):
            prompt.ask_user_and_save()
            return Client()

        raise


def ask_yes_no(question):
    while True:
        user_input = input(question + " (yes/no): ").strip().lower()
        if user_input in ["yes", "y"]:
            return True
        elif user_input in ["no", "n"]:
            return False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


class WekeoSource(FileSource):
    def __init__(self, query, limit=None, *args, **kwargs):
        assert_query(query)

        self.query = query
        self.limit = limit

        client()

        path = self._retrieve(query)
        super().__init__(path, *args, **kwargs)

    def _retrieve(self, query):
        def retrieve(target, query):
            os.makedirs(target, exist_ok=True)
            results = client().search(query, self.limit)

            question = (
                f"The file you are about to download is {bytes_to_string(results.volume)} big."
                "Make sure that you have enough free space in your cache or have changed "
                "the cache directory to a disk with enough space "
                "(Link: https://climetlab.readthedocs.io/en/latest/guide/caching.html)"
            )
            user_response = ask_yes_no(question)
            if user_response is None:
                user_response = True

            if user_response:
                results.download(target)
            else:
                print("Download cancelled")

        return self.cache_file(retrieve, query)


source = WekeoSource
