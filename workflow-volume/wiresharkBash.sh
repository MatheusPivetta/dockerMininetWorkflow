#!/bin/bash
echo "Iniciando Reordenação"
reordercap input/mycap.pcap input/mycap-reordered.pcap
echo "Finalizando Reordenação"
echo "Deletando antigo pcap"
rm -f input/mycap.pcap
echo "Container Finalizado"