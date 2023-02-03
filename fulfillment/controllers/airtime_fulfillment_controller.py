

from appemail.controllers import transaction_controller
from main.models import Setting
import json
from app_utils.helpers import get_custom_request, ResponseStatus, json_error_response, json_success_response
from transactions.helpers import save_airtime_failed_transaction, save_airtime_success_transaction
from main.libraries.hot_recharge import HotRechargeZW
from app_auth.models import User

from main.tasks import send_airtime_success_email, send_zesa_success_email
from fulfillment.models import TrackTransaction
from munch import Munch
from fulfillment.tasks import *
from fulfillment.helpers import get_exception_name, save_user_transaction, send_user_reponse

# try:
#     zwl_rate = int(Setting.objects.get(name="USD_TO_ZWL_RATE").value)
# except Setting.DoesNotExist:
#     zwl_rate = 120
    
zwl_rate = 120

                
def buy_airtime_for_user(request, order):
    hot_recharge = HotRechargeZW()
   
    airtime_amount = float(order.total) * zwl_rate
    mobile_number = "0" + order.mobile_number
    response = hot_recharge.recharge_pinless(mobile_number, airtime_amount)
    # response = Munch({"Status":"down", "ReplyCode": 2, "ReplyMsg": "Recharge to 0772358338 of $600.0 was successful. The initial balance was $332.45 final balance is $932.45", "WalletBalance": 708.0, "Amount": 600.0, "Discount": 1.0, "InitialBalance": 332.452006, "FinalBalance": 932.452006, "Window": "2022-02-28T00:00:00+02:00", "Data": 0.0, "SMS": 0, "AgentReference": "f6b782ea", "RechargeID": 110461948, "ErrorMessage": ""})
    
            
    if response["Status"] == "success":
        order.transaction.transaction_object = json.dumps(response)
        order.fulfilled = True
        order.save()
        order.transaction.save()
        save_user_transaction(order, response)
        request = get_custom_request(request)
        send_airtime_success_email.delay(request, order.id)
        message = "Order paid successfully. Order fulfilled. Thank you!"
        return send_user_reponse(ResponseStatus.SUCCESS, order, response, message)
    else:
        exception_name = "unknown"
        message = ""
        
        if (response['Status'] == "down"):
            exception_name = TrackTransaction.ExceptionType.SERVICE_DOWN.label
        elif (response['Status'] == "error"):
            exception_name = TrackTransaction.ExceptionType.SERVICE_ERROR.label
        elif (response['Status'] == "limit_error"):
            # Send email to chisach 
            exception_name = TrackTransaction.ExceptionType.LIMIT_ERROR.label
        elif (response['Status'] == "insufficient_balance"):
            # send email to chisach
            exception_name = TrackTransaction.ExceptionType.INSUFFICIENT_BALANCE.label
        else:
            exception_name = TrackTransaction.ExceptionType.SERVICE_ERROR.label
            
            
      
        user = request.user
        request = Munch(get_custom_request(request))
        exception_transaction = TrackTransaction.objects.create(
            order = order,
            user = user,
            request = Munch.toJSON(request),
            response = Munch.toJSON(response),
            timeout = 15,
            timeout_multiplier = 2,
            exception_name = exception_name,
        )
        
        transaction_id = exception_transaction.id
        tsk_track_transaction.delay(transaction_id)
        message = "Order paid successfully. Order is pending. We will update you through your email."
        
        return send_user_reponse(ResponseStatus.PENDING, order, response,message)

    
    
def bg_buy_airtime_for_user(track_transaction):
    hot_recharge = HotRechargeZW()
    request_string = track_transaction.request
    
    try:
        request = Munch.fromJSON(request_string)
    except:
        request = Munch({})
        
    order = track_transaction.order
    exception_name = track_transaction.exception_name
    
    try:
        prev_response = Munch.fromJSON(track_transaction.response)
    except json.JSONDecodeError:
        prev_response = Munch({})
        

    airtime_amount = float(order.total) * zwl_rate
    mobile_number = "0" + order.mobile_number
    
    service_errors = [TrackTransaction.ExceptionType.SERVICE_DOWN, TrackTransaction.ExceptionType.LIMIT_ERROR,  TrackTransaction.ExceptionType.INSUFFICIENT_BALANCE, TrackTransaction.ExceptionType.SERVICE_ERROR]
    

    response = hot_recharge.recharge_pinless(mobile_number, airtime_amount)
    # response = {"Status":"success", "ReplyCode": 2, "ReplyMsg": "Recharge to 0772358338 of $600.0 was successful. The initial balance was $332.45 final balance is $932.45", "WalletBalance": 708.0, "Amount": 600.0, "Discount": 1.0, "InitialBalance": 332.452006, "FinalBalance": 932.452006, "Window": "2022-02-28T00:00:00+02:00", "Data": 0.0, "SMS": 0, "AgentReference": "f6b782ea", "RechargeID": 110461948, "Status": "success", "ErrorMessage": ""}
   
    resp_status = response['Status']
        
    # Went through                     
    if resp_status == 'success':
        order.transaction.transaction_object = json.dumps(response)
        order.fulfilled = True
        
        order.save()
        order.transaction.save()
        
        save_user_transaction(order, response)
        send_airtime_success_email.delay(request, order.id)
         
    return Munch({
            "status": resp_status,
            "request": request, 
            "order": order, 
            "response": response   
    })