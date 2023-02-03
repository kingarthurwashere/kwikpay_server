
from fulfillment.models import TrackTransaction
from app_utils.helpers import json_success_response
from transactions.helpers import save_airtime_success_transaction, save_zesa_success_transaction
from main.models import Order


def send_user_reponse(status, order, response, message=None):
    
    if (message == None):
        message = "Order paid successfully. Order fulfilled."
    response["OrderID"] = order.id
    response["FullFilledStatus"] = order.fulfilled
    return json_success_response(status, message, response)

def save_user_transaction(order, response):
    print("[Save User Transaction] -> Saving transaction...")
    
    if order.service == Order.Service.AIRTIME:
        save_airtime_success_transaction(order.transaction, response)
    elif order.service == Order.Service.ELECTRIC_BILL:
        save_zesa_success_transaction(order.transaction, response)

def get_exception_name(resp_status):
    if resp_status == "pending":
        return TrackTransaction.ExceptionType.PENDING.label
    elif resp_status == "down":
        return TrackTransaction.ExceptionType.SERVICE_DOWN.label
    elif resp_status == "error":
        return TrackTransaction.ExceptionType.SERVICE_ERROR.label
    elif resp_status == "limit_error": 
        exception_name = TrackTransaction.ExceptionType.LIMIT_ERROR.label
    elif resp_status == "insufficient_balance":
        exception_name = TrackTransaction.ExceptionType.INSUFFICIENT_BALANCE.label
    else:
        exception_name = TrackTransaction.ExceptionType.SERVICE_ERROR.label   