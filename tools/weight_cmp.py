from analysis.common import WeightFuncs
from data.cdn.sof_cdn import QuestionsCDN

def get_weight(tag1, tag2, method=WeightFuncs.inter_divide_union):
    tag1_q = QuestionsCDN.get_tag_questions(tag1)
    tag2_q = QuestionsCDN.get_tag_questions(tag2)
    n1 = len(tag1_q)
    n2 = len(tag2_q)
    nu = len(tag1_q | tag2_q)
    weight1 = method(n1, n2, nu)
    weight2 = WeightFuncs.inter_divide_min(n1, n2, nu)
    return [n1, n1+n2-nu, nu, weight1, weight2]


if __name__ == '__main__':
    tag_list = [
    "reactjs",
    "node.js",
    "jquery",
    "ajax",
    "java",
    "android",
    "database",
    "python"
    ]
    for tag in tag_list:
        print(f"{tag} {get_weight(tag, 'javascript')}")