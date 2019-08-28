from typing import List
from math import cos, sin, pi
import os
from .data_prepare import encode_img, sort3d, merge_dicts, tupled_dict_to_list



def get_queue1(nodes: list, canvas_size: tuple) -> list:
  coords = []
  center = (canvas_size[0] / 2, canvas_size[1] / 2)
  radius = min(canvas_size) / 2 - max([node.size for node in nodes])
  count = len(nodes)

  for i in range(len(nodes)):
    coords.append((int(center[0] + radius*cos(2*pi*i/count)),
                  int(center[1] + radius*sin(2*pi*i/count))))
  
  return coords



def get_queue(node, center: tuple, vector: float = 0, segment: float = 2*pi, radius: int = 150) -> List[tuple]:
  if node.isVisualized:
    return []
  
  coords: List[tuple] = [(node.ind, center)]
  node.isVisualized = True
  #radius: int = 100#СДЕЛАТЬ РАССЧИТЫВАЕМЫМ ПАРАМЕТРОМ НА ОСНОВЕ КОЛ-ВА ЛИСТЬЕВ, ЧТОБЫ НЕ СЛИВАТЬ ВСЁ В КУЧУ
  
  #count_leafs_on_next_ring: int = len(set([id(node) for leaf in node.leafs]))
  leafs_set = set()
  for leaf in node.leafs:
    if leaf.ind != node.ind and not leaf.isVisualized:
      leafs_set.add(leaf.ind)
  #for leaf in node.leafs:
  #  for l in leaf.leafs:
  #    if l.ind != node.ind and not l.isVisualized:
  #      leafs_set.add(id(l))
  count_leafs_on_next_ring: int = len(leafs_set)

  old_fargs = dict()
  d: float = segment / len([l for l in node.leafs if not l.isVisualized])# шаг, с которым ноды будут размещаться в сегменте
  for ind, leaf in enumerate(node.leafs):
    if leaf.isVisualized:
      continue
    
    farg: float = vector - segment/2 + ind*d
    old_fargs[leaf.ind] = farg
    coord: tuple = (center[0] + int(radius * cos(farg)), center[1] + int(radius*sin(farg)))#центр новой ноды
    coords.append((leaf.ind, coord))
    leaf.isVisualized = True

  for leaf in node.leafs:
    #d: float = segment / len(node.leafs)# шаг, с которым ноды будут размещаться в сегменте
    #farg: float = vector - segment/2 + ind*d
    #coord: tuple = (center[0] + int(radius * cos(farg)), center[1] + int(radius*sin(farg)))#центр новой ноды
    #coords.append((leaf.ind, coord))
    
    for nind, new_node in enumerate(leaf.leafs):
      if new_node.isVisualized:
        continue
        
      new_segment: float = 2*pi*len(new_node.leafs) / count_leafs_on_next_ring - (pi/5)
      new_vector: float = old_fargs[leaf.ind] + pi
            
      leafs_set = set()
      for l in new_node.leafs:
        if new_node.ind != l.ind and not l.isVisualized:
          leafs_set.add(new_node.ind)
      
      if len(leafs_set) % 2:
        #new_vector += pi# / 12
        #new_segment -= pi / 8
        pass
      
      nd: float = new_segment / len(leafs_set)# шаг, с которым ноды будут размещаться в сегменте
      new_farg = new_vector - new_segment/2 + nind*nd
      new_center = (coord[0] + int(radius*cos(new_farg)), coord[1] + int(radius*sin(new_farg)))
      radius = radius if radius % 2 else int(radius / 2)
      coords += get_queue(new_node, new_center, new_vector, new_segment, radius)#рекурентно пополняем список

  return coords

def get_coords(graph, canvas_size: tuple) -> List[tuple]:
  center = tuple(int(c / 2) for c in canvas_size)
  sorted_edges = sort3d(graph.edges)
  
  return get_queue(graph.nodes[sorted_edges[0]], center)

def make_page(img_base64: List[str], nodes: list, coords: List[tuple], edges) -> str:
  '''
  Create a html page fills with canvas.
  Graph drawn on canvas.
  @params
  img_Base64: list of base 64 encoded images
  nodes: list of graph nodes
  coords: list of (x, y [z]) tuples
  @returns
  string with htl page
  '''
  assert len(img_base64) == len(nodes), 'Lengts of first arg and second are not same.'
  f'{len(img_base64)} != {len(nodes)}'

  img_inits = ""
  img_onload = ""
  for key in edges:
    e = edges[key]
    for ind2, link in enumerate(e):
      for bone in link:
        #why third cycle? for loops over one node
        # I'll do it with arc algo
        img_onload += 'tmpCtx.moveTo(%d,%d);\ntmpCtx.lineWidth = %d;\n \
          tmpCtx.strokeStyle = "%s"\ntmpCtx.lineTo(%d, %d);\n \
          tmpCtx.stroke();\n'  % (coords[key][0], coords[key][1],
                                bone.thickness, bone.color,
                                coords[ind2][0], coords[ind2][1])
  
  for ind, pack in enumerate(zip(img_base64, nodes, coords)):
    src = pack[0]
    size = (pack[1].size, pack[1].size)
    coord = pack[2]

    img_inits += f'var img{ind} = new Image({size[0]},{size[1]});\n'
    img_inits += f'img{ind}.src = "data:image/jpeg;base64,{src}";\n'
    
    img_onload += 'img%d.onload = function() {\n \
            tmpCtx.save();\n \
            tmpCtx.beginPath();\n \
            tmpCtx.arc(%d, %d, 25, 0, Math.PI * 2, true);\n \
            tmpCtx.closePath();\n \
            tmpCtx.clip();\n \
            tmpCtx.drawImage(img%s, %d, %d, 50, 50);\n \
            tmpCtx.restore();\n \
            tmpCtx.font = "14px Arial"\n \
            tmpCtx.fillText("%s", %d, %d);\n \
        ' % (ind, coord[0], coord[1], ind, coord[0] - 25, coord[1] - 25,
            pack[1].title, coord[0] - 25, coord[1] + 25 + 14)
    if ind == len(nodes) - 1:
      pass
    
    img_onload += '};\n'

  head = '<!DOCTYPE html>\n<html>\n<head>\n<title>Image drawing</title>\n \
        </head>\n<body>\n<canvas id="canvas" width=1000 height=1000></canvas>\n<script type="text/javascript">\n \
        var canvas = document.getElementById("canvas");\n \
        var tmpCtx = canvas.getContext("2d");\n'
  end = '</script></body></html>'
  
  with open(os.path.join('web.html'), 'w', encoding='utf-8') as file:
    file.write(head)
    file.write(img_inits)
    file.write(img_onload)
    file.write(end)
  return ''


def get_page(graph):
  imgz = [encode_img(node.img) for node in graph.nodes]
  coords = get_coords(graph, (1000, 1000))
  
  coords = tupled_dict_to_list(coords)
  
  return make_page(imgz, graph.nodes, coords, graph.edges)