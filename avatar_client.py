"""
avatar_client.py

Small client to start the avatar_3d process and send simple commands over TCP.

Usage:
  from avatar_client import Avatar3D
  a = Avatar3D.start()
  a.set_lipsync(0.8)
  a.blink()
  a.stop()
"""
import subprocess
import sys
import socket
import time
import json
import threading
import os

DEFAULT_PORT = 52000


class Avatar3D:
    def __init__(self, script_path=None, port=DEFAULT_PORT):
        self.port = port
        self.proc = None
        self.script_path = script_path or os.path.join(os.path.dirname(__file__), 'avatar_3d.py')
        self._sock = None
        self._connected = False

    def start(self, wait=2.0):
        if self.proc:
            return self
        cmd = [sys.executable, self.script_path]
        self.proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # wait for server to come up
        start = time.time()
        while time.time() - start < wait:
            try:
                s = socket.create_connection(('127.0.0.1', self.port), timeout=0.7)
                self._sock = s
                self._connected = True
                return self
            except Exception:
                time.sleep(0.2)
        self.stop()
        raise RuntimeError("3D avatar failed to start or connect")

    def _send(self, obj):
        try:
            if not self._sock:
                self._sock = socket.create_connection(('127.0.0.1', self.port), timeout=1.0)
            self._sock.sendall((json.dumps(obj) + '\n').encode('utf-8'))
        except Exception:
            pass

    def set_lipsync(self, level: float):
        self._send({'cmd': 'lipsync', 'level': float(level)})

    def blink(self):
        self._send({'cmd': 'blink'})

    def stop(self):
        self._send({'cmd': 'stop'})
        try:
            if self._sock:
                self._sock.close()
        except Exception:
            pass
        self._connected = False
        try:
            if self.proc:
                self.proc.terminate()
        except Exception:
            pass

    @property
    def connected(self):
        return self._connected


def start_demo():
    a = Avatar3D()
    a.start()
    for i in range(20):
        a.set_lipsync(abs((i % 6) - 3) / 3.0)
        time.sleep(0.22)
    a.blink()
    time.sleep(1.0)
    a.stop()


if __name__ == '__main__':
    start_demo()
