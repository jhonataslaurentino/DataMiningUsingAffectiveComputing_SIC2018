import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import csv
import nltk

dados=[]
'''Leitura dos dados das tabelas CSV'''
with open("base_treino_limpa.csv") as arquivocsv:
    ler = csv.reader(arquivocsv, delimiter=",")
    for linha in ler:
        dados.append(linha[0])
        

''' Cria a nuvem de palavras '''
wordcloud = WordCloud(max_font_size=100,width = 1520, height = 535).generate(str(dados))
plt.figure(figsize=(16,9))
fig1 = plt.gcf()
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
fig1.savefig('Nuvem_Oficina_limpa.png', dpi=100)
