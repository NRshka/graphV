from Graph import Graph, Node, Edge
from web import web_gen
from PIL import Image
from web.data_prepare import generate_unique_colors

import sys





if __name__ == "__main__":
  count_nodes = 7
  flower_img = Image.open('flower.jpg')
  # g = Graph([Node(flower_img, 50, 'title1'), Node(flower_img, 20, 'title2'),
  #           Node(flower_img, 10, 'title3'), Node(flower_img, 90, 'title4'),
  #           Node(flower_img, 10, 'title5'), Node(flower_img, 10, 'title6'),
  #           Node(flower_img, 10, 'title7'), Node(flower_img, 10, 'title8'),
  #           Node(flower_img, 10, 'title9'), Node(flower_img, 10, 'title10')])
  g = Graph([Node(flower_img, 10, 'title' + str(i)) for i in range(count_nodes-1)] + [Node(size=30, group=0)])

  g.add_edge(0, 2)
  g.add_edge(2, 1)
  g.add_edge(0, 3)
  g.add_edge(0, 4)
  g.add_edge(1, 5, Edge(thickness=3))
  g.add_edge(1, 6, Edge(color="ff0000"))

  web_gen.get_page(g)