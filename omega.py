"""This script reads the pid in judas.txt and sends the SIGKILL signal
to that process, killing Floria when she's in background/ethereal mode.
"""
import os

with open("judas.txt", "r") as failsafe:
    floria_pid = failsafe.readline()

os.kill(floria_pid, signal.SIGKILL)