# Readme

本项目用于根据用户提供的生词本 `./collection.txt` 文件来生成复习所用的单词本。

具体使用参数约定如下：

```python
1. -n 表示用户希望从自己所选择范围内具体想要复习的单词数量
2. --r 表示用户希望随机选择单词（不输入 --r 则表示不希望随机选择）
3. -s 表示用户希望从第几个单词开始
4. -l 表示用户希望复习的单词范围大小，也即从 start 开始，长度为 length
```

例如：`python3 selector.py -n 100 --r -s 20 -l 200` 表示希望从生词本的第 20 个单词开始到第 220 个单词结束的范围内随机抽取 100 个生词生成生词本。

生词本存放于 `./data` 路径下，含有翻译完全和未翻译两种。旧的生词本不会被新生成的生词本覆盖。

# 项目环境

项目的基本环境在 `./requirements.yaml` 下，请运行如下指令 `conda env create -n <env_name> -f ./requirements.yaml` 添加新的 conda 环境。

代码中利用的谷歌翻译库安装方法如下：

1. Enter the file that contains the library:

```shell
cd py-googletrans
```

2.  Command to load the library: 

```shell
python3 setup.py install
```

Or use anthor universal command: 

```shell
pip install -e $(pwd)
```

注：如果该安装包安装失败的话，可尝试使用pygtrans库，安装方法如下：在conda的虚拟环境中输入
```shell
pip install pygtrans
```
即可完成安装，使用时只需
```python
from pygtrans import translate
```
即可。（目前自动安装的版本是 1.4.0）
