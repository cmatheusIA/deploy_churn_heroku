

from flask import Flask,request
import pickle
import pandas as pd
from processing.data_prep import Data_Prepared
#from parameter.data_prep import Data_Prepared



#load model
model = pickle.load(open('api_v1/rotas/models/churn_randomFlorest.pkl','rb'))
#/media/cmatheus/dadosProjetos/portfolio/Churn/api/api_v1/model/churn_randomFlorest.pkl


#instanciando o flask

app = Flask(__name__)



#criando endpoints;
@app.route('/',methods = ['GET'])
def index():
    return "<h1> Api funciona na rota /predict =D</h1>"


@app.route('/predict',methods=['POST'])
def predict():
    dados_json=request.get_json()
    #coletando os dados
    if dados_json:
        if isinstance(dados_json,dict):
            df_raw = pd.DataFrame(dados_json,index=[0])
        else:
            df_raw = pd.DataFrame(dados_json,columns=dados_json[0].keys() )
    #predict
    dp = Data_Prepared()
    
    df_prepared = dp.get_df_transform(df_raw)
    pred = model.predict(df_prepared)

    df_prepared['predicao_churn'] = pred

    return df_prepared.to_json(orient='records')



if __name__=='__main__':
    #start flask
    app.run(host='0.0.0.0', port='5000',debug=True)