from redis import Redis
from data.config.config import config
from data.cdn.sof_cdn import QuestionsCDN, TagRelatedCDN
import argparse
import numpy as np

redis = Redis(connection_pool=config.redis)

def save():
    redis.save()

def save_to_db():
    # QuestionsCDN.load_to_cache()
    QuestionsCDN.save_to_db()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='cache tools')
    parser.add_argument('command')
    args = parser.parse_args()
    if args.command == 'save':
        save()
    elif args.command == 'save_to_db':
        save_to_db()
    elif args.command == 'tags_have_question':
        print(f'more than 100 questions: {len(QuestionsCDN.tags_have_questions(100))}')
        print(f'more than 50 questions: {len(QuestionsCDN.tags_have_questions(50))}')
    elif args.command == 'tag_related':
        tag_related = TagRelatedCDN.get_related_weight_all()
        values = list(tag_related.values())
        for i in np.arange(0, 0.1, 0.01):
            values = list(filter(lambda w: w > i, values))
            print(f'weight larger than {i}: {len(values)}')
