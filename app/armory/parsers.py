from enum import Enum
import base64
import pathlib

MODULES_PATH = "\\modules"
BAITS_PATH = "\\baits"


class Bait(Enum):
    FETCH = "fetch.js"

class Module(Enum):
    BROWSER_PLUGINS = 'browser_plugins.js',
    TIMEZONE = 'timezone.js',
    LANGUAGE = 'language.js',
    SCREEN_RESOLUTION = 'screen_resolution.js'

class Parser:
    def __init__(self, path):
        self.path = path

    def b64_encode(self):
        with open(self.path, "rb") as text:
            encoded_text = base64.b64encode(text.read())

        return encoded_text
    
    def uglify_js(self):
        pass

class ModuleParser(Parser):
    def __init__(self, module: Module):
        super().__init__(f"{pathlib.Path(__file__).parent.resolve()}\\{MODULES_PATH}\\{module.value}")

class BaitParser(Parser):
    def __init__(self, bait: Bait):
        super().__init__(f"{pathlib.Path(__file__).parent.resolve()}\\{BAITS_PATH}\\{bait.value}")

