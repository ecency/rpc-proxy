# RPC-PROXY

Generalized, easy to use RPC Proxy written in Python with support to `websocket` and `http` connections. Includes config example for [Hive blockchain](https://hive.io). It is written with simple and clean code that can be used by any blockchain or software with JSON-RPC protocols. We have tried number of RPC proxy scripts some of them are over-engineered and some lack extensibility or complicated to get started. So we wrote rpc-proxy in hopes to help others as well as ourselves. 

Our RPC, full node on Hive uses this: https://rpc.ecency.com

## Installation

```
$ git clone https://github.com/ecency/rpc-proxy && cd rpc-proxy && pip3 install -e .
```

## Usage

`$ rpc_proxy --config ./path/to/config.json`


### Environment Variables

|	               	|	Default	        |
|	------------	|	------------    |
|	     HOST     	|	  127.0.0.1     |
|	     PORT     	|	  5002          |
|	     WORKERS    |	  4             |
|	     DEBUG     	|	  False         |


**Redis server must be working at 127.0.0.1:6379**
