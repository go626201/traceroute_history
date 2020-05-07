#! /usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
traceroute_history is a quick tool to make traceroute / tracert calls, and store it's results into a database if it
differs from last call.

Traceroute History user interface and API

"""

__intname__ = 'traceroute_history.user_interface'
__author__ = 'Orsiris de Jong'
__copyright__ = 'Copyright (C) 2020 Orsiris de Jong'
__licence__ = 'BSD 3 Clause'
__version__ = '0.4.0'
__build__ = '2020050601'


from typing import List
from fastapi import Depends, FastAPI, Request, HTTPException
from sqlalchemy.orm import Session
import crud
import schemas
from database import db_scoped_session
import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import psutil
import ofunctions
import traceroute_history
from database import load_database, get_db
import config_management

logger = ofunctions.logger_get_logger()

# TODO conf file loader
config = config_management.load_config('traceroute_history.conf')
load_database(config)

app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount('/assets', StaticFiles(directory='assets'), name='assets')


def get_system_data():
    try:
        cpu = psutil.cpu_percent()
    except NameError:
        cpu = -1
    try:
        memory = psutil.virtual_memory()._asdict()['percent']
    except NameError:
        memory = -1

    return {
        'cpu': cpu,
        'memory': memory,
        'version': traceroute_history.__version__,
        'ui_version': __version__,
    }


"""
Main API functions
"""
@app.post('/target/', response_model=schemas.Target)
def create_target(target: schemas.TargetCreate, db: Session = Depends(get_db)):
    db_target = crud.get_target(db=db, name=target.name)
    if db_target:
        raise HTTPException(status_code=400, detail='Target already exists')
    return crud.create_target(db=db, target=target)

@app.get('/targets/', response_model=List[schemas.Target])
def read_targets(skip: int = 0, limit : int = None, db: Session = Depends(get_db)):
    targets = crud.get_targets(db=db, skip=skip, limit=limit)
    return targets

@app.get('/target/{id}', response_model=schemas.Target)
def read_target_by_id(id: int, db: Session = Depends(get_db)):
    db_target = crud.get_target(db=db, id=id)
    if db_target is None:
        raise HTTPException(status_code=404, detail='Target does not exist')
    return db_target

@app.get('/target/name/{name}', response_model=schemas.Target)
def read_target_by_name(name: str, db: Session = Depends(get_db)):
    db_target = crud.get_target(db=db, name=name)
    if db_target is None:
        raise HTTPException(status_code=404, detail='Target does not exist')
    return db_target

@app.delete('/target/{id}')
def delete_traceroute_by_id(id, db: Session = Depends(get_db)):
    db_operation = crud.delete_target(db=db, id=id)
    if db_operation is None:
        raise HTTPException(status_code=404, detail='Target does not exist')
    return db_operation


@app.post('/group', response_model=schemas.Group)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    db_group = crud.get_group(db=db, name=group.name)
    if db_group:
        raise HTTPException(status_code=400, detail='Group already exists')
    return crud.create_group(db=db, group=group)


@app.get('/groups', response_model=List[schemas.Group])
def read_groups(skip: int = 0, limit: int = None, db: Session = Depends(get_db)):
    groups = crud.get_groups(db=db, skip=skip, limit=limit)
    return groups

@app.get('/group/{id}', response_model=schemas.Group)
def read_groupby_id(id: int, db: Session = Depends(get_db)):
    db_group = crud.get_group(db=db, id=id)
    if db_group is None:
        raise HTTPException(status_code=404, detail='Group does not exist')
    return db_group

@app.post('/target/{id}/traceroutes', response_model=schemas.Traceroute)
def create_traceroute_for_target(id: int, traceroute: schemas.TracerouteCreate, db: Session = Depends(get_db)):
    return crud.create_target_traceroute(db=db, traceroute=traceroute, target_id=id)


@app.get('/target/{id}/traceroutes', response_model=schemas.Traceroute)
def read_traceroutes_for_target(id: int, skip: int = 0, limit: int = None, db: Session = Depends(get_db)):
    return crud.get_traceroutes_by_target(db=db, target_id=id, skip=skip, limit=limit)

@app.get('/traceroutes', response_model=schemas.Traceroute)
def read_traceroutes(skip: int = 0, limit: int = None, db: Session = Depends(get_db)):
    traceroutes = crud.get_traceroutes(db=db, skip=skip, limit=limit)
    print(traceroutes)
    return traceroutes


"""
GUI functions
"""

@app.get('/')
async def index(request: Request):
    targets = traceroute_history.list_targets(include_tr=True, formatting='web')
    print(targets)
    return templates.TemplateResponse('targets.html',
                                      {'request': request, 'targets': targets, 'system': get_system_data()})



if __name__ == '__main__':
    uvicorn.run('user_interface:app', host='127.0.0.1', port=5001, log_level='info', reload=True)