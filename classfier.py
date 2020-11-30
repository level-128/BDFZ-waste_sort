import json.decoder
import re
from typing import *

database_filename = "garbage_category_database.json"
database = {}
with open(database_filename, "r", encoding="utf-8") as fh:
    database = json.load(fh)

pattern = re.compile(r'\"confidence\":\"(?P<confidence>[0-9\.]+)\".*?\"tag\":\"(?P<tagname>.*?)\"')


def decode_from_api(api_result):
    return [(match["tagname"], match["confidence"]) for match in pattern.finditer(api_result)]


def classify(tags):
    for tag, confidence in tags:
        for key in database:
            if tag in database[key]:
                return tag, key, confidence
    return None


if __name__ == "__main__":
    test_str = '{"result":{"tags":[{"confidence":"73.86","i18n_tag":{"en":"Mountain","zh":"山"},"tag":"山","' \
               'type":"object"},{"confidence":"72.78","i18n_tag":{"en":"Scenery","zh":"风光"},"tag":"风光","t' \
               'ype":"object"},{"confidence":"68.09","i18n_tag":{"en":"Natural","zh":"自然"},"tag":"自然","ty' \
               'pe":"object"},{"confidence":"65.5","i18n_tag":{"en":"Sky","zh":"天空"},"tag":"天空","type":"o' \
               'bject"}]}}'
    print(classify(test_str))
