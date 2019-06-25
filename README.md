# key-exchange module
This key exchange is not venerable to middle man attacks.  

Disclaimer: use at your own discretion. This module is at its testing process
and may have vulnerabilities. 

## Server
#### client authentication
```python
from key_exchange.src.base import KeyExchange
ke = KeyExchange()
```
generate one time private key. Do not reuse this key if connection failed.
```python
ke.generate_private_key()
```
send `ke.public_key` to the client.
The packet that is received from the client must me equal to:
```python
ke.returned_client_packet(username, loc='data/')
```
If so, client is authenticated and has the servers public key.


## Client
```python
from key_exchange.src.base import KeyExchange
ke = KeyExchange()
```
use the `server_public_key` that is received from the server, and send the
result of the function below to the server.
```python
ke.client_packet(password, server_public_key)
```