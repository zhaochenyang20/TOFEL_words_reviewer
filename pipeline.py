import os


def pipline():
    """
    批量生成 10 个单词本
    """
    import os
    for _ in range(10):
        os.system("python selector.py --r -n 100")


if __name__ == "__main__":
    pipline()