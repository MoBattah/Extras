import requests
import json

#This script will turn off all integration checks that meet the uncheck list declared below

headers = {
    'app-key': "asfdsadfsadfasfdk",
    'Authorization': "Basic asfsafsafasdfsafsadfsdafVVCeHZDbHVlcw==",
    'Cache-Control': "no-cache",
    'Postman-Token': "asdfsafsfasfasdfsadf"
    }

def main():
    checks = getChecks()

def getChecks():
    turl = "https://api.pingdom.com/api/2.1/checks/"
    checkList = requests.request("GET", turl, headers=headers)
    checkjson = json.loads(checkList.text)
    check_id = checkjson["checks"][0]["id"]
    for x in range(0,122):
        try: check_id = checkjson['checks'][x]['id']
        except IndexError:
            print(str(x)+" is too much")
        print(check_id)
        curl = turl + str(check_id)
        integrationCheck = requests.request("GET", curl, headers=headers)
        integrationjson = json.loads(integrationCheck.text)
        integration = integrationjson["check"]['integrationids']
        name = integrationjson["check"]["name"]
        uncheck = ("IFC","DIA","HEAT","zzTEST")
        if any(s in name for s in uncheck):
            payload = {"integrationids": ""}
            modifyIntegration = requests.request("PUT", curl, params=payload, headers=headers)
            print("Modified integration for ", name)
        else:
            print("No need to modify ", name)

    return checkList.json()


if __name__ == "__main__":
    main()
