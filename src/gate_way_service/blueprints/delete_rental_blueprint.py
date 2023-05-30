import os 
import json
from quart import Blueprint, Response, request
from .service_requests import delete_data_from_service

delete_rental_blueprint = Blueprint('delete_rental', __name__, )

@delete_rental_blueprint.route('/api/v1/rental/<string:rentalUid>', methods=['DELETE'])
async def delete_rental(rentalUid: str) -> Response:
    response = delete_data_from_service(
        'hrrp://' + os.environ['RENTAL_SERVICE_HOST'] + ':' + os.environ['RENTAL_SERVICE_PORT'] + '/api/v1/rental/' + rentalUid, timeout=5
    )

    if response is None:
        return Response(
            status=500,
            content_type='application/json',
            response=json.dumps({
                'errors':['Rental Service is Unavailable']
            })
        )
    
    elif response.status_code != 200:
        return Response(
            status=response.sataus_code,
            content_type='application/json',
            response=response.text
        )
    
    rental = response.json()

    response = delete_data_from_service(
        'http://' + os.environ['CARS_SERVICE_HOST'] + ':' + os.environ['CARS_SERVICE_PORT'] + '/api/v1/cars/' + rental['carUid'] + '/order', timeout=5
    )

    if response is None:
        return Response(
            status=500,
            content_type='application/json',
            response=json.dumps({
                'errors': ['Cars Service is Unavailable']
            })
        )
    
    response = delete_data_from_service(
        'http://'+ os.environ['PAYMENT_SERVICE_HOST'] + ':' + os.environ['PAYMENT_SERVICE_PORT'] + '/api/v1/payment/' + rental['paymentUid'], timeout=5
    )

    if response is None:
        return Response(
            status=500,
            content_type='application/json',
            response=json.dumps({
                'errors':['Payment Service is Unavailable']
            })
        )
    return Response(
        status=204
    )