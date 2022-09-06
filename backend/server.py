# Created by Team D all rights reserved
# naming conventions
# Flask routines follow camel case (e.g. manageXyz)
# helper functions should be lower cased seperated by an underscore (e.g. word_word2_word3)

from tabnanny import check
import datetime
import vt
from datetime import date, datetime
from flask import Flask, redirect, url_for, request, render_template, jsonify
import json
from flask_cors import CORS
import sqlite3


# Creates Flask instance - app
app = Flask(__name__)

app.config.from_object(__name__)

CORS(app, resources={r"/*": {'origins': "*"}})

@app.route("/")
def API_base_route():
    return "<p>Please use POST on '/hashes'</p>See Docs for example!"

@app.route("/extra",methods=['GET'] )
def getExtraData():
    con = sqlite3.connect("vtdb.db", check_same_thread=False)
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS hash(md5 text PRIMARY KEY, UNIQUE(md5))''')

    cur.execute('''CREATE TABLE IF NOT EXISTS report(hash text, size real, type text, sha256 text, sha1 text, dateadded text, datevt text, numharmless real, nummalicious real, numsuspicious real, numundetected real, vendors text, popular real,UNIQUE(sha256))''')
    cur.execute("SELECT * from report ORDER BY popular DESC LIMIT 5")
    checkDb = cur.fetchone()
    report = {"Popular": [], "Date": []}
    response_obj = {}
    #check if in database
    if checkDb:
        cur.execute("SELECT * from report ORDER BY popular DESC LIMIT 5")
        checkHash = cur.fetchall()
        # Add in the popularity to report
        for hashes in range(len(checkHash)):
            # TempPop will store the [Hash, Popularity]
            tempPop = [checkHash[hashes][0],checkHash[hashes][12]]
            report["Popular"].append(tempPop) 

        # Getting the dates
        cur.execute("SELECT * from report ORDER BY dateadded DESC LIMIT 5")
        checkHash = cur.fetchall()
        # Adding it to our report
        for hashes in range(len(checkHash)):
            # tempDate will store the [Hash, DateAddded]
            tempDate = [checkHash[hashes][0],checkHash[hashes][5]]
            report["Date"].append(tempDate) 

        response_obj['db_report'] = [
            report
        ]
        response_obj['count'] = 1
        response_obj['status_msg'] = "DEBUG !!!"
    # If it doesnt exist we just return an empty report
    else:
        # Use empty data to populate our 5 array to display
        for i in range(5):
            report["Popular"].append(["N/A", "0"])
            report["Date"].append(["N/A", "N/A"]) 

        response_obj['db_report'] = [
            report
        ]
        response_obj['count'] = 1
        response_obj['status_msg'] = "DEBUG !!!"
    con.close()

    return jsonify(response_obj)

@app.route("/hashes", methods=['GET', 'POST'])
def manangeHashes():
    response_obj = {'status_msg': 'OK'}
    if request.method == 'POST':
        post_data = request.json
        hash_id = post_data['Hash']
        try:
            report = get_hash_report(hash_id)
        except ValueError as e:
            response_obj['status_msg'] = 'INVALID Hash'
            return jsonify(response_obj)
        response_obj['hash_report'] = [
            report
        ]
        response_obj['count'] = 1
        response_obj['status_msg'] = "DEBUG !!!"

    else:
        response_obj['status_msg'] = "UNCONFIGURED!!!"

    return jsonify(response_obj)


def get_hash_report(hash_id):
    #create dict to hold hash report
    con = sqlite3.connect("vtdb.db", check_same_thread=False)
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS hash(md5 text PRIMARY KEY, UNIQUE(md5))''')

    cur.execute('''CREATE TABLE IF NOT EXISTS report(hash text, size real, type text, sha256 text, sha1 text, dateadded text, datevt text, numharmless real, nummalicious real, numsuspicious real, numundetected real, vendors text, popular real,UNIQUE(sha256))''')
    report = {"Hash": hash_id}
    
    #checks to see if hash is in database
    cur.execute("SELECT * FROM hash WHERE md5 = (?)", (hash_id,))

    #gets the data from the cursor from last call, in this case checks to see if hash is nonetype or it exists
    checkDb = cur.fetchone()
    #check if in database
    if checkDb:

        #we now go get the attributes from report where its foreign key is the same as the one passed into function
        cur.execute("SELECT * FROM report where hash = (?)", (hash_id,))

        #we grab its attributes
        checkHash = cur.fetchone()

        #set the report to be stuff from database
        report["Size"] = checkHash[1] #int
        report["Type"] = checkHash[2] #string
        report["SHA256"] = checkHash[3] #string
        report["SHA1"] = checkHash[4] #string
        report["DateAdded"] = checkHash[5] #string
        report["DateVT"] = checkHash[6] #string
        report["NumHarmless"] = checkHash[7] #int
        report["NumMalicious"] = checkHash[8] #int
        report["NumSuspicious"] = checkHash[9]  #int
        report["NumUndetected"] = checkHash[10] 
        report["Vendors"] = checkHash[11] # 11
        report["Popular"] = checkHash[12] + 1
        #print(report["DateAdded"])
        cur.execute("UPDATE report SET popular = (?) WHERE hash = (?)", (report["Popular"], hash_id))
        cur.execute("UPDATE report SET DateAdded = (?) WHERE hash = (?)", (datetime.today().strftime('%m/%d/%Y'), hash_id))

        #print(report["Vendors"])
        tempArray = []
        # Putting our stuff from vendor (dict) into an Array
        # Making it easier for Frontend
        newArray = json.loads(report["Vendors"])
        for stuff in newArray:
            tempArray.append(newArray[stuff])
        report["Processed_Vendor"] = tempArray
        #returns report
        
        #write code to take info from database
    
    #make call to api if not in db
    else:
        print("Not in DB")
        client = vt.Client("73ae9b0fcaff2b92a989c01d97542bfa041e2f7dfa955bb6f600fc53a2384675")
        try:
            file = client.get_object("/files/" + str(hash_id))
        except vt.error.APIError as e:
            con.close()  # close DB
            client.close()  # close VirusTotal
            raise ValueError("Invalid Hash")
        # print(file)

        report["Size"] = file.size #int
        report["Type"] = file.type #string
        report["SHA256"] = file.sha256 #string
        report["SHA1"] = file.sha1 #string
        report["DateAdded"] = date.today().strftime("%m/%d/%Y") #string
        report["DateVT"] = file.first_submission_date.strftime("%m/%d/%Y") #string
        report["NumHarmless"] = file.last_analysis_stats["harmless"] #int
        report["NumMalicious"] = file.last_analysis_stats["malicious"] #int
        report["NumSuspicious"] = file.last_analysis_stats["suspicious"]  #int
        report["NumUndetected"] = file.last_analysis_stats["undetected"] #int
        report["Vendors"] = json.dumps(file.last_analysis_results)  # Vendors(string)
        report["Popular"] = 1
        tempArray = []
        # Putting our stuff from vendor (dict) into an Array
        # Making it easier for Frontend
        newArray = json.loads(report["Vendors"])
        for stuff in newArray:
            tempArray.append(newArray[stuff])
        report["Processed_Vendor"] = tempArray
        client.close()
        
        #store new hash into db
    curr_report = report
    

    theHash = curr_report.get("Hash")

#might insert this hash into hash table if it doesnt exist
    cur.execute("INSERT OR IGNORE INTO hash(md5) VALUES(?)", (theHash,))

    #gets all other data from report
    r_size = curr_report.get("Size")
    r_type = curr_report.get("Type")
    r_sha256 = curr_report.get("SHA256")
    r_sha1 = curr_report.get("SHA1")
    r_dateadded = curr_report.get("DateAdded")
    r_datevt = curr_report.get("DateVT")
    r_numharmless = curr_report.get("NumHarmless")
    r_nummalicious = curr_report.get("NumMalicious")
    r_numsuspicious = curr_report.get("NumSuspicious")
    r_numundetected = curr_report.get("NumUndetected")
    r_vendors = curr_report.get("Vendors")
    r_popular = curr_report.get("Popular")



    #might insert all this data into report table if it doesnt exist

    # TODO: ADD NumUndetected to the database 
    # TODO: ADD Popular Counter
    cur.execute("INSERT OR IGNORE INTO report(hash,size, type, sha256, sha1, dateadded, datevt, numharmless, nummalicious, numsuspicious, numundetected, vendors, popular) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (theHash, r_size, r_type, r_sha256, r_sha1, r_dateadded, r_datevt, r_numharmless, r_nummalicious, r_numsuspicious, r_numundetected, r_vendors, r_popular))

    con.commit()
    con.close()

    return report

#print(get_hash_report("44d88612fea8a8f36de82e1278abb02f"))

#curr_report = get_hash_report("44d88612fea8a8f36de82e1278abb02f")

#gets the hash from the report


if __name__ == "__main__":
    app.run(debug=True)