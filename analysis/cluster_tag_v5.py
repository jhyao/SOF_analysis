"""
step1: filtrate related weight 
step2: make weighted graph
step3: adjust weight with adjust_weight_file
step4: get small components, put them all in 'others' class
step5: check ignore_tags_file
step6: get laplacian matrix, get eigvecs
step7-pre1: pagerank on graph
step7-pre2: get top 100 tag
step7-pre3: get component graph of these 100 tag
step7: clustering with k-means, move small group to 'others' class
step8: match group name, draw graph, save file
step9: check clustering result, with classify method
"""

import functools
from scipy.sparse.linalg import eigs
import numpy as np

from analysis.classify_tag_v1 import TagClassifier
from analysis.common import *
import logging

from data.cdn.sof_cdn import TagsCDN, TagRelatedCDN, CoreTagClfCache, CoreTagRankCache

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def related_weight_filter(related_weight, min_weight=0.1, save=True, msg=None):
    # delete related with small weight
    related_weight_filted = list(filter(lambda related: related[2] > min_weight, related_weight))
    save_step_data(related_weight_filted, step='related_weight_filted', transfer_item=lambda item: f'{item[0]} {item[1]} {item[2]}',
                   save=save, msg=msg)
    logger.info(f'related weight filter finished, related: {len(related_weight_filted)}')
    return related_weight_filted
pos = None
def make_graph(related_weight_filted, save=True, msg=None):
    graph = nx.Graph()
    for related in related_weight_filted:
        graph.add_edge(related[0], related[1], weight=float(related[2]))
    global pos
    pos = nx.spring_layout(graph)
    save_graph(graph, 'tag-link.png', pos=pos, save=save, msg=msg)
    logger.info(f'create graph finish, tags: {len(graph.nodes)}')
    return graph


def weight_adjust(graph, adjust_file_path, save=True, msg=None):
    if adjust_file_path:
        adjust_weight = load_file(adjust_file_path)
        for related in adjust_weight:
            if graph.has_edge(related[0], related[1]):
                graph[related[0]][related[1]]['weight'] = related[2]
                logger.debug(f"adjust weight: {related[0]} {related[1]} {graph[related[0]][related[1]]['weight']}")
            else:
                graph.add_edge(related[0], related[1], weight=related[2])
                logger.debug(f"add weight: {related[0]} {related[1]} {related[2]}")
        save_graph(graph, 'tag-adjusted.png', save=save, msg=msg)
        save_step_data(adjust_weight, 'adjust_weight.txt', save=save, msg=msg)
    return graph


def get_center_tags(graph, k):
    tagranks = nx.pagerank(graph)
    tags = [(tag, tagranks[tag]) for tag in tagranks]
    tags.sort(key=lambda item: item[1], reverse=True)
    center_tags = [item[0] for item in tags[:k]]
    logger.info(f'center tags : {center_tags}')
    return center_tags


def center_tags_group(graph: nx.Graph, center_tags: list):
    subgraph = graph.subgraph(center_tags)
    components = nx.connected_components(subgraph)
    result = []
    for component in components:
        i = min([center_tags.index(tag) for tag in component])
        result.append(center_tags[i])
    return result


def laplacian_eigs(G, k, nodelist=None, save=True, msg=None):
    L = nx.laplacian_matrix(G, nodelist=nodelist)
    node_num = len(nodelist) if nodelist else len(G.nodes)
    eigval, eigvec = eigs(L, node_num - 2)
    dim = len(eigval)
    dictEigval = dict(zip(eigval, range(0, dim)))
    eigval_sort = np.sort(eigval)
    logger.debug(eigval_sort)
    kEig = eigval_sort[0: k]
    ix = [dictEigval[val] for val in kEig]
    eigvecs = eigvec[:, ix]
    if save:
        file_path = create_step_file_path('eigvecs.txt')
        np.savetxt(file_path, eigvecs)
    logger.info('gen eigvecs finished')
    return eigvecs


def graph_clustering(graph, k=8, individual_tags=None, ignore_tags=None, min_component=3, save=True, msg=None):
    # move small components to 'others' class, then do clustering on large components
    k = len(individual_tags) if individual_tags else k
    components = nx.connected_components(graph)
    small_node_sets = set()
    nodelist = set()
    individual_tags = set(individual_tags)
    for c in components:
        if set(c) & individual_tags:
            nodelist |= c
        else:
            small_node_sets |= c
            logger.debug('small component ' + str(c))
    # move ignore tags to others
    if ignore_tags:
        small_node_sets |= ignore_tags
        nodelist -= ignore_tags
        save_step_data(ignore_tags, 'ignore_tags.txt', save=save, msg=msg)
    nodelist = list(nodelist)
    # get laplacian matrix and do clustering
    eigvecs = laplacian_eigs(graph, k, nodelist=nodelist)
    # get init center for kmeans
    if individual_tags:
        init_center = eigvecs[[nodelist.index(center) for center in individual_tags if center not in small_node_sets]]
        clf = KMeans(k, init=init_center).fit(eigvecs).labels_
    else:
        clf = KMeans(k).fit(eigvecs).labels_

    # match k-means labels with nodelist order
    result = {}
    for i, c in enumerate(clf):
        if c in result:
            result[c].append(nodelist[i])
        else:
            result[c] = [nodelist[i]]

    # mark every class with the most important tag of the class
    tagranks = nx.pagerank(graph)
    for c in list(result.keys()):
        if len(result[c]) < min_component:
            # move small class to others
            small_node_sets |= set(result.pop(c))
            continue
        result[c].sort(key=functools.cmp_to_key(lambda a, b: tagranks[a] - tagranks[b]), reverse=True)
        result[result[c][0]] = result[c]
        result.pop(c)
    # add small components to final clf result
    result['others'] = list(small_node_sets)
    save_graph(graph, 'tag-clf.png', pos=pos, clf=result, save=save, msg=msg)
    save_step_data(result, 'tag-clf.json', save=save, msg=msg)
    save_step_data(tagranks, 'tag-rank.json', save=save, msg=msg)
    return result, tagranks


def check_clustering(clf, save=True, msg=None):
    clifer = TagClassifier(from_db=False, from_api=False, update=False)
    core_tags = list(clf.keys())
    if 'others' in core_tags:
        core_tags.remove('others')
    fail_list = []
    for c in clf:
        for tag in clf[c]:
            weights = [clifer.get_weight(tag, core) for core in core_tags]
            max_weight = max(weights)
            if max_weight != weights[core_tags.index(c)] or max_weight == 0:
                fail_list.append([tag, c, core_tags[weights.index(max_weight)]])
    save_step_data(fail_list, 'check_fail_tags.txt', save=save, msg=msg, transfer_item=lambda item: f'item[0] item[1] item[2]')
    return fail_list


def save_to_cdn(tag_clf, tag_rank):
    tag_clf.pop('others', [])
    CoreTagClfCache.set(tag_clf)
    CoreTagRankCache.set(tag_rank)


def tag_clustering(related_weight, k=20, ignore_tags_path=None, adjust_path=None,
                   min_weight=0.1, min_component=10, individual_tags=None,
                   file_dir=None, step=None, save_middle=True, msg=None, **kwargs):
    if file_dir is not None:
        config['file_dir'] = file_dir
    if step is not None:
        config['step'] = step if step > 0 else 1
    step = config['step']

    if ignore_tags_path:
        ignore_tags = set(load_file(ignore_tags_path))
    else:
        ignore_tags = None
    related_weight_filted = related_weight_filter(related_weight, min_weight=min_weight, save=False, msg=msg)
    graph = make_graph(related_weight_filted, save=save_middle, msg=msg)
    graph = weight_adjust(graph, adjust_file_path=adjust_path, save=save_middle, msg=msg)
    result, tagranks = graph_clustering(graph, k=k, individual_tags=individual_tags, ignore_tags=ignore_tags, min_component=min_component, save=True, msg=msg)
    return result, tagranks

if __name__ == '__main__':
    min_weight = 0.25
    min_component = 10
    clustering_method = ClusterMethod.kmeans
    individual_tags = ['java', 'android', 'c#', 'apache-spark',
                       'javascript', 'css',
                       'python', 'ios', 'c++', 'php',
                       'sql', 'ruby', 'r', 'git', 'algorithm', 'linux']
    # input_path = r'E:\SOF\file\2018-04-23 16-02-54\4'
    # adjust_path = r'E:\SOF\file\tag_clustering\tag_weight_fix.txt'
    output_path = r'E:\SOF\file\tag_clustering_v4'
    # ignore_path = r'E:\SOF\file\tag_clustering\ignore_tags.txt'
    # individual_tags = None
    input_path = None
    adjust_path = None
    ignore_path = None

    related_weight = TagRelatedCDN.get_tag_related_filtered(min_weight)

    msg = f"version:4, related weight data from {input_path}\nmin_weight={min_weight}, min_component={min_component},clustering_method={clustering_method.__name__}, weight adjusted\n{individual_tags}\n"
    result, tagranks = tag_clustering(related_weight, file_dir=output_path, adjust_path=adjust_path,
                            ignore_tags_path=ignore_path, individual_tags=individual_tags,
                            min_component=min_component, min_weight=min_weight, save_middle=True, msg=msg)
    save_to_cdn(result, tagranks)
    # check_result(result, save=True, msg=None)
