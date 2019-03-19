import os
import numpy as np


class Data:
    def __init__(self):
        self.x = []
        self.y = []
        self.x_t = []
        self.y_t = []
        self.read_all()
        self.n = len(self.x)
        print("N: ", self.n)

    def read_all(self):
        os.chdir("../logs/features/")
        log_files = os.listdir()
        n = len(log_files)
        for i in range(n):
            log_file_name = log_files[i]
            log_file = open(log_file_name, "r")
            log = log_file.read()
            lines = log.split("\n")
            for line in lines:
                if line.find("pt") != -1:
                    continue
                if line == '':
                    continue
                datas = line.split("|")
                x = []
                for k in range(2, len(datas) - 2):
                    data = datas[k].split(" ")
                    for j in range(len(data)):
                        # if i % 2 == 0:
                        #     x.append(float("%.4f" % float(data[i])))
                        # else:
                        if data[j] == '':
                            continue
                        x.append(float(data[j]))
                data = datas[-2].split(" ")
                # y = [float(data[0]), float(data[1])]
                y = onekey(int(data[0]) - 1, 11)
                self.x.append(np.asarray(x))
                self.y.append(np.asarray(y))
        n = len(self.x)
        nn = int(n / 10 * 8)
        self.x_t = np.asarray(self.x[nn:])
        self.y_t = np.asarray(self.y[nn:])
        self.x = np.asarray(self.x[:nn])
        self.y = np.asarray(self.y[:nn])
        os.chdir("../..")


def onekey(n, l):
    lst = [0 for i in range(l)]
    lst[n] = 1
    return lst
