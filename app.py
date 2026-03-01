from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

NEBULA_WEBHOOK_URL = 'https://api.nebula.gg/webhooks/triggers/trig_069a389a03497ff9800052fc1d320c08/webhook'
NEBULA_SECRET = '609316a5-483e-4bfd-ad39-8a4b2b8913f4'

@app.route('/webhook', methods=['POST'])
def webhook_proxy():
    body = request.get_data()
    headers = {
        'Content-Type': 'application/json',
        'X-Webhook-Secret': NEBULA_SECRET
    }
    cb_signature = request.headers.get('X-CC-Webhook-Signature')
    if cb_signature:
        headers['X-CC-Webhook-Signature'] = cb_signature
    try:
        response = requests.post(NEBULA_WEBHOOK_URL, data=body, headers=headers, timeout=10)
        return Response(f'Forwarded to Nebula. Status: {response.status_code}', status=200)
    except Exception as e:
        return Response(f'Error: {str(e)}', status=500)

@app.route('/health', methods=['GET'])
def health():
    return {'status': 'ok', 'service': 'coinbase-nebula-proxy'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)