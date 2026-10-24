# Acolher – Plataforma Educacional

Projeto acadêmico sobre autismo, práticas inclusivas para professores e rede de apoio à comunidade escolar. HTML, CSS e JavaScript, sem compilação.

## Conteúdos

- `index.html`: apresentação, caminhos de navegação e rede de apoio (`#rede-apoio`).
- `autismo.html`: compreensão do espectro e inclusão escolar.
- `professores.html`: práticas inclusivas, central de situações e articulação com a rede.
- `referencias.html` e `referencias.txt`: fontes para consulta, cópia e download.

## Prévia local

Na pasta do projeto, execute:

```bash
python3 -m http.server 8766 --bind 127.0.0.1
```

Abra http://127.0.0.1:8766/index.html. Os links usam arquivos reais e funcionam na prévia estática. O `servidor.py` antigo inclui um túnel público e não é necessário para visualizar localmente.

## Aparência e preferências

Estilos principais em `assets/css/design.css`; os guias também usam `assets/css/style.css`. Foram preservados paleta, tipografia, ilustrações, cartões e botões. As preferências de acessibilidade são guardadas no navegador. Os recursos do portal são educativos.

## Publicação

A configuração `vercel.json` mantém os endereços sem extensão na hospedagem Vercel. A navegação não depende de reescrever endereços via JavaScript. Editar estes arquivos não publica automaticamente o site.
