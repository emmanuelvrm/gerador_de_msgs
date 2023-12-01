#!/usr/bin/env python
# coding: utf-8

# In[34]:


from PIL import Image, ImageDraw, ImageFont
import os

# Ler o arquivo de texto e adicionar cada linha a uma lista
def ler_arquivo_texto(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
    return linhas

# Ler a pasta de imagens e adicionar os nomes dos arquivos a uma lista
def ler_pasta_imagens(caminho_pasta):
    arquivos_imagens = []
    for arquivo in os.listdir(caminho_pasta):
        if arquivo.endswith(".jpg") or arquivo.endswith(".png"):
            arquivos_imagens.append(os.path.join(caminho_pasta, arquivo))
    return arquivos_imagens

# Recortar todas as imagens para a proporção 16:9
def recortar_imagens(arquivos_imagens):
    for arquivo in arquivos_imagens:
        imagem = Image.open(arquivo)
        largura, altura = imagem.size
        proporcao_alvo = 9 / 16

        if largura / altura > proporcao_alvo:
            nova_largura = altura * proporcao_alvo
            recorte_esquerda = int((largura - nova_largura) / 2)
            recorte_direita = largura - recorte_esquerda
            imagem_recortada = imagem.crop((recorte_esquerda, 0, recorte_direita, altura))
        else:
            nova_altura = largura / proporcao_alvo
            recorte_superior = int((altura - nova_altura) / 2)
            recorte_inferior = altura - recorte_superior
            imagem_recortada = imagem.crop((0, recorte_superior, largura, recorte_inferior))

        imagem_recortada.save(arquivo)

# Adicionar cada texto a uma imagem
def adicionar_texto_imagens(arquivos_imagens, linhas_texto):
    for i, arquivo in enumerate(arquivos_imagens):
        imagem = Image.open(arquivo)
        desenho = ImageDraw.Draw(imagem)
        texto = linhas_texto[i].strip()
        areas_texto = 3  # Número de áreas de texto

        cor_texto = (255, 255, 255)  # Branco
        cor_borda = (0, 0, 0)  # Preto
        tamanho_borda = 2

        largura_imagem, altura_imagem = imagem.size
        altura_area_texto = altura_imagem // areas_texto

        tamanho_max_fonte = 200
        tamanho_fonte = tamanho_max_fonte
        fonte = ImageFont.truetype("arial.ttf", tamanho_fonte)

        partes_texto = texto.split(",")
        num_partes = len(partes_texto)

        for j, parte_texto in enumerate(partes_texto):
            parte_texto = parte_texto.strip()

            while tamanho_fonte > 1:
                largura_texto, altura_texto = desenho.textsize(parte_texto, font=fonte)
                if largura_texto <= largura_imagem * 0.8 and altura_texto <= altura_area_texto * 0.8:
                    break
                tamanho_fonte -= 1
                fonte = ImageFont.truetype("arial.ttf", tamanho_fonte)

            pos_x = (largura_imagem - largura_texto) // 2
            pos_y = (altura_area_texto - altura_texto) // 2

            pos_y += j * altura_area_texto  # Ajusta a posição vertical para cada área de texto

            desenho.text((pos_x - tamanho_borda, pos_y), parte_texto, font=fonte, fill=cor_borda)
            desenho.text((pos_x + tamanho_borda, pos_y), parte_texto, font=fonte, fill=cor_borda)
            desenho.text((pos_x, pos_y - tamanho_borda), parte_texto, font=fonte, fill=cor_borda)
            desenho.text((pos_x, pos_y + tamanho_borda), parte_texto, font=fonte, fill=cor_borda)
            desenho.text((pos_x, pos_y), parte_texto, font=fonte, fill=cor_texto)

        imagem.save(arquivo)

        
# Caminho do arquivo de texto
arquivo_texto = "texto.txt"

# Caminho da pasta de imagens
pasta_imagens = os.getcwd()

# Ler o arquivo de texto
linhas_texto = ler_arquivo_texto(arquivo_texto)

# Ler a pasta de imagens
arquivos_imagens = ler_pasta_imagens(pasta_imagens)

# Recortar as imagens
recortar_imagens(arquivos_imagens)

# Adicionar texto às imagens
adicionar_texto_imagens(arquivos_imagens, linhas_texto)


# In[ ]:





# In[ ]:




