from samNeuralNet import samNeuralNet as snn

if (snn.isNetwork("network.snn")):
    net = snn.loadNetwork("network.snn")
    print("Loaded")
else:
    net = snn.createNetwork(3,4,4,2)
    snn.saveNetwork(net,"network.snn")
    print("Created")

print(net.name)
