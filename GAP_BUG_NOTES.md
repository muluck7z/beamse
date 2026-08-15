# Bug: buraco branco/reservado entre cards na aba Methods (mobile)

## Análise do usuário (via cloud AI)
1. Skeleton/placeholder preso (linhas pontilhadas cinza-clara no meio das duas imagens).
2. Cards com altura fixa cortando conteúdo ("Auto Click" cortando o botão do card anterior).
3. Elemento position absolute/fixed invisível ocupando área e empurrando conteúdo.

## Achados até agora (Beamse)
- Tab metodos (linha 2630+): HTML limpo, sem placeholder extra entre #metodos-list e os cards.
- 6 elementos `.tut-video-banner` com `data-src` (linhas 2352, 2380, 2408, 2533, 2579, 2611).
  - Banners 2352-2408: dentro da tab v1/roubo (tutorial principal?) — são os vídeos de banner da aba Tutorial PC.
  - Banner 2533: bypass (panel bypass), 2579: cookie (panel cookie-cel?), 2611: authenticator (panel authenticator).
- CSS .tut-video-banner (linha 1313-1350) + `.tut-video-banner-inner{aspect-ratio:4/3}` no mobile (linha 1390).
- JS linha 4214: `openModal(banner.getAttribute('data-src'))` — click no banner abre modal de vídeo.
- clearVideoSources/restoreVideoSources: troca o src dos vídeos entre tabs (data-origSrc).

## Hipótese principal agora
O `.tut-video-banner` tem altura fixa (aspect-ratio 4/3 no mobile, ou 16/9 no desktop) e os vídeos estão com preload=metadata — quando o vídeo não carrega (rede instável/URL raw.githubusercontent que pode falhar), o banner FICA com o espaço reservado vazio, criando o "buraco branco" entre os cards, empurrando o card seguinte para baixo.
No Beaming NÃO existe .tut-video-banner (usa video-player com controls, o vídeo renderiza dentro do fluxo).

## AÇÃO PLANEJADA
Colapsar .tut-video-banner quando o vídeo não carregar: adicionar JS onerror/onstalled nos vídeos dos banners que adiciona classe 'failed' e esconde o banner (display:none), liberando o espaço. Também checar se os URLs raw.githubusercontent.com funcionam (pode ser 404 → banner vazio perpetuo).
Alternativa: mudar data-src dos banners para media.githubusercontent.com (como o authenticator, linha 2611, que já usa a versão correta) — o raw.githubusercontent.com NÃO redireciona para o arquivo binário em alguns casos; media. sim.

## Estrutura confirmada
- Os 3 banners (2352, 2380, 2408) estão DENTRO de tutorial-card em uma tab (Webhook, Tutorial 01...). Eles têm altura fixa (aspect-ratio 16/9 desktop, 4/3 mobile) e vídeos com preload=metadata.
- Se a ab do usuário mostrava esses banners como casca vazia entre os cards de métodos, ele está vendo uma tab que contém tutoriais + métodos misturados? OU os cards de métodos dele têm altura cortada.
- URLs dos vídeos OK (HTTP 200, application/octet-stream).

## Ação final planejada
1. Colapsar banners sem vídeo carregado: JS onerror/stalled nos vídeos → esconde o banner (height:0). Assim o espaço reservado nunca fica branco.
2. Verificar onde exatamente esses 3 banners aparecem na navegação (qual tab/panel).

## Estado operacional
- Beamse: /home/ubuntu/Beamse. Push: git push origin main -q && git push beamse-lower HEAD:beamse-lower -q
- Últimos commits: a8b0df4 (trigger webhook), 29328ee (preload metadata), 6e4838c (sem panel-fade).
- Screenshot usuário: aba Methods, cards com buraco branco gigante e "Auto Click" cortando botão do card anterior.
