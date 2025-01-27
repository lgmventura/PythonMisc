#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 19:28:30 2025

@author: luiz
"""

import json

resolution = [3840, 1920] # [1920, 1080]
                    #^^^ because of the margins

slides_fp = '/home/luiz/Documents/Viagens/Vietnã 2024 - 2025/slides_dia4.json'

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

        script_item = f'''      {{
        type: "video",
        id: "video{idx}",
        src: "{slide["file"]}",
        muted: {str(muted).lower()},
        start: {start},
        end: {end}
      }},
        '''
        #.replace('{idx}', f'{idx}').replace('{start}', f'{start}').replace('{end}', f'{end}')
        
    elif slide['file'].lower().endswith('.jpg'):
        script_item = f'''      {{
        type: "photo",
        id: "photo{idx}",
        src: "{slide["file"]}",
        start: {start},
        end: {end},
        zoom_pan
      }},
        '''
        #.replace('{idx}', f'{idx}').replace('{start}', f'{start}').replace('{end}', f'{end}')
        
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
        script_item = script_item.replace('zoom_pan', zoom_pan_str)
    script_items.append(script_item)
    start = start + slide['duration']

script_items_str = '\n'.join(script_items)

middle_lines = '''
  </div>

  <!-- Áudio da narração -->
  <audio id="narration" src="{audio}" preload="auto" controls></audio>

  <script>
    const slides = [
'''.replace('{audio}', f'{audio_fp}')

final_lines = '''    ];

    const presentation = document.getElementById("presentation");
    const narration = document.getElementById("narration");

    let activeElement = null;
    let lastTime = -1;

    // Função para carregar dinamicamente os slides
    function loadSlide(slide) {
      const element = document.createElement(slide.type === "photo" ? "img" : "video");
      element.classList.add("media");
      element.id = `slide-${slide.start}`;
      element.src = slide.src;

      if (slide.type === "video") {
        element.muted = slide.muted;
        element.preload = "auto";
      }

      presentation.appendChild(element);
      console.log(`Carregado: ${slide.src}`);
      return element;
    }

    // Função para animar os slides
    function animateSlide(slide, element, progress) {
      if (slide.type === "photo") {
        const zoomLevel = slide.zoom[0] + progress * (slide.zoom[1] - slide.zoom[0]);
        const panX = slide.pan[0].x + progress * (slide.pan[1].x - slide.pan[0].x);
        const panY = slide.pan[0].y + progress * (slide.pan[1].y - slide.pan[0].y);

        element.style.transform = `scale(${zoomLevel})`;
        element.style.transformOrigin = `${panX}% ${panY}%`;
      }
    }

    // Função principal para controlar os slides
    function updateSlides() {
      const currentTime = narration.currentTime;

      //if (currentTime === lastTime) return; // Evita atualizações desnecessárias
      //lastTime = currentTime;

      slides.forEach(slide => {
        const elementId = `slide-${slide.start}`;
        let element = document.getElementById(elementId);

        if (currentTime >= slide.start && currentTime <= slide.end) {
          if (!element) {
            element = loadSlide(slide);
          }

          // Exibe e anima o slide atual
          if (activeElement && activeElement !== element) {
            activeElement.style.opacity = 0;
            if (activeElement.tagName === "VIDEO") {
              activeElement.pause();
            }
          }

          element.style.opacity = 1;
          activeElement = element;

          if (slide.type === "video") {
            if (element.paused) {
              element.play();
            }
          } else {
            const progress = (currentTime - slide.start) / (slide.end - slide.start);
            animateSlide(slide, element, progress);
          }
        } else if (element && currentTime > slide.end) {
          // Remove slides antigos
          presentation.removeChild(element);
          console.log(`Removido: ${slide.src}`);
        }
      });
      requestAnimationFrame(updateSlides);
    }

    // Sincroniza com o áudio
    //narration.addEventListener("timeupdate", updateSlides);

    // Inicia a animação quando o áudio começar
    narration.addEventListener("play", () => {
      //updateSlides();
      requestAnimationFrame(updateSlides);
    });
    
        
    // Pausa a atualização se a narração for pausada
    narration.addEventListener("pause", () => {
      cancelAnimationFrame(updateSlides);
    });
  </script>
</body>
</html>

'''

with open(out_html_fp, 'w') as f:
    f.write(header)
    f.write(middle_lines)
    f.write(script_items_str)
    f.write(final_lines)
