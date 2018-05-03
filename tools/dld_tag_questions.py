from data.cdn.sof_cdn import QuestionsCDN, TagsCDN

if __name__ == '__main__':
    for i, tag in enumerate(TagsCDN.get_tags(10000)):
        print(f'count {i}')
        QuestionsCDN.get_tag_questions(tag, save=False, from_db=False, min_num=100)
