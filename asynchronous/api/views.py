from django.shortcuts import render
import httpx
import asyncio
from django.http import JsonResponse
import logging
import time

logger = logging.getLogger('api')


# Create your views here.

# helper fucntion
async def fetch_data(client, url): # async function ko asynchronous bnata h
    try:
        response = await client.get(url) # await asynchronous may pause krdeti h execution ko but baqi execution chlta rhta h
        return response.json()
    except Exception as e:
        logger.error(f"Error feching data from {url} | {str(e)}")
        return {'error': 'API failed'}
    
async def Dashboard(request):
    start_time = time.time()
    logger.info('Dashboard')
    urls = {
        "news": "https://newsapi.org/v2/everything?q=Lahore&apiKey=99a24b9d5f6f478ba1b0b9d12b125323",
        "weather": "https://api.weatherapi.com/v1/current.json?key=52fe6c8181ad44a291351150261504&q=Lahore"
    }
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        
        news_task = fetch_data(client, urls['news'])
        weather_task = fetch_data(client, urls['weather'])
        
        news, weather = await asyncio.gather(news_task, weather_task) # asyncio aik time may multiple kam efficiently manage krta h
        
    end_time = time.time()
    
    logger.info(f"Dashboard data fetched in {end_time - start_time}s")
        
    return JsonResponse({
        'status': 'Success',
        'response_time': end_time - start_time,
        'data': {
            'news': news,
            'weather': weather
        }
    })