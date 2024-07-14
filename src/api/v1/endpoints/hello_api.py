import logging

from fastapi import APIRouter
router = APIRouter()


@router.get('/api/hello')
def hello():
    logging.info('api hello')

    return {'data' : 'hello'}
