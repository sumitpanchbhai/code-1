import psycopg2
import pandas as pd


class connection:
    def __init__(self):
        self.conn = psycopg2.connect(
            host='65.1.154.91',
            database='mobilserv',
            user='ro_user_ms',
            password='Dpenhq$@158'
        )
        self.cur = self.conn.cursor()
    def my_connection(self,customer,machine,startdate,enddate):
        try:
            sql = 'select round(extract(epoch from ts)) ts,raw_data->21 as "Total KW",raw_data->29 as "kWh" FROM mobilserv.gmiiot_machine_data'
            if customer is not None:
                sql += f' where customer_id={customer}'
            if machine is not None:
                sql += f' and machine_id={machine}'
            if startdate is not None and enddate is not None:
                sql += f' and extract(epoch from ts) between {startdate} and {enddate};'
            self.cur.execute(sql)
            # print(sql)
            data = pd.DataFrame(self.cur, columns=['TS', 'Total_kW', 'kWh'])
            return data
        except psycopg2.Error as e:
            print('Error occure while database connection',e)


# myobject = connection()
# myobject.my_connection(customer=35,machine=33,startdate=1648139685,enddate=1648139782)
