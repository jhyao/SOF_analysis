from data.cdn.sof_cdn import QuestionsCDN, UserTagsCDN

# q = QuestionsCDN.get_tag_questions('sharepoint', save=False)
# print(q)

t = UserTagsCDN.get_user_tags(12345)
print(t)