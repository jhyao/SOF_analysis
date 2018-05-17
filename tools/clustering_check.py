from analysis.classify_tag_v1 import TagClassifier
from data.cache.sof_cache import CoreTagClfCache


def check(clf):
    clifer = TagClassifier(from_db=False, from_api=False, update=True)
    core_tags = list(clf.keys())
    if 'others' in core_tags:
        core_tags.remove('others')
    fail_list = []
    for c in clf:
        for tag in clf[c]:
            weights = [clifer.get_weight(tag, core) for core in core_tags]
            max_weight = max(weights)
            if max_weight != weights[core_tags.index(c)] or max_weight == 0:
                fail_list.append([tag, c, core_tags[weights.index(max_weight)]])
    return fail_list

if __name__ == '__main__':
    clf = CoreTagClfCache.get()
    for item in check(clf):
        print(item)