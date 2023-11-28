#!/usr/bin/env python

from mininet.cli import CLI

from mininet.net import Mininet

from mininet.link import Link,TCLink,Intf

from mininet.node import Controller

 

if '__main__' == __name__:

  net = Mininet(link=TCLink)

  h1 = net.addHost('h1')

  h2 = net.addHost('h2')

  h3 = net.addHost('h3')

  s1 = net.addSwitch('s1')

  c0 = net.addController('c0', controller=Controller)

  net.addLink(h1, s1)

  net.addLink(h2, s1)

  net.addLink(h3, s1)

  net.build()

  c0.start()

  #open a terminal for s1 and type the following commands

  #ovs-vsctl del-port s1-eth3

  #ovs-vsctl add-port s1 s1-eth3 -- --id=@p get port s1-eth3 -- --id=@m create mirror name=m0 select-all=true output-port=@p -- set bridge s1 mirrors=@m

  s1.start([c0])

  CLI(net)

  net.stop()