## **This is a Python3 implementation of a private Blockchain.**   

The purpose of this implementation is to discover possible applications of our use case (tokenizing campaigns and storing them in a secure ledger) in the context of a traditional Blockchain.  

## **How to initialize Fractal Networks**

You can initialize and launch your Blockchain nodes on the cluster of Virtual Machines.  

Example configurations with JSON config. files (nodesConfiguration.json):

### **Example 1**

![Alt-Text](/files/exampleFractalConfig.png)  

Example JSON Config File:

```shell
[
    {
      "network" : 20000,
      "masters" :  ["ip_address1", "ip_address2", "ip_address3"],
      "slaves" : ["ip_address4", "ip_address5"]
    },
    {
      "network" : 21000,
      "masters" :  ["ip_address1", "ip_address2"],
      "slaves" : ["ip_address3", "ip_address4", "ip_address5"]
    },
    {
      "network" : 22000,
      "masters" :  ["ip_address1", "ip_address3"],
      "slaves" : ["ip_address2", "ip_address4", "ip_address5"]
    }
]
```

### **Example 2**

![Alt-Text](/files/exampleFractalConfig2.png) 

Example JSON Config File:

```shell
[
    {
      "network" : 20000,
      "masters" :  ["ip_address1", "ip_address2", "ip_address3", "ip_address4", "ip_address5"],
      "slaves" : []
    },
    {
      "network" : 21000,
      "masters" :  ["ip_address5"],
      "slaves" : ["ip_address2", "ip_address3", "ip_address4"]
    },
    {
      "network" : 22000,
      "masters" :  ["ip_address2"],
      "slaves" : ["ip_address1", "ip_address3", "ip_address4"]
    },
    {
      "network" : 23000,
      "masters" :  ["ip_address3"],
      "slaves" : ["ip_address1", "ip_address2", "ip_address3"]
    },
    {
      "network" : 24000,
      "masters" :  ["ip_address4", "ip_address5"],
      "slaves" : ["ip_address1", "ip_address2"]
    },
    {
      "network" : 25000,
      "masters" :  ["ip_address4", "ip_address5"],
      "slaves" : ["ip_address1", "ip_address2"]
    }, 
    {
      "network" : 26000,
      "masters" :  ["ip_address2""ip_address4"],
      "slaves" : ["ip_address1", "ip_address5"]
    },
    {
      "network" : 27000,
      "masters" :  ["ip_address2", "ip_address3"],
      "slaves" : ["ip_address1", "ip_address5"]
    },
    {
      "network" : 28000,
      "masters" :  ["ip_address3"],
      "slaves" : ["ip_address2", "ip_address4", "ip_address5"]
    },    
]
```

#### **Bigger Pentagonal Fractal configuration** 
  
![Alt-Text](/files/fractal-topology.png)  
