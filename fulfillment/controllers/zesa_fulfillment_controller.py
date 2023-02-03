from appemail.controllers import transaction_controller
from main.models import Setting
import json

from app_utils.helpers import ResponseStatus, get_custom_request, json_error_response, json_success_response, get_custom_request
from transactions.helpers import save_airtime_failed_transaction, save_airtime_success_transaction, save_zesa_failed_transaction, save_zesa_success_transaction
from main.libraries.hot_recharge import HotRechargeZW
from hotrecharge.HotRechargeException import PendingZesaTransaction

from main.tasks import send_zesa_success_email
from fulfillment.models import TrackTransaction
from munch import Munch
from fulfillment.helpers import get_exception_name, save_user_transaction, send_user_reponse
from app_auth.models import User

# try:
#     zwl_rate = int(Setting.objects.get(name="USD_TO_ZWL_RATE").value)
# except Setting.DoesNotExist:
#     zwl_rate = 120

zwl_rate = 120

def buy_zesa_for_user(request, order):
    hot_recharge = HotRechargeZW()
    zesa_amount = float(order.total) * zwl_rate
    meter_number = order.meter_number
    mobile_number = "0" + order.mobile_number
                    
  
    response = hot_recharge.recharge_zesa(zesa_amount, mobile_number, meter_number)
    # response = {"ReplyCode": 2, "ReplyMsg": "Success ZESA Token Purchase \r\nFor 01620187847 of $100\r\nCommission 0.0000% - HOT Recharge", "WalletBalance": 0.0, "Amount": 100.0, "ProviderFees": 7.0, "Discount": 0.0, "Meter": "01620187847", "AccountName": "", "Address": "", "Tokens": [{"ZesaReference": "POWERT3EMDB6514272", "Token": "5827 7691 4379 1041 8407", "Units": 7.4, "NetAmount": 94.34, "Arrears": 0.0, "Levy": 5.66, "TaxAmount": 0.0}], "AgentReference": "995d67fd", "RechargeID": 110938243, "CustomerInfo": {"Reference": "", "CustomerName": "MORDECAI SACHIKONYE\n35 CORONATION", "Address": "", "MeterNumber": "01620187847"}, "Status": "down", "ErrorMessage": ""}

                
    # Went through                     
    if response['Status'] == 'success':
        order.transaction.transaction_object = json.dumps(response)
        order.transaction.save()
        order.fulfilled = True
        order.save()
        
        save_user_transaction(order, response)
        request = get_custom_request(request)
        send_zesa_success_email.delay(request, order.id)
        message = "Order paid successfully. Order fulfilled!"
        return send_user_reponse(ResponseStatus.SUCCESS, order, response, message)
    else:
        exception_name = "unknown"
        message = ""
        
        if (response['Status'] == "pending"):
            exception_name = TrackTransaction.ExceptionType.PENDING.label
        elif (response['Status'] == "down"):
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
        request = get_custom_request(request)
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
        
        
        from fulfillment.tasks import  tsk_track_transaction
        tsk_track_transaction.delay(transaction_id)
        message = "Order paid successfully. Order is pending. We will update you through your email."
        
        return send_user_reponse(ResponseStatus.PENDING, order, response,message)
    
def bg_buy_zesa_for_user(track_transaction):
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

    zesa_amount = float(order.total) * zwl_rate
    meter_number = order.meter_number
    mobile_number = "0" + order.mobile_number
    
    service_errors = [TrackTransaction.ExceptionType.SERVICE_DOWN, TrackTransaction.ExceptionType.SERVICE_ERROR]
    
    if exception_name in service_errors:
        response = hot_recharge.recharge_zesa(zesa_amount, mobile_number, meter_number)
        # response = {"ReplyCode": 2, "ReplyMsg": "Success ZESA Token Purchase \r\nFor 01620187847 of $100\r\nCommission 0.0000% - HOT Recharge", "WalletBalance": 0.0, "Amount": 100.0, "ProviderFees": 7.0, "Discount": 0.0, "Meter": "01620187847", "AccountName": "", "Address": "", "Tokens": [{"ZesaReference": "POWERT3EMDB6514272", "Token": "5827 7691 4379 1041 8407", "Units": 7.4, "NetAmount": 94.34, "Arrears": 0.0, "Levy": 5.66, "TaxAmount": 0.0}], "AgentReference": "995d67fd", "RechargeID": 110938243, "CustomerInfo": {"Reference": "", "CustomerName": "MORDECAI SACHIKONYE\n35 CORONATION", "Address": "", "MeterNumber": "01620187847"}, "Status": "success", "ErrorMessage": ""}
    if exception_name == TrackTransaction.ExceptionType.PENDING:
        recharge_id = prev_response['RechargeID']
        response = hot_recharge.query_zesa_transaction(recharge_id)
        
    resp_status = response['Status']
    
    print(resp_status)
        
    # Went through                     
    if resp_status == 'success':
        order.transaction.transaction_object = json.dumps(response)
        order.fulfilled = True
        order.transaction.save()
        order.save()
        save_user_transaction(order, response)
        send_zesa_success_email.delay(request, order.id)
        
    return Munch({
            "status": resp_status,
            "request": request, 
            "order": order, 
            "response": response   
    })