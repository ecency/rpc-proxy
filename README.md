# RPC-PROXY

Installation instructions for Linux(Ubuntu).

### Clone
`$ git clone https://github.com/ecency/rpc-proxy`

`$ cd rpc-proxy`

### Install dependencies
`$ virtualenv venv -p python3`

`$ source venv/bin/activate`

`$ pip install -r requirements.txt`

### Make your config file
`$ cp config.example.json config.json`

### Make your env.sh file

Tip for WSGI_WORKERS: **(cpu core count * 2) + 1**

`$ cp env.sh.example env.sh`

`$ source env.sh`

### Run in development mode
`$ source venv/bin/activate`

`$ python run.py`

### Run in production mode
`script/wsgi` file starts app in gunicorn wsgi container.

`$ script/wsgi`

### Running wsgi app with Supervisor

`$ apt-get install supervisor`

`$ systemctl enable supervisor`

`$ nano /etc/supervisor/conf.d/rpc-proxy.conf`

```
[program:proxy]
command=/path/to/script/wsgi
directory=/root
autostart=true
autorestart=true
```

`$ service supervisor restart`