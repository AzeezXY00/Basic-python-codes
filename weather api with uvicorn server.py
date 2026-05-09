from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/")
async def hello_world():
    return {"hello": "world"}

@app.get("/weather")
async def get_weather():
    api_key = "e27d08365d37fb916678b0ddc17f5044"  # paste your key here
    city = "Lagos"
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        )
    return response.json()