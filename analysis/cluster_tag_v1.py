import networkx as nx
from scipy.sparse.linalg import eigs
import matplotlib.pyplot as plt
import matplotlib.colors
import numpy as np
from sklearn.cluster import KMeans
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
    logger.info('create graph finish')
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
    return graph


def laplacian_eigs(G, k, save=True, msg=None):
    L = nx.normalized_laplacian_matrix(G)
    eigval, eigvec = eigs(L, len(G.nodes) - 2)
    dim = len(eigval)
    dictEigval = dict(zip(eigval, range(0, dim)))
    kEig = np.sort(eigval)[0: k]
    ix = [dictEigval[val] for val in kEig]
    eigvecs = eigvec[:, ix]
    if save:
        file_path = create_step_file_path('eigvecs.txt')
        np.savetxt(file_path, eigvecs)
    logger.info('gen eigvecs finished')
    return eigvecs


def kmeans_clustering(eigvecs, k, save=True, msg=None):
    clf = KMeans(n_clusters=k)
    s = clf.fit(eigvecs)
    clf = s.labels_
    save_step_data(str(clf), 'clf', save=save, msg=msg)
    return clf


def show_class(clf, graph, save=True, msg=None):
    result = {}
    nodelist = list(graph.nodes)
    for i, c in enumerate(clf):
        c = str(c)
        if c in result:
            result[c].append(nodelist[i])
        else:
            result[c] = [nodelist[i]]
    save_step_data(result, 'tag-clf.json', save=save, msg=msg)
    save_graph(graph, 'tag-clf.png', clf=result, save=save, msg=msg)
    return result


def tag_clustering(k, related_weight_file_path, min_weight=0.1, file_dir=None, step=None, adjust_path=None, save_middle=True, msg=None, **kwargs):
    if file_dir is not None:
        config['file_dir'] = file_dir
    if step is not None:
        config['step'] = step if step > 0 else 1
    step = config['step']

    related_weight = load_file(related_weight_file_path)
    related_weight_filted = related_weight_filter(related_weight, min_weight=min_weight, save=save_middle, msg=msg)
    graph = make_graph(related_weight_filted, save=save_middle, msg=msg)
    graph = weight_adjust(graph, adjust_file_path=adjust_path, save=save_middle, msg=msg)
    eigvecs = laplacian_eigs(graph, k, save=save_middle, msg=msg)
    clf = kmeans_clustering(eigvecs, k, save=save_middle, msg=msg)
    result = show_class(clf, graph, save=True, msg=msg)


if __name__ == '__main__':
    k = 20
    min_weight = 0.2
    input_path = r'E:\SOF\file\2018-04-20 13-04-48\step4'
    adjust_path = r'E:\SOF\file\tag_clustering\tag_weight_fix.txt'
    output_path = r'E:\SOF\file\tag_clustering'
    msg = f'related weight data from {input_path}, min_weight={min_weight}, k={k}, weight adjusted'
    tag_clustering(k, input_path, file_dir=output_path, adjust_path=adjust_path, min_weight=min_weight, save_middle=True, msg=msg)

