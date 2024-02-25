import utils
import consts

LAST_CHAPTER = 29
MANGA_NAME = 'avalon-of-disaster'

for chapter in range(1, LAST_CHAPTER):
  manga_url = utils.prepare_chapter_url(MANGA_NAME, chapter)
  utils.setup_storage(MANGA_NAME, chapter)
  image_sources = utils.extract_image_source(manga_url)
  
  for (idx, source) in enumerate(image_sources):
    file_count = idx + 1
    filename = utils.get_file_full_path(source, MANGA_NAME, chapter, file_count)
    utils.download_image(source, filename)