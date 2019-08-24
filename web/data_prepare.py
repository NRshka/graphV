import base64
from PIL.Image import Image
import io
from typing import Union


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