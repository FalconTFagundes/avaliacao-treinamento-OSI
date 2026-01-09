# Sistema de Avaliação

Sistema web de avaliação técnica para treinamentos operacionais. Desenvolvido em Python puro, sem dependências externas, com **perguntas totalmente configuráveis via arquivo de texto**.

## 📋 Sobre

Sistema simples e eficiente que permite aplicar questionários técnicos para funcionários em treinamento. As respostas são coletadas via formulário web e armazenadas automaticamente em arquivo de texto para análise posterior.

## ⚡ Características

- **Zero dependências**: Roda apenas com Python 3 nativo
- **Perguntas configuráveis**: Edite `perguntas.txt` sem mexer no código
- **Interface web moderna**: Design responsivo e intuitivo
- **Geração de PDF**: Comprovante automático de participação
- **Armazenamento local**: Todas as respostas em arquivo .txt
- **Multi-dispositivo**: Acesso via celular, tablet ou computador na rede local
- **Flexível**: Suporta questões abertas e múltipla escolha

## 🎯 Funcionalidades

- Questionário dinâmico baseado em arquivo de texto
- Validação de preenchimento
- Salvamento automático com timestamp
- Comprovante em PDF para o participante
- Interface amigável com feedback visual

## 🚀 Tecnologias

- Python 3 (servidor HTTP nativo)
- HTML5 + CSS3 + JavaScript
- TailwindCSS (via CDN)
- jsPDF (geração de PDF no cliente)

## 📦 Estrutura

```
avaliacao-treinamento-OSI/
├── server.py          # Servidor Python completo
├── perguntas.txt      # Arquivo de configuração das perguntas
├── executar.bat       # Atalho para iniciar no Windows
└── respostas.txt      # Arquivo gerado automaticamente com as respostas
```

## 📸 Screenshots do Sistema

<img width="1365" height="680" alt="1" src="https://github.com/user-attachments/assets/6405a26e-34c0-487c-bada-22078c2a0cb1" />
<img width="1348" height="679" alt="2" src="https://github.com/user-attachments/assets/3a58d2c3-5858-4aad-8372-c5a91c11e769" />
<img width="1365" height="680" alt="3" src="https://github.com/user-attachments/assets/62ac5272-344c-4db5-8ac9-216b88d3bb97" />
<img width="1350" height="623" alt="4" src="https://github.com/user-attachments/assets/c43e3861-c206-4b20-8202-2d5cc3d4a69c" />



## 🔧 Como Usar

### 1. Executar o Servidor

**Windows (Modo Fácil):**
- Dê duplo clique no arquivo `executar.bat`

**Windows (Terminal):**
```bash
python server.py
```

**Linux/Mac:**
```bash
python3 server.py
```

### 2. Acessar o Sistema

Abra o navegador no endereço exibido no terminal (ex: `http://192.168.1.100:3000`)

### 3. Personalizar as Perguntas

Edite o arquivo `perguntas.txt` seguindo o formato:

```
# Comentários começam com #

# Questões abertas (texto livre)
1. Sua pergunta aqui?
2. Outra pergunta?

# Questão de múltipla escolha
3. Pergunta com alternativas? [MULTIPLA_ESCOLHA]
a) Primeira alternativa
b) Segunda alternativa
c) Terceira alternativa
```

**Reinicie o servidor** após editar o arquivo de perguntas.

## 🔒 Segurança

Sistema projetado para uso em rede local corporativa. Não possui autenticação ou criptografia, adequado para ambientes internos controlados.

## 📝 Licença

Este projeto não possui licença comercial e é disponibilizado apenas para fins educacionais e demonstrativos.
