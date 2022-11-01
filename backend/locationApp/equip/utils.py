from flask import url_for, current_app
import os
import secrets
from PIL import Image

def save_picture(form_picture):
  random_hex = secrets.token_hex(8)
  _, f_ext = os.path.splitext(form_picture.filename)

  sizes = {
    's': [250, 250],
    'm': [500, 500],
    'l': [1920, 1080]
  }
  for key, size in sizes.items():    
    output_size = (size[0], size[0])
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    picture_fn = random_hex + '_' + key + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/equip_pics', picture_fn)
    i.save(picture_path)

  return random_hex + '_m' + f_ext