#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║          ACOLHER – Servidor & Túnel Público             ║
║                                                         ║
║  Inicia o servidor local e cria um link público HTTPS   ║
║  para compartilhar o site com qualquer pessoa.          ║
║                                                         ║
║  Uso:  python3 servidor.py                              ║
║  Parar: Ctrl+C                                          ║
╚══════════════════════════════════════════════════════════╝
"""

import http.server
import socketserver
import subprocess
import threading
import signal
import sys
import os
import re
import time

# ── Configurações ──────────────────────────────────────────
PORTA = 3000
DIRETORIO = os.path.dirname(os.path.abspath(__file__))

# ── Cores no terminal ─────────────────────────────────────
class Cor:
    AZUL    = "\033[94m"
    VERDE   = "\033[92m"
    AMARELO = "\033[93m"
    VERMELHO= "\033[91m"
    NEGRITO = "\033[1m"
    RESET   = "\033[0m"
    CIANO   = "\033[96m"

def banner():
    print(f"""
{Cor.AZUL}{Cor.NEGRITO}╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   💙  A C O L H E R  –  Plataforma Educacional          ║
║                                                          ║
║   Educação • Inclusão • Bem-estar                        ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝{Cor.RESET}
""")

def log(emoji, msg, cor=Cor.RESET):
    print(f"  {emoji}  {cor}{msg}{Cor.RESET}")

# ── Servidor HTTP Local (silencioso) ──────────────────────
class ServidorSilencioso(http.server.SimpleHTTPRequestHandler):
    """Serve os arquivos sem poluir o terminal com cada request."""
    def log_message(self, format, *args):
        pass  # silencia os logs do servidor

servidor_httpd = None
tunnel_process = None

def iniciar_servidor():
    global servidor_httpd
    os.chdir(DIRETORIO)
    servidor_httpd = socketserver.TCPServer(("", PORTA), ServidorSilencioso)
    servidor_httpd.serve_forever()

# ── Túnel SSH (localhost.run) ─────────────────────────────
def iniciar_tunel():
    global tunnel_process
    log("🔗", "Conectando ao túnel público...", Cor.AMARELO)

    tunnel_process = subprocess.Popen(
        [
            "ssh",
            "-o", "StrictHostKeyChecking=no",
            "-o", "ServerAliveInterval=60",
            "-o", "ServerAliveCountMax=3",
            "-R", f"80:localhost:{PORTA}",
            "nokey@localhost.run"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    # Lê a saída do SSH procurando a URL pública
    url_encontrada = False
    for linha in tunnel_process.stdout:
        # Procura a linha com a URL .lhr.life
        match = re.search(r'https://[a-z0-9]+\.lhr\.life', linha)
        if match and not url_encontrada:
            url = match.group(0)
            url_encontrada = True
            print()
            print(f"  {Cor.VERDE}{Cor.NEGRITO}╔══════════════════════════════════════════════════════════╗")
            print(f"  ║                                                          ║")
            print(f"  ║   ✅  SITE NO AR! Compartilhe este link:                 ║")
            print(f"  ║                                                          ║")
            print(f"  ║   🌐  {url:<50} ║")
            print(f"  ║                                                          ║")
            print(f"  ║   Páginas disponíveis:                                   ║")
            print(f"  ║     • {url}/                            ║")
            print(f"  ║     • {url}/autismo.html                ║")
            print(f"  ║     • {url}/professores.html            ║")
            print(f"  ║     • {url}/estudantes.html             ║")
            print(f"  ║                                                          ║")
            print(f"  ╚══════════════════════════════════════════════════════════╝{Cor.RESET}")
            print()
            log("⏹️ ", f"Para desligar: pressione {Cor.NEGRITO}Ctrl+C{Cor.RESET}", Cor.AMARELO)
            print()

    # Se o processo terminou sem encontrar URL
    if not url_encontrada:
        log("❌", "Não foi possível obter a URL pública.", Cor.VERMELHO)
        log("💡", "Verifique sua conexão com a internet.", Cor.AMARELO)

# ── Encerramento limpo ────────────────────────────────────
def encerrar(sig=None, frame=None):
    print()
    log("🛑", "Encerrando...", Cor.AMARELO)

    if tunnel_process:
        tunnel_process.terminate()
        try:
            tunnel_process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            tunnel_process.kill()
        log("🔗", "Túnel público desconectado.", Cor.CIANO)

    if servidor_httpd:
        servidor_httpd.shutdown()
        log("🖥️ ", "Servidor local encerrado.", Cor.CIANO)

    print()
    log("👋", f"{Cor.NEGRITO}Até mais! O site não está mais acessível externamente.{Cor.RESET}", Cor.AZUL)
    print()
    sys.exit(0)

# ── Main ──────────────────────────────────────────────────
if __name__ == "__main__":
    signal.signal(signal.SIGINT, encerrar)
    signal.signal(signal.SIGTERM, encerrar)

    banner()

    # 1. Inicia o servidor HTTP em background
    log("🖥️ ", f"Iniciando servidor local na porta {Cor.NEGRITO}{PORTA}{Cor.RESET}...", Cor.CIANO)
    thread_servidor = threading.Thread(target=iniciar_servidor, daemon=True)
    thread_servidor.start()
    time.sleep(0.5)
    log("✅", f"Servidor local ativo: {Cor.NEGRITO}http://localhost:{PORTA}{Cor.RESET}", Cor.VERDE)
    print()

    # 2. Inicia o túnel (bloqueia até Ctrl+C)
    iniciar_tunel()

    # Se o túnel caiu sozinho, encerra tudo
    encerrar()
