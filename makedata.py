import os

class Data:
    def __init__(self,batch_size):
        self.x = []
        self.y = []
        self.x_t = []
        self.y_t = []
        self.i_t = 0
        self.i = 0
        self.batch_size = batch_size
        self.read_all()
        self.n = len(self.x)
        print("N: ", self.n)
    def read_all(self):
        os.chdir("logs/features/")
        log_files = os.listdir()
        n = len(log_files)
        for i in range(int(n/10*9)):
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
                for i in range(2,len(datas)-2):
                    data = datas[i].split(" ")
                    for d in data:
                        x.append(float(d))
                data = datas[-2].split(" ")
                y = [float(data[0]), float(data[1])]

                self.x.append(x)
                self.y.append(y)
        for i in range(int(n*9/10), n):
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
                for i in range(2, len(datas) - 2):
                    data = datas[i].split(" ")
                    for d in data:
                        x.append(float(d))
                data = datas[-2].split(" ")
                y = [float(data[0]), float(data[1])]

                self.x_t.append(x)
                self.y_t.append(y)
    def get_batch(self):
        i = self.i
        self.i += self.batch_size
        return self.x[i:i+self.batch_size], self.y[i:i+self.batch_size]
    def get_batch_t(self):
        i = self.i_t
        self.i_t += self.batch_size
        return self.x_t[i:i+self.batch_size], self.y_t[i:i+self.batch_size]

    def restart(self):
        self.i = 0
        self.i_t = 0
