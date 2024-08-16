#!/bin/bash

# Caminho para a pasta principal
PASTA="workflow-volume/cicflowmeter"

# Verifica se o diretório existe
if [ -d "$PASTA" ]; then
  # Encontra todas as subpastas e remove os arquivos dentro delas
  find "$PASTA"/* -type d -exec find {} -type f -delete \;
  echo "Todos os arquivos nas subpastas dentro de $PASTA foram removidos."
else
  echo "A pasta $PASTA não existe."
fi