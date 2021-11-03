from fastapi import FastAPI, BackgroundTasks
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
import time
import asyncio

class Topic(BaseModel):
    name: str
    description: Optional[str] = None

# go to localhost:8000/docs and localhost:8000/redocs to see the SwaggerUI
app = FastAPI()


@app.get('/topics/{name}')
def read_topic(topic_name):
    return {'topic_name': topic_name}


@app.get('/topics/{id}')
def read_topic(topic_id: int):
    return {'topic_id', topic_id}


@app.get('/topics/')
def read_topics(topic_id: int, q: Optional[str] = None):
    topic_items = ['OCR', 'GAN', 'RNN']
    dic = {'topic_name': topic_items[topic_id]}
    if q:
        dic['q'] = q
    return dic


@app.post('/topics/')
def create_topic(topic: Topic):
    return topic


def logging_task(data):
    with open('log.txt', mode='w') as f:
        f.write(str(data))


@app.post('/background-task/{user_id}')
def create_background_task(user_id: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(logging_task, {'user_id': user_id, 'timestampo': datetime.timestamp(datetime.now())})
    return {'message': f'Registered task for {user_id}'}


@app.get('/concurrent')
async def concurrent_task():
    tasks = []
    start = time.time()
    for i in range(10):
        tasks.append(asyncio.create_task(task1()))
        tasks.append(asyncio.create_task(task2()))

    response = await asyncio.gather(*tasks)
    end = time.time()
    return {'response': response, 'time_taken': (end-start)}


async def task1():
    await asyncio.sleep(2)
    return 'Task1 Completed'


async def task2():
    await asyncio.sleep(1)
    return 'Task2 Completed'
