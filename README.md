# RPC-PROXY

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