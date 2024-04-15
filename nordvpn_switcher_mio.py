import subprocess
import time
import subprocess, re, random, datetime

    # Nordvpn shinanigance skip to line 105
def getCountries():
    """
    This function will return a list of the current countries with available servers for your nordvpn account.
    """
    nord_output = subprocess.Popen(["nordvpn", "countries"], stdout=subprocess.PIPE)
    countries = re.split("[\t \n]", nord_output.communicate()[0].decode("utf-8"))
    while "" in countries:
        countries.remove("")
    return countries

def chooseRandom(country_list):
    """
    This function will randomly choose a country out of the available countries list.
    """
    return country_list[random.randrange(0, len(country_list))]

def logIn(random_country):
    """
    This function will take the randomly chosen country and attempt to log in to NordVPN using that country.
    """
    print("{} has been selected as the random country.".format(random_country))
    # subprocess.call(["nordvpn", "c", random_country])
    cmd = ["nordvpn", "c", random_country]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = proc.communicate()
    if "Whoops! We couldn't connect you" in o.decode('ascii'):
        print("not connected. Retrying...")
        logIn(chooseRandom(getCountries()))
    else:
        print("Connected to {}".format(random_country))

def checkConnection():
    print("checkConnection connection!")
    cmd = ['nordvpn', 'c']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = proc.communicate()
    if "Connected" in o.decode('ascii'):
        return True
    else:
        return False

def tryConnection():
    print("Trying connection!")
    cmd = ['nordvpn', 'c']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)
    if checkConnection() == True:
        print("Successfull Connection with:\n" + email +" " +password)
    else:
        print("Failed")
        cmd = ['nordvpn', 'logout']
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Logged out")

def loginWithPassword(email, password):
    cmd = ['nordvpn', 'login', '--username', email, '--password', password]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # print(proc)
    o, e = proc.communicate()
    stdout = proc.communicate()[0]
    # print (format(stdout))
    if "is not correct" in o.decode('ascii'):
        print("Wrong password")

    if "already logged in" in o.decode('ascii'):
        print("Already logged in")
        nord_output = subprocess.Popen(["nordvpn", "status"], stdout=subprocess.PIPE)
        status = re.split("[\r \n :]", nord_output.communicate()[0].decode("utf-8"))[-2]
        if status == "Disconnected":
            print("Disconnected from nord!")
            logIn(chooseRandom(getCountries()))
        else:
            print("Connected...")
            print("Calling diconnecting to randomize...")
            subprocess.call(["nordvpn", "disconnect"])
            logIn(chooseRandom(getCountries()))


#loginWithPassword("email", "password")

logIn(chooseRandom(getCountries()))