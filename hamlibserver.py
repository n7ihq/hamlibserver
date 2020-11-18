# Adapted from hamlibserver.py by James C. Ahlstrom
# This software is Copyright (C) 2012 by James C. Ahlstrom, and is
# licensed for use under the GNU General Public License (GPL).
# See http://www.opensource.org.
# Note that there is NO WARRANTY AT ALL.  USE AT YOUR OWN RISK!!

import sys
import time
import socket
import string
import si5351

PORT = 4575

# This module creates a Hamlib TCP server that implements the rigctl protocol.  To start the server,
# run "python hamlibserver.py" from a command line.  To exit the server, type control-C.  Connect a
# client to the server using localhost and port 4575.  The TCP server will imitate a software defined
# radio, and you can get and set the frequency, etc.

# Only the commands dump_state, freq, mode, ptt and vfo are implemented.
# This is not a real hardware server.  It is meant as sample code to show how to implement the protocol
# in SDR control software.  You can test it with "rigctl -m 2 -r localhost:4575".

# SoftRock "dump_state"
dump = """ 0
2
2
800000.000000 53700000.000000 0x4 -1 -1 0x1 0x0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0x4 1
0 0
0 0
0
0
0
0


0x0
0x0
0x0
0x0
0x0
0x0
"""

class HamlibHandler:
    """This class is created for each connection to the server.  It services requests from each client"""
    SingleLetters = {		# convert single-letter commands to long commands
        'f': 'freq',
        'm': 'mode',
        't': 'ptt',
        'v': 'vfo',
    }

    def __init__(self, app, sock, address):
        self.app = app		# Reference back to the "hardware"
        self.sock = sock
        sock.settimeout(0.0)
        self.address = address
        self.received = ''
        h = self.Handlers = {}
        h[''] = self.ErrProtocol
        h['dump_state'] = self.DumpState
        h['get_freq'] = self.GetFreq
        h['set_freq'] = self.SetFreq
        h['get_mode'] = self.GetMode
        h['set_mode'] = self.SetMode
        h['get_vfo'] = self.GetVfo
        h['get_ptt'] = self.GetPtt
        h['set_ptt'] = self.SetPtt

    def Send(self, text):
        """Send text back to the client. Convert string to bytes"""
        try:
            self.sock.sendall(text.encode())
        except socket.error:
            self.sock.close()
            self.sock = None

    def Reply(self, *args):  # args is name, value, name, value, ..., int
        """Create a string reply of name, value pairs, and an ending integer code."""
        if len(args) > 1:		# Use simple format
            t = ''
            for i in range(1, len(args) - 1, 2):
                t = "%s%s\n" % (t, args[i])
        else:		# No names; just the required integer code
            t = "RPRT %d\n" % args[0]
        print('Reply', t)
        self.Send(t)

    def ErrParam(self):		# Invalid parameter
        self.Reply(-1)

    def UnImplemented(self):  # Command not implemented
        self.Reply(-4)

    def ErrProtocol(self):  # Protocol error
        self.Reply(-8)

    def Process(self):
        """This is the main processing loop, and is called frequently.  It reads and satisfies requests."""
        if not self.sock:
            return 0
        try:  # Read any data from the socket, convert bytes to string
            text = self.sock.recv(1024).decode()
        except socket.timeout:  # This does not work
            pass
        except socket.error:  # Nothing to read
            pass
        else:					# We got some characters
            self.received += text
        if '\n' in self.received:  # A complete command ending with newline is available
            # Split off the command, save any further characters
            cmd, self.received = self.received.split('\n', 1)
        else:
            return 1
        cmd = cmd.strip()		# Here is our command
        print('Get', cmd)
        if not cmd:			# ??? Indicates a closed connection?
            print('empty command')
            self.sock.close()
            self.sock = None
            return 0
        if cmd[0:1] == '\\':		# long form command starting with backslash
            args = cmd[1:].split()
            self.cmd = args[0]
            self.params = args[1:]
            self.Handlers.get(self.cmd, self.UnImplemented)()
        else:						# single-letter command
            self.params = cmd[1:].strip()
            cmd = cmd[0:1]
            if cmd in 'Qq':	# Quit command
                return 0
            try:
                t = self.SingleLetters[cmd.lower()]
            except KeyError:
                self.UnImplemented()
            else:
                if cmd in string.ascii_uppercase:
                    self.cmd = 'set_' + t
                else:
                    self.cmd = 'get_' + t
                self.Handlers.get(self.cmd, self.UnImplemented)()
        return 1

    # These are the handlers for each request

    def DumpState(self):
        self.Send(dump)

    def GetFreq(self):
        self.Reply('Frequency', self.app.freq, 0)

    def SetFreq(self):
        try:
            x = float(self.params)
            self.Reply(0)
        except:
            self.ErrParam()
        else:
            x = int(x + 0.5)
            self.app.freq = x
            si5351.setFrequency(4 * self.app.freq)

    def GetMode(self):
        self.Reply('Mode', self.app.mode, 'Passband', self.app.bandwidth, 0)

    def SetMode(self):
        try:
            mode, bw = self.params.split()
            bw = int(float(bw) + 0.5)
            self.Reply(0)
        except:
            self.ErrParam()
        else:
            self.app.mode = mode
            self.app.bandwidth = bw

    def GetVfo(self):
        self.Reply('VFO', self.app.vfo, 0)

    def GetPtt(self):
        self.Reply('PTT', self.app.ptt, 0)

    def SetPtt(self):
        try:
            x = int(self.params)
            self.Reply(0)
        except:
            self.ErrParam()
        else:
            if x:
                self.app.ptt = 1
            else:
                self.app.ptt = 0

class App:
    """This is the main application class.  It listens for connectons from clients and creates a server for each one."""

    def __init__(self):
        self.hamlib_clients = []
        self.hamlib_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.hamlib_socket.bind(('localhost', PORT))
        self.hamlib_socket.settimeout(0.0)
        self.hamlib_socket.listen(0)
        # This is the state of the "hardware"
        self.freq = 7074000
        self.mode = 'CW'
        self.bandwidth = 2400
        self.vfo = "VFO"
        self.ptt = 0
        # Initialize Si5351 frequency
        si5351.setFrequency(4 * self.freq)

    def Run(self):
        while True:
            time.sleep(0.1)
            try:
                conn, address = self.hamlib_socket.accept()
            except socket.error:
                pass
            else:
                print('Connection from', address)
                self.hamlib_clients.append(HamlibHandler(self, conn, address))
            for client in self.hamlib_clients:
                ret = client.Process()
                if not ret:		# False return indicates a closed connection; remove the server
                    self.hamlib_clients.remove(client)
                    print('Remove', client.address)
                    break


if __name__ == "__main__":
    try:
        App().Run()
    except KeyboardInterrupt:
        sys.exit(0)
