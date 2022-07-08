import numpy as np
import argparse
from googletrans import Translator
from IPython import embed
from tqdm import tqdm
import os
import re


def parser_data():
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
    args = parser.parse_args()
    return args.random, args.num


def make_review(random, num, index):
    with open("./collection.txt", "r") as f:
        words = np.asarray(list(filter(None, f.read().split("\n"))))
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


def get_index():
    for _, __, files in os.walk("./data"):
        index = 0
        for file in files:
            if file.endswith(".txt"):
                index = max(
                    index, max([int(each) for each in (re.findall(r"\d+", file))])
                )
    return index

def pipline():
    import os
    for _ in range(10):
        os.system("python selector.py --r -n 100")

if __name__ == "__main__":
    try:
        make_review(*parser_data(), get_index())
    except Exception as e:
        embed(header=f"{e}")
