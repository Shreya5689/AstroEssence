import requests
from bs4 import BeautifulSoup

def astroyogi(rashi):
    mapping = {
        "mesh": "mesh",
        "karka": "kark",
        "vrish": "vrishabha",
        "mithun": "mithun",
        "simha": "singh",
        "kanya": "kanya",
        "vrishchik": "vrishchik",
        "tula": "tula",
        "dhanu": "dhanu",
        "makara": "makar",
        "kumbh": "kumbh",
        "meena": "meen"
    }
    url = f"https://hindi.astroyogi.com/rashifal/aaj-ka/{mapping[rashi]}-rashifal"
    url_love = f"https://hindi.astroyogi.com/rashifal/aaj-ka/{mapping[rashi]}-rashifal-love"
    url_career = f"https://hindi.astroyogi.com/rashifal/aaj-ka/{mapping[rashi]}-rashifal-career"
    url_finance = f"https://hindi.astroyogi.com/rashifal/aaj-ka/{mapping[rashi]}-rashifal-finance"
    url_health = f"https://hindi.astroyogi.com/rashifal/aaj-ka/{mapping[rashi]}-rashifal-health"
    
    try:
        response_prediction = requests.get(url)
        response_love = requests.get(url_love)
        response_career = requests.get(url_career)
        response_finance = requests.get(url_finance)
        response_health = requests.get(url_health)
        
        returnobj = {}
        
        if response_prediction.status_code == 200:
            soup = BeautifulSoup(response_prediction.text, "lxml")
            prediction = soup.find('p', class_='top15 text-justify line27 top17')
            prediction_text = prediction.text.strip()
            prediction_text = prediction_text.split('\n\n\n')[0]
            returnobj['prediction'] = prediction_text
            
        if response_love.status_code == 200:
            soup = BeautifulSoup(response_love.text, "lxml")
            love = soup.find('p', class_='top15 text-justify line27 top17')
            love_text = love.text.strip()
            love_text = love_text.split('\n\n\n')[0]
            returnobj['love'] = love_text
            
        if response_career.status_code == 200:
            soup = BeautifulSoup(response_career.text, "lxml")
            career = soup.find('p', class_='top15 text-justify line27 top17')
            career_text = career.text.strip()
            career_text = career_text.split('\n\n\n')[0]
            returnobj['career'] = career_text
            
        if response_finance.status_code == 200:
            soup = BeautifulSoup(response_finance.text, "lxml")
            finance = soup.find('p', class_='top15 text-justify line27 top17')
            finance_text = finance.text.strip()
            finance_text = finance_text.split('\n\n\n')[0]
            returnobj['finance'] = finance_text
            
        if response_health.status_code == 200:
            soup = BeautifulSoup(response_health.text, "lxml")
            health = soup.find('p', class_='top15 text-justify line27 top17')
            health_text = health.text.strip()
            health_text = health_text.split('\n\n\n')[0]
            returnobj['health'] = health_text
            
        return returnobj
    
    except requests.RequestException as e:
        print(f"Error during requests to {url}: {str(e)}")
        return None