import sys
from bs4 import BeautifulSoup
from requests import Session
from urllib.parse import urljoin

session = Session()
session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"

def readfile():
    SQLQueries = []
    with open("SQLInjectionQueries.txt", "r") as file:
        for line in file:
            query = line.split("\n")
            SQLQueries.append(query[0])
    return SQLQueries

def testInjection(URL, queries):
    soup = BeautifulSoup(session.get(URL).content, "html.parser")
    allForms = soup.find_all("form")
    print(f"Testing {len(queries)} queries on {len(allForms)} form(s).")
    results = []
    for query in queries:
        print(f"--------------------THE RESULTS FOR QUERY: {query}--------------------")
        counter = 1
        for form in allForms:
            print(f"--------------------THE RESULTS FOR FORM #{counter}--------------------")
            requestURL = urljoin(URL,form.attrs.get("action")[1:])
            print(requestURL)
            inputs = getInputs(form)
            payload = {}
            for input in inputs:
                if input["type"] != "submit":
                    payload[input["name"]] = query
            if form.attrs.get("method", "get").lower() == "post":
                res = session.post(requestURL, data=payload)
            elif form.attrs.get("method", "get").lower() == "get":
                res = session.get(requestURL, params=payload)
            print(res.text)
            counter+=1

def getInputs(form):
    inputs = []
    for input in form.find_all("input"):
        data = { "name": input.attrs.get("name"), "type": input.attrs.get("type", "text") }
        inputs.append(data)
    return inputs

def printResults(results):
    for result in results:
        print()

if __name__ == "__main__":
    #make sure there is a URL argument
    if len(sys.argv) != 2:
        "The only argument for this file is a URL"
        exit()
    URL = sys.argv[1]
    testQueries = readfile()
    testInjection(URL, testQueries)