import numpy as np
import argparse
from googletrans import Translator
from IPython import embed
from tqdm import tqdm
import os
import re


def parser_data():
    """
    从命令行读取用户参数
    做出如下约定：
    1. -n 表示用户希望从自己所选择范围内具体想要复习的单词数量
    2. --r 表示用户希望随机选择单词（不输入 --r 则表示不希望随机选择）
    3. -s 表示用户希望从第几个单词开始
    4. -l 表示用户希望复习的单词范围大小，也即从 start 开始，长度为 length
    具体的边界条件请查看代码细节
    Returns:
        _type_: _description_
    """
    parser = argparse.ArgumentParser(
        prog="TOELF words reviewer",
        description="choose random or sorted method.",
        allow_abbrev=True,
    )
    parser.add_argument(
        "-n",
        "--num",
        dest="num",
        type=int,
        default=50,
        help="how many words would you like to review",
    )
    parser.add_argument(
        "--r",
        action="store_true",
        dest="random",
        help="if you want to random select, then input --r, ohterwise do not",
    )
    # store_true 是 argpaser 的特殊行为，请自行查找使用方法
    parser.add_argument(
        '-s',
        dest="start",
        type=int,
        default=0,
        help='which index to start reading from',
    )
    parser.add_argument(
        '-l',
        dest="length",
        type=int,
        default=0,
        help='how many words would you randomly choose from',
    )
    args = parser.parse_args()
    return args.random, args.num, args.start, args.length


def make_review(random, num, start, length, index):
    """
    生成单词本的主函数
    Args:
        random ( bool ): 是否生成随机单词本
        num ( int ): 生成单词本所含单词的个数
        start ( int ): 从生词本的第几个单词开始
        length ( int ): 表示用户希望复习的单词范围大小，也即从 start 开始，长度为 length
        index (_type_): 从 ./data 文件夹下查找所有单词本最大的编号，即 index，将 index + 1 记为当做单词本的编号
    """
    try:
        with open("./collection.txt", "r") as f:
            words = np.asarray(list(filter(None, f.read().split("\n"))))
        # 此处使用了 numpy 模块的 asarray 方法，将字符串列表转换为 ndarray，实际上，原生列表 + 列表切片也能完成同样的功能
        # cut the words and fix some boundary conditions

        if length > 0 and length <= len(words):
            if start + length > len(words):
                words = words[start:]
            else:
                words = words[start:start + length]
            if num > length:
                num = length

        if random:
            print("random select")
            rng = np.random.default_rng()
            if num > words.size:
                num = words.size
            words = rng.choice(words, num, replace=False)
        translator = Translator(service_urls=["translate.googleapis.com"])
        with open(f"./data/untraslated_{index + 1}.txt", "w") as f:
            for idx, each in enumerate(words):
                similar_words = each.split(",")
                f.write(f"第 {idx + 1} 词组： ")
                for word in similar_words:
                    f.write(f"{word} ")
                f.write("\n")
        with open(f"./data/traslated_{index + 1}.txt", "w") as f:
            for i in tqdm(range(num)):
                similar_words = words[i].split(",")
                print(similar_words)
                f.write(f"第 {i + 1} 词组： ")
                for each in similar_words:
                    try:
                        f.write(
                            each + ":" + translator.translate(each, dest="zh-CN").text + " "
                        )
                    except Exception as e:
                        f.write(each + ":" + "翻译失败 ")
                f.write("\n")
        print("Done!")
    except Exception as e:
        embed(header=str(e))


def get_index():
    """
    使用 os.walk 方法来获取所有单词本的编号，返回单词本的最大编号，即 index
    Returns:
        index: 单词本的最大编号
    """
    for _, __, files in os.walk("./data"):
        index = 0
        for file in files:
            if file.endswith(".txt"):
                index = max(
                    index, max([int(each) for each in (re.findall(r"\d+", file))])
                )
    return index


if __name__ == "__main__":
    """使用 try except 来捕获异常，利用 embed 来处理异常"""
    make_review(*parser_data(), get_index())
