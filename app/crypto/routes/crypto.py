from fastapi import FastAPI, HTTPException
from fastapi import APIRouter
import time
import requests
from prometheus_client import generate_latest
from fastapi.responses import PlainTextResponse
from app.crypto.routes.decorador_monitor import monitor_instance

router = APIRouter()


@router.get("/crypto")
@monitor_instance.track
def get_crypto_data():
    """
    Endpoint para obter dados de preços de criptomoedas.
    """
    try:
        response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
        response.raise_for_status()
        data = response.json()
        return {
            "Bitcoin (USD)": data["bpi"]["USD"]["rate"],
            "Bitcoin (EUR)": data["bpi"]["EUR"]["rate"]
        }
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail="Erro ao buscar dados da API externa")


@router.get("/crypto/history/{currency}")
@monitor_instance.track
def get_crypto_history(currency: str):
    try:
        response = requests.get(f"https://api.coingecko.com/api/v3/coins/{currency}/market_chart",
                                params={"vs_currency": "usd", "days": 7})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail="Erro ao buscar histórico de preços")


@router.get("/convert")
@monitor_instance.track
def convert_currency(amount: float, from_currency: str, to_currency: str):
    try:
        response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{from_currency}")
        response.raise_for_status()
        rates = response.json().get("rates", {})
        if to_currency not in rates:
            raise HTTPException(status_code=400, detail="Moeda de destino inválida")
        converted_amount = amount * rates[to_currency]
        return {"converted_amount": converted_amount}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail="Erro ao buscar taxa de câmbio")

@router.get("/slow-request")
@monitor_instance.track
def slow_request():
    time.sleep(5)  # Simula um atraso de 5 segundos
    return {"status": "processed"}