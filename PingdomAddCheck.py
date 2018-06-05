import requests
import json

headers = { #FILL IN HEADER INFORMATION
    'app-key': "YourAppKey",
    'Authorization': "BasicAuthToken",
    'Cache-Control': "no-cache",
    'Postman-Token': "yourpostmantoken"
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
        #if checkjson[x]
        curl = turl + str(check_id)
        integrationCheck = requests.request("GET", curl, headers=headers)
        integrationjson = json.loads(integrationCheck.text)
        integration = integrationjson["check"]['integrationids']
        print(integration)
        if integration == []:
            payload = {"integrationids": 79874} #instead of 79874, put in your integration
            modifyIntegration = requests.request("PUT", curl, params=payload, headers=headers)
            print("modified integration for " + str(check_id))
        else:
            print("No need to modify " + str(check_id))

    return checkList.json()


if __name__ == "__main__":
    main()
