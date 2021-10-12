# richard lee
# 合并两个图片文件夹，去重

import hashlib
import os
from collections import defaultdict
import shutil
import logging

logging.basicConfig(level=logging.NOTSET)  # 设置日志级别


# ! 注意备份
# 合并 dir1, dir2 中的图片到 dir1，并删除 dir2
def merge_two(dir1, dir2, is_backend=True):

    logging.info("Merge %s and %s to %s" % (dir1, dir2, dir1))

    maps = defaultdict(bool)

    s = set()

    # 备份一下dir1
    if is_backend:
        shutil.copytree(dir1, dir1+"_backend")

    for fn in [*map(lambda x: os.path.join(dir1, x), os.listdir(dir1)), *map(lambda x: os.path.join(dir2, x), os.listdir(dir2))]:
        # 根据名字去重一下
        bn = os.path.basename(fn)
        if maps[bn]:
            continue

        maps[bn] = True

        # 根据图片内容MD5去重
        with open(fn, "rb") as fp:
            img = fp.read()
            md5 = hashlib.md5()
            md5.update(img)
            digest = md5.hexdigest()

            if digest in s:
                continue

            s.add(digest)

            with open(os.path.join(dir1, bn), "wb") as dfp:
                dfp.write(img)

    if is_backend: # 备份一下dir2
        os.rename(dir2, dir2+"_backend")
    else:  # 删除冗余
        shutil.rmtree(dir2)


# 合并farther_dir下所有子目录中的图片，必须用绝对路径
def merge_all(farther_dir):

    logging.info("Merge all in %s" % farther_dir)

    is_backend = True  # 只备份一次

    while True:

        dirs = list(filter(lambda x: os.path.isdir(x) and "backend" not in x,
                           map(lambda x: os.path.join(farther_dir, x),
                           os.listdir(farther_dir))))

        logging.info("Merge %d dirs, include: %s" % (len(dirs), dirs))

        if len(dirs) <= 2:  # 最后两个
            if len(dirs) == 2:
                merge_two(dirs[0], dirs[1], is_backend)

            os.rename(dirs[0], os.path.join(farther_dir, "merged"))  # 最终保存目录为merged
            logging.info("Merged successfully.")
            break

        if is_backend and len(dirs)//2*2 != len(dirs):  # 奇数个文件夹，需要单独备份一下最有一个文件夹
            os.rename(dirs[-1], dirs[-1] + "_backend")

        for i in range(0, len(dirs)//2*2, 2):  # 本轮抛弃单独的那个文件夹
            merge_two(dirs[i], dirs[i+1], is_backend)

        is_backend = False


if __name__ == "__main__":
    merge_all(r'D:\MyFile\projects\git projects\Spiders\baidu图片\temp')
    # merge_two()

