"""
step1: filtrate related weight 
step2: make weighted graph
step3: adjust weight with adjust_weight_file
step4: get small components, put them all in 'others' class
step5: check ignore_tags_file
step6: get laplacian matrix, get eigvecs
step7: select clustering algorithms, move small group to 'others' class
step8: match group name, draw graph, save file
step9: check clustering result, pass or fail
"""

import functools
from scipy.sparse.linalg import eigs
import numpy as np
from analysis.common import *
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def related_weight_filter(related_weight, min_weight=0.1, save=True, msg=None):
    # delete related with small weight
    related_weight_filted = list(filter(lambda related: related[2] > min_weight, related_weight))
    save_step_data(related_weight_filted, step='related_weight_filted', transfer_item=lambda item: f'{item[0]} {item[1]} {item[2]}',
                   save=save, msg=msg)
    logger.info(f'related weight filter finished, related: {len(related_weight_filted)}')
    return related_weight_filted

def make_graph(related_weight_filted, save=True, msg=None):
    graph = nx.Graph()
    for related in related_weight_filted:
        graph.add_edge(related[0], related[1], weight=float(related[2]))
    save_graph(graph, 'tag-link.png', save=save, msg=msg)
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


def graph_clustering(graph, k, clustering_method=None, ignore_tags=None, min_component=3, save=True, msg=None):
    # move small components to 'others' class, then do clustering on large components
    components = nx.connected_components(graph)
    small_node_sets = set()
    nodelist = set()
    for c in components:
        if len(c) < min_component:
            small_node_sets |= c
            logger.debug('small component ' + str(c))
        else:
            nodelist |= c
    # move ignore tags to others
    if ignore_tags:
        small_node_sets |= ignore_tags
        nodelist -= ignore_tags
        save_step_data(ignore_tags, 'ignore_tags.txt', save=save, msg=msg)
    nodelist = list(nodelist)
    small_node_sets = list(small_node_sets)
    # get laplacian matrix and do clustering
    eigvecs = laplacian_eigs(graph, k, nodelist=nodelist)
    clf = clustering_method(k, eigvecs)

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
            small_node_sets.extend(result.pop(c))
            continue
        result[c].sort(key=functools.cmp_to_key(lambda a, b: tagranks[a] - tagranks[b]), reverse=True)
        result[result[c][0]] = result[c]
        result.pop(c)
    # add small components to final clf result
    result['others'] = list(small_node_sets)
    save_graph(graph, 'tag-clf.png', clf=result, save=save, msg=msg)
    save_step_data(result, 'tag-clf.json', save=save, msg=msg)
    save_step_data(tagranks, 'tag-rank.json', save=save, msg=msg)
    return result


def check_clf(tag_clf, individual_tags, save=True, msg=None):
    if not individual_tags:
        return
    mix_result = []
    for c in tag_clf:
        mix = set(individual_tags) & set(tag_clf[c])
        if len(mix) > 1:
            mix_result.append(list(mix))
            logger.info(f'clf check mix: {mix}')
    save_step_data(mix_result, 'check_result.txt', save=save, msg=msg)
    return mix_result

def tag_clustering(k, related_weight_file_path, ignore_tags_path=None, adjust_path=None,
                   min_weight=0.1, min_component=10, clustering_method=None, individual_tags=None,
                   file_dir=None, step=None, save_middle=True, msg=None, **kwargs):
    if file_dir is not None:
        config['file_dir'] = file_dir
    if step is not None:
        config['step'] = step if step > 0 else 1
    step = config['step']

    related_weight = load_file(related_weight_file_path)
    if ignore_tags_path:
        ignore_tags = set(load_file(ignore_tags_path))
    else:
        ignore_tags = None
    related_weight_filted = related_weight_filter(related_weight, min_weight=min_weight, save=False, msg=msg)
    graph = make_graph(related_weight_filted, save=save_middle, msg=msg)
    graph = weight_adjust(graph, adjust_file_path=adjust_path, save=save_middle, msg=msg)
    result = graph_clustering(graph, k, clustering_method=clustering_method, ignore_tags=ignore_tags, min_component=min_component, save=True, msg=msg)
    check_result = check_clf(result, individual_tags, save=True, msg=msg)
    if len(check_result) > 0:
        logger.debug(check_result)
        logger.warning('check clf failed')
    else:
        logger.info('check clf pass')


if __name__ == '__main__':
    k = 18
    min_weight = 0.3
    min_component = 5
    clustering_method = ClusterMethod.spectral
    individual_tags = ['python', 'ios', 'r', 'android', 'c#', 'javascript', 'html', 'java', 'php', 'c++']
    input_path = r'E:\SOF\file\2018-04-23 16-02-54\4'
    adjust_path = r'E:\SOF\file\tag_clustering\tag_weight_fix.txt'
    output_path = r'E:\SOF\file\tag_clustering'
    ignore_path = r'E:\SOF\file\tag_clustering\ignore_tags.txt'
    msg = f'version:2, related weight data from {input_path}, min_weight={min_weight}, k={k}, min_component={min_component}, clustering_method={clustering_method.__name__}, weight adjusted'
    tag_clustering(k, input_path, clustering_method=clustering_method, file_dir=output_path, adjust_path=adjust_path,
                   ignore_tags_path=ignore_path, individual_tags=individual_tags,
                   min_component=min_component, min_weight=min_weight, save_middle=True, msg=msg)

