# main.py
from fastapi import FastAPI, HTTPException
import requests
import os

app = FastAPI()

# Configuracao inicial da API TMDb (substitua por sua chave real)
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

@app.get("/filmes/{titulo}")
def buscar_filme(titulo: str):
    url = f"{TMDB_BASE_URL}/search/movie?query={titulo}&api_key={TMDB_API_KEY}&language=pt-BR"
    resposta = requests.get(url)

    if resposta.status_code != 200:
        raise HTTPException(status_code=404, detail="Filme nao encontrado")

    return resposta.json()

@app.get("/populares")
def filmes_populares():
    url = f"{TMDB_BASE_URL}/movie/popular?api_key={TMDB_API_KEY}&language=pt-BR"
    resposta = requests.get(url)

    if resposta.status_code != 200:
        raise HTTPException(status_code=404, detail="Nao foi possivel buscar filmes populares")

    return resposta.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
