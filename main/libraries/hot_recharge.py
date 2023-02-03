import hotrecharge
from hotrecharge.HotRechargeException import *
from kwikpay_server import settings

config = hotrecharge.HRAuthConfig(
            access_code=settings.HOT_RECHARGE_EMAIL, 
            access_password=settings.HOT_REACHARGE_PASSWORD, 
            reference="random-ref"
        )
        
# TODO: Finish implementing HotRecharge class
        
class HotRechargeZW(hotrecharge.HotRecharge):
    def __init__(self):
        super(HotRechargeZW, self).__init__(config)
        
        
    def get_curret_evds(self):
        try:
            evds = self.getEVDs()
            return len(evds.InStock)
        except hotrecharge.HotRechargeException as e:
            print("[-] There was an error: ", e.__str__())
            
            
    def recharge_bundles(self, phone_number, bundle_product_code):
        try:
            # option message to send to user
            customer_sms =  " Amount of %AMOUNT% for data %BUNDLE% recharged! " \
                            " %ACCESSNAME%. The best %COMPANYNAME%!"

            # need to update reference manually, if `use_random_ref` is set to False
            self.updateReference('<new-random-string>')
            response = self.dataBundleRecharge(product_code=bundle_product_code, number=phone_number, mesg=customer_sms)

            print(response)

        except Exception as ex:
            print(f"There was a problem: {ex}")
            
            
            
    
    def recharge_pinless(self, phone_number, amount):
        try:
            customer_sms = "Recharge of %AMOUNT% successful" \
                        "Initial balance $%INITIALBALANCE%" \
                        "Final Balance $%FINALBALANCE%" \
                        "%COMPANYNAME%"


            response = self.rechargePinless(amount=amount, number=phone_number, mesg=customer_sms)
            status = "success"
            
            if (type(response) == dict):
                response = Munch(response)
            elif (type(response) == Munch):
                pass
                
            
        except (WebServiceException, ServiceError) as err:
            response = e.response
            status = "down"
        except hotrecharge.InvalidContact as e:
            response = err.response
            status = "invalid_contact"
        except hotrecharge.RechargeAmountLimit as e:
            response = e.response
            status = "limit_error"
        except hotrecharge.PrepaidPlatformFail as e:
            response = err.response
            status = "wrong_number_or_network"
        except hotrecharge.InsufficientBalance as e:
            response = e.response
            status = "insufficient_balance"
        except HotRechargeException as e:
            response = e.response
            status = "error"
        
           
        response["Status"] = status 
        return response
        
    def recharge_zesa(self, zesa_amount, mobile_number, meter_number):
        status = ""
        try:
            response = self.rechargeZesa(zesa_amount, mobile_number, meter_number)
            status = "success"
            
            if (type(response) == dict):
                response = Munch(response)
            elif (type(response) == Munch):
                pass
        except PendingZesaTransaction as err:
            response = err.response
            status = "pending"
        except (WebServiceException, ServiceError) as err:
            response = err.response
            status = "down"
        except HotRechargeException as err:
            response = err.response
            status = "error"
            
        response["Status"] = status
        return response
    

    def query_zesa_transaction(self, recharge_id):
        status = ""
        try:
            response = self.queryZesaTransaction(recharge_id)
            status = "success"
        except PendingZesaTransaction as err:
            response = err.response
            status = "pending"
        except (WebServiceException, ServiceError) as err:
            response = err.response
            status = "down"
        except HotRechargeException as err:
            response = err.response
            status = "error"
           
        response["Status"] = status 
        return response

            
            

            
    def get_zesa_customer(self,meter_number):
        try: 
            zesa_customer = self.checkZesaCustomer(meter_number)
            return zesa_customer

        except Exception as err:
            print('[ERROR] Error getting zesa customer: ', err)
     