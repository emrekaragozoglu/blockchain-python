## **This is a Python3 implementation of a blockchain.**   

The purpose of this implementation is to discover possible adaptations of our use case (tokenizing campaigns and storing them in a secure ledger) in the context of a traditional blockchain.  

## **Before getting started**  

Create a folder on integration cluster (under /opt/apps) OR on your local machine by naming it as **blockchain**  

To install all the necessary libraries make sure that you have following files in your **blockchain** folder:  
* begin.sh
* /files/requirements.txt

### **With using virtualenv:**  

To install them just run the command below, which: 
* will create your virtualenv with a name **blockchain-py3** 
* will install all the necessary libraries in your virtualenv

```shell
sh begin.sh
```

To activate your virtualenv:
```shell
source blockchain-py3/bin/activate
```

To deactivate your virtualenv:
```shell
deactivate
```

## **How to initialize a blockchain node**

You can initialize and run your blockchain nodes either on localhost or on cluster:  

### **Version 4 (p2p):**  

![Alt-Text](/files/node_v0_5.png)  

Activate your virtualenv:
```shell
source blockchain-py3/bin/activate
```

Initialize the first node on integration cluster on master <master_ip>
```shell
python node.py
```  

And, initialize other nodes on other machines in the cluster by following the same procedure described above. 

### **Version 5 (p2p and multi-layered networks):** 

#### **Single-Master configuration:**  

![Alt-Text](/files/node_v0_5_singlemaster.png)  

**Activate your virtualenv:**
```shell
source blockchain-py3/bin/activate
```

**Initialize the master node on integration cluster on master <master_ip> with 2 different ports (2 separate networks)**
```shell
python node_multilayer_singlemaster.py master <port_no_1> <port_no_2>
```  

Example:
```shell
python node_multilayer_singlemaster.py master 20000 30000
```

**And, initialize other nodes on other machines in the cluster (choose the network by choosing the port among the ports available on master)**
```shell
python node_multilayer_singlemaster.py slave <port_no_1 OR port_no_2>
```

Example:
```shell
python node_multilayer_singlemaster.py slave 20000
```

#### **Multiple-Master configuration:** 
  
![Alt-Text](/files/node_v0_5_multimaster.png)  

**Activate your virtualenv:**
```shell
source blockchain-py3/bin/activate
```

**Initialize the first and second master nodes on integration cluster on different machines with 2 different ports for 2 diff. networks**
```shell
python node_multilayer_multimaster.py master <port_no_1> <port_no_2>
```  

Example:
```shell
python node_multilayer_multimaster.py master 20000 30000
```

**And, initialize other nodes on other machines in the cluster (choose the network by choosing the port among the ports available on master)**
```shell
python node_multilayer_multimaster.py slave <master_ip_2> <master_ip_2> <port_no_1 OR port_no_2>
```

Example:
```shell
python node_multilayer_multimaster.py slave 10.230.141.61 <master_ip> 20000
```

## **How to interact with a blockchain node**

### **Version 4 & 5**  

After launching the script among **node.py** OR **node_multilayer_singlemaster.py** OR **node_multilayer_multimaster.py**;

You will be able to access to corresponsing node's chain by passing the command:
```shell
get chain
``` 

to send a hey to peers (connection test):
```shell
hey
``` 

to get the active peers list:
```shell
get peers
``` 

to get the network that the node belongs to:
```shell
get network
``` 

to get the unvalidated transactions list:
```shell
get txs
``` 

to mine:
```shell
mine
``` 

to reach a consensus:
```shell
consensus
``` 

to shut down the node properly:
```shell
q
``` 