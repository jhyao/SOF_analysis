import os

from analysis.analysis_models import TagRelated
from data.models.sof_models import QuestionTags, Question, Tag
import logging

tag_related_path = 'E:\\SOF\\file\\tag_related.txt'
tag_related_weight_path = 'E:\\SOF\\file\\tag_related_weight.txt'
tag_index_path = 'E:\\SOF\\file\\tag_index.txt'

tag_index = {}  # {'tag': }
related_set = set()
tag_questions = {}
tag_list = []
related_pool = []
pool_size = 200


def index(tag):
    if tag in tag_index:
        return tag_index[tag]
    else:
        return create_tag(tag)

def create_tag(tag):
    Tag.create(name=tag)
    return Tag.get(name=tag).id


def renew_file(path):
    if os.path.exists(path):
        os.remove(path)
    f = open(path, 'w+')
    f.close()


def renew_result_table():
    TagRelated.drop_table()
    TagRelated.create_table()


def related_rate(tag1, tag2):
    tag1_count = QuestionTags.select(QuestionTags.question_id).distinct().where(QuestionTags.tag == tag1).count()
    tag2_count = QuestionTags.select(QuestionTags.question_id).distinct().where(QuestionTags.tag == tag2).count()
    all_count = QuestionTags.select(QuestionTags.question_id).where(
        (QuestionTags.tag == tag2) | (QuestionTags.tag == tag1)).distinct().count()
    common = tag1_count + tag2_count - all_count
    return common / min([tag1_count, tag2_count])


def get_related_weight_file():
    """
    result file format:
    tag1id tag2id weight
    """
    renew_file(tag_related_weight_path)
    renew_result_table()
    f = open(tag_related_weight_path, 'a')
    for tag in Tag.select(Tag.id, Tag.name):
        tag_index[tag.name] = tag.id
    for question in Question.select(Question.question_id):
        question_id = question.question_id
        tags = [question_tag.tag for question_tag in
                QuestionTags.get_all(QuestionTags.question_id == question_id)]
        for tag in tags:
            if tag in tag_questions:
                tag_questions[tag].add(question_id)
            else:
                tag_questions[tag] = {question_id}
        for i in range(len(tags)):
            for j in range(i + 1, len(tags)):
                if tags[i] > tags[j]:
                    related = (tags[j], tags[i])
                else:
                    related = (tags[i], tags[j])
                if not related in related_set:
                    related_set.add(related)
    for related in related_set:
        tag1_count = len(tag_questions[related[0]])
        tag2_count = len(tag_questions[related[1]])
        all = len(tag_questions[related[0]] | tag_questions[related[1]])
        weight = (tag1_count + tag2_count - all) / min(tag1_count, tag2_count)
        tag_from = index(related[0])
        tag_to = index(related[1])
        # TagRelated.insert_or_update(TagRelated.tag_from == tag_from, TagRelated.tag_to == tag_to,
        #                             tag_from=tag_from, tag_to=tag_to, weight=weight)
        related_pool.append({'tag_from': tag_from, 'tag_to': tag_to, 'weight': weight})
        if len(related_pool) >= pool_size:
            QuestionTags.insert_many_execute(related_pool)
        f.write(f'{tag_from} {tag_to} {weight}\n')
        print(f'{tag_from} {tag_to} {weight}')
    QuestionTags.insert_many_execute(related_pool)
    f.close()


if __name__ == '__main__':
    get_related_weight_file()
    # print(create_tag('xxxxxxx'))