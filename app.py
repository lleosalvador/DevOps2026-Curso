from fastapi import FastAPI
from datetime import datetime
import requests

APP = FastAPI()
TAREFAS = []

""" 
{
    "id" -> int,
    "titulo" -> str,
    "descricao" -> str,
    "concluida" -> bool,
    "criada_em" -> datetime
}
"""

def criar_tarefa(titulo, descricao):
    return {
        "id": len(TAREFAS),
        "titulo": titulo,
        "descricao": descricao,
        "concluida": False,
        "criada_em": datetime.now().isoformat(timespec="seconds")
    }

@APP.get("/tarefas")
async def tarefas():
    lista_somente_id_titulo = []

    for tarefa in TAREFAS:
        id_tarefa = tarefa['id']
        titulo_tarefa = tarefa['titulo']

        lista_somente_id_titulo.append({id_tarefa: titulo_tarefa})

    return lista_somente_id_titulo

@APP.post("/tarefas", status_code=201)
async def post_tarefa(titulo: str, descricao: str):
    global TAREFAS

    tarefa_nova = criar_tarefa(titulo, descricao)

    TAREFAS.append(tarefa_nova)

    return {"mensagem": "OK"}

@APP.get("/tarefas/{id}")
async def tarefa_especifica(id: int):

    for tarefa in TAREFAS:
        if id == int(tarefa["id"]):
            return tarefa

    return {"mensagem": "Tarefa não existe"}

@APP.put("/tarefas/{id}")
async def concluir_tarefa(id: int):
    for tarefa in TAREFAS:
        if id == int(tarefa['id']) and tarefa['concluida'] == False:
            tarefa['concluida'] = True
            tarefa['concluida_em'] = datetime.now().isoformat(timespec='seconds')
            titulo = tarefa['titulo']

            try:
                resp = requests.post(
                    f"http://localhost:8000/notificar?id={id}&titulo={titulo}",
                    timeout=1
                    )
                print(resp)
            except Exception as e:
                print(e)
            return {"mensagem": "Tarefa atualizada"}
    return {"mensagem": "Tarefa não existe"}

@APP.delete("/tarefas/{id}")
async def apagar_tarefa(id: int):

    global TAREFAS

    indice = 0
    for tarefa in TAREFAS:
        if id == int(tarefa['id']):
            TAREFAS.pop(indice)
            return {"mensagem": "Tarefa apagada"}

        indice += 1
    return {"mensagem": "Tarefa não existe"}

@APP.get("/")
async def index():
    return {"mensagem": "Olá, mundo!"}
