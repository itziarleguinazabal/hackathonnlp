import json
import sys

from os.path import join, dirname
from watson_developer_cloud import AlchemyLanguageV1
alchemy_language = AlchemyLanguageV1(api_key='1d6917c321063437a34fe0b8adbfbbfc0b0193b4')
reload(sys)
sys.setdefaultencoding('utf-8')

url = 'http://www.cuentosinfantilesadormir.com/cuento-pinocho.htm'
#url ='http://www.cuentosinfantilesadormir.com/cuento-bambi.htm'
#url ='http://www.cuentosinfantilesadormir.com/cuento-cenicienta.htm'
#url='http://www.childrenstory.info/childrenstories/pinocchio.html'
#print("TEXTO A ANALIZAR")
#print(json.dumps(alchemy_language.text(url=url),indent=2))


response = alchemy_language.entities(url=url)

print(response)

num_pers=1

print('')
print('PERSONAJES DEL TEXTO')
print('')
for entity in response['entities']:
    if float(entity['relevance']) > 0.3:
        print('Personaje ',num_pers,':' ,entity['text'])
        num_pers +=1
    else:
        print()

with open('data_personajes.txt', 'w') as outfile:
     json.dump(response, outfile, sort_keys = True, indent = 4, ensure_ascii=False)


print('')
print('CONCEPTOS DEL TEXTO')
print('')
response = alchemy_language.concepts(url=url)

num_concep=1
for concepto in response['concepts']:
    if float(concepto['relevance']) > 0.5:
        print('Concepto ',num_concep,':' ,concepto['text'].encode('utf-8').strip())
        num_concep +=1
    else:
        print()
print('')

with open('data_conceptos.txt', 'w') as outfile:
     json.dump(response, outfile, sort_keys = True, indent = 4, ensure_ascii=False)

#Extraer las principales relaciones del texto
print("RELACIONES EN EL TEXTO")
print('')
response=response=alchemy_language.relations(url=url, entities=1, require_entities=1)

with open('data_relaciones.txt', 'w') as outfile:
     json.dump(response, outfile, sort_keys = True, indent = 4, ensure_ascii=False)

num_rel=1
for relation in response['relations']:
        print('Relation ',num_rel,':',relation['subject']['text'].encode('utf-8').strip(),'->' ,relation['action']['text'].encode('utf-8').strip(),'->' ,relation['object']['text'].encode('utf-8').strip())
        num_rel +=1

print('')
#Extraer los principales sentimientos del texto
print("SENTIMENTOS EN EL TEXTO")
print('')
response=alchemy_language.sentiment(url=url)
if response['status'] == 'OK':
    print('SENTIMENTO :' ,response['type'].encode('utf-8').strip())
else:
    print('Error in sentiment analysis call ')

with open('data_sentimientos.txt', 'w') as outfile:
     json.dump(response, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
