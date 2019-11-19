#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info

# datacenter capacity in nodes and cores per node
dc = [
      (13, 23),
      (7, 12),
      (7, 8),
      (12, 8),
      (31, 32),
      (31, 32),
      (10, 16),
      (8, 12),
      ]

speeds = [
          [1000, 931, 376, 822, 99, 677, 389, 935],
          [931, 1000, 97, 672, 381, 82, 408, 93],
          [376, 97, 1000, 628, 95, 136, 946, 175],
          [822, 672, 628, 1000, 945, 52, 77, 50],
          [99, 381, 95, 945, 1000, 822, 685, 535],
          [677, 82, 136, 52, 822, 1000, 69, 639],
          [389, 408, 946, 77, 685, 69, 1000, 243],
          [935, 93, 175, 50, 535, 639, 243, 1000],
]

def create_topology():
    net = Mininet(controller=Controller)

    info('*** Adding controller\n')
    net.addController('c0')

    hosts = []
    info('*** Adding hosts\n')
    num_hosts = len(dc)
    for i in range(1, num_hosts+1):
        name = 'h%d' % i
        ip = '10.0.0.%d' % i
        hosts.append(net.addHost(name, ip))

    switches = []
    info('*** Adding switch\n')
    for i in range(1, num_hosts+1):
        name = 's%d' % i
        switch.append(net.addSwitch(name))

    info('*** Creating links\n')
    for h, s in zip(hosts, switches):
        net.addLink(h, s)
    for i in range(num_hosts):
        for k in range(i+1, num_hosts):
            net.addLink(s[i], s[k],
                        bw='%dm' % speeds[i][k])

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_topology()
