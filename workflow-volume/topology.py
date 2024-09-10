from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import OVSController
import multiprocessing
import time, datetime



def run_h1(h1_cmd):
    h1.cmd(h1_cmd)
def run_h2(h2_cmd):
    h2.cmd(h2_cmd)
def run_h3(h3_cmd):
    h3.cmd(h3_cmd)
    
def syn_flood_attack(target, interface, duration_in_s):
    # Start tcpdump and ping concurrently
    
    h3_cmd = "time tshark -i " + interface + "  -a duration:"+ duration_in_s +" \
                           -w cicflowmeter/attack_input/mycap.pcap"
                           
                    #    -b duration:10 \
                    #    -b files:10000 \
                    #    -b filesize:1000 \                           
    
    h1_cmd = "timeout " + duration_in_s + "s hping3 -S -V -d 120 -w 64 -p 80 --rand-source --flood " + target
    
    
    # Create processes for tcpdump and ping
    collect_process = multiprocessing.Process(target=run_h3, args=(h3_cmd,))
    traffic_process = multiprocessing.Process(target=run_h1, args=(h1_cmd,))
    
    # Start the processes
    print(datetime.datetime.now(),"Coleta iniciada")
    collect_process.start()
    print(datetime.datetime.now(),"Trafico iniciado")
    traffic_process.start()
    
    # Wait for both processes to finish
    
    traffic_process.join()
    print(datetime.datetime.now(),"Trafico finalizado")
    collect_process.join()
    print(datetime.datetime.now(),"Coleta finalizada")
    
    
def benign_traffic(file_name, target, interface, duration_in_s):
    # Start tcpdump and ping concurrently
    
    h3_cmd = "time tshark -i " + interface + "  -a duration:"+ duration_in_s +" \
                           -w cicflowmeter/benign_input/"+ file_name +".pcap"
                    #    -b duration:60 \
                    #    -b files:1000 \
                    #    -b filesize:100000 \

    h1_cmd = "timeout " + duration_in_s + "s hping3 " + target
      
    # Create processes for tcpdump and ping
    collect_process = multiprocessing.Process(target=run_h3, args=(h3_cmd,))
    traffic_process = multiprocessing.Process(target=run_h1, args=(h1_cmd,))
    
    # Start the processes
    collect_process.start()
    print(datetime.datetime.now(),"Coleta iniciada")
    traffic_process.start()
    print(datetime.datetime.now(),"Trafico iniciado")
    
    
    # Wait for both processes to finish
    traffic_process.join()
    print(datetime.datetime.now(),"Trafico finalizado")
    collect_process.join()
    print(datetime.datetime.now(),"Coleta finalizada")
    
    
    
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
    
    
    
    print(datetime.datetime.now(), " - Topologia Iniciada")
    
    
    target = "10.0.0.2"
    interface = "h3-eth0"
    attack_duration_s = "10"
    benign_duration_s = "60"
    
    time.sleep(3)
    print(datetime.datetime.now(), " - Iniciando fluxo Benigno")
    
    benign_traffic("my_pcap", target, interface, benign_duration_s)
    
    
    time.sleep(3)
    
    print(datetime.datetime.now(), " - Iniciando ataque:")
    
    syn_flood_attack(target, interface, attack_duration_s)
    


    net.stop()
