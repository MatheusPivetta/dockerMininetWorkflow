#!/bin/bash
service openvswitch-switch start
echo "Iniciando"
python3 topology.py
echo "Finalizado"


