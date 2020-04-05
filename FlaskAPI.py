from datetime import datetime
import numpy as np
import flask
import pickle


app = flask.Flask(__name__)
app.config["DEBUG"] = True

model = pickle.load(open("PredictModel.sav", 'rb'))

def predict(dmc_name):
	dmc_name = np.float(dmc_name)
	input_date = np.float(((dt.date.today().toordinal()-datetime(1900,1,1).toordinal())))
	output_date = model.predict(np.array([[dmc_name,input_date]]))

	output_date = datetime.fromordinal(datetime(1900,1,1).toordinal()+ int(output_date[0]))

	output_date =str(output_date.date()).split("-")
	output_date.reverse()
	final_result = "/".join(output_date)

	return final_result

@app.route('/prediction', methods=['GET','POST'])
def prediction():

    res = predict(flask.request.args.get("dmc_name"))
    return res

if __name__ == "__main__":
    app.run(use_reloader=False, port = 5005)