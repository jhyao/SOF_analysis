from data.cdn.sof_cdn import QuestionsCDN

q = QuestionsCDN.get_tag_questions('sharepoint', save=False)
print(q)