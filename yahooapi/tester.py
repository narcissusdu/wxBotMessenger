"""yahoo api tester"""
import urllib.parse
import urllib.request
import json

def main():
    """main entrance"""
    yql = 'select * from geo.places where text="西安"'
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_url = baseurl + urllib.parse.urlencode({'q':yql}) + "&format=json"
    result = urllib.request.urlopen(yql_url).read()
    data = json.loads(result)
    print(data)


if __name__ == "__main__":
    main()
    