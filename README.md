# ChatBot

## Requirements

- [python 3.8.x](https://www.python.org/downloads/release/python-380/)
- [Bot Framework Emulator](https://github.com/microsoft/BotFramework-Emulator) 
- Knowledge of asynchronous programming in Python

## Setup

1. **Setup Virtual Environment** 
```
python3 -m venv .venv
source .venv/bin/activate
```

2. **Download Dependencies** 
```
pip install --upgrade pip
pip3 install -r requirements.txt
```

3. **Run the Utility**
```
export SQL_PASSWORD=<sql password>
python3 app.py
```

4. **Launch Bot Framework Emulator and Configure**  
<img src="images/emulator-config.png" width="70%">

## Publish 

* Reference: https://jd-bots.com/2021/09/27/deploy-a-basic-python-bot-to-azure-microsoft-bot-framework/


az login
az account set --subscription f0beb3e8-8b48-4fa5-8b61-882f6fba2a4f
az identity create --resource-group user63 --name user63-identity-0987
```
az identity create --resource-group user63 --name user63-identity-0987
{
  "clientId": "fcdf9be1-77bf-4d4e-8a1d-3d2b97838e5c",
  "id": "/subscriptions/f0beb3e8-8b48-4fa5-8b61-882f6fba2a4f/resourcegroups/user63/providers/Microsoft.ManagedIdentity/userAssignedIdentities/user63-identity-0987",
  "location": "centralus",
  "name": "user63-identity-0987",
  "principalId": "32254413-e1c4-4f1b-b5f0-8a1ce24e9720",
  "resourceGroup": "user63",
  "tags": {},
  "tenantId": "6601fd5c-1786-4b69-90b9-8db643e16413",
  "type": "Microsoft.ManagedIdentity/userAssignedIdentities"
}
```

az deployment group create --resource-group user63 --template-file deploymentTemplates/deployUseExistResourceGroup/template-BotApp-with-rg.json --parameters @deploymentTemplates/deployUseExistResourceGroup/parameters-for-template-BotApp-with-rg.json 

az deployment group create --resource-group <group-name> --template-file <template-file> --parameters @<parameters-file>

## References
* [Create a bot with the Bot Framework SDK using Python](https://learn.microsoft.com/en-us/azure/bot-service/bot-service-quickstart-create-bot?view=azure-bot-service-4.0&tabs=csharp%2Cvs)