import ast
import datetime
import json
import os

import itertools
import networkx as nx
from matplotlib import pyplot as plt

from analysis.analysis_models import TagRelated
from data.models.sof_models import QuestionTags, Question, Tag
import logging

logger = logging.getLogger(__name__)


config = {
    'file_dir': 'E:\\SOF\\file',
    'step_file_dir': None,
    'step_file_name': 'step',
    'step': 1
}

def create_file_folder():
    file_dir = config['file_dir']
    if not os.path.isdir(file_dir):
        os.mkdir(file_dir)
    step_file_dir = str(datetime.datetime.today()).split('.')[0].replace(':', '-')
    path = os.path.join(file_dir, step_file_dir)
    os.mkdir(path)
    return step_file_dir

def create_step_file(step):
    if config['step_file_dir'] is None:
        config['step_file_dir'] = create_file_folder()
    file_path = os.path.join(config['file_dir'], config['step_file_dir'], config['step_file_name'] + str(step))
    if os.path.isfile(file_path):
        return open(file_path, 'w')
    else:
        return open(file_path, 'x')


def load_step_file(step):
    if config['step_file_dir'] is None:
        return None
    file_path = os.path.join(config['file_dir'], config['step_file_dir'], config['step_file_name'] + str(step))
    if not os.path.isfile(file_path):
        return None
    with open(file_path, 'r') as step_file:
        result = []
        for line in step_file:
            line = line.rstrip()
            if line.startswith('#') or line == '':
                pass
            elif line.startswith('{') or line.startswith('['):
                result.append(json.loads(line))
            else:
                result.append([ast.literal_eval(num) for num in line.split(' ')])
        return result

def get_tag_id(tag, tag_index):
    return tag_index[tag]


def index_tags_ids(min_question_num):
    # step1: index tags with it's id
    tag_index = {}
    for tag in Tag.raw(
            'select tag.id, tag.name from questiontags left join tag on questiontags.tag = tag.name group by questiontags.tag having count(question_id) > (%s)',
            min_question_num).execute():
        tag_index[tag.name] = tag.id
    with create_step_file('1-1') as tag_index_file:
        tag_index_file.write('# step1-1: get tag index\n')
        tag_index_file.write(json.dumps(tag_index))
    with create_step_file('1-2') as step1_file:
        step1_file.write('# step1-2: get index tag\n')
        index_tag = {}
        for tag in tag_index:
            index_tag[tag_index[tag]] = tag
        step1_file.write(json.dumps(index_tag))
    logger.info(f'get tag index finished, tags: {len(tag_index.keys())}')
    return tag_index


def index_tags_questions(tag_index):
    # step2: index questions and tags to find questions of tag and tags of question
    if tag_index is None:
        tag_index = load_step_file('1-1')
    tag_questions_index = {}
    question_tags_index = {}
    for question_tag in QuestionTags.raw(
                    'select * from questiontags where tag in ' + str(tuple(tag_index.keys()))).execute():
        tag = get_tag_id(question_tag.tag, tag_index)
        question_id = question_tag.question_id
        if tag in tag_questions_index:
            tag_questions_index[tag].append(question_id)
        else:
            tag_questions_index[tag] = [question_id]
        if question_id in question_tags_index:
            question_tags_index[question_id].append(tag)
        else:
            question_tags_index[question_id] = [tag]
    with create_step_file('2-1') as step21_file:
        step21_file.write('# step2-1: index tag questions\n')
        step21_file.write(json.dumps(tag_questions_index))
    with create_step_file('2-2') as step22_file:
        step22_file.write('# step2-2: index question tags\n')
        step22_file.write(json.dumps(question_tags_index))
    logger.info(f'index tag questions finished, questions: {len(question_tags_index.keys())}')
    return tag_questions_index, question_tags_index


def get_related_couples(question_tags_index):
    # get all related couple
    if question_tags_index is None:
        question_tags_index = load_step_file('2-2')
    related_set = set()
    step3_file = create_step_file(3)
    step3_file.write('# step3: get all related couple\n')
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
                    step3_file.write(f'{related[0]} {related[1]}\n')
    step3_file.close()
    logger.info(f'get all related couple finished, related: {len(related_set)}')
    return related_set


def calculate_related_weight(tag_questions_index, related_set):
    # calculate weight of related couples
    if tag_questions_index is None:
        tag_questions_index = load_step_file('2-1')
    if related_set is None:
        related_set = load_step_file('3')
    related_weight = []
    step4_file = create_step_file(4)
    step4_file.write('# step4: calculate related weight\n')
    for related in related_set:
        tag1_count = len(tag_questions_index[related[0]])
        tag2_count = len(tag_questions_index[related[1]])
        all = len(set(tag_questions_index[related[0]]) | set(tag_questions_index[related[1]]))
        weight = (tag1_count + tag2_count - all) / min(tag1_count, tag2_count)
        step4_file.write(f'{related[0]} {related[1]} {weight}\n')
        related_weight.append((related[0], related[1], weight))
    step4_file.close()
    logger.info(f'calculate related weight finished, related: {len(related_weight)}')
    return related_weight


def related_weight_filter(related_weight, min_weight=0.1):
    # delete related with small weight
    if related_weight is None:
        related_weight = load_step_file(4)
    related_weight_filted = list(filter(lambda related: related[2] > min_weight, related_weight))
    with create_step_file(5) as f:
        f.write(f'# related weight larger than {min_weight}\n')
        for item in related_weight_filted:
            f.write(f'{item[0]} {item[1]} {item[2]}\n')
    logger.info(f'related weight filter finished, related: {len(related_weight_filted)}')
    return related_weight_filted


def graph_clustering(related_weight_filted, index_tag):
    graph = nx.Graph()
    graph.add_nodes_from(index_tag.keys())
    for related in related_weight_filted:
        graph.add_edge(related[0], related[1], weight=related[2])



def tag_related_pretreatment(min_question_num=100, min_weight=0.1, step_file_dir=None, step=None, **kwargs):
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
        tag_index, index_tag = index_tags_ids(min_question_num)
    if config['step'] <= 2:
        tag_questions_index, question_tags_index = index_tags_questions(tag_index)
    if config['step'] <= 3:
        related_couples = get_related_couples(question_tags_index)
    if config['step'] <= 4:
        related_weight = calculate_related_weight(tag_questions_index, related_couples)
    if config['step'] <= 5:
        related_weight_filted = related_weight_filter(related_weight, min_weight)
    if config['step'] <= 6:
        # related_weight_filted = related_weight_filter(related_weight_filted, index_tag)
        pass


if __name__ == '__main__':
    tag_related_pretreatment(min_weight=0.1, step_file_dir='2018-04-18 14-51-26', step=5)
    # print(create_tag('xxxxxxx'))