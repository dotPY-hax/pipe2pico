# pipe2pico
**Pipe to a remote micropython repl via serial**

This is a small python script to pipe python into a connected Raspberry Pi pico (or any other board which runs the micropython repl I guess).


```
$ echo "print('hello world')" | ./PycharmProjects/pipe2pico/repl
hello world
```
to run a script on micropython by piping it into repl


```
$ cat /tmp/test_file.py | ./PycharmProjects/pipe2pico/repl
(name='micropython', version=(1, 19, 1), _machine='Raspberry Pi Pico W with RP2040', _mpy=4358)
```
to do the same with a file

----


You can also pipe "directly" into the picos '/main.py' file by using

```
$ cat /tmp/test_file.py | ./PycharmProjects/pipe2pico/main
```
----
**Requirements**

pyserial

```
pip install pyserial
```
or via the requirements.txt
