# Get-hotel-rooms-API 🏨📊

Uma API Flask leve, rápida e otimizada para raspagem de dados de tarifas e disponibilidade de quartos diretamente do motor de reservas da **Omnibees**.

Este projeto foi desenvolvido com foco em baixo consumo de recursos, ideal para integrações com agentes de IA (como no n8n) ou sistemas de automação de orçamentos em tempo real.

---

## 🚀 Diferencial Técnico: Otimização Sem Selenium

A versão inicial deste projeto utilizava **Selenium WebDriver** para renderização do conteúdo. Mas para garantir planos de hospedagem gratuitos e tempo de resposta mais rápido para assistentes de IA, o projeto foi refatorado para usar **Scraping Direto** com as bibliotecas `requests` e `BeautifulSoup4`.

### Comparativo Técnico (Dados Reais medidos em ambiente local):

| Métrica                        |          Com Selenium WebDriver           |        Requests + BS4 (Atual)        |
| :----------------------------- | :---------------------------------------: | :----------------------------------: |
| **Tempo de Resposta (Médio)**  |              ~6 a 8 segundos              |         **1.01 segundos** ⚡         |
| **Consumo de RAM**             |              ~150MB - 300MB               |              **< 30MB**              |
| **Manutenção / Estabilidade**  | Baixa (Quebra com atualizações do Chrome) | **Alta (Independente de navegador)** |
| **Compatibilidade Cloud Free** | Instável (Estoura limite de RAM de 512MB) | **100% Estável (Leve e otimizado)**  |

> 💡 **Nota de Engenharia:** Durante a fase de testes, o Selenium apresentou falha crítica de execução (`SessionNotCreatedException`) devido à atualização automática do navegador Chrome local para a versão 149, enquanto o Driver estava na versão 142. Este problema clássico de incompatibilidade de ambiente foi completamente eliminado com a refatoração para requisições HTTP puras.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.13**
- **Flask**: Micro-framework para criação das rotas da API.
- **Flask-CORS**: Liberação de acessos para requisições vindas do front-end.
- **BeautifulSoup4**: Parseamento e extração de dados do HTML.
- **Requests**: Requisições HTTP rápidas simulando um usuário real.
- **Gunicorn**: Servidor WSGI robusto para o ambiente de produção.

---

## ⚙️ Como Executar o Projeto Localmente

### Pré-requisitos

Certifique-se de ter o Python instalado em sua máquina.

1. **Clone o repositório:**

   ```bash
    git clone [https://github.com/HeitorBackes/Get-hotel-rooms-API.git](https://github.com/HeitorBackes/Get-hotel-rooms-API.git)
    cd Get-hotel-rooms-API
   ```

2. Crie e ative um ambiente virtual (recomendado):

   ```bash
    python -m venv venv

    # No Windows (PowerShell):
    .\venv\Scripts\Activate.ps1

    # No Windows (Prompt de Comando):
    venv\Scripts\activate

    # No Linux/macOS:
    source venv/bin/activate
   ```

3. Instale as dependências:

   ```bash
    pip install -r requirements.txt
   ```

4. Inicie o servidor local:

   ```bash
    python app.py
   ```

O servidor iniciará localmente no endereço: http://localhost:5000

## 📊 Executando o Benchmark de Performance

Se quiser validar a diferença de performance e velocidade na sua própria máquina, você pode rodar o script de testes isolado que compara os métodos:

1. Instale a biblioteca `psutil` (opcional, apenas para exibir o consumo exato de memória RAM do processo no terminal):

   ```bash
    pip install psutil
   ```

2. Execute o script de benchmark:
   ```bash
    python benchmark.py
   ```
   (Nota: O script é inteligente. Se você não possuir o `chromedriver.exe` configurado na raiz da pasta, ele executará o teste com requests de forma limpa e exibirá um aviso amigável no console sobre o Selenium).

## 🔌 Documentação da API

1. Verificar Status do Servidor
   Verifica se a API está online e respondendo adequadamente.

- Rota: /
- Método: GET
- Resposta de Sucesso (HTTP 200):

  ```JSON
  "Servidor de raspagem de dados está online e otimizado!"
  ```

### 2. Buscar Dados de Quartos e Preços

Acessa o motor de reservas do hotel e retorna a lista de quartos e tarifas ativas.

- **Rota:** `/get_room_data`
- **Método:** `GET`
- **Parâmetros de Consulta (Query Params):**

| Parâmetro      |   Tipo    | Obrigatório | Descrição                                 | Exemplo    |
| :------------- | :-------: | :---------: | :---------------------------------------- | :--------- |
| `unidade`      | _string_  |     Sim     | ID de identificação do hotel na Omnibees. | `8221`     |
| `dataCheckIn`  | _string_  |     Sim     | Data de entrada no formato (DDMMAAAA).    | `15082026` |
| `dataCheckOut` | _string_  |     Sim     | Data de saída no formato (DDMMAAAA).      | `18082026` |
| `numGuests`    | _integer_ |     Sim     | Quantidade total de hóspedes.             | `2`        |

- Exemplo de Requisição Local:

  ```HTTP
  GET http://localhost:5000/get_room_data?unidade=8221&dataCheckIn=15082026&dataCheckOut=18082026&numGuests=2
  ```

- Resposta de Sucesso (HTTP 200):

  ```JSON
  {
    "status": "success",
    "room_data": {
      "Suíte Standard Casal": "R$ 350,00",
      "Apartamento Luxo Família": "R$ 520,00",
      "Suíte Master com Hidro": "R$ 780,00"
    }
  }
  ```

- Resposta de Erro - Parâmetros Ausentes (HTTP 400):

  ```JSON
  {
    "status": "error",
    "message": "Parâmetros \"unidade\", \"dataCheckIn\", \"dataCheckOut\" e \"numGuests\" são obrigatórios."
  }
  ```
