#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 19:28:30 2025

@author: luiz
"""

import json

resolution = [3840, 1920] # [1920, 1080]
                    #^^^ because of the margins

slides_fp = '/home/luiz/Documents/Viagens/Vietnã 2024 - 2025/slides_dia2.json'

audio_fp = 'narracao.mp3'

out_html_fp = '/media/luiz/HDp1/Câmeras/EOSR6mk2/20250112/100EOSR6/slide_show.html'

with open(slides_fp, 'r') as f:
    fs = f.read()

try:
    slides = json.loads(fs)
except json.JSONDecodeError as e:
    print(f"JSON Decode Error: {e.msg}")
    print(f"Error occurred at line {e.lineno}, column {e.colno}")
    raise(RuntimeError(e.msg))

header = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Apresentação com Zoom, Pan e Vídeos</title>
  <style>
    body {
      margin: 0;
      overflow: hidden;
      background-color: black;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
    }

    #presentation {
      position: relative;
      width: {0}px;
      height: {1}px;
      overflow: hidden;
      z-index: 0;
    }

    .media {
      position: absolute;
      width: 100%;
      height: 100%;
      object-fit: contain;
      transform-origin: center;
      opacity: 0;
      z-index: 1; /* Certifique-se de que está acima do fundo */
    }
  </style>
</head>
<body>
  <div id="presentation">
'''.replace('{0}', f'{resolution[0]}').replace('{1}', f'{resolution[1]}')

items = []
script_items = []
start = 0
end = 0
for idx, slide in enumerate(slides):
    end = end + slide['duration']
    if slide['file'].lower().endswith('.mp4'):
        if 'muted' in slide.keys():
            if isinstance(slide['muted'], str):
                muted = False if slide['muted'].lower() == 'false' else True
            elif isinstance(slide['muted'], int):
                muted = bool(slide['muted'])
        else:
            muted = True  # default
        if muted:
            video_item = f'<video id="video{idx}" class="media" src="{slide["file"]}" muted></video>'
        else:
            video_item = f'<video id="video{idx}" class="media" src="{slide["file"]}"></video>'
        items.append(video_item)
        script_item = '''      {
        type: "video",
        id: "video{idx}",
        start: {start},
        end: {end}
      },
        '''.replace('{idx}', f'{idx}').replace('{start}', f'{start}').replace('{end}', f'{end}')
        
    elif slide['file'].lower().endswith('.jpg'):
        items.append(f'<img id="photo{idx}" class="media" src="{slide["file"]}" alt="Foto {idx}">')
        script_item = '''      {
        type: "photo",
        id: "photo{idx}",
        start: {start},
        end: {end},
        {zoom_pan}
      },
        '''.replace('{idx}', f'{idx}').replace('{start}', f'{start}').replace('{end}', f'{end}')
        
        zoom_pan_str = '''zoom: [1.0, 1.0],
        pan: [
                {x: 50, y: 50},
                {x: 50, y: 50}
             ]'''
        if 'zoom' in slide.keys():
            zoom_pan_str = f'zoom: {slide["zoom"]},\n'
        if 'pan' in slide.keys():
            pan_str = str(slide["pan"]).replace("'", "")
            zoom_pan_str = zoom_pan_str + f'        pan: {pan_str}\n'
        script_item = script_item.replace('{zoom_pan}', zoom_pan_str)
    script_items.append(script_item)
    start = start + slide['duration']

items_str = '\n'.join(items)
script_items_str = '\n'.join(script_items)

middle_lines = '''
  </div>

  <!-- Áudio da narração -->
  <audio id="narration" src="{audio}" preload="auto" controls></audio>

  <script>
    const slides = [
'''.replace('{audio}', f'{audio_fp}')

final_lines = '''    ];

    const narration = document.getElementById("narration");

    function animate() {
      const currentTime = narration.currentTime;

      slides.forEach(slide => {
        const element = document.getElementById(slide.id);
        
        if (currentTime >= slide.start && currentTime < slide.end) {
          // Mostra o slide
          element.style.opacity = 1;

          if (slide.type === "photo") {
            // Calcula progresso para fotos
            const duration = slide.end - slide.start;
            const progress = (currentTime - slide.start) / duration;

            // Aplica zoom
            const zoomLevel = slide.zoom[0] + progress * (slide.zoom[1] - slide.zoom[0]);
            element.style.transform = `scale(${zoomLevel})`;

            // Aplica pan
            const panStart = slide.pan[0];
            const panEnd = slide.pan[1];

            const panX = panStart.x + progress * (panEnd.x - panStart.x);
            const panY = panStart.y + progress * (panEnd.y - panStart.y);

            element.style.transformOrigin = `${panX}% ${panY}%`;
            //element.style.transformOrigin = `${panX_px}px ${panY_px}px`;
          } else if (slide.type === "video") {
            // Inicia o vídeo quando visível
            if (element.paused) {
              element.play();
            }
          }
        } else {
          // Esconde o slide
          element.style.opacity = 0;

          if (slide.type === "video") {
            // Pausa o vídeo quando não visível
            element.pause();
            element.currentTime = 0; // Reinicia o vídeo
          }
        }
      });

      requestAnimationFrame(animate);
    }

    narration.addEventListener("play", () => {
      requestAnimationFrame(animate);
    });
  </script>
</body>
</html>

'''

with open(out_html_fp, 'w') as f:
    f.write(header)
    f.write(items_str)
    f.write(middle_lines)
    f.write(script_items_str)
    f.write(final_lines)
