# Stract
Stract API - Processo seletivo

Este projeto é um servidor Flask que consome uma API de dados de anúncios e gera relatórios em formato CSV. Ele foi desenvolvido como parte do processo seletivo da Stract.

## Requisitos

Python 3.9 ou superior.
Bibliotecas: Flask, requests.

## Instalação

Siga os passos abaixo para configurar e executar o projeto:

1. Clone o repositório

```bash
git clone https://github.com/GirardiMatheus/Stract.git
cd Stract
```
2. Crie e ative o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```
3. Instale as dependências

```bash
pip install -r requirements.txt
```
## Executando o Projeto

1. Inicie o servidor Flask

```bash
python3 run.py
```
O servidor estará disponível em http://127.0.0.1:5000.


## Endpoints Disponíveis

1. Raiz (/)

Retorna informações sobre o desenvolvedor.
Exemplo de resposta:
```json

{
    "name": "Matheus Girardi",
    "email": "girardimatheus27@gmail.com",
    "linkedin": "https://www.linkedin.com/in/matheus-girardi-4857581a8/"
}
```
2. Anúncios por Plataforma (/<plataforma>)

Retorna todos os anúncios de uma plataforma específica.
Exemplo de uso:
```bash
curl http://loc127.0.0.1:5000/meta_ads
```
Saída: Um CSV com os anúncios da plataforma.

3. Resumo por Plataforma (/<plataforma>/resumo)

Retorna um resumo dos anúncios de uma plataforma, agregado por conta.
Exemplo de uso:
```bash
curl http://127.0.0.1:5000/meta_ads/resumo
```
Saída: Um CSV com o resumo por conta.
4. Todos os Anúncios (/geral)

Retorna todos os anúncios de todas as plataformas.
Exemplo de uso:
```bash
curl http://127.0.0.1:5000/geral
```
Saída: Um CSV com todos os anúncios.
5. Resumo Geral (/geral/resumo)

Retorna um resumo consolidado de todas as plataformas.
Exemplo de uso:
```bash
curl http://127.0.0.1:5000/geral/resumo
```
Saída: Um CSV com o resumo por plataforma.
## Estrutura do Projeto

```
/Stract
│
├── app/
│   ├── __init__.py          # Inicialização do Flask
│   ├── routes.py            # Definição dos endpoints
│   ├── api.py               # Lógica para chamadas à API
│   └── utils.py             # Funções utilitárias
│
├── run.py                   # Script para iniciar o servidor
├── .gitignore               # Arquivos e pastas ignoradas pelo Git
├── requirements.txt         # Dependências do projeto
└── README.md                # Documentação do projeto
```
## Parando o Servidor

Para parar o servidor, pressione Ctrl + C no terminal onde ele está sendo executado.

## Contato

Se tiver dúvidas ou sugestões, entre em contato:

Nome: Matheus Girardi
E-mail: girardimatheus27@gmail.com
LinkedIn: [Matheus Girardi](https://www.linkedin.com/feed/)
