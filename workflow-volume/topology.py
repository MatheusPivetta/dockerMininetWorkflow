from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import OVSController
import multiprocessing
import time

def run_tcpdump(h3_cmd):
    h3.cmd(h3_cmd)

def run_ping(h1_cmd):
    h1.cmd(h1_cmd)

if __name__ == '__main__':
    net = Mininet(link=TCLink)
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')
    s1 = net.addSwitch('s1')
    c0 = net.addController('c0', controller=OVSController)
    
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)
    
    net.build()
    c0.start()
    s1.start([c0])
    
    # Remove the third port from the switch
    s1.cmd('ovs-vsctl del-port s1-eth3')
    # Add mirroring configuration to the switch
    s1.cmd('ovs-vsctl add-port s1 s1-eth3 -- --id=@p get port s1-eth3 -- --id=@m create mirror name=m0 select-all=true output-port=@p -- set bridge s1 mirrors=@m')
    
    # Start tcpdump and ping concurrently
    h3_cmd = "tcpdump -i h3-eth0 -G 30 -W 1 -w input/mycap.pcap"
    h1_cmd = "timeout 20s hping3 -S -V -d 120 -w 64 -p 80 --rand-source --flood 10.0.0.2"
    
    # Create processes for tcpdump and ping
    tcpdump_process = multiprocessing.Process(target=run_tcpdump, args=(h3_cmd,))
    ping_process = multiprocessing.Process(target=run_ping, args=(h1_cmd,))
    
    # Start the processes
    tcpdump_process.start()
    ping_process.start()
    
    # Wait for both processes to finish
    tcpdump_process.join()
    ping_process.join()
    
    net.stop()
