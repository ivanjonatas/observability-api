# Monitoramento de API com Prometheus e OpenTelemetry 🚀

Este projeto é uma aplicação de exemplo desenvolvida em **FastAPI** que implementa práticas de **monitoramento e observabilidade** utilizando **Prometheus, Grafana e OpenTelemetry**.  

A aplicação simula endpoints de uma API e coleta métricas como latência, contagem de requisições e rastreamento (tracing) distribuído.  

---

## 🎯 Objetivo
Fornecer um ambiente para aprendizado e prática de técnicas de observabilidade, ajudando desenvolvedores a instrumentar APIs, coletar métricas, configurar tracing e criar dashboards no Grafana.  

---

## 🛠️ Tecnologias Utilizadas
- **FastAPI** - Framework Python para desenvolvimento de APIs rápidas e eficientes.  
- **Prometheus** - Coleta de métricas e monitoramento.  
- **Grafana** - Visualização de métricas e criação de dashboards.  
- **OpenTelemetry** - Tracing distribuído e instrumentação de serviços.  
- **Uvicorn** - Servidor ASGI para execução da API.  
- **Requests** - Biblioteca para consumo de APIs externas.  
- **Docker e Docker Compose** - Para facilitar a execução do Prometheus e Grafana.  

---

## ⚙️ Funcionalidades
- 📊 **Exposição de Métricas** no formato Prometheus.  
- ⏱️ **Coleta de Latência** de requisições.  
- 🧩 **Tracing distribuído** com OpenTelemetry.  
- 🚦 **Health Check Endpoint** para verificação do status da API.  
- 📡 **Dashboard no Grafana** para visualização de métricas em tempo real.  