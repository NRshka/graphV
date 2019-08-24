from Graph import Graph, Node
from web import web_gen
from PIL import Image







if __name__ == "__main__":
  flower_img = Image.open('flower.jpg')
  g = Graph([Node(flower_img, 50, 'title1'), Node(flower_img, 20, 'title2'),
            Node(flower_img, 10, 'title3'), Node(flower_img, 90, 'title4')])
  g.add_edge(0, 'title2')
  g.add_edge(1, 2)
  g.add_edge(2, 0)
  g.add_edge(3, 0)
  
  print(g.edges)
  web_gen.get_page(g)