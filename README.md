This project is based on a google API, which requires loading the library locally.

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

3. Go back to the last file:

```shell
cd ..
```

4. Run `selector.py` : 

```shell
>> python selector.py --help
usage: TOELF words reviewer [-h] [-n NUM] [--r] [-s START] [-l LENGTH]

choose random or sorted method.

optional arguments:
  -h, --help         show this help message and exit
  -n NUM, --num NUM  how many words would you like to review
  --r                if you want to random select, then input --r, ohterwise do not
  -s START           which index to start reading from
  -l LENGTH          how many words would you randomly choose from
```

