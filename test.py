from Graph import Graph, Node
from web import web_gen
from PIL import Image

import random as rand





if __name__ == "__main__":
  count_nodes = 10
  flower_img = Image.open('flower.jpg')
  # g = Graph([Node(flower_img, 50, 'title1'), Node(flower_img, 20, 'title2'),
  #           Node(flower_img, 10, 'title3'), Node(flower_img, 90, 'title4'),
  #           Node(flower_img, 10, 'title5'), Node(flower_img, 10, 'title6'),
  #           Node(flower_img, 10, 'title7'), Node(flower_img, 10, 'title8'),
  #           Node(flower_img, 10, 'title9'), Node(flower_img, 10, 'title10')])
  g = Graph([Node(flower_img, 10, 'title' + str(i + 1)) for i in range(count_nodes)])
  g.add_edge(0, 'title2')
  g.add_edge(1, 2)
  g.add_edge(2, 0)
  g.add_edge(3, 0)
  for i in range(1000):
    for j in range(rand.randint(0, 2*count_nodes)):
      a = rand.randint(0, count_nodes - 1)
      b = rand.randint(0, count_nodes - 1)
      g.add_edge(a, b)
  
  web_gen.get_page(g)