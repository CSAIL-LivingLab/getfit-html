import os
from datahub import DataHub
from datahub.constants import *
from thrift import Thrift
from thrift.protocol import TBinaryProtocol
from thrift.transport import THttpClient
from thrift.transport import TTransport
import secret

import os
import csv

''' 
    This is how to call the a SQL script across new users of the getfit app.

    You will need to

    1) define the secret.py allUsers array
    2) make sure that your script in allUserScript.sql is what you want
    3) import this file:
        >> from run_script_on_all_users import *
    
    This will run your sql script for all new users.

'''
# get the current directory
CURRENT_DIRECTORY = os.getcwd()
resultArray = [];

def runTheScript():
    sqlFile = open(CURRENT_DIRECTORY + "/allUserScript.sql", 'rb')
    sqlScript = sqlFile.read()


    for user in secret.allUsers:
        print "\n" + user
        try:
            transport = THttpClient.THttpClient('http://datahub.csail.mit.edu/service')
            transport = TTransport.TBufferedTransport(transport)
            protocol = TBinaryProtocol.TBinaryProtocol(transport)
            client = DataHub.Client(protocol)
            con_params = ConnectionParams(repo_base=user, app_id=secret.DHAPPID, app_token=secret.DHAPPTOKEN)
            con = client.open_connection(con_params=con_params)

            res = client.execute_sql(
                con=con,
                query=sqlScript,
                query_params=None)

            resultArray.append(res)

        except Exception, e:
            print "\n---EXCEPTION---"
            print e

        


# you need to defin an array before running


runTheScript()


print "Your variable, resultArray contains the results of your script, run over all users"