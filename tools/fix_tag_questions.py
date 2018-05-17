from data.cdn.sof_cdn import QuestionsCDN

if __name__ == '__main__':
    QuestionsCDN.cache.add_tag_questions('reactjs', QuestionsCDN.get_tag_questions("{'reactjs'}"))
    QuestionsCDN.cache.add_tag_questions('jquery', QuestionsCDN.get_tag_questions("{'jquery'}"))
    QuestionsCDN.cache.add_tag_questions('react-redux', QuestionsCDN.get_tag_questions("{'react-redux'}"))
    QuestionsCDN.cache.add_tag_questions('node.js', QuestionsCDN.get_tag_questions("{'node.js'}"))
    QuestionsCDN.cache.hdel("{'reactjs'}")
    QuestionsCDN.cache.hdel("{'jquery'}")
    QuestionsCDN.cache.hdel("{'react-redux'}")
    QuestionsCDN.cache.hdel("{'node.js'}")
