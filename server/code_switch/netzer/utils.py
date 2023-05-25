def hazard(r, s):
    num, den = 1, 1
    if s < len(r):
        num = r[s]
        den = sum([r[n] for n in range(len(r)) if n >= s])

    return num / den


def test_hazard():
    r = [0, 4, 2, 1, 1]
    for s in range(len(r)+1):
        h = hazard(r, s)
        print("s = {}".format(s))
        print("h = {}".format(h))
        print("*"*3)


if __name__ == '__main__':
    test_hazard()