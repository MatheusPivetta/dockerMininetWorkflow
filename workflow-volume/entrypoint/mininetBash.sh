#!/bin/bash
service openvswitch-switch start
echo "Instalando requisitos"
apt-get update
ln -fs /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime
DEBIAN_FRONTEND=noninteractive apt-get install hping3 tshark -y
apt-get install iperf3 -y
echo "Finalizando instalação de requisitos"
echo "Iniciando topologia"
python3 topology.py
echo "Finalizado topologia"
