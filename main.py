# this is the main python file
import datetime, time
from Src.utils import AccountMethods


print("\n\t\tWelcome to MALLYA BANK\n")
uip = input("Please select from the following options:\n\n \
Verify_account ----------------------------------------- 1\n \
Check_Account_balance ---------------------------------- 2\n \
Exit --------------------------------------------------- 3\n \n"
            )

ac = AccountMethods()

if int(uip) ==1:
    Account_Id = input("Please key in Account ID, followed by Password: \n")
    Password = input("Enter the Password: \n")

    itr = 0
    while itr < 3:
        try:
            if ac.verify(Account_Id, Password):
                print("Account verified!")
                time.sleep(5)
            else:
                print("Could not verify the account details")
                time.sleep(5)
            
            break
        
        except Exception:
            if itr == 2:
                print(f"An error occured while connecting to the database ☹️     Time: {datetime.datetime.now()}. Seems the database is down for now, please try again in some time.")
            
            else:
                print(f"An error occured while connecting to the database ☹️     Time: {datetime.datetime.now()}. Trying to connect to database again in few seconds, hold tight...")
                
            time.sleep(5)
        
        itr+=1



elif int(uip) == 2:
    Account_Id = input("Please key in Account ID, followed by Password: \n")
    Password = input("Enter the Password: \n")
    
    itr = 0
    while itr < 3:

        try:

            resultant_df = ac.account_balance(Account_Id, Password)

            if not resultant_df.empty:

                print(f"Your Account balance is:  {int(resultant_df['amount_actual'][0])}")
                time.sleep(5)
            else:
                print("Could not verify the account details, make sure account details are keyed in correctly")
                time.sleep(5)

            break
        
        except Exception as e:
            if itr == 2:
                print(f"There is an error connecting to database to verify credentials:  {e}. \n \
                      Please try after sometime.")

            else:

                print(f"There was an error accessing the database to verify the account information.    Time: {datetime.datetime.now()}. Trying again in few seconds, hold on...")

            
            time.sleep(5)


        itr+=1


else:
    print("Have a nice day 😊!")
    time.sleep(5)