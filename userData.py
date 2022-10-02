import pandas as pd 
import os 

file = "./data/user_data.csv"

def addUser(df, email_id):

    if getUser(email_id).size == 0:
        df_orig = pd.read_csv(file)

        if(os.path.exists(file) and os.path.isfile(file)):
            os.remove(file)

        frames = [df_orig, df]
        result = pd.concat(frames)

        result.to_csv(file, index=False)

def getUser(email_id):
    df_orig = pd.read_csv(file)

    print(df_orig)

    df = df_orig[(df_orig['email_id'] == email_id)]
    print(df)
    return df