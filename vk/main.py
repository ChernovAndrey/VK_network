import vk_api
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd


class User(object):

    def __init__(self, login='xxx', password='xxx', id=28929682):
        vk_session = vk_api.VkApi(login, password)
        vk_session.auth()
        self.api = vk_session.get_api()
        self.nodes = None
        self.count_nodes = None
        self.adj_matrix = None
        # self.G = nx.Graph()
        self.id = id
        # self.match_dict = None
        self.flag_self = False

    def set_friends(self):
        d = self.api.friends.get(user_id=self.id)
        if self.flag_self:
            d['items'].append(self.id)

        self.nodes = np.array(d['items'])
        self.count_nodes = len(self.nodes)
        print('count nodes: ', self.count_nodes)
        self.adj_matrix = pd.DataFrame(0, dtype='int64', index=self.nodes, columns=self.nodes)

    def set_relations(self):
        for i in range(self.count_nodes):
            if i % 20 == 0:
                print('function set relations progress: ', i / self.count_nodes)
            try:
                d = self.api.friends.get(user_id=self.nodes[i])
            except:
                continue
            cur_friends = np.array(d['items'])
            common_friends = np.intersect1d(self.nodes, cur_friends, assume_unique=True)
            self.adj_matrix.loc[self.nodes[i], common_friends] = 1
            self.adj_matrix.loc[common_friends, self.nodes[i]] = 1


U = User()
U.set_friends()
U.set_relations()
G = nx.from_numpy_matrix(U.adj_matrix.values)

nx.draw(G, with_labels=False, font_weight='bold', node_size=10)
plt.savefig('network_andrey.png')
nx.write_gpickle(G, "andrey.gpickle")
# plt.show()
