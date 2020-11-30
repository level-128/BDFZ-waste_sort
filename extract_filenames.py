import os
import glob
import re


def to_json(ls):
    return ", ".join(['"' + tag + '"' for tag in set(ls)])


pathname = input("Enter path name: ")
print("")

result = []
for fl in glob.glob(pathname + "/*"):
    basename = os.path.basename(fl)
    # "塑料瓶1.jpg" -> "塑料瓶"
    match = re.match(r"(?P<tag>[^0-9]+)[0-9]*\.", basename)
    if match:
        result.append(match["tag"])

print(to_json(result))
