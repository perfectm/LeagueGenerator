import json

# Read JSON data from file
with open("milb.json", "r") as json_file:
    json_data = json.load(json_file)

# Assuming json_data is an array of JSON objects
for data in json_data:
    # Extract team name from each JSON object
    team_name = data["name"]
    mascot = data["teamName"]
    team_location = team_name.replace(mascot,"")
    
    try:
        league = data["league"]["name"]
        #print("league:", league)
        if league in ('Pacific Coast League','International League','Eastern League','Midwest League','Southern League','South Atlantic League','Carolina League'):
            print("Mascot:", mascot, "Location:", team_location)
    except:
        continue
        #print("no league for ",team_name)    
    #print("Mascot:", mascot, "Location:", team_location)
