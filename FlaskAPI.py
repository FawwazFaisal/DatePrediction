from datetime import datetime
import datetime as dt
import numpy as np
import flask
import pickle


app = flask.Flask(__name__)
app.config["DEBUG"] = True

model = pickle.load(open("NewPredictModel.sav", 'rb'))

def predict(type, dmc_name):
	dmc_name = np.float(dmc_name)
	type = np.float(type)
	input_date = np.float(((dt.date.today().toordinal()-datetime(1900,1,1).toordinal())))
	output_date = model.predict(np.array([[type,dmc_name,input_date]]))
	
	output_date = datetime.fromordinal(datetime(1900,1,1).toordinal()+ int(output_date[0]))

	output_date =str(output_date.date()).split("-")
	output_date.reverse()
	final_result = "/".join(output_date)

	return final_result

@app.route('/prediction', methods=['GET','POST'])
def prediction():
	type = flask.request.args.get("type")
	dmc_name = flask.request.args.get("dmc_name")
	res = predict(type, dmc_name)
	return res

if __name__ == "__main__":
    app.run(use_reloader=False, port = 5005)