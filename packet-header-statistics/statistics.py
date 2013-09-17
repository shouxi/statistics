#python 3.3.2

import ipaddress

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

fin = r'20080112KANS0000'

'''
format:
-----------------------------------------------------------------------------------------------
index: |   0   |    1    |    2    |    3    |    4    |    5    |    6    |   7  |     8     |
-----------------------------------------------------------------------------------------------
field: | dpkts | doctets | srcaddr | dstaddr | nexthop | srcport | dstport | prot | tcp_flags |
-----------------------------------------------------------------------------------------------
eg: 1,40,155.31.208.0,65.55.200.0,64.57.28.24,1313,443,6,16

'''
ip2int = lambda x:int(ipaddress.IPv4Address(x))

def decode(line):
    fdecoder = (int, int,
                ip2int, ip2int, ip2int,
                int, int, int, int,)
    return [fdecoder[i](d) for i, d in enumerate(line.split(","))]

with open(fin) as fi:
    line = fi.readline()

    srcip = []
    dstip = []

    srcport = []
    dstport = []

    for line in iter(fi.readline, ''):
        t = decode(line)
        
        srcip.append(t[2])
        dstip.append(t[3])

        srcport.append(t[5])
        dstport.append(t[6])        


unused = [(ip2int("0.0.0.0"), ip2int("0.255.255.255")), #/8
          (ip2int("10.0.0.0"), ip2int("10.255.255.255")), #/8
          (ip2int("127.0.0.0"), ip2int("127.255.255.255")), #/8
          (ip2int("169.254.0.0"), ip2int("169.254.255.255")), #/16
          (ip2int("172.16.0.0"), ip2int("172.31.255.255")), #/12
          (ip2int("192.0.0.0"), ip2int("192.0.0.255")), #/24
          (ip2int("192.0.2.0"), ip2int("192.0.2.255")), #/24
          (ip2int("192.88.99.0"), ip2int("192.88.99.255")), #/24
          (ip2int("192.168.0.0"), ip2int("192.168.255.255")), #/16
          (ip2int("198.18.0.0"), ip2int("198.18.127.255")), #/15
          (ip2int("198.51.100.0"), ip2int("198.51.100.255")), #/24
          (ip2int("203.0.113.0"), ip2int("203.0.113.255")), #/24
          (ip2int("224.0.0.0"), ip2int("239.255.255.255")), #/4 int(0b11101111) is 239
          (ip2int("240.0.0.0"), ip2int("255.255.255.255")), #/4 int(0b11110000) is 240
          ]

print("drawing...")

plt.figure(1)
plt.grid(True)
plt.xlabel('src ip addr')
plt.ylabel('dst ip addr')
#plt.scatter(x, y)    
plt.hist2d(srcip, dstip, range = [[0, 2**32-1], [0, 2**32-1]], bins=150, norm=LogNorm())
plt.colorbar()

for minx, maxx in unused:
    plt.axvspan(minx, maxx, facecolor='g', alpha=0.2)
    plt.axhspan(minx, maxx, facecolor='g', alpha=0.2)

plt.savefig(fin + '-ip.pdf')
plt.savefig(fin + '-ip.png', dpi = 300)

print("drawing...")

plt.figure(2)
plt.grid(True)
plt.xlabel('src port')
plt.ylabel('dst port')
#plt.scatter(srcport, dstport)    
plt.hist2d(srcport, dstport, range=[[0, 65535], [0, 65535]], bins=150, norm=LogNorm())
plt.colorbar()

plt.savefig(fin + '-port.pdf')
plt.savefig(fin + '-port.png', dpi = 300)

print("ok")
plt.show()
