import os
import re
from pathlib import Path


def collect_guid(data_path):
    p = Path(data_path)
    guid_files = p.glob('*')
    name_list = []
    for f in guid_files:
        if re.match(r'^\S{32}', f.name):
            name_list.append(f.name)
    print(name_list)

collect_guid(r'E:\DGM\yangyu_SKY-20190415GHW_1187\x5_mobile\mobile_dancer\trunk\client\player_output\apk\Data')
