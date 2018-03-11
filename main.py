from flask import Flask
from flask import render_template
from flask import request
import re


app = Flask(__name__)

def get_freq_ips(ips_list):
    dict_ip = {}
    for ip in ips_list:
        dict_ip.setdefault(ip, 0)
        dict_ip[ip] += 1
    return dict_ip


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        f = request.files['file'].read()
        txt = str(f.decode('utf-8'))

        pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        ips = re.findall(pattern, txt)


        amount_str = request.form['amount']
        try:
            amount = int(amount_str) if amount_str != '' else len(ips)
        except ValueError:
            amount = len(ips)

        frequency_str = request.form['frequency']
        try:
            frequency = int(frequency_str) if frequency_str != '' else 100
        except ValueError:
            frequency = 100



        dict_ips = get_freq_ips(ips)
        result = sorted(dict_ips.items(), key=lambda x: x[1], reverse=True)[:amount]

        ban = []
        for key, value in result:
            if value >= frequency:
                ban.append({'ip': key, 'frequency': value})


        return render_template('index.html', ips=ban)
    return render_template('index.html')



if __name__ == '__main__':
    app.run()
