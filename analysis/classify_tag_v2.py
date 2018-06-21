from analysis.common import *
from data.cdn.sof_cdn import QuestionsCDN, TagsCDN, CoreTagClfCache, TagRelatedCache
import numpy as np

from data.models.sof_models import Tag, QuestionTags


class TagClassifier(object):
    def __init__(self, min_question_num=100, min_weight=0.1,
                 update=False, from_db=True, from_api=True, from_cache=True,
                 related_cache=False, save_db=True):
        self.min_question_num = min_question_num
        self.tag_clf = CoreTagClfCache.get()
        self.core_tag_index = dict([(tag, c) for c in self.tag_clf for tag in self.tag_clf[c]])
        self.tag_questions = QuestionsCDN.get_tag_questions_cached()
        self.from_db = from_db
        self.from_api = from_api
        self.from_cache = from_cache
        self.update = update
        self.min_weight = min_weight
        self.related_cache = related_cache
        self.save_db = save_db

    def get_questions(self, tag):
        questions = self.tag_questions.setdefault(tag, set())
        if len(questions) < self.min_question_num:
            result_qs = QuestionsCDN.get_tag_questions(tag, save=self.from_db, min_num=self.min_question_num,
                                                       from_db=self.from_db, from_api=self.from_api,
                                                       from_cache=self.from_cache)
            self.tag_questions[tag] |= result_qs
        return self.tag_questions[tag]

    def get_weight(self, tag1, tag2, weight_func=WeightFuncs.inter_divide_min):
        # logger.debug(f'weight to tag: {tag1} to {tag2}')
        weight = TagRelatedCache.get_tag_related(tag1, tag2) if self.related_cache else -1
        if weight < 0 or self.update:
            tag1_set = self.get_questions(tag1)
            tag2_set = self.get_questions(tag2)
            weight = weight_func(len(tag1_set), len(tag2_set), len(tag1_set | tag2_set))
            if self.related_cache:
                TagRelatedCache.set_tag_related(tag1, tag2, weight)
        return weight

    def average_weight_to_group(self, tag, c):
        # logger.debug(f'weight to group: {tag} to {c}')
        weights = [self.get_weight(tag, member) for member in self.tag_clf[c]]
        # return sum(weights) / len(weights)
        weights_filtered = list(filter(lambda x: x>=self.min_weight, weights))
        if len(weights_filtered):
            return sum(weights_filtered) / len(weights_filtered)
        else:
            return 0

    def weights_to_groups(self, tag):
        weights = dict(
            [(c, self.average_weight_to_group(tag, c)) for c in self.tag_clf.keys() if c != 'others'])
        return weights

    def classify_tag(self, tag):
        # if tag in self.core_tag_index and not self.self_check:
        #     return self.core_tag_index[tag]
        if self.update:
            category = self.analysis_clf(tag)
            logger.info(f'{category}')
            if category['category'] != 'invalid':
                TagsCDN.set_tag_category(tag, category, to_db=self.save_db)
        else:
            category = TagsCDN.get_tag_category(tag, from_db=self.save_db)
            if not category:
                category = self.analysis_clf(tag)
                logger.info(f'{category}')
                if category['category'] != 'invalid' or self.from_api:
                    TagsCDN.set_tag_category(tag, category, to_db=self.save_db)
        return category

    def analysis_clf(self, tag):
        questions = self.get_questions(tag)
        if len(questions) < self.min_question_num:
            category = {
                'tag': tag,
                'category': 'invalid',
                'weights': {},
                'is_core': False
            }
        else:
            weights = self.weights_to_groups(tag)
            category = {
                'tag': tag,
                'weights': weights
            }
            if tag not in self.core_tag_index:
                category['category'] = self.detect_category(weights)
                category['is_core'] = False
            else:
                category['category'] = self.core_tag_index[tag]
                category['is_core'] = True
        return category

    @staticmethod
    def detect_category(weights):
        # 1st quartile (25%)
        values = list(filter(lambda w: w > 0, weights.values()))
        if not values:
            return 'others'
        else:
            return max(weights, key=lambda item: weights[item])
        # Q1 = np.percentile(values, 25)
        # # 3rd quartile (75%)
        # Q3 = np.percentile(values, 75)
        # # Interquartile range (IQR)
        # IQR = Q3 - Q1
        # # outlier step
        # outline = Q3 + 1.5 * IQR
        # # Determine a list of indices of outliers for feature col
        # related_weights = dict([(tag, weights[tag]) for tag in weights if weights[tag] > outline])
        # if len(related_weights) == 1:
        #     category = list(related_weights.keys())[0]
        # else:
        #     category = 'others'

        # return category

    def core_tags_check(self):
        count = 0
        for tag in self.core_tag_index:
            weights = self.classify_tag(tag)['weights']
            category = self.detect_category(weights)
            if category != self.core_tag_index[tag]:
                print(f'{tag} {self.core_tag_index[tag]} {category}')
                count += 1
        print(count)


if __name__ == '__main__':
    clifer = TagClassifier(from_db=False, from_api=False, update=True, min_weight=0.1, save_db=False, related_cache=False)
    TagsCDN.clear_tag_category()
    tags = Tag.select().where(Tag.count >= 100).order_by(-Tag.count).execute()
    for i, tag in enumerate(tags):
        logger.info(f'count {i}')
        c = clifer.classify_tag(tag.name)
    clifer.classify_tag('sdf')
    # clifer.core_tags_check()
    # weights = clifer.weights_to_groups('c++')
    # category = clifer.detect_category(weights)
    # print(category)