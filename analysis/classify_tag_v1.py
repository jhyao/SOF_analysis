from analysis.common import *
from data.cdn.sof_cdn import QuestionsCDN, TagsCDN
import numpy as np

from data.models.sof_models import Tag, QuestionTags


class TagClassifier(object):
    def __init__(self, min_question_num=50, self_check=False, from_db=False):
        self.min_question_num = min_question_num if min_question_num <= 100 else 100
        self.self_check = self_check
        self.tag_clf = TagsCDN.get_core_tag_clf()
        self.core_tag_index = dict([(tag, c) for c in self.tag_clf for tag in self.tag_clf[c]])
        self.tag_questions = QuestionsCDN.get_tag_questions_cached()
        self.from_db = from_db

    def get_questions(self, tag):
        questions = self.tag_questions.setdefault(tag, set())
        if len(questions) < self.min_question_num:
            self.tag_questions[tag] |= QuestionsCDN.get_tag_questions(tag, save=self.from_db, min_num=self.min_question_num)
        return self.tag_questions[tag]

    def get_weight(self, tag1, tag2, weight_func=WeightFuncs.inter_divide_min):
        # logger.debug(f'weight to tag: {tag1} to {tag2}')
        tag1_set = self.get_questions(tag1)
        tag2_set = self.get_questions(tag2)
        return weight_func(len(tag1_set), len(tag2_set), len(tag1_set | tag2_set))

    def average_weight_to_group(self, tag, c):
        # logger.debug(f'weight to group: {tag} to {c}')
        weights = [self.get_weight(tag, member) for member in self.tag_clf[c]]
        return sum(weights) / len(weights)

    def weights_to_groups(self, tag):
        weights = dict(
            [(c, self.average_weight_to_group(tag, c)) for c in self.tag_clf.keys() if c != 'others'])
        logger.debug(f'{tag} weights: {weights.values()}')
        return weights

    def classify_tag(self, tag):
        if tag in self.core_tag_index and not self.self_check:
            return self.core_tag_index[tag]
        category = TagsCDN.get_tag_category(tag)
        if not category or self.self_check:
            weights = self.weights_to_groups(tag)
            related_weights = self.detect_outliers(weights)
            if related_weights:
                category = max(related_weights, key=lambda item: related_weights[item])
            else:
                category = 'others'
            # if weights[category] < 0.01:
            #     category = 'others'
            logger.info(f'{tag} belongs to {category}')
            if not self.self_check:
                TagsCDN.set_tag_category(tag, category)
        return category

    @staticmethod
    def detect_outliers(weights):
        # 1st quartile (25%)
        Q1 = np.percentile(list(weights.values()), 25)
        # 3rd quartile (75%)
        Q3 = np.percentile(list(weights.values()), 75)
        # Interquartile range (IQR)
        IQR = Q3 - Q1
        # outlier step
        outlier_step = 1.5 * IQR
        # Determine a list of indices of outliers for feature col
        outlier_list_col = dict([(tag, weights[tag]) for tag in weights if weights[tag] > IQR + outlier_step])
        return outlier_list_col


if __name__ == '__main__':
    clifer = TagClassifier(from_db=True)
    for i, tag in enumerate(Tag.raw('select tag.id, tag.name from questiontags left join tag on questiontags.tag = tag.name group by questiontags.tag having count(question_id) > 50').execute()):
        logger.info(f'count {i}')
        c = clifer.classify_tag(tag.name)