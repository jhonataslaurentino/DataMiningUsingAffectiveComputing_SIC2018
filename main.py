import nltk
import csv
#nltk.download()
nltk.download('stopwords')
nltk.download('rslp')
base = []
basetreinamento = []
baseteste = []

with open("base.csv") as arquivocsv:
    ler = csv.reader(arquivocsv, delimiter=",")
    for linha in ler:
        base.append(linha[0])

with open("base_treino.csv") as arquivocsv:
    ler = csv.reader(arquivocsv, delimiter=",")
    for frase, classe in ler:
        basetreinamento.append((frase,classe))

with open("base_teste.csv") as arquivocsv:
    ler = csv.reader(arquivocsv, delimiter=",")
    for frase, classe in ler:
        baseteste.append((frase,classe))


stopWordsNLTK = nltk.corpus.stopwords.words('portuguese')
#print(stopWordsNLTK)

#Deixa apenas o radical e remove stopwords 
def aplicastemmer(texto):
    stemmer = nltk.stem.RSLPStemmer() #Blibioteca BR de Stemmer 
    frasessstemming = []
    for(palavras, emocao) in texto:
        constemming = [str(stemmer.stem(p)) for p in palavras.split() if p not in stopWordsNLTK]
        frasessstemming.append((constemming, emocao))
    return frasessstemming

frasesComStemming =  aplicastemmer(basetreinamento)
#print(frasesComStemming)
frasesComStemmingTESTE = aplicastemmer(baseteste) #1

#Cria um vetor simples com todas as palavras da base de dados
def buscapalavas(frases):
    todasaspalavras = []
    for(palavras, emocao) in frases:
        todasaspalavras.extend(palavras)
    return todasaspalavras

palavras = buscapalavas(frasesComStemming)
#print(palavras)
palavrasTESTE = buscapalavas(frasesComStemmingTESTE) #2

#Elimina palavras repetidas

def buscafrequencia(palavras):
    palavras= nltk.FreqDist(palavras)
    return palavras

frequencia = buscafrequencia(palavras)
#print(frequencia.most_common(10))
frequenciaTESTE = buscafrequencia(palavrasTESTE) #3

def buscapalavrasunicas(frequencia):
    freq = frequencia.keys()
    return freq
#Todas as variações de palavras na base sem repetição
palavrasunicas = buscapalavrasunicas(frequencia)
#print(palavrasunicas)
palavrasunicasTESTE = buscapalavrasunicas(frequenciaTESTE) #4

#Função que dada uma determinada frase ela diz quais palavras dessa frase existem na base

def extratorpalavras(documento):
    doc = set(documento)
    caracteristicas = {}
    for palavras in palavrasunicas:
        caracteristicas['%s' % palavras] = (palavras in doc)
    return caracteristicas


#Base completa é utilizada para treinamento na aprendizagem de máquina
basecompleta = nltk.classify.apply_features(extratorpalavras, frasesComStemming)
#print(basecompleta)

basecompletaTESTE = nltk.classify.apply_features(extratorpalavras, frasesComStemmingTESTE) #5


'''______________TABELA DE PROBABILIDADE____________'''

classificador = nltk.NaiveBayesClassifier.train(basecompleta)
#print(classificador.labels())

#Palavras mais determinantes
#print(classificador.show_most_informative_features(10))

#TESTA A ACURACIA DO ALGORITIMO PARA A BASE
print("Acuracia: ",nltk.classify.accuracy(classificador,basecompletaTESTE))


'''______________MATRIZ____________'''
from nltk.metrics import ConfusionMatrix
esperado =[]
previsto =[]
for(frase, classe) in basecompletaTESTE:
    resultado = classificador.classify(frase)
    previsto.append(resultado)
    esperado.append(classe)
    
matriz = ConfusionMatrix(esperado,previsto)
print(matriz)


'''______________TESTANDO FRASE ____________'''
teste = 'Triste época! É mais fácil desintegrar um átomo do que um preconceito' #Albert Einstein
testestemming = []
stemmer = nltk.stem.RSLPStemmer()

for (palavras) in teste.split():
    comstemming = [p for p in palavras.split()]
    testestemming.append(str(stemmer.stem(comstemming[0])))

novo = extratorpalavras(testestemming)
#print("O sentimento da frase é de: ", classificador.classify(novo))



