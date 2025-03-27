# Tecnologias Assistivas para Surdos - API

## Descrição

Este projeto é um produto de mestrado profissional e consiste em uma API estática composta por arquivos JSON que fornecem informações sobre diversas tecnologias assistivas para surdos. A API inclui arquivos de índice organizados por categoria, custo, etapas de ensino, necessidade de conexão com a internet, entre outros.

Os arquivos JSON são gerados automaticamente a partir de um script Python (`main.py`), que processa os dados contidos no arquivo `tecnologias.csv` e gera a estrutura organizada dos arquivos JSON na pasta `api/`.

---

## Estrutura do Projeto
`api/` # Diretório com os arquivos JSON gerados
`api/categorias.json` # Lista de categorias de tecnologias assistivas
`api/custo.json` # Classificação das tecnologias por custo
`api/etapas_ensino.json` # Mapeamento das tecnologias para diferentes etapas de ensino
`api/requer_internet.json` # Indica quais tecnologias necessitam de conexão com a internet
`api/indice.json` # Arquivo de índice geral das tecnologias
`api/.json` # Arquivos JSON individuais de cada tecnologia assistiva
`imagens/` # Diretório com imagens de cada tecnologia; O arquivo de imagem da tecnologia é '<slug>.jpg'
`index.html` # Arquivo HTML para apresentação da API
`main.py` # Script Python para geração dos arquivos JSON
`tecnologias.csv` # Fonte de dados original com as tecnologias assistivas
`README.md` # Documentação do projeto

---

## Como Utilizar

### 1. Executando o Script de Geração
- Certifique-se de ter o Python instalado (versão 3).
- Execute o seguinte comando no terminal para gerar os arquivos JSON:
```
  python3 main.py
```
-  Os arquivos JSON serão criados na pasta `api/`.
  
### 2. Acessando os Dados
-   Os arquivos JSON podem ser acessados diretamente pelo caminho `api/<tecnologia>.json`.
-   Para consultar as lista de tecnologias disponíveis, utilize o arquivo `api/indice.json`.
-   Para consultar as lista de tecnologias disponíveis por categoria, utilize o arquivo `api/categorias.json`.

### 3. Documentação
-   Consulte o arquivo `index.html` para toda a documentação da API.

---

## Contribuição
Caso queira contribuir com este projeto, siga os passos:
1.  Faça um fork do repositório.
2.  Crie uma nova branch para suas alterações.
3.  Faça commit das suas mudanças.
4.  Envie um pull request.

---

## Contato
Para mais informações, entre em contato pelo e-mail: [seu-email@example.com](mailto:seu-email@example.com).
