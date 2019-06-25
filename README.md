# key-exchange module
This is a key exchange method that is not venerable to middle man attacks.  

__Disclaimer__: use at your own discretion. This module is at its testing
process
and may have vulnerabilities. 

## Server
#### client authentication
```python
from key_exchange.src.base import KeyExchange
ke = KeyExchange()
```
generate a one-time private key. Do not reuse this key if the connection
failed.
```python
ke.generate_private_key()
```
send `ke.public_key` to the client.
Use the first packet that is received from the client (`client_packet`) in the
function below.
```python
ke.authenticate_client(username, client_packet, loc='data/')
```
If the function returns `True`, the client is authenticated and has the servers
public key.  

If the client is not authenticated stop here. Otherwise, start the process of
establishing server authentication for the client.




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
To establish trust to the server.
