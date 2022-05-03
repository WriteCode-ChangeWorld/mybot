from loguru import logger
from Arsenal.bot_img_search.bot_img_search import Bot_Img_Search

engines = Bot_Img_Search.engines
search = engines["Ascii2d"]().search

# file
def test_file(file=None):
    logger.info(file)
    result = search(file=file)
    return result

# url
def test_url(url=None):
    logger.info(url)
    result = search(url=url)
    return result

# if __name__ == "__main__":
#     file = r""
#     url = ""
#     test_file(file=file)
#     test_url(url=url)