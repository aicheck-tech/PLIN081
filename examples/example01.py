import random


def train_test_split(data):
    random.shuffle(data)
    train = data[:len(data) // 2]
    random.shuffle(data)
    test = data[len(data) // 2:]
    return train, test


def trainTestValidationSplit(x):
    random.seed(158)
    if not x or len(x) < 3: raise ValueError("")
    random.shuffle(x)
    i = len(x) // 3
    return x[:i], x[i:i+i], x[2*i:]


def train_test_split_petr(data : list, ratio: float =0.8)-> tuple[list,list]:
    train = len(data)* ratio
    test = len(data) *ratio
    data = sorted(set(data))
    return random.sample(data,train),random.sample(data, test)
