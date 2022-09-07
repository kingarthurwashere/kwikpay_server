from transactions.models import AirtimeTransaction, ZesaTransactions
import json


def save_zesa_success_transaction(transaction_id, response):
    try:
        ZesaTransactions.objects.create(
            transaction_id=transaction_id,
            status=response["Status"],
            error_message=response["ErrorMessage"],
            agent_reference=response["AgentReference"],
            discount=response["Discount"],
            recharge_id=response["RechargeID"],
            reply_code=response["ReplyCode"],
            reply_message=response["ReplyMsg"],
            wallet_balance=response["WalletBalance"],
            meter=response["Meter"],
            address=response["Address"],
            account_name=response["AccountName"],
            tokens=json.dumps(response["Tokens"]),
        )
    except Exception as e:
        print(e)


def save_zesa_failed_transaction(transaction_id, response):
    try:
        ZesaTransactions.objects.create(
            transaction_id=transaction_id,
            status=response["Status"],
            error_message=response["ErrorMessage"],
        )
    except Exception as e:
        print(e)


def save_airtime_success_transaction(transaction_id, response):
    try:
        AirtimeTransaction.objects.create(
            transaction_id=transaction_id,
            status=response["Status"],
            amount=response["Amount"],
            error_message=response["ErrorMessage"],
            agent_reference=response["AgentReference"],
            data=response["Data"],
            discount=response["Discount"],
            final_balance=response["FinalBalance"],
            initial_balance=response["InitialBalance"],
            recharge_id=response["RechargeID"],
            reply_code=response["ReplyCode"],
            reply_message=response["ReplyMsg"],
            sms=response["SMS"],
            wallet_balance=response["WalletBalance"],
            window=response["Window"],
        )
    except Exception as e:
        print(e)


def save_airtime_failed_transaction(transaction_id, response):
    try:
        AirtimeTransaction.objects.create(
            transaction_id=transaction_id,
            status=response["Status"],
            error_message=response["ErrorMessage"],
        )
    except Exception as e:
        print(e)
