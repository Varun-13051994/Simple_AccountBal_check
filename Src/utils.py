from configparser import ConfigParser
import pandas as pd
import pyodbc as od
import time, datetime

class AccountMethods:

    def __init__(self):
        config = ConfigParser()
        config.read(r"C:\Users\sumithras\Documents\Python_projects_folder\Simple_AccountBal_check\Src\Configurations.ini")

        # Read config values
        self._Driver = config['Database_Parameters']['Driver']
        self._Server = config['Database_Parameters']['Server']
        self._Database = config['Database_Parameters']['Database']
        self._UID = config['Database_Parameters']['UID']
        self._PWD = config['Database_Parameters']['PWD']
        self._TrustServerCertificate = config['Database_Parameters']['TrustServerCertificate']

        # Build connection string
        self.conn = (
                    f"Driver={self._Driver};"
                    f"Server={self._Server};"
                    f"Database={self._Database};"
                    f"UID={self._UID};"
                    f"PWD={self._PWD};"
                    f"TrustServerCertificate={self._TrustServerCertificate};"
                    )
    

    def verify(self, acct, password):

        account_id = acct
        pw = password

        Verify_Query = f"""
                            SELECT Account_Id, SecureKey
                            FROM Bank_Accounts_UsersTable
                            WHERE Account_Id = {account_id}
                        """
        
        emptydf = pd.DataFrame()
        
        try:
            conn_str = od.connect(self.conn)
            df = pd.read_sql(Verify_Query, conn_str)
            conn_str.close()

        except Exception as e:
            df = emptydf
            raise Exception("Could not connect to Database: {e}") from e
            

        if df.empty:
            return False
        elif df["Account_Id"][0] == int(account_id) and df["SecureKey"][0] == pw:
            return True
        else:
            return False
 
    
    @classmethod
    def account_balance(cls, acct, pw):

        Acc_bal_Query = f"""
                            SELECT SUM(CASE WHEN transaction_type = 'debit'
                                                THEN -1*amount
                                                ELSE amount
                                                END) amount_actual
                            FROM Bank_Accounts_TransactionTable
                            WHERE Account_Id = {acct}
                        """
    
        oj = cls()

        try:
            if oj.verify(acct, pw):

                conn_str = od.connect(oj.conn)
                
                df = pd.read_sql(Acc_bal_Query, conn_str)
                conn_str.close()

                return df
            
            else:
                return pd.DataFrame()
        
        except Exception as e:
            raise Exception("Error connecting to the Database, try again after few minutes.")
            
    