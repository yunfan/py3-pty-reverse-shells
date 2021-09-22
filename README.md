This is a playground repo for my study on reverse pty shells

i had study the concept from <https://github.com/infodox/python-pty-shells>

but there's three problems

- the code cant work because of the pty file is not a seekable any more
- i want to build a 3-role model
- i want to use high level protocol as the tunnel, which cant be used easily as ordinary socket like tcp/udp

