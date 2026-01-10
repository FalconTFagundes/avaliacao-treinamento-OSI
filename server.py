#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BigCard Training - Sistema de Avaliação
Servidor Python simples para coletar respostas de treinamento
Perguntas configuráveis via perguntas.txt
Salva tudo em respostas.txt
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime
import os

PORT = 3000
DATA_FILE = "respostas.txt"
QUESTIONS_FILE = "perguntas.txt"
CONFIG_FILE = "config.txt"

class ConfigLoader:
    """Carrega configurações do sistema do arquivo config.txt"""
    
    def __init__(self, filename):
        self.filename = filename
        self.instituicao = "BIGCARD"  # Valor padrão
        self.cor = "#0066cc"  # Azul padrão
        self.cor_rgb = (0, 102, 204)  # RGB para PDF
        self.load_config()
    
    def load_config(self):
        """Lê o arquivo de configuração"""
        if not os.path.exists(self.filename):
            print(f"⚠️  Arquivo {self.filename} não encontrado. Usando valores padrão.")
            return
        
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Ignora comentários e linhas vazias
                    if not line or line.startswith('#'):
                        continue
                    
                    # Processa configurações
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip().upper()
                        value = value.strip()
                        
                        if key == 'INSTITUICAO':
                            self.instituicao = value
                        elif key == 'COR':
                            self.cor = value
                            self.cor_rgb = self._parse_color(value)
        except Exception as e:
            print(f"⚠️  Erro ao ler {self.filename}: {e}. Usando valores padrão.")
    
    def _parse_color(self, color_str):
        """Converte string de cor para RGB (para usar no PDF)"""
        color_str = color_str.strip()
        
        # Se for RGB explícito (ex: "255,0,0" ou "rgb(255,0,0)")
        if ',' in color_str:
            color_str = color_str.replace('rgb(', '').replace(')', '').strip()
            parts = [int(x.strip()) for x in color_str.split(',')]
            if len(parts) == 3:
                return tuple(parts)
        
        # Se for hexadecimal (ex: "#ff5733")
        if color_str.startswith('#'):
            hex_color = color_str.lstrip('#')
            if len(hex_color) == 6:
                return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Cores nomeadas comuns
        color_map = {
            'blue': (0, 102, 204),
            'red': (220, 53, 69),
            'green': (40, 167, 69),
            'yellow': (255, 193, 7),
            'orange': (253, 126, 20),
            'purple': (111, 66, 193),
            'pink': (232, 62, 140),
            'black': (0, 0, 0),
            'gray': (108, 117, 125),
            'grey': (108, 117, 125),
        }
        
        color_lower = color_str.lower()
        if color_lower in color_map:
            return color_map[color_lower]
        
        # Se não conseguir parsear, retorna azul padrão
        return (0, 102, 204)
    
    def get_instituicao(self):
        return self.instituicao
    
    def get_cor(self):
        return self.cor
    
    def get_cor_rgb(self):
        return self.cor_rgb

class QuestionLoader:
    """Carrega e gerencia as perguntas do arquivo de texto"""
    
    def __init__(self, filename):
        self.filename = filename
        self.questions = []
        self.load_questions()
    
    def load_questions(self):
        """Lê o arquivo de perguntas e organiza os dados"""
        if not os.path.exists(self.filename):
            raise FileNotFoundError(f"Arquivo {self.filename} não encontrado!")
        
        with open(self.filename, 'r', encoding='utf-8') as f:
            lines = [line.rstrip() for line in f.readlines()]
        
        current_question = None
        alternativas = []
        
        for line in lines:
            # Ignora linhas vazias e comentários
            if not line.strip() or line.strip().startswith('#'):
                continue
            
            # Detecta início de questão
            if line[0].isdigit() and '. ' in line:
                # Salva questão anterior se existir
                if current_question:
                    if alternativas:
                        current_question['alternativas'] = alternativas
                    self.questions.append(current_question)
                    alternativas = []
                
                # Nova questão
                parts = line.split('. ', 1)
                numero = int(parts[0])
                texto = parts[1]
                
                # Verifica se é múltipla escolha
                is_multipla = '[MULTIPLA_ESCOLHA]' in texto
                if is_multipla:
                    texto = texto.replace('[MULTIPLA_ESCOLHA]', '').strip()
                
                current_question = {
                    'numero': numero,
                    'texto': texto,
                    'tipo': 'multipla_escolha' if is_multipla else 'aberta'
                }
            
            # Detecta alternativas (linhas que começam com a), b), c), etc)
            elif line.strip() and line.strip()[0].lower() in 'abcdefghij' and line.strip()[1:3] == ') ':
                alternativas.append(line.strip())
        
        # Adiciona última questão
        if current_question:
            if alternativas:
                current_question['alternativas'] = alternativas
            self.questions.append(current_question)
    
    def get_total_questions(self):
        return len(self.questions)
    
    def get_question_text(self, index):
        """Retorna o texto da questão (índice começa em 0)"""
        if 0 <= index < len(self.questions):
            q = self.questions[index]
            return f"{q['numero']}. {q['texto']}"
        return ""
    
    def get_question_type(self, index):
        """Retorna o tipo da questão: 'aberta' ou 'multipla_escolha'"""
        if 0 <= index < len(self.questions):
            return self.questions[index]['tipo']
        return 'aberta'
    
    def get_alternativas(self, index):
        """Retorna as alternativas de uma questão de múltipla escolha"""
        if 0 <= index < len(self.questions):
            return self.questions[index].get('alternativas', [])
        return []

# Carrega as configurações no início
try:
    config_loader = ConfigLoader(CONFIG_FILE)
    print(f"✅ Configurações carregadas:")
    print(f"   • Instituição: {config_loader.get_instituicao()}")
    print(f"   • Cor: {config_loader.get_cor()} (RGB: {config_loader.get_cor_rgb()})")
except Exception as e:
    print(f"❌ ERRO ao carregar configurações: {e}")
    exit(1)

# Carrega as perguntas no início
try:
    question_loader = QuestionLoader(QUESTIONS_FILE)
    print(f"✅ {question_loader.get_total_questions()} perguntas carregadas de {QUESTIONS_FILE}")
except Exception as e:
    print(f"❌ ERRO ao carregar perguntas: {e}")
    print(f"   Certifique-se que o arquivo '{QUESTIONS_FILE}' existe no mesmo diretório.")
    exit(1)

class BigCardHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        """Serve o formulário HTML"""
        if self.path == '/' or self.path == '/formulario':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(get_formulario_html().encode('utf-8'))
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Recebe e salva as respostas no TXT"""
        if self.path == '/enviar':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            salvar_resposta(data)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True}).encode('utf-8'))
        else:
            self.send_error(404)
    
    def log_message(self, format, *args):
        pass

def salvar_resposta(data):
    """Salva resposta formatada no arquivo TXT"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    linha = f"\n{'='*100}\n"
    linha += f"DATA/HORA: {timestamp}\n"
    linha += f"NOME: {data['nome']}\n"
    linha += f"TOTAL DE RESPOSTAS: {len(data['respostas'])}/{question_loader.get_total_questions()}\n"
    linha += f"{'='*100}\n\n"
    
    for i, resposta in enumerate(data['respostas']):
        pergunta_texto = question_loader.get_question_text(i)
        tipo = question_loader.get_question_type(i)
        
        linha += f"{pergunta_texto}\n"
        
        if tipo == 'multipla_escolha':
            # Converte índice para texto da alternativa
            alternativas = question_loader.get_alternativas(i)
            if 0 <= int(resposta) < len(alternativas):
                linha += f"RESPOSTA: {alternativas[int(resposta)]}\n\n"
            else:
                linha += f"RESPOSTA: [Alternativa inválida: {resposta}]\n\n"
        else:
            linha += f"RESPOSTA: {resposta}\n\n"
    
    with open(DATA_FILE, 'a', encoding='utf-8') as f:
        f.write(linha)
    
    print(f"✅ Nova resposta salva: {data['nome']}")

def get_formulario_html():
    """Gera o HTML do formulário dinamicamente com base nas perguntas carregadas"""
    
    # Obtém configurações
    instituicao = config_loader.get_instituicao()
    cor = config_loader.get_cor()
    cor_rgb = config_loader.get_cor_rgb()
    
    # Gera o HTML das questões
    questions_html = ""
    for i in range(question_loader.get_total_questions()):
        tipo = question_loader.get_question_type(i)
        texto = question_loader.get_question_text(i)
        
        if tipo == 'multipla_escolha':
            # Questão de múltipla escolha
            alternativas = question_loader.get_alternativas(i)
            questions_html += f'''
      <div class="question">
        <div class="question-title">{texto}</div>
'''
            for j, alt in enumerate(alternativas):
                letra = alt[0].lower()
                questions_html += f'''
        <div class="radio-option">
          <input type="radio" name="q{i}" value="{j}" id="q{i}{letra}">
          <label for="q{i}{letra}">{alt}</label>
        </div>
'''
            questions_html += '      </div>\n'
        else:
            # Questão aberta
            questions_html += f'''
      <div class="question">
        <div class="question-title">{texto}</div>
        <textarea id="q{i}" class="form-input" placeholder="Digite sua resposta..."></textarea>
      </div>
'''
    
    # Template HTML completo
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>BigCard - Avaliação de Treinamento</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ 
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      background: #f8f9fa;
      color: #2c3e50;
    }}
    .container {{
      max-width: 900px;
      margin: 0 auto;
      padding: 20px;
    }}
    .header {{
      background: white;
      padding: 40px;
      text-align: center;
      border-bottom: 3px solid {cor};
      margin-bottom: 30px;
    }}
    .logo {{
      font-size: 32px;
      font-weight: 700;
      color: {cor};
      margin-bottom: 10px;
      letter-spacing: -0.5px;
    }}
    .subtitle {{
      color: #6c757d;
      font-size: 16px;
    }}
    .card {{
      background: white;
      border: 1px solid #e0e0e0;
      border-radius: 8px;
      padding: 30px;
      margin-bottom: 20px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    .question {{
      background: white;
      border: 1px solid #e0e0e0;
      border-radius: 8px;
      padding: 25px;
      margin-bottom: 20px;
      transition: border-color 0.3s;
    }}
    .question:hover {{
      border-color: {cor};
    }}
    .question-title {{
      font-size: 16px;
      font-weight: 600;
      color: #2c3e50;
      margin-bottom: 15px;
      line-height: 1.6;
    }}
    .form-label {{
      display: block;
      font-weight: 600;
      color: #495057;
      margin-bottom: 8px;
      font-size: 14px;
    }}
    .form-input {{
      width: 100%;
      padding: 12px 16px;
      border: 2px solid #e0e0e0;
      border-radius: 6px;
      font-size: 15px;
      transition: border-color 0.3s;
      background: #fafafa;
    }}
    .form-input:focus {{
      outline: none;
      border-color: {cor};
      background: white;
    }}
    textarea.form-input {{
      resize: vertical;
      min-height: 120px;
      font-family: inherit;
      line-height: 1.5;
    }}
    .radio-option {{
      display: flex;
      align-items: flex-start;
      padding: 14px;
      margin-bottom: 10px;
      border: 2px solid #e0e0e0;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.3s;
      background: #fafafa;
    }}
    .radio-option:hover {{
      border-color: {cor};
      background: white;
    }}
    .radio-option input[type="radio"] {{
      margin-right: 12px;
      margin-top: 3px;
      cursor: pointer;
    }}
    .radio-option label {{
      cursor: pointer;
      color: #495057;
      line-height: 1.5;
      flex: 1;
    }}
    .btn {{
      width: 100%;
      padding: 16px;
      border: none;
      border-radius: 6px;
      font-size: 16px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.3s;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .btn-primary {{
      background: {cor};
      color: white;
    }}
    .btn-primary:hover {{
      background: {cor};
      opacity: 0.9;
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba({cor_rgb[0]}, {cor_rgb[1]}, {cor_rgb[2]}, 0.3);
    }}
    .btn-success {{
      background: #28a745;
      color: white;
    }}
    .btn-success:hover {{
      background: #218838;
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
    }}
    .hidden {{
      display: none;
    }}
    .result-container {{
      text-align: center;
      padding: 50px 30px;
    }}
    .result-icon {{
      width: 80px;
      height: 80px;
      margin: 0 auto 20px;
      background: #28a745;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
    }}
    .result-icon svg {{
      width: 50px;
      height: 50px;
    }}
    .result-title {{
      font-size: 28px;
      font-weight: 700;
      color: #2c3e50;
      margin-bottom: 10px;
    }}
    .result-subtitle {{
      font-size: 16px;
      color: #6c757d;
      margin-bottom: 30px;
    }}
  </style>
</head>
<body>
  <div class="header">
    <div class="logo">{instituicao}</div>
    <div class="subtitle">Avaliação de Treinamento Técnico</div>
  </div>

  <div class="container">
    <!-- Formulário Inicial -->
    <div id="formSection" class="card">
      <h2 style="font-size: 24px; color: #2c3e50; margin-bottom: 20px;">Identificação</h2>
      <label class="form-label">Nome Completo</label>
      <input type="text" id="nome" class="form-input" placeholder="Digite seu nome completo">
      <button onclick="iniciarAvaliacao()" class="btn btn-primary" style="margin-top: 20px;">
        Iniciar Avaliação
      </button>
    </div>

    <!-- Questionário -->
    <div id="quizSection" class="hidden">
      <div class="card" style="background: rgba({cor_rgb[0]}, {cor_rgb[1]}, {cor_rgb[2]}, 0.1); border-color: {cor};">
        <p style="margin: 0; color: {cor}; font-weight: 600;">
          📝 Responda todas as {question_loader.get_total_questions()} questões abaixo
        </p>
      </div>

{questions_html}

      <div class="card">
        <button onclick="enviarRespostas()" class="btn btn-success">
          Enviar Respostas
        </button>
      </div>
    </div>

    <!-- Resultado -->
    <div id="resultSection" class="hidden">
      <div class="card result-container">
        <div class="result-icon">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
        </div>
        <div class="result-title">Avaliação Enviada com Sucesso!</div>
        <div class="result-subtitle">Suas respostas foram registradas e serão analisadas.</div>
        <button onclick="baixarComprovante()" class="btn btn-primary">
          📄 Baixar Comprovante em PDF
        </button>
      </div>
    </div>

  </div>

  <script>
    const TOTAL_QUESTIONS = {question_loader.get_total_questions()};
    const QUESTION_TYPES = {json.dumps([question_loader.get_question_type(i) for i in range(question_loader.get_total_questions())])};
    let userData = {{}};

    function iniciarAvaliacao() {{
      const nome = document.getElementById('nome').value.trim();
      
      if (!nome) {{
        alert('⚠️ Por favor, preencha seu nome completo!');
        return;
      }}
      
      userData = {{ nome }};
      document.getElementById('formSection').classList.add('hidden');
      document.getElementById('quizSection').classList.remove('hidden');
      window.scrollTo(0, 0);
    }}

    async function enviarRespostas() {{
      const respostas = [];
      
      for (let i = 0; i < TOTAL_QUESTIONS; i++) {{
        if (QUESTION_TYPES[i] === 'multipla_escolha') {{
          const radio = document.querySelector(`input[name="q${{i}}"]:checked`);
          if (!radio) {{
            alert(`⚠️ Por favor, responda a questão ${{i + 1}}!`);
            window.scrollTo(0, document.querySelector(`.question:nth-child(${{i + 2}})`).offsetTop - 100);
            return;
          }}
          respostas.push(radio.value);
        }} else {{
          const resposta = document.getElementById(`q${{i}}`).value.trim();
          if (!resposta || resposta.length < 10) {{
            alert(`⚠️ Por favor, responda completamente a questão ${{i + 1}}!`);
            window.scrollTo(0, document.getElementById(`q${{i}}`).offsetTop - 100);
            return;
          }}
          respostas.push(resposta);
        }}
      }}

      try {{
        const response = await fetch('/enviar', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{
            nome: userData.nome,
            respostas: respostas
          }})
        }});

        if (response.ok) {{
          mostrarResultado();
        }} else {{
          alert('❌ Erro ao enviar. Tente novamente!');
        }}
      }} catch (error) {{
        alert('❌ Erro de conexão. Verifique se o servidor está rodando!');
        console.error(error);
      }}
    }}

    function mostrarResultado() {{
      document.getElementById('quizSection').classList.add('hidden');
      document.getElementById('resultSection').classList.remove('hidden');
      window.scrollTo(0, 0);
    }}

    function baixarComprovante() {{
      const {{ jsPDF }} = window.jspdf;
      const pdf = new jsPDF();
      
      // Cabeçalho com cor configurável
      pdf.setFillColor({cor_rgb[0]}, {cor_rgb[1]}, {cor_rgb[2]});
      pdf.rect(0, 0, 210, 35, 'F');
      
      pdf.setTextColor(255, 255, 255);
      pdf.setFontSize(26);
      pdf.setFont(undefined, 'bold');
      pdf.text('{instituicao}', 105, 20, {{ align: 'center' }});
      
      pdf.setFontSize(12);
      pdf.setFont(undefined, 'normal');
      pdf.text('Comprovante de Avaliação', 105, 28, {{ align: 'center' }});
      
      // Corpo
      pdf.setTextColor(0, 0, 0);
      pdf.setFontSize(14);
      pdf.text('COMPROVANTE DE PARTICIPAÇÃO', 105, 55, {{ align: 'center' }});
      
      pdf.setFontSize(11);
      pdf.setFont(undefined, 'normal');
      pdf.text('Certificamos que', 105, 75, {{ align: 'center' }});
      
      pdf.setFontSize(16);
      pdf.setFont(undefined, 'bold');
      pdf.text(userData.nome, 105, 90, {{ align: 'center' }});
      
      pdf.setFontSize(11);
      pdf.setFont(undefined, 'normal');
      pdf.text('concluiu e enviou as respostas da', 105, 105, {{ align: 'center' }});
      pdf.text('Avaliação de Treinamento Técnico', 105, 113, {{ align: 'center' }});
      pdf.text('Operador de Sistemas de Informática', 105, 121, {{ align: 'center' }});
      
      // Info
      pdf.setFontSize(10);
      pdf.setTextColor(100, 100, 100);
      pdf.text(`Data: ${{new Date().toLocaleDateString('pt-BR')}}`, 105, 145, {{ align: 'center' }});
      pdf.text(`Horário: ${{new Date().toLocaleTimeString('pt-BR')}}`, 105, 152, {{ align: 'center' }});
      
      // Rodapé
      pdf.setFontSize(9);
      pdf.text('As respostas estão sendo analisadas.', 105, 170, {{ align: 'center' }});
      pdf.text('Este documento é apenas um comprovante de participação.', 105, 176, {{ align: 'center' }});
      
      pdf.setDrawColor({cor_rgb[0]}, {cor_rgb[1]}, {cor_rgb[2]});
      pdf.line(20, 190, 190, 190);
      
      pdf.setFontSize(8);
      pdf.text('{instituicao} - Sistema de Avaliação de Treinamento', 105, 195, {{ align: 'center' }});
      
      // Salvar
      pdf.save(`Comprovante_${{userData.nome.replace(/\\s+/g, '_')}}.pdf`);
    }}
  </script>
</body>
</html>'''

def main():
    import socket
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    except:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    
    server = HTTPServer(('0.0.0.0', PORT), BigCardHandler)
    
    print('\n' + '='*70)
    print('🚀 BIGCARD TRAINING - SERVIDOR PYTHON')
    print('='*70)
    print(f'📱 FUNCIONÁRIO acessa: http://{local_ip}:{PORT}')
    print(f'💾 Respostas salvas em: {DATA_FILE}')
    print(f'📝 Perguntas carregadas de: {QUESTIONS_FILE}')
    print(f'📂 Para ver respostas: abra o arquivo {DATA_FILE} no Bloco de Notas')
    print('='*70)
    print('✅ Servidor rodando! Pressione CTRL+C para parar')
    print('='*70 + '\n')
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n\n⏹️  Servidor parado!')
        server.shutdown()

if __name__ == '__main__':
    main()