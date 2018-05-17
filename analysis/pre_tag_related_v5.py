"""
get data from cache
"""
from analysis.common import *
from data.cdn.sof_cdn import QuestionsCDN, TagRelatedCDN


def get_tag_id(tag, tag_index):
    return tag_index[tag]


def index_tags_questions(min_questions=100, save=True, msg=None):
    # step2: index questions and tags to find questions of tag and tags of question
    tag_questions_index = QuestionsCDN.get_tag_questions_filtered(min_question=min_questions)
    question_tags_index = {}
    for tag in tag_questions_index:
        for question in tag_questions_index[tag]:
            if question in question_tags_index:
                question_tags_index[question].append(tag)
            else:
                question_tags_index[question] = [tag]
    save_step_data(tag_questions_index, step='tag_questions.json', save=save, msg=msg)
    save_step_data(question_tags_index, step='question_tags.json', save=save, msg=msg)
    logger.info(f'index tag questions finished, questions: {len(question_tags_index.keys())}, tags: {len(tag_questions_index.keys())}')
    return tag_questions_index, question_tags_index


def get_related_couples(question_tags_index, save=True, msg=None):
    # get all related couple
    if question_tags_index is None:
        question_tags_index = load_step_file('question_tags.json')
    related_set = set()
    for question_id in question_tags_index:
        tags = question_tags_index[question_id]
        for i in range(len(tags)):
            for j in range(i + 1, len(tags)):
                if tags[i] > tags[j]:
                    related = (tags[j], tags[i])
                else:
                    related = (tags[i], tags[j])
                if related not in related_set:
                    related_set.add(related)
    save_step_data(related_set, step='related_couples.txt', transfer_item=lambda item: f'{item[0]} {item[1]}', save=save, msg=msg)
    logger.info(f'get all related couple finished, related: {len(related_set)}')
    return related_set


def calculate_related_weight(tag_questions_index, related_set, weight_func=None, save=True, msg=None):
    # calculate weight of related couples
    if tag_questions_index is None:
        tag_questions_index = load_step_file('tag_questions.json')
    if related_set is None:
        related_set = load_step_file('related_couples.txt')
    if not weight_func:
        weight_func = WeightFuncs.inter_divide_min
    related_weight = []
    for related in related_set:
        tag1_count = len(tag_questions_index[related[0]])
        tag2_count = len(tag_questions_index[related[1]])
        all = len(set(tag_questions_index[related[0]]) | set(tag_questions_index[related[1]]))
        weight = weight_func(tag1_count, tag2_count, all)
        related_weight.append((related[0], related[1], weight))
    save_step_data(related_weight, step='related_weight.txt', transfer_item=lambda item: f'{item[0]} {item[1]} {item[2]}',
                   save=save, msg=msg)
    logger.info(f'calculate related weight finished, related: {len(related_weight)}')
    return related_weight


# def related_weight_filter(related_weight, min_weight=0.1, save=True, msg=None):
#     # delete related with small weight
#     if related_weight is None:
#         related_weight = load_step_file(4)
#     related_weight_filted = list(filter(lambda related: related[2] > min_weight, related_weight))
#     save_step_data(related_weight_filted, step='5', transfer_item=lambda item: f'{item[0]} {item[1]} {item[2]}',
#                    save=save, msg=msg)
#     logger.info(f'related weight filter finished, related: {len(related_weight_filted)}')
#     return related_weight_filted

def save_related(related_weight):
    TagRelatedCDN.set_tag_related_many(related_weight)


def tag_related_pretreatment(min_question_num=100, save_middle=True, msg=None, weight_func=None, step_file_dir=None, step=None, **kwargs):
    tag_index = None
    tag_questions_index = None
    question_tags_index = None
    related_couples = None
    related_weight = None
    related_weight_filted = None
    index_tag = None

    if step_file_dir is not None:
        config['step_file_dir'] = step_file_dir
    if step is not None:
        config['step'] = step if step > 0 else 1
    step = config['step']

    if config['step'] <= 1:
        pass
    if config['step'] <= 2:
        (tag_questions_index, question_tags_index) = index_tags_questions(min_questions=min_question_num, save=save_middle, msg=msg)
    if config['step'] <= 3:
        related_couples = get_related_couples(question_tags_index,save=save_middle, msg=msg)
    if config['step'] <= 4:
        related_weight = calculate_related_weight(tag_questions_index, related_couples, save=True, msg=msg, weight_func=weight_func)
    if config['step'] <= 5:
        save_related(related_weight)


if __name__ == '__main__':
    min_question_num = 100
    weight_func = WeightFuncs.inter_divide_min
    msg = f'min_question_num={min_question_num}, weight_func={weight_func.__name__}'
    TagRelatedCDN.clear_cache()
    tag_related_pretreatment(min_question_num=min_question_num, weight_func=weight_func, msg=msg)
    # print(create_tag('xxxxxxx'))