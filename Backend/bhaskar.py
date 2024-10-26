import requests
from bs4 import BeautifulSoup

def bhaskar(rashi):
    mapping = {
        "mesh": 1,
        "karka": 2,
        "vrish":3,
        "mithun": 4,
        "simha": 5,
        "kanya": 6,
        "vrishchik": 7,
        "tula": 8,
        "dhanu": 9,
        "makara": 10,
        "kumbh": 11,
        "meena": 12
    }
    url = f"https://www.bhaskar.com/rashifal/{mapping[rashi]}/today/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            predictiondiv = soup.find_all('div', class_='a6b3d8fe')
            returnobj = {}
            prediction =""
            for i in range(0,len(predictiondiv)-1):
                prediction+=predictiondiv[i].text.strip()
            returnobj['prediction'] = prediction
            return returnobj
            
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error during requests to {url}: {str(e)}")
        return None