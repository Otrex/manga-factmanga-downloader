import os
import errno
import shutil
import requests
import consts
from bs4 import BeautifulSoup
from tqdm.auto import tqdm


def downloading(func):
  def wrapper(*args, **kwargs):
    print(f'  Downloading: {args[1]}')
    result = func(*args, **kwargs)
    return result
  return wrapper

def extract_file_extension(url):
  filename = os.path.basename(url.split("/")[-1])
  extension = os.path.splitext(filename)[1]
  if extension:
    return extension.lower().strip(".")
  else:
    return None
  
def get_file_full_path(url, manga_name, chapter, file_count):
  ext = extract_file_extension(url)
  path = os.path.join(consts.BASE_FOLDER, manga_name, f'{consts.CHAPTER_PREFIX}{chapter}', f'p-{file_count}.{ext}')
  return path
  
def extract_image_source(url):
  response = requests.get(url)
  response.raise_for_status()
  soup = BeautifulSoup(response.content, 'html.parser')
  divs = soup.find_all('div', class_=consts.IMAGE_WRAPPER_CLASS)
  return [
    div.find('img').get('data-src') for div in divs
  ]
  
def setup_storage(name, chapter):
  image_dir = os.path.join(consts.BASE_FOLDER, name, f'{consts.CHAPTER_PREFIX}{chapter}')
  try:
    os.makedirs(image_dir, exist_ok=True)
    print(f'Downloading: {name}[{consts.CHAPTER_PREFIX}{chapter}]')
  except OSError as e:
    if e.errno != errno.EEXIST:
      raise
    
def prepare_chapter_url(manga_name, chapter):
  return f'{consts.FACT_MANGA_BASE_URL}/{manga_name}/{consts.CHAPTER_PREFIX}{chapter}'
    
def download_image_legacy(url, filename):
  if not os.path.exists(filename):
    image_response = requests.get(url)
    image_response.raise_for_status()
    with open(os.path.join(filename), 'wb') as f:
      f.write(image_response.content)
    
    print(f'Downloaded image: {filename}')
  
@downloading
def download_image(url, filename):
  if not os.path.exists(filename):
    with requests.get(url, stream=True) as r:
      total_length = int(r.headers.get("Content-Length"))
      with tqdm.wrapattr(r.raw, "read", total=total_length, desc="")as raw:
        with open(filename, 'wb')as output:
          shutil.copyfileobj(raw, output)