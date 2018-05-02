from analysis.classify_tag_v1 import TagClassifier
from data.cdn.sof_cdn import UserTagsCDN

clifer = TagClassifier()

def user_interest(user_id):
    user_tags = UserTagsCDN.get_user_tags(user_id)
    result = {}
    for item in user_tags:
        category = clifer.classify_tag(item['tag'])['category']
        if category in result:
            result[category][0] += item['question_count']
            result[category][1] += item['question_score']
            result[category][2] += item['answer_count']
            result[category][3] += item['answer_score']
        else:
            result[category] = [item['question_count'], item['question_score'], item['answer_count'], item['answer_score']]
    result.pop('invalid')
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
    print(user_interest(12345))