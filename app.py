from flask import Flask, request, render_template, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/buscar", methods=["POST"])
def buscar_veiculo():
    placa = request.form.get("placa")

    if not placa:
        return jsonify({"erro": "Por favor, insira uma placa válida."}), 400

    url = f"https://www.ipvabr.com.br/placa/{placa}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extraia informações desejadas (exemplo: título ou meta description)
            title = soup.title.string if soup.title else "Título não encontrado"
            vehicle_info = soup.find("meta", attrs={"property": "og:description"})
            vehicle_description = vehicle_info["content"] if vehicle_info else "Informações não encontradas."

            return jsonify({"title": title, "description": vehicle_description})
        else:
            return jsonify({"erro": f"Erro ao buscar informações: {response.status_code}"}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"erro": f"Erro na requisição: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
