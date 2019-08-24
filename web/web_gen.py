from typing import List
from math import cos, sin, pi
import os
from web.data_prepare import encode_img



def get_queue(nodes: list, canvas_size: tuple) -> list:
  coords = []
  center = (canvas_size[0] / 2, canvas_size[1] / 2)
  radius = min(canvas_size) / 2 - max([node.size for node in nodes])
  count = len(nodes)

  for i in range(len(nodes)):
    coords.append((int(center[0] + radius*cos(2*pi*i/count)),
                  int(center[1] + radius*sin(2*pi*i/count))))
  
  return coords


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
      for e in edges:
        img_onload += 'tmpCtx.moveTo(%d,%d);\ntmpCtx.lineTo(%d, %d);\n \
          tmpCtx.stroke();\n'  % (coords[e[0]][0], coords[e[0]][1], coords[e[1]][0], coords[e[1]][1])
    
    img_onload += '};\n'

  head = '<!DOCTYPE html>\n<html>\n<head>\n<title>Image drawing</title>\n \
        </head>\n<body>\n<canvas id="canvas" width=500 height=500></canvas>\n<script type="text/javascript">\n \
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
  coords = get_queue(graph.nodes, (500, 500))
  
  return make_page(imgz, graph.nodes, coords, graph.edges)