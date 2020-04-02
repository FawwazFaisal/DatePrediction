from datetime import datetime
import numpy as np
import flask
import pickle


app = flask.Flask(__name__)
app.config["DEBUG"] = True

model = pickle.load(open("PredictModel.sav", 'rb'))
def floatHourToTime(fh):
    h, r = divmod(fh, 1)
    m, r = divmod(r*60, 1)
    return (int(h),int(m),int(r*60))
def predict(dmc_name,date):
	dmc_name = np.float(dmc_name)
	date = np.float(date)
	result = model.predict(np.array([[dmc_name,date]]))
	

	result_date = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(result) - 2)
	input_date = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(date) - 2)
	hour, minute, second = floatHourToTime(result % 1)
	hour, minute, second = floatHourToTime(date % 1)
	result_date = result_date.replace(hour=hour, minute=minute, second=second)
	input_date = input_date.replace(hour=hour, minute=minute, second=second)
	final_result ="Complaint Launched on: "+ str(input_date)+" will be resolved on: "+str(result_date)
	return final_result

@app.route('/prediction', methods=['GET','POST'])
def prediction():

    res = predict(flask.request.args.get("dmc_name"), flask.request.args.get("date"))
    return res

if __name__ == "__main__":
    app.run(use_reloader=False, port = 5005)