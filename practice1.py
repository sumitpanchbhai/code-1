from flask import Flask,jsonify,request
import pandas as pd

from conn import *
from practice3 import connection

app = Flask(__name__)

db_object = connection()

@app.route('/energy_consumption')
def energy_consumption():
    if request.args.get("customer_id"):
        customer = request.args.get("customer_id")
    else:
        customer = None
    if request.args.get("machine_id"):
        machine = request.args.get("machine_id")
    else:
        machine = None
    if request.args.get("startdate"):
        startdate = request.args.get("startdate")
    else:
        startdate = None
    if request.args.get("enddate"):
        enddate = request.args.get("enddate")
    else:
        enddate = None
    print("customer",customer)
    print("machine",machine)
    print("startdate",startdate)
    print("enddate",enddate)
    new_df = db_object.my_connection(machine=machine,customer=customer,startdate=startdate,enddate=enddate)
    # df = pd.read_csv('C:/Users/sumit/OneDrive/Desktop/TRILAB_EM.csv')
    # new_df = df[['TS', 'Total_kW', 'kWh']]
    lst = []
    for i in new_df['Total_kW']:
        if i < 10:
            lst.append('Level_1')
        elif i > 10 and i < 15:
            lst.append('Level_2')
        elif i > 15:
            lst.append('Leve_3')

    status = {'state': lst}
    new_df_1 = pd.DataFrame(status)
    result = pd.concat([new_df, new_df_1], axis=1)

    # Total_kW_raw = new_df['Total_kW'].values.tolist()
    no_time_change = []
    no_kwh_change = []
    no_change_state = []

    first = result['state'][0]
    first_TS = result['TS'][0]
    first_kwh = result['kWh'][0]
    for i in result.index:
        if result['state'][i] != first:
            # for no change state
            no_change_state.append(first)
            no_time_change.append(result['TS'][i - 1] - first_TS)
            no_kwh_change.append(result['kWh'][i - 1] - first_kwh)

            first = result['state'][i]
            first_TS = result['TS'][i]
            first_kwh = result['kWh'][i]

    no_change = pd.DataFrame(list(zip(no_kwh_change, no_time_change, no_change_state))
                                 , columns=['kWh', 'TS', 'state'])

    level_2 = []
    level_3 = []
    level_1 = []
    for i in no_change.index:
        if no_change['state'][i] == 'Level_2':
            level_2.append(round(no_change['kWh'][i], 2))
        elif no_change['state'][i] == 'Leve_3':
            level_3.append(round(no_change['kWh'][i], 2))
        else:
            level_1.append(round(no_change['kWh'][i], 2))

    def Average(lst):
        return sum(lst) / len(lst)

    def min_func(lst):
        min = lst[0]
        for i in lst:
            if i < min:
                min = i
            return min
    #
    def max_func(lst):
        max = lst[0]
        for i in lst:
            if i > max:
                max = i
        return max
    data = []
    for i in [level_1, level_2, level_3]:
        data.append({"min" : min_func(i), "max" : max_func(i), "avg" : round(Average(i),2)})

    #
    # for i in [level_1, level_2, level_3]:
    #     max.append(max_func(i))
    #
    # for i in [level_1, level_2, level_3]:
    #     avg.append(Average(i))

        # final = pd.DataFrame(list(zip(min, max, avg)), columns=['MIN', 'MAX', 'AVG'],
        #                      index=['LEVEL-1', 'LEVEL-2', 'LEVEL-3'])
    print('data is', data)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True,port=5001)