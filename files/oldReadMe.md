## **This is a Python3 implementation of a blockchain.**   

The purpose of this implementation is to discover possible adaptations of our usecase (tokenizing campaigns and storing them in a secure ledger) in the context of a traditionnal blockchain.  

## **Before getting started**  

Create a folder on integration cluster (under /opt/apps) OR on your local machine by naming it as **pop-blockchain**  

To install all the necessary libraries make sure that you have following files in your **pop-blockchain** folder:  
* begin.sh
* requirements.txt

### **With using virtualenv:**  

To install them just run the command below, which: 
* will create your virtualenv with a name **pop-blockchain-py3** 
* will install all the necessary libraries in your virtualenv

```shell
sh begin.sh
```

To activate your virtualenv:
```shell
source pop-blockchain-py3/bin/activate
```

To deactivate your virtualenv:
```shell
deactivate
```

**And please add the JSONView extension to better display the json responses in Chrome**
```shell
https://chrome.google.com/webstore/detail/jsonview/chklaanhfefbnpoihckbnefhakgolnmc?hl=en
```

## **How to initialize a blockchain node**

You can initialize and run your blockchain nodes either on localhost or on cluster:  

### **Cluster Mode:**  

**Version 3:**  

Before launching the flask servers you will need to disable the proxy:
```shell
unset http_proxy
unset https_proxy
``` 

Activate your virtualenv:
```shell
source pop-blockchain/bin/activate
```

Initialize the first node on integration cluster on master 10.230.140.7:20000
```shell
export FLASK_APP=node_v0_3_1.py
flask run --host=0.0.0.0 --port 20000
```  

And, initialize other nodes on other machines in the cluster by following the same procedure described above.  

**Version 4 (p2p):**  

Activate your virtualenv:
```shell
source pop-blockchain-py3/bin/activate
```

Initialize the first node on integration cluster on master 10.230.140.7:20000
```shell
python node.py
```  

And, initialize other nodes on other machines in the cluster by following the same procedure described above. 

**Version 5 (p2p and multi-layered networks):** 

![Alt-Text](/files/node_v0_5.png)

Activate your virtualenv:
```shell
source pop-blockchain-py3/bin/activate
```

Initialize the first node on integration cluster on master **10.230.140.7** with 2 different ports (2 separate networks)
```shell
python node_multi_layer.py master <port_no_1> <port_no_2>
```  

And, initialize other nodes on other machines in the cluster (choose the network by choosing the port among the ports available on master)
```shell
python node_multi_layer.py slave <port_no_1 OR port_no_2>
```

### **Local Mode:**  

Activate your virtualenv:
```shell
source pop-blockchain/bin/activate
```

Initialize the first node on localhost:5000  
```shell
export FLASK_APP=blockchain_node_v0_2.py
flask run --port 5000
```  

And, initialize other nodes on localhost using different ports  
```shell
export FLASK_APP=blockchain_node_v0_2.py
flask run --port <port_number>
``` 


## **How to interact with a blockchain node**

### **version 3**  

**Launch the script requestor.py by uncommenting the request that you want to perform**
```shell
python requestor.py
or
try curl
```

**To launch a node:**
```shell
http://localhost:<port_number>/
or
http://<ip_of_the_machine>:<port_number>/
``` 

**To mine a new block on a node:**
```shell
http://localhost:<port_number>/mine
or
http://<ip_of_the_machine>:<port_number>/mine
```  

Or try to send multiple requests with curl:
```shell
ab -n <number_of_requests> http://<ip_of_the_machine>:<port_number>/mine
```  

**To display the whole chain on a node:**
```shell
http://localhost:<port_number>/chain
or
http://<ip_of_the_machine>:<port_number>/chain
```

**To display the current peers of a node:**
```shell
http://localhost:<port_number>/nodes
or
http://<ip_of_the_machine>:<port_number>/nodes
```

**To display the unvalidated transactions on a node:**
```shell
http://localhost:<port_number>/transaction/get
or
http://<ip_of_the_machine>:<port_number>/transaction/get
```

Advertising: As soon as a node has been crated, it advertises and register itself to other peering nodes:
```shell
Send POST request to http://localhost:<port_number>/nodes/register
or
Send POST request to http://<ip_of_the_machine>:<port_number>/nodes/register
```

Consensus: This request is automatically sent to all peers by the Node which has just mined a new block
```shell
Send GET request to http://localhost:<port_number>/nodes/resolve
or
Send GET request to http://<ip_of_the_machine>:<port_number>/nodes/resolve
```

### **version 4 & 5**  

After launching the node.py script;

You will be able to access to corresponsing node's chain by passing the command:
```shell
'get chain'
``` 

to get the active peers list:
```shell
'get peers'
``` 

to get the network that the node belongs to:
```shell
'get network'
``` 

to get the unvalidated transactions list:
```shell
'get txs'
``` 

to mine:
```shell
'mine'
``` 

to reach a consensus:
```shell
'consensus'
``` 

to shut down the node properly:
```shell
'q'
``` 