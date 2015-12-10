#!/usr/bin/python

import socket
import time
import pigpio

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('192.168.0.221', 5000))
serversocket.listen(5) # maximum 5 connections
connection, address = serversocket.accept()

signals = {
        'forward':40,
        'reverse':10,
        'left':64,
        'right':58,
        'forwardright':52,
        'forwardleft':46,
        'reverseright':28,
        'reverseleft':34,
        'idle':0,
        'quit':666
        }

def fill_wave(pulses_buffer, direction):
    for i in range(0, 4):
        pulses_buffer.append(pigpio.pulse(1<<GPIO, 0, 1500))
        pulses_buffer.append(pigpio.pulse(0, 1<<GPIO, 500))
    for i in range(0, signals[direction]):
        pulses_buffer.append(pigpio.pulse(1<<GPIO, 0, 500))
        pulses_buffer.append(pigpio.pulse(0, 1<<GPIO, 500))

def cleanup():
    pi.wave_tx_stop()

def quit():
    cleanup()
    pi.stop()
    exit()

GPIO = 4
forward = []
reverse = []
left = []
right = []
forright = []
forleft = []
revright = []
revleft = []
wids = [0]*8
fill_wave(forward, 'forward')
fill_wave(reverse, 'reverse')
fill_wave(left, 'left')
fill_wave(right, 'right')
fill_wave(forright, 'forwardright')
fill_wave(forleft, 'forwardleft')
fill_wave(revright, 'reverseright')
fill_wave(revleft, 'reverseleft')

waves = {
        0:forward,
        1:reverse,
        2:left,
        3:right,
        4:forright,
        5:forleft,
        6:revright,
        7:revleft
        }

pi = pigpio.pi()
for i in range(0, 8):
    pi.wave_add_generic(waves[i])
    wids[i] = pi.wave_create()

while True:
    buf = connection.recv(64)
    if len(buf) > 0:
        buf = buf.strip()
        pi.set_mode(GPIO, pigpio.OUTPUT)
        print buf
        if buf == 'forward':
            pi.wave_send_repeat(wids[0])
        elif buf == 'reverse':
            pi.wave_send_repeat(wids[1])
        elif buf == 'left':
            pi.wave_send_repeat(wids[2])
        elif buf == 'right':
            pi.wave_send_repeat(wids[3])
        elif buf == 'forwardright':
            pi.wave_send_repeat(wids[4])
        elif buf == 'forwardleft':
            pi.wave_send_repeat(wids[5])
        elif buf == 'reverseright':
            pi.wave_send_repeat(wids[6])
        elif buf == 'reverseleft':
            pi.wave_send_repeat(wids[7])
        elif buf == 'idle':
            cleanup()
        elif buf == 'quit':
            quit()
