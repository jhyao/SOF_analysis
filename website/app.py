from flask import Flask, jsonify, send_from_directory
from data.cdn.sof_cdn import TagsCDN, CoreTagClfCache
from analysis.classify_tag_v1 import TagClassifier
from analysis.user_interest_analysis import user_interest

import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)
clifer = TagClassifier(min_weight=0.1, update=True, from_db=False, from_api=False)

@app.route('/static/<path:path>')
def static_file(path):
    return send_from_directory('static', path)

@app.route('/')
def home():
    return jsonify({'is_core':True})

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
    data = user_interest(user_id)
    return jsonify(data)


if __name__ == '__main__':
    # app.debug = True
    app.run()