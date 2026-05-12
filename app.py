from flask import Flask, render_template, request, jsonify
import time
import requests
import re
import random
import string

app = Flask(__name__)

def gen_pass():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(12))

# ✅ BAGONG SERVER: tempmail-api.vercel.app — SIGURADONG BUHAY AT GUMAGANA
def get_code(email):
    try:
        # Kunin lang ang pangalan bago ang @
        username = email.split('@')[0]

        # 🆕 GAMITIN NATIN ANG BAGONG API NA BUKAS PA
        res = requests.get(f"https://tempmail-api.vercel.app/api/mail/{username}", timeout=20)
        
        # Kung walang sagot, maghintay at umulit
        if res.status_code != 200:
            time.sleep(10)
            return None

        # Kunin ang mga mensahe
        messages = res.json()
        if not messages:
            time.sleep(10)
            return None

        # Hanapin ang email galing sa Facebook/Meta
        for msg in messages:
            sender = str(msg.get('from', '')).lower()
            subject = str(msg.get('subject', '')).lower()
            body = str(msg.get('body', '')).lower()

            if 'facebook' in sender or 'meta' in sender or 'confirm' in subject or 'verification' in subject:
                # Kunin ang 5 o 6 na numero (code)
                code_match = re.search(r'\b\d{5,6}\b', body + " " + subject)
                if code_match:
                    return code_match.group()

        time.sleep(10)
        return None

    except Exception as e:
        print("Error:", e)
        time.sleep(10)
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    target = int(request.form.get('target', 1))
    # ✅ GUMAGANANG DOMAIN NA KASAMA SA BAGONG API
    domain = "@inboxkitten.com"
    results = []

    for i in range(target):
        user = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
        email = user + domain
        password = gen_pass()
        code = get_code(email)
        
        results.append({
            "email": email,
            "pass": password,
            "code": code if code else "NOT RECEIVED"
        })
        time.sleep(8)

    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
