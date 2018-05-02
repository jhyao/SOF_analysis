from data.cdn.sof_cdn import TagsCDN
from analysis.common import *

index = {}
tags = TagsCDN.get_tag_index()
for category in tags.values():
    if category['category'] in index:
        index[category['category']].append(category['tag'])
    else:
        index[category['category']] = [category['tag']]
for c in index:
    print(f'{c} {len(index[c])}')
save_step_data(index, '', file_path=r'E:\SOF\file\tag_index_all.json')
