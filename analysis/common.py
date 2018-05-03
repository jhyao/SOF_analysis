import ast
import datetime
import json
import os
import logging

import matplotlib.colors
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.cluster import *
from data.model2json import ModelEncoder

config = {
    'file_dir': 'E:\\SOF\\file',
    'step_file_dir': None,
    'step_file_name': '',
    'step': 1
}

logger = logging.getLogger(__name__)


class WeightFuncs:
    @staticmethod
    def inter_divide_union(a, b, u):
        try:
            return (a + b - u) / u
        except:
            return 0
    @staticmethod
    def inter_divide_min(a, b, u):
        try:
            return (a + b - u) / min(a, b)
        except:
            return 0
    @staticmethod
    def inter_divide_max(a, b, u):
        try:
            return (a + b - u) / max(a, b)
        except:
            return 0


class ClusterMethod:
    @staticmethod
    def kmeans(n_clusters, eigvecs):
        s = KMeans(n_clusters=n_clusters).fit(eigvecs)
        return s.labels_

    @staticmethod
    def agglomerative(n_clusters, eigvecs):
        s = AgglomerativeClustering(n_clusters=n_clusters).fit(eigvecs)
        return s.labels_

    @staticmethod
    def spectral(n_clusters, eigvecs):
        s = SpectralClustering(n_clusters=n_clusters).fit(eigvecs)
        return s.labels_


def create_file_folder():
    file_dir = config['file_dir']
    if not os.path.isdir(file_dir):
        os.mkdir(file_dir)
    step_file_dir = str(datetime.datetime.today()).split('.')[0].replace(':', '-')
    path = os.path.join(file_dir, step_file_dir)
    os.mkdir(path)
    return step_file_dir

def create_step_file_path(step):
    if config['step_file_dir'] is None:
        config['step_file_dir'] = create_file_folder()
    file_path = os.path.join(config['file_dir'], config['step_file_dir'], config['step_file_name'] + str(step))
    return file_path

def create_step_file(step, file_path=None):
    file_path = file_path or create_step_file_path(step)
    if os.path.isfile(file_path):
        return open(file_path, 'w')
    else:
        return open(file_path, 'x')


def load_step_file(step):
    if config['step_file_dir'] is None:
        return None
    file_path = os.path.join(config['file_dir'], config['step_file_dir'], config['step_file_name'] + str(step))
    if not os.path.isfile(file_path):
        return None
    return load_file(file_path)


def load_file(file_path):
    with open(file_path, 'r') as step_file:
        result = []
        for line in step_file:
            line = line.rstrip()
            if line.startswith('#') or line == '':
                pass
            elif line.startswith('{') or line.startswith('['):
                result.append(json.loads(line))
            else:
                if len(line.split(' ')) > 1:
                    result.append([transfer_field(field) for field in line.split(' ')])
                else:
                    result.append(transfer_field(line))
        return result

def transfer_field(field):
    try:
        field = ast.literal_eval(field)
    except:
        pass
    return field


def save_step_data(data, step, transfer_item=None, save=True, msg=None, file_path=None):
    if not save:
        return
    file = create_step_file(step, file_path)
    if msg:
        for l in msg.split('\n'):
            file.write(f'# {l}\n')
    if isinstance(data, dict):
        file.write(ModelEncoder().encode(data))
    elif hasattr(data, '__iter__'):
        for item in data:
            if transfer_item:
                file.write(transfer_item(item) + '\n')
            else:
                file.write(str(item) + '\n')
    else:
        pass
    file.close()


def save_graph(graph, step, clf=None, save=True, msg=None, fig_size=20, node_size=5,
               edge_color='#acacac', edge_cm='Greys', clf_cm='gist_rainbow', font_size=12):
    if not save:
        return
    file_path = create_step_file_path(step)
    pos = nx.spring_layout(graph)
    fig = plt.figure(figsize=(fig_size, fig_size))
    if msg:
        fig.suptitle(msg)
    if clf is None:
        nx.draw(graph, pos, with_labels=True, font_weight='bold', node_size=node_size)
    else:
        nx.draw_networkx_edges(graph, pos, edge_color=edge_color, edge_cmap=plt.cm.get_cmap(edge_cm))
        clf_colors_mapper = plt.cm.ScalarMappable(matplotlib.colors.Normalize(0, len(clf.keys()) - 1),
                                                  plt.cm.get_cmap(clf_cm))
        for i, c in enumerate(clf.keys()):
            color = clf_colors_mapper.to_rgba(i)
            # logger.debug(color)
            nx.draw_networkx_nodes(graph, pos, nodelist=clf[c], node_size=node_size, node_color=color)
            nx.draw_networkx_labels(graph, pos, labels=dict((n, n) for n in clf[c]), font_size=font_size, font_color=color)
    plt.savefig(file_path)
