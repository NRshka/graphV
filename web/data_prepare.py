import base64
from PIL.Image import Image
import io
from typing import Union, List





def generate_unique_colors(count: int) -> List[str]:
  '''
  Make list of contrast colors in HTML codes
  @params
  count: int - count of unique elements
  @returns
  list of color codes ['#f305ac', ...]
  '''
  two_step: int = (count + 1) // 3
  third_step: int = two_step + count % 3
  res = []

  for i in range(1, two_step + 1):
    h = hex(int(i*16/two_step))[2:]
    if len(h) == 1:
      h = '0' + h
    color = '#' + h + '0000'
    res.append(color)
  for i in range(1, two_step + 1):
    h = hex(int(i*16/two_step))[2:]
    if len(h) == 1:
      h = '0' + h
    color = '#00' + h + '00'
    res.append(color)
  for i in range(1, third_step + 1):
    h = hex(int(i*16/third_step))[2:]
    if len(h) == 1:
      h = '0' + h
    color = '#0000' + h
    res.append(color)

  return res


def isIntersect(x1, y1, x2, y2, x3, y3, x4, y4):
  '''
  Check is sections are intersected
  @params
  coordinates
  @returns
  bool
  '''
  denominator = (y4-y3) * (x1-x2) - (x4-x3) * (y1-y2)
  if denominator == 0:
    if (x1*y2 - x2*y1)*(x4-x3) - (x3*y4 - x4*y3)*(x2-x1) == 0 and (x1*y2 - x2*y1)*(y4-y3) - (x3*y4 - x4*y3)*(y2-y1) == 0:
      return True
    else:
      return False
  else:
    numerator_a = (x4-x2)*(y4-y3)-(x4-x3)*(y4-y2)
    numerator_b = (x1-x2)*(y4-y2)-(x4-x2)*(y1-y2)
    Ua = numerator_a / denominator
    Ub = numerator_b / denominator
    if Ua >=0 and Ua <=1 and Ub >=0 and Ub <=1:
      return True
    else:
      return False
    
  raise ValueError('Unexpected error')


def encode_img(img:Union[Image, bytes]) -> str:
  '''
  Encode image to base64 coding
  @params
  img: PIL Image or bytes
  @returns
  string, base64 encoding
  '''

  data = b''

  if isinstance(img, Image):
    buffer = io.BytesIO()
    img.save(buffer, "JPEG")
    data = buffer.getvalue()
    del buffer
  elif isinstance(img, bytes):
    data = img
  else:
    raise TypeError(f"Incorrect type of first argument: img. \
      It must be {'PIL Image'} or {'bytes'}")

  return str(base64.b64encode(data), 'utf-8')


def merge_dicts(dict1: dict, dict2: dict) -> dict:
  new_dict = {}

  for key in dict1:
    new_dict[key] = dict1[key]
  
  for key in dict2:
    new_dict[key] = dict2[key]
  
  return new_dict


def sort3d(matrix: dict) -> list:
  '''
  Sort nodes by count of edges
  @params
  matrix: dictionary with edges from graph
  @returns
  list of node's indices
  One time i'm gonna get murdered because of this line
  '''
  #Test show this method more slow
  #return dict(sorted(matrix.items(),
  #      key=lambda s: sum([len(itemgetter(i)(s[1])) for i in range(len(matrix))])))
  return list(dict(sorted(matrix.items(),
        key=lambda s: sum([len(row) for row in s[1]]),
        reverse=True)).keys())

def tupled_dict_to_list(x: List[tuple]) -> List[tuple]:
  '''
  Convert tupled form of dict with numeric indices to list
  @params
  x: [(ind1, item1), (ind2, item2), ...]
  @returns
  list: [item1, item2, ...]
  '''
  s = sorted(x)
  l = []

  for tup in s:
    l += [tup[1]]
  
  return l