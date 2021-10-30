from github import Github as g
from github.MainClass import Github
import os
import tarfile
import requests

class assets:
    gh = None
    config = dict()
    release = dict()
    session = None

    # validate if the config has a length
    def validate_config(self, name: str, value: str):
        if(value != None and len(value) > 0):
            return True
        else:
            self.workflow("error", "Missing field; " + name)
            return False

    # get config item
    def get_config(self, name: str):
        if name in self.config:
            return self.config[name]
        else:
            return None

    # output for action workflow
    def output(self, name: str, value: str):
        print(f"::set-output name={name}::{value}")

    # github action formatted output
    # TODO: config to disable debug mode
    def workflow(self, type: str, message: str):
        if(type == "debug" or type == "warning" or type == "error"):
            print(f"::{type}::{message}")

            if type == "error":
                exit(1)
        else:
            print(message)

    # extract an archive
    def extract_archive(self, path: str, output: str):
        self.workflow('debug', 'Extracting ' + path)
        tar = tarfile.open(path)
        tar.extractall(output)

    # determine if string is empty, for config items
    def is_empty(self, string: str) -> bool:
        return not (string and string.strip())

    # download and save assets
    def download(self, url: str, filename: str):
        self.workflow('debug', 'Download asset ' + filename)

        if self.session == None:
            self.session = requests.Session()

        headers = {'Authorization': 'token ' + os.environ.get('INPUT_TOKEN'),
                   'Accept': 'application/octet-stream'}

        response = self.session.get(url, stream = True, headers=headers)
        dest = self.get_config('base_dir') + self.get_config('arg_output') + filename

        with open(dest, 'wb') as f:
            for chunk in response.iter_content(1024*1024):
                f.write(chunk)

        # do we need to extract?
        if self.get_config('arg_extract') and filename.find('.tar') != -1:
            self.extract_archive(self.get_config('arg_output') + filename, self.get_config('arg_output'))

    # main logic
    def run(self):
        release = self.gh.get_repo(self.get_config('arg_repo_name')).get_release(self.get_config('arg_tag'))

        if release == None:
            self.workflow('error', 'Unable to find tag; ' + self.get_config('arg_tag'))
            return

        for asset in release.get_assets():
            self.download(asset.url, asset.name)

    def __init__(self):
        # static basedir for github action container
        self.config['base_dir'] = '/github/workspace/'

        # config map
        config = {
            'arg_tag': 'INPUT_TAG',
            'arg_repo_name': 'INPUT_REPO_NAME',
            'arg_extract': 'INPUT_EXTRACT',
            'arg_output': 'INPUT_OUTPUT_DIR',
            'base_dir': 'INPUT_BASE_DIR'
        }

        for c_key, c_value in config.items():
            value = os.environ.get(c_value)

            if not self.is_empty(value):
                self.config[c_key] = value

        # validate required config
        if (not self.validate_config("tag", self.get_config('arg_tag')) and
            not self.validate_config("output directory", self.get_config('arg_output_dir')) and
            not self.validate_config("repo name", self.get_config('arg_repo_name'))):
            self.workflow("error", "Missing required fields")
            exit(1)

        # connect to github
        self.gh = Github(os.environ.get('INPUT_TOKEN'))

        # run app
        self.run()

assets()