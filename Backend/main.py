import json
import os
import google.generativeai as genai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from astroyogi import astroyogi
from bhaskar import bhaskar
from dotenv import load_dotenv
import textwrap
import uvicorn

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_rashifal(rashi):
    data_obj = {}
    try:
        data_obj["source1"] = bhaskar(rashi)
    except Exception as e:
        print(f"Error fetching data from bhaskar: {e}")
        data_obj["source1"] = ""
    
    try:
        data_obj["source2"] = astroyogi(rashi)
    except Exception as e:
        print(f"Error fetching data from astroyogi: {e}")
        data_obj["source2"] = ""

    return json.dumps(data_obj)

def get_data(rashi):
    try:
        rashifal_data = get_rashifal(rashi)
        response = model.generate_content(
            textwrap.dedent("""\
            Please process the following resume bullet points and return a JSON object with the following structure:

            IMPORTANT: Assume yourself to be an expert deducer and an expert advisor of actionable insights. Based on the data at hand, you give definitive and easy-to-follow things that a person can do or should take care of.
            The data is for the current day ONLY.
            
            The task is to assign ratings and 3 things which give actionable insights based on the following criteria:
            1. Keep in mind all the data that has been collected from the 2 sources.
            2. The data is of the current day only. The actionables should be for the current day only. 
            3. The ratings should be between 1-10.
            4. Consider the data from all the sources and assign a rating based on the data.
            5. The insights should be actionable and easy to follow.
            Example: You should not go outside a lot today. Instead, you should stay indoors and take care of your health.
            
            The JSON structure should be as follows:

            {
                "career": [
                    rating: 1-10,
                    insight1: "Insight 1",
                    insight2: "Insight 2",
                    insight3: "Insight 3"
                ],
                "love": [
                    rating: 1-10,
                    insight1: "Insight 1",
                    insight2: "Insight 2",
                    insight3: "Insight 3"
                ],
                "health": [
                    rating: 1-10,
                    insight1: "Insight 1",
                    insight2: "Insight 2",
                    insight3: "Insight 3"
                ],
                "money": [
                    rating: 1-10,
                    insight1: "Insight 1",
                    insight2: "Insight 2",
                    insight3: "Insight 3"
                ],
                "relations": [
                    rating: 1-10,
                    insight1: "Insight 1",
                    insight2: "Insight 2",
                    insight3: "Insight 3"
                ]
            }

            All fields are required.

            Important: Only return a single piece of valid JSON text.
            """) + rashifal_data, generation_config={'response_mime_type': 'application/json'}
        )
        result = json.loads(response.text)
        return result
    except Exception as e:
        return {"error": f"Error generating insights: {str(e)}"}

@app.get("/get_data/{rashi}")
def get_rashi_data(rashi: str):
    try:
        result = get_data(rashi)
        return result
    except Exception as e:
        return {"error": f"Failed to fetch data for {rashi}: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)