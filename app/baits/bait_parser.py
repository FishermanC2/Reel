from enum import Enum
import base64

class Bait(Enum):
    FETCH = "fetch.js"
    AJAX = "ajax.js"


class BaitParser:
    def __init__(self, bait: Bait):
        self.bait_file = bait.value

    def b64_encode(self):
        with open(self.bait_file, "rb") as bait_text:
            encoded_bait = base64.b64encode(bait_text.read())

        return encoded_bait

