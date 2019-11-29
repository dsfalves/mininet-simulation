#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, TCLink
from mininet.topo import Topo

# datacenter capacity in nodes and cores per node

def new_host(net, num_hosts):
    hosts = []
    routers = []
    links = {}
    counters = {}
    for i in range(1, num_hosts+1):
        h = net.addHost('h%d' % i)
        r = net.addHost('r%d' % i)
        hosts.append(h)
        routers.append(r)
        net.addLink(h, r)
        counters[r.name] = 1
        links[r.name] = []
    for r in routers:
        for o in routers:
            if r.name < o.name:
                net.addLink(r, o)
                links[r.name].append((o.name, '%s-eth%d' % (r.name, counters[r.name])))
                links[o.name].append((r.name, '%s-eth%d' % (o.name, counters[o.name])))
                counters[r.name] += 1
                counters[o.name] += 1

    return hosts, routers, links


def config_hosts(hosts):
    for i, host in enumerate(hosts):
        num = i + 1
        dev = '%s-eth0' % host.name
        ifconfig = 'ifconfig %s 0' % dev
        add = 'ip addr add 192.168.%d.1/24 brd + dev %s' % (num, dev)
        route = 'ip route add default via 192.168.%d.2' % num
        info('*** running\n%s\n%s\n%s\n' % (ifconfig, add, route))
        host.cmd(ifconfig)
        host.cmd(add)
        host.cmd(route)


def config_routers(routers, links):
    for i, r1 in enumerate(routers):
        name = r1.name
        num = int(name[1:])
        for k in range(len(links)+1):
            clean = 'ifconfig %s-eth%d 0' % (name, k)
            r1.cmd(clean)
        r1.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
        r1.cmd('ifconfig %s-eth0 192.168.%d.2 netmask 255.255.255.0' % (name, num))
        for name2, dev in links[name]:
            num_other = int(name2[1:])
            num2 = num_other
            me = 1
            other = 2
            num1 = num
            if num2 > num1:
                smaller = 2
                num1, num2 = num2, num1
                other, me = me, other
            config = 'ifconfig %s 192.168.%d%d.%d netmask 255.255.255.0' % (dev, num1, num2, me)
            route = 'ip route add 192.168.%d.0/24 via 192.168.%d%d.%d' % (num_other, num1, num2, other)
            r1.cmd(config)
            r1.cmd(route)
    

def create_topology():
    net = Mininet(link=TCLink)
    hosts, routers, links = new_host(net, 3)
    h1, h2, h3 = hosts
    r1, r2, r3 = routers
    net.build()

    config_routers(routers, links)
    config_hosts(hosts)

    CLI(net)

    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_topology()
