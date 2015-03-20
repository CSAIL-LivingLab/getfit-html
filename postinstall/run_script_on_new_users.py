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
    2) import this file
    3) copy allUsers into oldUsers.csv
    4) make sure that your script in sqlScript.sql is what you want
    5) import this file:
        >> from filter_new_users import *
    
    This will run your sql script for all new users.

'''
# get the current directory
CURRENT_DIRECTORY = os.getcwd()

    
def defineOldUserList():
    ''' the user var looks like ['al_carter', ' foo']
    '''
    oldUserFile = open(CURRENT_DIRECTORY + "/oldUsers.csv", 'rb')
    existingUserString = csv.reader(oldUserFile)
    oldUserList = list(existingUserString)[0]
    return oldUserList


def filterNewUsers():
    global oldUserList
    newUsers = []
    for user in secret.allUsers:
        # yeah, it's naieve. Also, we're cycling through < 200 users.
        if user not in oldUserList:
            newUsers.append(user)
    return newUsers


def runTheScript():
    sqlFile = open(CURRENT_DIRECTORY + "/sqlScript.sql", 'rb')
    sqlScript = sqlFile.read()


    for user in newUsers:
        print user
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

            print res;


        except Exception, e:
            print "\n---EXCEPTION---"
            print e

        


# you need to defin an array before running


oldUserList = defineOldUserList()
newUsers = filterNewUsers()
runTheScript()


print "\n\n\nNOW MAKE SURE TO MOVE allUsers into oldUsers.csv!!!\n\n"