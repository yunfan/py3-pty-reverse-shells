# Usage

just add a dependance library

please ensure you had installed it via

```
python3 -m pip install -r ./requirements.txt
```

also this only works on \*nix platforms

first

`python3 listener.py 127.0.0.1 12345` listen on a tcp port,

then

`python3 executor.py 127.0.0.1 12345`

now you got the shell control of executor side on the listener side

of course you could try it in your LAN or even Internet(please ensure 

that listener is accesable from executor)
