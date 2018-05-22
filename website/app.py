from flask import Flask, jsonify, send_from_directory
from data.cdn.sof_cdn import TagsCDN, CoreTagClfCache
from analysis.classify_tag_v1 import TagClassifier
import analysis.user_interest_analysis as user_analysis

import logging

logger = logging.getLogger(__name__)

clifer_config = {
    'min_question_num': 100, 'min_weight': 0.1,
    'from_db': False, 'from_api': False, 'from_cache': True,
    'related_cache': False, 'save_db': False, 'update': False
}

user_tags_config = {
    'from_db': False,
    'from_cache': True,
    'from_api': True,
    'max_page': 5
}

app = Flask(__name__)
clifer = TagClassifier(min_question_num=clifer_config['min_question_num'], min_weight=clifer_config['min_weight'],
                       update=clifer_config['update'], from_db=clifer_config['from_db'],
                       from_api=clifer_config['from_api'], from_cache=clifer_config['from_cache'],
                       related_cache=clifer_config['related_cache'], save_db=clifer_config['save_db'])
user_analysis.set_clifer(clifer)
user_analysis.set_config(**user_tags_config)

@app.route('/static/<path:path>')
def static_file(path):
    return send_from_directory('static', path)


@app.route('/')
def home():
    return jsonify({'is_core': True})


@app.route('/api/tagclf')
def get_tag_clf():
    return jsonify(CoreTagClfCache.get())


@app.route('/api/tag/<tag_name>/classify')
def get_tag_category(tag_name):
    category = clifer.classify_tag(tag_name)
    logger.info(category)
    return jsonify(category)


@app.route('/api/user/<user_id>/interest')
def get_user_interest(user_id):
    data = user_analysis.user_interest(user_id)
    return jsonify(data)


if __name__ == '__main__':
    # app.debug = True
    app.run()
