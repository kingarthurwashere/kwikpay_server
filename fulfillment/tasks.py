from celery import shared_task
from fulfillment.models import TrackTransaction
from fulfillment.helpers import get_exception_name
import time, json
from munch import Munch
from fulfillment.controllers.zesa_fulfillment_controller import *
from fulfillment.controllers import airtime_fulfillment_controller as airtime_controller
from main.models import Order


closed_reason = TrackTransaction.ClosedReason
trans_status = TrackTransaction.TransactionStatus


@shared_task
def tsk_track_transaction(id):
   
   
   tracked_transaction = TrackTransaction.objects.get(id=id)
   final_status = Munch()
   
   while tracked_transaction.status != trans_status.CLOSED:

      #   Calculate time 
       sleep_time = int(tracked_transaction.timeout) * int(tracked_transaction.timeout_multiplier)
       print("[Track Transaction] -> Sleeping for {0} seconds".format(sleep_time))
       time.sleep(sleep_time )
       
       
       tracked_transaction.status = TrackTransaction.TransactionStatus.OPEN.label
       tracked_transaction.save()
       
       # Extract details and retry transaction 
       order = tracked_transaction.order
       exception_name = tracked_transaction.exception_name
       
       # Retry Transaction 
       print("[Track Transaction] -> Retrying transaction")
       if order.service == Order.Service.ELECTRIC_BILL:
          result = bg_buy_zesa_for_user(track_transaction=tracked_transaction)
       elif order.service == Order.Service.AIRTIME:
          result = airtime_controller.bg_buy_airtime_for_user(track_transaction=tracked_transaction)
       
       if (result.status == "success"):
            print("[Track Transaction] -> Transaction succeeded exiting!")
            tracked_transaction.status = TrackTransaction.TransactionStatus.CLOSED.label
            tracked_transaction.reason = TrackTransaction.ClosedReason.WENT_THROUGH.label
            tracked_transaction.save()
            final_status.status = "success"
            final_status.message = "Transaction went through"
            break
       else:
          print("[Track Transaction] -> Transaction failed again. retrying!")
          tracked_transaction.exception_name = get_exception_name(result.status)
          tracked_transaction.status = TrackTransaction.TransactionStatus.ON_HOLD.label
               
          # Increase retries and timeout 
          tracked_transaction.retry_times += 1
          tracked_transaction.timeout *= tracked_transaction.timeout_multiplier
          tracked_transaction.save()
          
          
          # If retries are more than max_retries, close the transaction
          if tracked_transaction.max_retries < tracked_transaction.retry_times:
               print("[Track Transaction] -> Transaction reached max retries exiting!")
               tracked_transaction.status = TrackTransaction.TransactionStatus.CLOSED.label
               tracked_transaction.reason = TrackTransaction.ClosedReason.RETRY_REACHED.label
               tracked_transaction.save()
               final_status.status = "failed"
               final_status.message = "Max retries reached"
               break
       
   return final_status          
       
       
           
    
    
       
   
   
   
    