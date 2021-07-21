from flask import Flask, jsonify, render_template, request
import json
import pickle
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/companypage')
def cmp_page():


    data = pd.read_csv('static/data/list_interface_test.csv')
    firm_id = [1161049216, 1199729421, 160269670, 127671566, 1052240272, 1232004753, 1151775635, 789380757, 790724630,
               1160048160]
    data = data[data['entid'].isin(firm_id)]
    data = data.to_dict(orient='records')


    return jsonify(data=data)


@app.route('/risktypecount')
def risktypecount():

    df = pd.read_csv('static/data/label_risk_company.csv')
    data = df.CaseType.value_counts().reset_index()
    data.columns = ['riskType', 'companyNum']
    data = data.to_dict(orient='records')
    return jsonify(data=data)

@app.route('/industryrisk')
def industryrisk():

    df = pd.read_csv('static/data/industry_risk.csv')
    df.drop('Unnamed: 0', axis=1, inplace=True)
    data = df.sort_values(by="riskType").to_dict(orient='records')
    return jsonify(data=data)

@app.route('/relationship')
def relationship():

    target_firm = request.args.get('firm')
    with open('static/data/Relationship.pkl', 'rb') as fr:
        data = pickle.load(fr)
    target_data = data[int(target_firm)]

    return jsonify(data=target_data)

@app.route('/Radar')
def Radar():

    target_firm = request.args.get('firm')
    with open('static/data/Radar.pkl', 'rb') as fr:
        data = pickle.load(fr)
    target_data = data[int(target_firm)]

    return jsonify(data=target_data)


@app.route('/companyinfo')
def companyinfo():

    target_firm = request.args.get('firm')

    # 公司详情
    df = pd.read_csv('static/data/company_info.csv')
    df.set_index('entid', inplace=True)
    data = df.to_dict(orient='index')
    target_data = data[int(target_firm)]

    # 公司有无风险比例
    df_risk = pd.read_csv('static/data/risk_rate.csv')
    risk_firm = df_risk[df_risk['entid'] == int(target_firm)]
    risk_rate = round(risk_firm['4'].values[0], 4)

    # 公司风险类型比例
    category_rate_df = risk_firm[['rate_0', 'rate_1', 'rate_2', 'rate_3']].T.reset_index()
    category_rate_df.columns = ['type', 'value']
    category_rate_df['value'] = round(category_rate_df['value'], 4) * 100
    category_rate = category_rate_df.to_dict(orient='records')
    
    return_dic = {}
    return_dic['company'] = target_data
    return_dic['risk_rate'] = risk_rate
    return_dic['category_rate'] = category_rate
 # {"company":target_data,"risk_rate":risk_rate, "category_rate":category_rate}
    return jsonify(data=return_dic)
  #  return jsonify(data=target_data, risk_rate=risk_rate, category_rate=category_rate)

@app.route('/Subfactor')
def Subfactor():

    target_firm = request.args.get('firm')
    with open('static/data/subFactor.pkl', 'rb') as fr:
        data = pickle.load(fr)
    target_data = data[int(target_firm)]

    return jsonify(data=target_data)


@app.route('/focus')
def focus():

    data = pd.read_csv('static/data/focus_company.csv')
    data = data.sample(10).to_dict(orient='records')

    return jsonify(data=data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
