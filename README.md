# videonion

## Installation

```
virtualenv env
. env/bin/activate
pip install -e .
```

## Usage

On the server:

- Set up a .onion service, directing ports XXXX and YYYY to 127.0.0.1
- `videonion start --send_port=XXXX --recv_port=YYYY ADDRESS.onion`
- Give the displayed code to the client

On the client:

- `videonion join`
- Enter the code from the server.
