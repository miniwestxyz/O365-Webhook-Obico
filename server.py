from flask import Flask, request, jsonify
import requests
import logging

# Change here the URL to your Webhook for O365
WEBHOOKURL = "fisch.com"

app = Flask(__name__)

# Enter your Allowed IPs that can access this here. 
ALLOWED_IP = '1.1.1.1' 

def create_teams_message_card(event_type, data):
    if event_type == 'PrintStarted':
        filename = data.get('print', {}).get('filename', '')
        name = data.get('printer', {}).get('name', '')

        return {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "0078D7",
            "summary": "Started",
            "sections": [
                {
                    "activityTitle": "Druckauftrag Gestarted",
                    "activitySubtitle": "Obico for Octoprint",
                    "activityImage": "https://cdn-icons-png.flaticon.com/512/189/189664.png",  
                    "facts": [
                        {"name": "Drucker Name", "value": name},
                        {"name": "Dateiname", "value": filename}
                    ],
                }
            ]
        }

    elif event_type == 'PrintFailure':
        filename = data.get('print', {}).get('filename', '')
        name = data.get('printer', {}).get('name', '')

        return {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "0078D7",
            "summary": "Failure",
            "sections": [
                {
                    "activityTitle": "Fehler im Druck festgestellt.",
                    "activitySubtitle": "Obico for Octoprint",
                    "activityImage": "https://cdn2.iconfinder.com/data/icons/picons-basic-2/57/basic2-085_warning_attention-64.png",  # Ersetzen Sie dies durch eine geeignete URL
                    "facts": [
                        {"name": "Drucker Name", "value": name},
                        {"name": "Datei", "value": filename}
                    ],
                }
            ]
        }

    elif event_type == 'PrintDone':
        filename = data.get('print', {}).get('filename', '')
        name = data.get('printer', {}).get('name', '')

        return {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "0078D7",
            "summary": "Done",
            "sections": [
                {
                    "activityTitle": "Druck abgeschlossen",
                    "activitySubtitle": "Obico for Octoprint",
                    "activityImage": "https://cdn3.iconfinder.com/data/icons/basic-ui-6/38/Asset_60-64.png",  # Ersetzen Sie dies durch eine geeignete URL
                    "facts": [
                        {"name": "Druckername", "value": name},
                        {"name": "Datei", "value": filename}
                    ],
                }
            ]
        }

    else:
        return None


@app.route('/webhook', methods=['POST'])
def handle_webhook():
    requester_ip = request.remote_addr
    if requester_ip != ALLOWED_IP:
        return jsonify({'error': 'Unauthorized IP address'}), 403

    try:
        data = request.get_json()

        if 'event' not in data or 'type' not in data['event']:
            return jsonify({'error': 'Missing key "event" or "type" in JSON data'}), 400

        event_type = data['event']['type']
        teams_message_card = create_teams_message_card(event_type, data)

        if teams_message_card:
            webhook_url = WEBHOOKURL
            # An die Teams URL den Code ausführen um eine Nachrticht zu senden
            requests.post(webhook_url, json=teams_message_card)  # Versenden der Teams-Nachricht (hier müsstest du evtl. noch Anpassungen für eine erfolgreiche Übermittlung an Teams vornehmen)

        return 'OK', 200  # Erfolgreiche Verarbeitung

    except Exception as e:
        logging.error("An error occurred while processing the webhook data: %s", e)  
        return jsonify({'error': 'Error processing webhook data'}), 500  

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=25600, debug=False) 
