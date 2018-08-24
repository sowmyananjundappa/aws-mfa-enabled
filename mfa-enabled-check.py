import os
import sys
import json
list_users = []
valid_user = []
exempt = []
prof = sys.argv[1]
username = ""
def check_users():
    mfa_data = json.load(mfa_metadata_file)
    for mfa_check_index in range(len(mfa_data['Users'])):
        try:
            mfa_user_name = str(mfa_data['Users'][mfa_check_index]['UserName'])
            mfa_user_path = str(mfa_data['Users'][mfa_check_index]['Path'])
            if not mfa_user_name.startswith('test'):   #to exempt test user accounts
                list_users.append(mfa_user_name)
        except IndexError:
            pass
def print_users(p):
    for username in list_users:
                check_point = os.system("aws iam list-mfa-devices --user-name %(username)s --profile %(p)s --output json > /tmp/mfadata.json " % locals())
                with open('/tmp/mfadata.json') as mfa_mfadata_file:
                    mfa_data1 = json.load(mfa_mfadata_file)
                    try:
                        mfa_enabled_username = mfa_data1['MFADevices'][0]['UserName']
                        valid_user.append(mfa_enabled_username)
                    except IndexError:
                        pass
    final_user=set(list_users).difference(valid_user)
    d = list(final_user)
    for index in d:
        print (index)
        acc = "UserName:"+ index
        slack_msg(acc)
        file_store_data = open("path/for/temp/storage/mfa.csv", "a")
        file_store_data.write(str(prof)+",")
        file_store_data.write(str(index)+",")
        file_store_data.write("\n")

if __name__ == "__main__":
mfa_report = os.system("aws iam list-users --profile (prof)s --output json  > /tmp/mfa_metadata.json " % globals())
with open('/tmp/mfa_metadata.json') as mfa_metadata_file:
    check_users()
    print_users(prof)
