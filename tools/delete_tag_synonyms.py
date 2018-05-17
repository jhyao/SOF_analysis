from data.spider.sof_spider import TagsSynonymsApi
from data.models.sof_models import Tag

# get 3026 synonyms
# 263 in database
# delete 2766 count is null
# delete 263 from_tag is not null

if __name__ == '__main__':
    api = TagsSynonymsApi()
    for data in api.get_pages(page=25):
        for item in data:
            Tag.insert_or_update(Tag.name == item['from_tag'], name=item['from_tag'], from_tag=item['to_tag'])