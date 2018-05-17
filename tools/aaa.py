from data.cdn.sof_cdn import TagsCDN
from data.cdn.sof_cdn import TagsCDN

tags = TagsCDN.get_tag_index()
for tag in tags:
    clf = tags[tag]
    if not clf['is_core']:
        print(tag)

