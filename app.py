from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests
import os

app = Flask(__name__)
CORS(app)

# URL base do site de destino
BASE_URL = "https://book.omnibees.com/hotelresults?c=11362&version=4"

# Endpoint de teste para verificar se o servidor está online
@app.route('/')
def home():
    return "Servidor de raspagem de dados está online e otimizado!", 200

@app.route('/get_room_data', methods=['GET'])
def get_room_data():
    """
    Endpoint para raspar dados de quartos e preços de uma URL alvo de forma rápida.
    A raspagem é feita diretamente via requisição HTTP (requests) e parseada com BeautifulSoup.
    """

    # 1. Obter os parâmetros da consulta (query parameters) da URL
    unidade = request.args.get('unidade')
    dataCheckIn = request.args.get('dataCheckIn')
    dataCheckOut = request.args.get('dataCheckOut')
    numGuests = request.args.get('numGuests')

    # 2. Garantir que todos os parâmetros necessários foram fornecidos
    if not all([unidade, dataCheckIn, dataCheckOut, numGuests]):
        return jsonify({
            'status': 'error',
            'message': 'Parâmetros "unidade", "dataCheckIn", "dataCheckOut" e "numGuests" são obrigatórios.'
        }), 400

    # 3. Construir a URL alvo
    target_url = (
        f"{BASE_URL}&q={unidade}&CheckIn={dataCheckIn}&CheckOut={dataCheckOut}&ad={numGuests}"
    )

    # 4. Configurar Headers para evitar bloqueios
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        # Faz a requisição para a Omnibees
        response = requests.get(target_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return jsonify({
                'status': 'error',
                'message': f'Erro ao acessar o motor de reservas. Código HTTP: {response.status_code}'
            }), 502
            
        html_content = response.text

    except requests.exceptions.RequestException as e:
        return jsonify({
            'status': 'error',
            'message': f'Falha ao conectar com o servidor de destino: {str(e)}'
        }), 500

    # 5. Processar HTML com Beautiful Soup
    soup = BeautifulSoup(html_content, "html.parser")
    quartos = soup.find_all('p', {'class': 'room_name'})

    if not quartos:
        print(f"Aviso: Nenhuma tag 'p' com a classe 'room_name' encontrada para {target_url}.")
        return jsonify({
            'status': 'error', 
            'message': 'Nenhum quarto disponível ou parâmetros de busca incorretos.'
        }), 404

    room_data = {}
    for quarto in quartos:
        room_name = quarto.get_text(strip=True)
        price_element = quarto.find_next('span', {'class': 'price-total-bold'})
        
        if price_element:
            price = price_element.get_text(strip=True)
            room_data[room_name] = price
        else:
            print(f"Aviso: Preço não encontrado para o quarto: {room_name}")
            room_data[room_name] = "Preço não disponível"

    return jsonify({'status': 'success', 'room_data': room_data})

if __name__ == '__main__':
    # Configuração dinâmica de porta para rodar localmente ou na nuvem
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)