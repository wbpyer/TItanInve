from flask import Flask, send_file, request

from flask_cors import CORS
from logic import start_train
import numpy as np

app = Flask(__name__)


CORS(app, supports_credentials=True)

@app.route('/get-capital-curve')
def get_capital_curve():
    return send_file( './plot_None.png',  as_attachment=True)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

@app.route('/start-train', methods=['POST'])
def start_training():
    #从请求中获取数据
    data = request.json
    stocks = data['stocks']
    algorithm = data['algorithm']
    start_time = data['start_time']
    end_time = data['end_time']
    tradestart = data['tradestart']
    tradeend = data['tradeend']
    print (start_time,end_time,algorithm,stocks,tradestart,tradeend)
    result = start_train(stocks,start_time,end_time,tradestart,tradeend)
    
    result[0].replace([np.inf, -np.inf], "test", inplace=True)
    result[0].replace(np.nan, "test", inplace=True)

    result[1].replace([np.inf, -np.inf], "test", inplace=True)
    result[1].replace(np.nan, "test", inplace=True)

    res1 = result[0].to_dict()
    res2 = result[1].to_dict()  

    print(res1)
    print(res2)
    res_new1 = {}
    res_new2 = {}

    for k,v in res1.items():

        if is_number(v):
            v = round(float(v),3)
            res_new1[k] = v
        else:
            res_new1[k] = "test"
               
    for k,v in res2.items():
        

        if is_number(v):
            v = round(float(v),3)
            res_new2[k] = v 
        else:
            res_new2[k] = "test"


    res = {"DDPG": res_new1, "A2C": res_new2}
    

    print(res)
    return res




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000,debug=True)