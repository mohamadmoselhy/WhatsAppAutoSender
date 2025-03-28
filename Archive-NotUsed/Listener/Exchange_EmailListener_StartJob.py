import win32com.client
import os
from datetime import datetime, timedelta
import requests
import json
import argparse
from exchangelib import DELEGATE, Account, Credentials, Configuration



parser = argparse.ArgumentParser(description='Program to start a new job in case a new email is found in a specific folder in excel with subject filter.')

parser.add_argument("Mail_Username", help="The mail username that reads emails from.")
parser.add_argument("Mail_Password", help="The mail Password that reads emails from.")
parser.add_argument("Mail_folder_name", help="The mail folder to read emails from.")
parser.add_argument("Mail_Sender", help="The mail Sender filter to read emails.")
parser.add_argument("Mail_Subject", help="The mail subject filter to read emails.")
parser.add_argument("Mail_PreviousHours", help="Number of Previous hours to read emails from. If entered 0, it will check all mailbox.")
parser.add_argument("Orchestrator_TenantName", help="Name of orchestrator tenant where the process is deployed in.")
#parser.add_argument("Orchestrator_Username", help="Username to login to orchestrator tenant.")
#parser.add_argument("Orchestrator_Password", help="Password to login to orchestrator tenant")
parser.add_argument("OrchestratorProcessReleaseKey", help="UiPath Orchestrator Process unique identifier.")
parser.add_argument("OrchestratorRobotID", help="UiPath Orchestrator Robot unique identifier.")
parser.add_argument("OrchestratorMachineSessionID", help="UiPath Orchestrator Machine active session unique identifier.")
parser.add_argument("OrchestratorFolderName", help="UiPath Orchestrator folder name.")
parser.add_argument("OrchestratorJobInputArguments", help="UiPath Orchestrator Job Input Arguments.")
args = parser.parse_args()

########################################################################################################################################################################
#Variables Assigning

Mail_Username=args.Mail_Username
Mail_Password=args.Mail_Password
#Mail_folder_name="Inbox"
Mail_folder_name=args.Mail_folder_name
Mail_SenderFilter=args.Mail_Sender
#Mail_SubjectFilter='test'
Mail_SubjectFilter=args.Mail_Subject

#PreviousHours="0"
PreviousHours=args.Mail_PreviousHours
if PreviousHours.isnumeric():
    PreviousHours=int(PreviousHours)
else:
    PreviousHours=0
#Orchestrator_TenantName="Default"
Orchestrator_TenantName=args.Orchestrator_TenantName
Orchestrator_Username="EmailListener"
Orchestrator_Password="EmailListener@123"
#OrchestratorProcessReleaseKey="819e5ea2-6745-4a6d-ac09-5f850e1a38b3"
OrchestratorProcessReleaseKey=args.OrchestratorProcessReleaseKey
#OrchestratorRobotID=196
OrchestratorRobotID=int(args.OrchestratorRobotID)
#OrchestratorMachineSessionID=237
OrchestratorMachineSessionID=int(args.OrchestratorMachineSessionID)
#Orchestrator_Folder_Name="Etimad7"
Orchestrator_Folder_Name=args.OrchestratorFolderName
OrchestratorJobInputArguments=args.OrchestratorJobInputArguments


creds = Credentials(
    username='STCS\\'+Mail_Username,  
    password=Mail_Password
)
config = Configuration(server='mail.stcs.com.sa', credentials=creds)
a = Account(
    primary_smtp_address=Mail_Username+'@solutions.com.sa', 
    autodiscover=False,
    config=config,    
    access_type=DELEGATE
)
########################################################################################################################################################################


# Get mails from inbox
#outlook = win32com.client.Dispatch('outlook.application')
#mapi = outlook.GetNamespace("MAPI")
#root_folder = mapi.Folders.Item(1).Folders
root_folder=a.root
FolderFound=False
for folder in root_folder.glob('**/*'): 
        if folder.name == Mail_folder_name:
            print (folder.name + ' found')
            found_folder = folder
            FolderFound=True

if FolderFound == False:
    raise Exception("Unable to find folder named: "+Mail_folder_name)
messages = found_folder.all()
if PreviousHours>0:
    Mail_received_dt = datetime.now() - timedelta(hours=PreviousHours)
    Mail_received_dt = Mail_received_dt.strftime('%m/%d/%Y %I:%M %p')
    print(Mail_received_dt)    
    messages=messages.filter('isread:False AND subject:'+Mail_SubjectFilter+' AND Received:>='+Mail_received_dt+' AND from:'+Mail_SenderFilter) #in case mail sender not entered it takes exact match
else:
    Mail_received_dt = datetime.now() - timedelta(hours=500000)
    Mail_received_dt = Mail_received_dt.strftime('%m/%d/%Y %I:%M %p')
    messages=messages.filter('isread:False AND subject:'+Mail_SubjectFilter+' AND Received:>='+Mail_received_dt+' AND from:'+Mail_SenderFilter)
    


print(messages.count())
for message in messages:
    print(message.subject)




#start job if any number of mails match criteria of trigger
if messages.count()>0:
########################################################################################################################################################################

#Authenticate to Orchestrator
    data ={
        "tenancyName" : Orchestrator_TenantName,
        "usernameOrEmailAddress" : Orchestrator_Username,
        "password" : Orchestrator_Password
        }
    headers = { "Content-Type" : "application/json" }
    URL= "https://stcs-rpaappd01.stcs.com.sa/api/Account/Authenticate"
    x=requests.post(URL, headers=headers, json = data, verify=False)
    Token=x.json()['result']


########################################################################################################################################################################

#Start Job
    JobsEndPoint="https://stcs-rpaappd01.stcs.com.sa/odata/Jobs/UiPath.Server.Configuration.OData.StartJobs"
    JobsHeaders= {
    "Content-Type" : "application/json",
    "Authorization" : "Bearer "+Token,
    "X-UIPATH-FolderPath" : Orchestrator_Folder_Name
    }
    JobsBody={
    "startInfo":
    {"ReleaseKey":OrchestratorProcessReleaseKey,
    "RobotIds":[OrchestratorRobotID],
    "MachineSessionIds":[OrchestratorMachineSessionID],
    "JobsCount":1,
    "JobPriority":"Normal",
    "Strategy":"ModernJobsCount",
    "RuntimeType":"Unattended",
    "InputArguments":OrchestratorJobInputArguments
    }}
    Job=requests.post(JobsEndPoint, headers=JobsHeaders, json = JobsBody, verify=False)
    print (Job.status_code)
    print(Job.text)
