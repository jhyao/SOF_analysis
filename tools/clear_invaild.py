from data.cdn.sof_cdn import TagsCDN

tags = TagsCDN.get_tag_index()
print(len(tags))
for t in tags:
    c = tags[t]
    if c['category'] == 'invalid':
        print(f'delete {t}')
        TagsCDN.del_tag_category(t)