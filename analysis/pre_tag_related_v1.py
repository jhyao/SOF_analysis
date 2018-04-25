import os

from data.models.analysis_models import TagRelated
from data.models.sof_models import QuestionTags, Question, Tag

tag_related_path = 'E:\\SOF\\file\\tag_related.txt'
tag_related_weight_path = 'E:\\SOF\\file\\tag_related_weight.txt'
tag_index_path = 'E:\\SOF\\file\\tag_index.txt'

tag_index = {}  # {'tag': }
related_set = set()


def index(tag):
    return tag_index.setdefault(tag, Tag.get(name=tag).id)


def renew_file(path):
    if os.path.exists(path):
        os.remove(path)
    f = open(path, 'w+')
    f.close()


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
    renew_file(tag_related_path)
    f = open(tag_related_path, 'a')
    for question in Question.select():
        question_id = question.question_id
        tags = [question_tag.tag for question_tag in
                QuestionTags.get_all(QuestionTags.question_id == question_id)]
        for i in range(len(tags)):
            for j in range(i + 1, len(tags)):
                if tags[i] > tags[j]:
                    related = (index(tags[j]), index(tags[i]))
                else:
                    related = (index(tags[i]), index(tags[j]))
                if not related in related_set:
                    weight = related_rate(tags[i], tags[j])
                    TagRelated.insert_or_update(TagRelated.tag_from == related[0], TagRelated.tag_to == related[1],
                                                tag_from=related[0], tag_to=related[1], weight=weight)
                    related_set.add(related)
                    print(f'{tags[i]} {tags[j]} {weight}')
    f.close()


if __name__ == '__main__':
    get_related_weight_file()
