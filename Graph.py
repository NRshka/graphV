from dataclasses import dataclass
from typing import Union, Any, List, Optional
from collections.abc import Iterable

from PIL import Image




class Node:
  img: Any
  size: Union[float, int, None]
  title: str
  isVisualized: bool
  numEdges: int
  ind: int

  def __init__(self, img=None, size:Union[float, int, None]=None, title:Union[str, None]=None):
    self.img = img
    self.size = size
    self.leafs = []
    self.isVisualized = False
    self.numEdges = 0

    if title != None:
      self.title = title
    else:
      self.title = ''
  
  def set_ind(self, ind: int):
    self.ind = ind



class Edge:

  def __init__(self, length:Union[float, int, None]=None, thickess:Union[float, int, None]=None,
              color:Union[int, str, None]=None, title:Union[str, None]=None):
    pass


class AGraph:
  def __init__(self):
    pass
  
  def add_edge(self):
    raise "Why are yo trying to run method of abstract class?"


class Graph(AGraph):
  def __init__(self, nodes:Optional[Iterable]):
    self.nodes = []

    if nodes is None:
      self.edges = []
      return
    assert isinstance(nodes, Iterable), "Nodes list must be iterable"
    
    self.count_nodes = len(nodes)
    self.edges = {}#self.count_nodes*[self.count_nodes*[[]]]
    for i in range(self.count_nodes):
      self.edges[i] = [[] for j in range(self.count_nodes)]
    '''
    for i in range(self.count_nodes):
      self.edges.append([])
      for _ in range(self.count_nodes):
        self.edges[i].append([])
    '''
    for ind, node in enumerate(nodes):
      node.ind = ind
      self.nodes.append(node)
    
  def add_edge(self, node1:Union[int, str], node2:Union[int, str], edge:Optional[Edge]=None):
    '''
    @params
    node1: first node, if int - index in list, if str - title of node
    node2: second node
    @return None
    '''

    ind1 = 0
    if isinstance(node1, int):
      assert node1 >= 0 and node1 < self.count_nodes, f"Incorrect index of node1: {node1}"
      ind1 = node1
    elif isinstance(node1, str):
      #find index of node by title
      for ind, node in enumerate(self.nodes):
        if node1 == node.title:
          ind1 = ind
          break
    
    ind2 = 0
    if isinstance(node2, int):
      assert node2 >= 0 and node2 < self.count_nodes, f"Incorrect index of node2: {node2}"
      ind2 = node2
    elif isinstance(node2, str):
      #find index of node by title
      for ind, node in enumerate(self.nodes):
        if node2 == node.title:
          ind2 = ind
          break

    self.nodes[ind1].leafs.append(self.nodes[ind2])
    self.nodes[ind1].leafs = list(set(self.nodes[ind1].leafs))
    self.nodes[ind2].leafs.append(self.nodes[ind1])
    self.nodes[ind2].leafs = list(set(self.nodes[ind2].leafs))
    if isinstance(edge, Edge):
      #self.edges.append((ind1, ind2, edge))
      #self.edges[ind1] = [[] for i in range(self.count_nodes)]
      self.edges[ind1][ind2].append(edge)
      self.edges[ind2][ind1].append(edge)
    elif edge is None:
      #self.edges[ind1] = [[] for i in range(self.count_nodes)]
      self.edges[ind1][ind2].append(Edge())
      self.edges[ind2][ind1].append(Edge())
  
  def save(self, file_name):
    with open(file_name, 'w') as file:
      for node in self.nodes:
        file.write(str(node.ind) + ': ')
        file.write(' '.join([str(leaf.ind) for leaf in node.leafs]))
        file.write('\n')