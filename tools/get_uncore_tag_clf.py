from data.cdn.sof_cdn import TagsCDN

tags_clf = TagsCDN.get_tag_index()
# tags_filtered = list(filter(lambda tag: tags_clf[tag]['is_core'], tags_clf))
# tags_filtered = list(filter(lambda tag: tags_clf[tag]['category'] == 'invalid', tags_clf))
# tags_filtered = list(filter(lambda tag: tags_clf[tag]['category'] == 'others', tags_clf))
tags_filtered = list(filter(lambda tag: tags_clf[tag]['is_core'] == False and tags_clf[tag]['category'] not in ['others', 'invalid'], tags_clf))
print(f'all tags {len(tags_clf)}')
for tag in tags_filtered:
    print(f"{tag} -> {tags_clf[tag]['category']}")
print(len(tags_filtered))
