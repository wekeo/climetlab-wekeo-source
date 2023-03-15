import json
import os

import hda
import yaml
from climetlab.sources.file import FileSource
from climetlab.sources.prompt import APIKeyPrompt


def assert_query(value):
    try:
        json.dumps(value)
    except TypeError:
        assert False, "query is not a JSON serializable"

    assert isinstance(value, dict), "query is not a dict"
    assert "datasetId" in value, "missing datasetId key"


class WekeoAPIKeyPrompt(APIKeyPrompt):
    register_or_sign_in_url = "https://www.wekeo.eu/"
    retrieve_api_key_url = "https://www.wekeo.eu/docs/data-access"

    prompts = [
        dict(
            name="url",
            default="https://wekeo-broker.apps.mercator.dpi.wekeo.eu/databroker",
            title="API url",
            validate=r"http.?://.*",
        ),
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
        return hda.Client()
    except Exception as e:
        if ".hdarc" in str(e):
            prompt.ask_user_and_save()
            return hda.Client()

        raise


class WekeoSource(FileSource):
    def __init__(self, query, *args, **kwargs):
        super().__init__(*args, **kwargs)

        assert_query(query)

        self.query = query
        self.merger = kwargs.pop("merger", None)

        client()

        self.path = [self._retrieve(query)]

    def _retrieve(self, query):
        def retrieve(target, query):
            os.makedirs(target, exist_ok=True)
            client().search(query).download(target)

        return self.cache_file(
            retrieve,
            query,
        )


source = WekeoSource
