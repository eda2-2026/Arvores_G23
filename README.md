# Gerenciador de Estoque de Água

**Número da Lista**: 3<br>
**Conteúdo da Disciplina**: Árvores<br>

## Alunos
| Matrícula | Aluno |
| -- | -- |
| 23/1011220  |  Davi Camilo Menezes |
| 23/1026714  |  Euller Júlio da Silva |

## Apresentação do trabalho
[Link para o vídeo de apresentação]()

## Sobre
Descreva os objetivos do seu projeto e como ele funciona. 

## Screenshots
A seguir estão imagens do projeto em funcionamento.

### Execução local dos testes

![placeholder](docs/assets/testes.png)

Para garantir que a implementação da Árvore Rubro-Negra está funcionando como esperado, foram criados testes automatizados em `test_red_black_tree.py`, validando pontos como a inserção de lotes, o balanceamento da árvore, as rotações, a busca por chave, o percurso em ordem, o tratamento de chaves duplicadas e a preservação das propriedades, onde conforme a imagem, todos foram concluídos com sucesso.

## Instalação
**Linguagem**: Python<br>
**Framework**: Streamlit<br>
**Pré-requisitos:** Python 3.10+ instalado e `pytest` para rodar os testes<br>

### Como rodar

1. Clonar o repositório para a sua máquina
```bash
git clone https://github.com/eda2-2026/Arvores_Gerenciador-de-estoque-de-agua.git
```

2. Navegar até o diretório do projeto
```bash
cd Arvores_Gerenciador-de-estoque-de-agua
```

3. Instalar as dependências
```bash
python -m pip install streamlit pytest
```

4. Executar a aplicação
```bash
python -m streamlit run app.py
```

5. Rodar todos os testes
```bash
python -m pytest tests/ -v
```

**Observações**
- A aplicação é executada localmente por meio do *Streamlit* e disponibilizada em uma interface web, a qual é aberta automaticamente no navegador.
- Se `python` não estiver disponível no seu terminal, use `python3` nos comandos acima.

## Uso

Após executar `python -m streamlit run app.py`, o navegador abrirá automaticamente com a interface. Use o **menu lateral** para navegar entre as telas:

### Visualizar estoque
Exibe todos os lotes cadastrados em **ordem crescente de validade** (princípio FEFO — *First Expired, First Out*). Use o slider para controlar quantos itens são exibidos na tabela. O painel lateral mostra os totais do estoque e a altura atual da árvore rubro-negra.

###  Inserir item
Preencha o formulário com **produto, código do lote, quantidade, data de validade e fornecedor**, depois clique em **"Inserir lote"**. O item é imediatamente inserido na árvore e fica disponível nas demais telas.

###  Buscar por validade
Selecione uma data no calendário e clique em **"Buscar"**. O sistema retorna em **O(log n)** todos os lotes com exatamente aquela data de validade.

###  Próximos vencimentos
Use o slider para definir a **janela em dias** (padrão: 30). A tela lista todos os lotes que vencem dentro desse período e exibe, em separado, os lotes já vencidos.

### Percurso em ordem da árvore
Visualiza os **nós da árvore rubro-negra em ordem crescente de chave** (data de validade), mostrando quantos lotes existem em cada data. Você pode escolher exibir a partir das menores ou das maiores validades, e controlar o número de nós exibido

