#!/usr/bin/env python

import binascii
import random
import string
import sys
import time

import serial
from serial.tools.list_ports import comports


class Connection:
    def __init__(self):
        self.serial_connection = None


    def get_device(self):
        ports = comports()
        for port in ports:
            try:
                if "python" in port.manufacturer.lower():
                    return port.device
            except AttributeError:
                pass

    def connect_to_device(self):
        device = self.get_device()
        try:
            self.serial_connection = serial.Serial(device)
        except serial.serialutil.SerialException:
            sys.stderr.write(f"permission denied {device}\n")
            sys.exit()

        if not self.serial_connection.is_open:
            sys.stderr.write("NO DEVICE\n")
            sys.exit()

    def fire_and_forget(self, command):
        self.serial_connection.write(command)
        self.serial_connection.write(b"\r\n")

    def send_command_to_repl_and_wait(self, command):
        # use this some time
        terminator = "EOT".join(random.choices(string.ascii_letters, k=16))
        terminator_check = f"print('{terminator}')".encode()
        terminator = terminator.encode()
        command = command.replace(b"\n", b"\r\n")
        self.fire_and_forget(command)
        self.fire_and_forget(terminator_check)
        repl_output = b""
        while not self.serial_connection.in_waiting:
            time.sleep(0.1)
        while self.serial_connection.in_waiting or terminator not in repl_output:
            time.sleep(0.1)
            n_bytes = self.serial_connection.in_waiting
            repl = self.serial_connection.read(n_bytes)
            repl_output += repl
        repl_output = self.format_repl_output(repl_output)
        return repl_output

    def file_upload(self, content, remote_path):
        content = binascii.b2a_base64(content, newline=False).decode()
        repl_command = "import binascii; f = open('{}', 'w'); content = binascii.a2b_base64(b'{}'); f.write(content); f.close()".format(remote_path, content)
        self.send_command_to_repl_and_wait(repl_command.encode())
        self.reset()

    def reset(self):
        command = b"import machine; machine.reset()"
        self.fire_and_forget(command)

    def format_repl_output(self, repl_output):
        repl_output = repl_output.split(b"\r\n")
        self.serial_connection.reset_input_buffer()
        repl_output = repl_output[:-2]
        repl_output = [line for line in repl_output[1:] if not line.startswith(b">>>")]
        return repl_output


def pipe2repl():
    connection = Connection()
    connection.connect_to_device()
    input_ = sys.stdin.read().encode()
    result = connection.send_command_to_repl_and_wait(input_)
    for line in result:
        print(line.decode())


def pipe2main():
    connection = Connection()
    connection.connect_to_device()
    input_ = sys.stdin.read().encode()
    connection.file_upload(input_, "/main.py")
