from analysis.common import *

from analysis.analysis_models import TagRelated
from data.models.sof_models import QuestionTags, Question, Tag


def get_tag_id(tag, tag_index):
    return tag_index[tag]


def index_tags_ids(min_question_num, save=True, msg=None):
    # step1: index tags with it's id
    tag_index = {}
    index_tag = {}
    for tag in Tag.raw(
            'select tag.id, tag.name from questiontags left join tag on questiontags.tag = tag.name group by questiontags.tag having count(question_id) > (%s)',
            min_question_num).execute():
        tag_index[tag.name] = tag.id
    for tag in tag_index:
        index_tag[tag_index[tag]] = tag
    save_step_data(tag_index, step='1-1', save=save, msg=msg)
    save_step_data(index_tag, step='1-2', save=save, msg=msg)
    logger.info(f'get tag index finished, tags: {len(tag_index.keys())}')
    return tag_index, index_tag


def index_tags_questions(tag_index, save=True, msg=None):
    # step2: index questions and tags to find questions of tag and tags of question
    tag_questions_index = {}
    question_tags_index = {}
    for question_tag in QuestionTags.raw(
                    'select * from questiontags where tag in ' + str(tuple(tag_index.keys()))).execute():
        tag = question_tag.tag
        question_id = question_tag.question_id
        if tag in tag_questions_index:
            tag_questions_index[tag].add(question_id)
        else:
            tag_questions_index[tag] = {question_id}
        if question_id in question_tags_index:
            question_tags_index[question_id].add(tag)
        else:
            question_tags_index[question_id] = {tag}
    for question in question_tags_index:
        question_tags_index[question] = list(question_tags_index[question])
    for tag in tag_questions_index:
        tag_questions_index[tag] = list(tag_questions_index[tag])
    save_step_data(tag_questions_index, step='2-1', save=save, msg=msg)
    save_step_data(question_tags_index, step='2-2', save=save, msg=msg)
    logger.info(f'index tag questions finished, questions: {len(question_tags_index.keys())}')
    return tag_questions_index, question_tags_index


def get_related_couples(question_tags_index, save=True, msg=None):
    # get all related couple
    if question_tags_index is None:
        question_tags_index = load_step_file('2-2')
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
    save_step_data(related_set, step='3', transfer_item=lambda item: f'{item[0]} {item[1]}', save=save, msg=msg)
    logger.info(f'get all related couple finished, related: {len(related_set)}')
    return related_set


def calculate_related_weight(tag_questions_index, related_set, weight_func=None, save=True, msg=None):
    # calculate weight of related couples
    if tag_questions_index is None:
        tag_questions_index = load_step_file('2-1')
    if related_set is None:
        related_set = load_step_file('3')
    if not weight_func:
        weight_func = lambda a, b, u: (a + b - u) / min(a, b)
    related_weight = []
    for related in related_set:
        tag1_count = len(tag_questions_index[related[0]])
        tag2_count = len(tag_questions_index[related[1]])
        all = len(set(tag_questions_index[related[0]]) | set(tag_questions_index[related[1]]))
        weight = weight_func(tag1_count, tag2_count, all)
        related_weight.append((related[0], related[1], weight))
    save_step_data(related_weight, step='4', transfer_item=lambda item: f'{item[0]} {item[1]} {item[2]}',
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

def save_related_to_bd(related_weight):
    TagRelated.truncate_table()
    TagRelated.insert_many_execute(
        ({'tag_from': tag1, 'tag_to': tag2, 'weight': weight} for (tag1, tag2, weight) in related_weight)
    ).execute()


def tag_related_pretreatment(min_question_num=100, msg=None, step_file_dir=None, step=None, **kwargs):
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
        (tag_index, index_tag) = index_tags_ids(min_question_num, msg=msg)
    if config['step'] <= 2:
        if tag_index is None:
            tag_index = load_step_file('1-1')
        (tag_questions_index, question_tags_index) = index_tags_questions(tag_index, msg=msg)
    if config['step'] <= 3:
        related_couples = get_related_couples(question_tags_index, msg=msg)
    if config['step'] <= 4:
        related_weight = calculate_related_weight(tag_questions_index, related_couples, msg=msg)
    if config['step'] <= 5:
        save_related_to_bd(related_weight)

class WeightFuncs:
    inter_divide_union = lambda a, b, u: (a + b - u) / u
    inter_divide_min = lambda a, b, u: (a + b - u) / min(a, b)
    inter_divide_max = lambda a, b, u: (a + b - u) / max(a, b)

if __name__ == '__main__':
    tag_related_pretreatment(
        msg='min weight 0.1, weight=(tag1_count + tag2_count - all) / min(tag1_count, tag2_count)',
        step_file_dir='2018-04-20 13-04-48',
        step=5
    )
    # print(create_tag('xxxxxxx'))