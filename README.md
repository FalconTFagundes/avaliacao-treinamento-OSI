# BigCard Training - Sistema de Avaliação

Sistema web de avaliação técnica para treinamento de operadores de sistemas de informática da BigCard. Desenvolvido em Python puro, sem dependências externas, com **perguntas e configurações totalmente personalizáveis via arquivos de texto**.

## 📋 Sobre

Sistema simples e eficiente que permite aplicar questionários técnicos para funcionários em treinamento. As respostas são coletadas via formulário web e armazenadas automaticamente em arquivo de texto para análise posterior.

## ⚡ Características

- **Zero dependências**: Roda apenas com Python 3 nativo
- **Totalmente configurável**: Nome da instituição e cores personalizáveis via `config.txt`
- **Perguntas configuráveis**: Edite `perguntas.txt` sem mexer no código
- **Interface web moderna**: Design responsivo e intuitivo
- **Geração de PDF**: Comprovante automático de participação com cores personalizadas
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
├── config.txt         # Configurações de cor e nome da instituição
├── perguntas.txt      # Arquivo de configuração das perguntas
├── executar.bat       # Atalho para iniciar no Windows
└── respostas.txt      # Arquivo gerado automaticamente com as respostas
```

## 📸 Screenshots do Sistema

<img width="1365" height="680" alt="1" src="https://github.com/user-attachments/assets/6fd8ccde-85ed-4529-8ab3-5517326178ef" />
<img width="1365" height="680" alt="3" src="https://github.com/user-attachments/assets/045ffb0b-26a1-400b-a6f6-a342ef927213" />
<img width="1350" height="623" alt="4" src="https://github.com/user-attachments/assets/ba9c27cf-6025-4ae8-99b6-51dbd556a25e" />

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

### 4. Personalizar Visual e Nome da Instituição

Edite o arquivo `config.txt` para alterar:

**Nome da Instituição:**
```
INSTITUICAO: Nome da Sua Empresa
```

**Cargo/Função (aparece no certificado PDF):**
```
CARGO: Operador de Sistemas de Informática
```

**Cor do Sistema:**
```
# Opção 1: Nome da cor em inglês
COR: blue

# Opção 2: Código hexadecimal
COR: #ff5733

# Opção 3: RGB (separado por vírgulas)
COR: 255,0,0
```

**Exemplos de cores prontas:**
- `COR: blue` → Azul (padrão)
- `COR: #28a745` → Verde
- `COR: #ffc107` → Amarelo/Dourado
- `COR: #dc3545` → Vermelho
- `COR: #6f42c1` → Roxo
- `COR: #fd7e14` → Laranja

A cor será aplicada automaticamente em:
- Bordas do cabeçalho
- Logo e destaques
- Botões principais
- Fundo do certificado PDF

**Reinicie o servidor** após editar as configurações.

## 🔒 Segurança

Sistema projetado para uso em rede local corporativa. Não possui autenticação ou criptografia, adequado para ambientes internos controlados.

## 📝 Licença

Uso interno BigCard.
