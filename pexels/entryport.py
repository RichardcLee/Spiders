import os


def run(cmd):
    os.system(cmd)


if __name__ == '__main__':
    run("scrapy crawl pexels_spider")
