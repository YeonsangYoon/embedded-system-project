from flask import Flask, request
import argparse
from hx711 import HX711

# 디버그 모드 명령행 인자 설정 
parser = argparse.ArgumentParser()
parser.add_argument('--debug', dest = 'debug', action = 'store_true')
args = parser.parse_args()
debug = args.debug

app = Flask(__name__)

LC_DT_Pin = 8   #24 / 8
LC_SCK_Pin = 11 #23 / 11

@app.route('/')
def index():
    return 'OK'

@app.route('/avgweight', methods = ['POST'])
def get_avg_weight():
	w = hx7111.get_raw_data(10)
    
	return sum(w) / len(w)



if __name__ == '__main__':
    # Load Cell GPIO setting
	GPIO.setwarnings(False)
	hx711 = HX711(LC_DT_Pin, LC_SCK_Pin)
	hx711.reset()

    app.run(host='0.0.0.0', threaded=False, debug=False, port=5000)
