""" Aplicação para o módulo de extensão DevOps """

from datetime import datetime
from fastapi import FastAPI
from app.modelo import Tarefa
import requests
from requests.exceptions import ConnectionError as RequestConnectionError

APP = FastAPI()
TAREFAS = []

@APP.get("/tarefas")
async def tarefas():
    """ Rota para listar as tarefas. """
    lista_somente_id_titulo = []

    for tarefa in TAREFAS:
        id_tarefa = tarefa.id
        titulo_tarefa = tarefa.titulo

        lista_somente_id_titulo.append({id_tarefa: titulo_tarefa})

    return lista_somente_id_titulo

@APP.post("/tarefas", status_code=201)
async def post_tarefa(titulo: str, descricao: str):
    """ Rota para criar uma tarefa. """
    tarefa_nova = Tarefa(id=len(TAREFAS), titulo=titulo, descricao=descricao, data_criacao=datetime.now().isoformat(timespec='seconds'))

    TAREFAS.append(tarefa_nova)

    return {"mensagem": "OK"}

@APP.get("/tarefas/{id_tarefa}")
async def tarefa_especifica(id_tarefa: int):
    """ Rota para visualizar uma tarefa específica """

    for tarefa in TAREFAS:
        if id_tarefa == tarefa.id:
            return tarefa

    return {"mensagem": "Tarefa não existe"}

@APP.put("/tarefas/{id_tarefa}")
async def concluir_tarefa(id_tarefa: int):
    """ Rota para concluir uma tarefa. """

    for tarefa in TAREFAS:
        if id_tarefa == tarefa.id and tarefa.concluida is False:
            tarefa.finalizar()
            titulo = tarefa.titulo

            try:
                _ = requests.post(
                    f"http://localhost:8000/notificar?id={id}&titulo={titulo}",
                    timeout=1
                )
            except RequestConnectionError as e:
                print(e)

            return {"mensagem": "Tarefa atualizada"}

    return {"mensagem": "Tarefa não existe"}

@APP.delete("/tarefas/{id_tarefa}")
async def apagar_tarefa(id_tarefa: int):
    """ Rota para apagar tarefa. """

    indice = 0
    for tarefa in TAREFAS:
        if id_tarefa == tarefa.id:
            TAREFAS.pop(indice)
            return {"mensagem": "Tarefa apagada"}

        indice += 1

    return {"mensagem": "Tarefa não existe"}

@APP.get("/")
async def index():
    """ Rota raíz. """
    return {"mensagem": "Olá, mundo!"}

@APP.get("/autor")
async def autor():
    """ Rota para retornar o nome do autor da API. """
    return {"mensagem": "Leonardo Salvador"}
