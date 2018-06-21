"""
not in use
不对标签做绝对的分类，而是用到标签类的相关度加权计算
"""
from analysis.classify_tag_v1 import TagClassifier
from data.cdn.sof_cdn import UserTagsCDN

clifer = None
config = {
    'save': True,
    'from_db': True,
    'from_cache': True,
    'from_api': True,
    'max_page': None
}
cls = ['java', 'android', 'c#', 'hadoop',
       'javascript', 'css',
       'python', 'ios', 'c++', 'php',
       'sql', 'ruby', 'r', 'git', 'algorithm', 'linux']


def get_clifer():
    if clifer:
        return clifer
    else:
        return create_clifer()


def create_clifer(min_question_num=100, min_weight=0.1,
                  update=False, from_db=True, from_api=True, from_cache=True,
                  related_cache=False, save_db=True):
    global clifer
    clifer = TagClassifier(min_question_num=min_question_num, min_weight=min_weight,
                           update=update, from_db=from_db, from_api=from_api, from_cache=from_cache,
                           related_cache=related_cache, save_db=save_db)
    return clifer


def set_clifer(c):
    global clifer
    clifer = c


def set_config(**kwargs):
    config.update(**kwargs)


def user_interest(user_id):
    user_tags = UserTagsCDN.get_user_tags(user_id, save=config['save'], from_cache=config['from_cache'],
                                          from_db=config['from_db'], from_api=config['from_api'],
                                          max_page=config['max_page'])
    result = {}
    for c in cls:
        result[c] = [0,0,0,0]
    for item in user_tags:
        weights = get_clifer().classify_tag(item['tag'])['weights']
        for category in weights:
            result[category][0] += item['question_count'] * weights[category]
            result[category][1] += item['question_score'] * weights[category]
            result[category][2] += item['answer_count'] * weights[category]
            result[category][3] += item['answer_score'] * weights[category]
    result.pop('invalid', [])
    result.pop('others', [])
    for c in list(result.keys()):
        if sum(result[c]) == 0:
            result.pop(c)
    return result
    # cls = list(result.keys())
    # answer_interest = [result[c][1] for c in cls]
    # answer_sum = sum(answer_interest)
    # answer_interest = [i / answer_sum for i in answer_interest]
    # question_interest = [result[c][3] for c in cls]
    # question_sum = sum(question_interest)
    # question_interest = [i / question_sum for i in question_interest]
    # return {
    #     'cls': cls,
    #     'answer': answer_interest,
    #     'question': question_interest
    # }


if __name__ == '__main__':
    print(user_interest(1234))
