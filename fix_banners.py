import re

path = '/home/ubuntu/Beamse/index.html'
with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

changes = 0

# 1) Banner CSS: banner com .failed colapsa totalmente (sem espaço branco)
css_old = '''  .tut-video-banner{
    margin-bottom:18px;
    border-radius:14px;
    overflow:hidden;
    background:#000;
    border:1px solid rgba(17,17,17,0.3);
    cursor:pointer;
  }'''
css_new = '''  .tut-video-banner{
    margin-bottom:18px;
    border-radius:14px;
    overflow:hidden;
    background:#000;
    border:1px solid rgba(17,17,17,0.3);
    cursor:pointer;
  }
  /* Colapsa o banner se o vídeo falhar/não existir (sem buraco branco) */
  .tut-video-banner.failed{
    display:none;
    height:0;
    margin:0;
    padding:0;
    border:none;
    overflow:hidden;
  }'''
if css_old in html:
    html = html.replace(css_old, css_new)
    changes += 1
    print('CSS failed-rule added')
else:
    print('WARN: css_old not found')

# 2) Trocar URLs dos banners de raw.githubusercontent.com -> media.githubusercontent.com
def media_replace(m):
    url = m.group(0)
    return url.replace('https://raw.githubusercontent.com/', 'https://media.githubusercontent.com/media/')

# banners: data-src e <source src>
before = html
html = re.sub(r'(data-src="https://raw\.githubusercontent\.com/[^"]+"|<source src="https://raw\.githubusercontent\.com/[^"]+")', media_replace, html)
changes += (html != before and 1 or 0)
if html != before:
    print('Banner URLs switched to media.githubusercontent.com')
else:
    print('No banner URLs replaced')

# 3) JS: detectar falha de carregamento nos vídeos dos banners e colapsar
js_block = '''    // Colapsa banner de tutorial se o vídeo não carregar (remove o buraco branco)
    document.querySelectorAll('.tut-video-banner video').forEach(function(v){
      var banner = v.closest('.tut-video-banner');
      var settled = false;
      var settle = function(){
        if (settled) return;
        settled = true;
        // Só colapsa se o banner estiver vazio (sem metadados -> sem vídeo válido)
        if (!v.duration || !isFinite(v.duration)) {
          if (banner) banner.classList.add('failed');
        } else {
          // Vídeo ok: mostra o poster do primeiro frame quando possível
          banner.style.visibility = 'visible';
        }
      };
      v.addEventListener('error', settle);
      v.addEventListener('stalled', function(){ setTimeout(settle, 8000); });
      // Timeout de segurança: se nada aconteceu em 12s, checa
      setTimeout(function(){ if (!settled && (!v.duration || !isFinite(v.duration))) settle(); }, 12000);
    });'''

marker = "document.querySelectorAll('.tut-video-banner').forEach(function(banner){"
if marker in html:
    html = html.replace(marker, js_block + '\n    ' + marker)
    changes += 1
    print('JS collapse-on-fail added')
else:
    print('WARN: banner forEach marker not found')

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print('total change groups:', changes)
