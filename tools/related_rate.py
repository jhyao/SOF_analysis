from data.models.sof_models import Tag, QuestionTags


def related_rate(tag1, tag2):
    tag1_count = QuestionTags.select(QuestionTags.question_id).distinct().where(QuestionTags.tag == tag1).count()
    tag2_count = QuestionTags.select(QuestionTags.question_id).distinct().where(QuestionTags.tag == tag2).count()
    all_count = QuestionTags.select(QuestionTags.question_id).where((QuestionTags.tag == tag2) | (QuestionTags.tag == tag1)).distinct().count()
    print(f'{tag1}: {tag1_count}, {tag2}: {tag2_count}, all: {all_count}')
    common = tag1_count + tag2_count - all_count
    return common / min([tag1_count, tag2_count])

if __name__ == '__main__':
    print(related_rate('data.table', 'r'))