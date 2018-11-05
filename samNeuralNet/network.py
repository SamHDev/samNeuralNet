from . import error
import datetime
import json
import base64

def createNetwork(*rowss,weight=0,bias=0):
    rows = list(rowss)
    #print(rows)
    if (len(rows) < 2):
        raise(error.netCreateOptionError("Please Specify In/Out Neurons"))
        return None
    inCount = rows[0]
    outCount = rows[len(rows)-1]
    rows.pop(len(rows)-1)
    rows.pop(0)
    rowsCount = rows
    #print(inCount,str(rowsCount).replace("[","").replace("]","").replace(" ","").replace(","," "),outCount)

    data = {}
    data["network"] ={}
    data["network"]["name"] = "Network"
    data["network"]["nettype_version"] = 0.1
    data["network"]["datetime_created"] = datetime.datetime.utcnow().timestamp()
    data["network"]["datetime_updated"] = datetime.datetime.utcnow().timestamp()
    data["network"]["update_version"] = 0
    data["network"]["load_count"] = 1
    data["network"]["rowinfo"] = {"in":inCount,"out":outCount,"mid":rows,"all":list(rowss)}
    data["rows"] = []
    rvs = list(rowss)
    #print(rvs)
    netId = 0
    for r in rvs:
        row = {}
        row["rowCount"] = r
        row["rowType"] = None
        row["nets"] = []
        for rv in range(0,r):
            netId = netId + 1
            row["nets"].append({"id":netId,"bias":0,"cons":[]})
        #print(r)
        data["rows"].append(row)

    #print(json.dumps(data, indent=4))

    for ri in range(0,len(rvs)-1):
        if (ri != (len(rvs)-1)):
            #print("|{}".format(ri))
            for rv in range(0, rvs[ri]):
                #print("   |{}".format(rv))
                for rns in range(0, rvs[ri+1]):
                    con = {}
                    con["loc"] = [ri,rv,rns]
                    vid = data["rows"][ri+1]["nets"][rns]["id"]
                    con["id"] = vid
                    con["w"] = weight
                    #print("      |{} - {} - {}".format(rns,rvs[ri+1],vid))
                    data["rows"][ri]["nets"][rv]["cons"].append(con)

    net = NeuralNetwork(data)
    return net

def loadNetwork(file):
    import os
    cwd = os.getcwd()
    path = os.path.join(cwd,os.path.join(cwd,file))
    f = open(path,"rb")
    read = base64.b64decode(f.read().decode("UTF-8").split(":", 1)[1].encode("UTF-8")).decode("UTF-8")
    f.close()
    data = json.loads(read)
    net = NeuralNetwork(data)
    return net
def saveNetwork(net,file):
    import os
    cwd = os.getcwd()
    path = os.path.join(cwd,os.path.join(cwd,file))
    f = open(path,"wb")
    f.write(b'SamNeuralNetFile:'+base64.b64encode(json.dumps(net.dump()).encode("UTF-8")))
    f.close()
def isNetwork(file):
    try:
        import os
        cwd = os.getcwd()
        path = os.path.join(cwd, os.path.join(cwd, file))
        f = open(path, "rb")
        read = base64.b64decode(f.read().decode("UTF-8").split(":",1)[1].encode("UTF-8")).decode("UTF-8")
        f.close()
        json.loads(read)
        return True
    except:
        return False


class NeuralNetwork():
    def __init__(self,data):
        self.raw = data
        self.load()

    def load(self):
        self.name = self.raw["network"]["name"]
        self.net_version = self.raw["network"]["nettype_version"]

        self.created_time = datetime.datetime.utcfromtimestamp(self.raw["network"]["datetime_created"])
        self.update_time = datetime.datetime.utcfromtimestamp(self.raw["network"]["datetime_updated"])
        self.updated_version = self.raw["network"]["update_version"]
        self.load_count = self.raw["network"]["load_count"] + 1

        self.neurons = []

        for rv in self.raw["rows"]:
            row = []
            for nt in rv["nets"]:
                row.append(Neuron(self,[self.raw["rows"].index(rv),rv["nets"].index(nt)],nt))
            self.neurons.append(row)

        self.conns = []

        for rv in self.raw["rows"]:
            row = []
            for nt in rv["nets"]:
                neu = []
                for nu in nt["cons"]:
                    neu.append(Connection(self,[self.raw["rows"].index(rv),rv["nets"].index(nt),nt["cons"].index(nu)],nu))
                row.append(neu)
            self.conns.append(row)

    def setBias(self,row,nu,set):
        self.raw["rows"][row]["nets"][nu]["bias"] = set
        self.neurons[row][nu].bias = set
    def getNeuron(self,row,nu):
        return self.neurons[row][nu]

    def getConn(self,row,nu,con):
        return self.conns[row][nu][con]

    def dump(self):
        return self.raw

    def save(self,file):
        saveNetwork(self,file)



class Neuron():
    def __init__(self,net,loc,data):
        self.net = net
        self.loc = loc
        self.data = data

        self.id = self.data["id"]
        self.bias = self.data["bias"]
    def setBias(self,set):
        self.net.raw["rows"][self.loc[0]]["nets"][self.loc[1]]["bias"] = set

class Connection():
    def __init__(self, net, loc, data):
        self.net = net
        self.loc = loc
        self.data = data

        self.weight = self.data["w"]

