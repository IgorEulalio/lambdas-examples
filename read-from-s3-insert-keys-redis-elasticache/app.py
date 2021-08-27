import json
from redis import Redis
import logging
def insere_produto_elasticache(produto):
    sistema = produto["sistema"] 
    codigo = produto["codigo"] 
    classe_ativo = produto["classe_ativo"] 
    indexadores = produto["indexador"]
    
    produto = {"sistema": sistema, "codigo": codigo,
               "classe_ativo": classe_ativo, "indexadores": indexadores} 
    json_produtos = json.dumps(produto) 
    produto_key = sistema + "@" + codigo 
    redis.set(produto_key, json_produtos)


logging.basicConfig(level=logging.INFO)
redis = redis = Redis(host='localhost', port=6379, decode_responses=True, ssl=False)

if redis.ping():
    # Logica para download do arquivo csv do S3 bucket
    logging.info("Connected to Redis")

file = open('src/resources/alpha_betas.json',)
data = json.load(file)

produtos = data['alfa_betas']

indexadores = data['indexadores']
indexadores_json = json.dumps(indexadores)

redis.set('indexadores', indexadores_json)
for produto in produtos:
    insere_produto_elasticache(produto)
