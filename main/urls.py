from django.urls import path
from .controllers import paypal_controller, general_controller
from .controllers import stripe_controller, payment_controller, order_controller, recharge_controller, profile_controller


urlpatterns =[   
 
 
 # Profile
  path("user-profile", profile_controller.user_profile, name="user-profile"),
  path("user-orders", profile_controller.user_orders, name="user-orders"),
  path("user-password", profile_controller.user_password, name="user-password"),
  
 # Recharge
  path("zesa-check-customer", recharge_controller.check_zesa_customer, name="check_zesa_customer"),
  path("recharge", recharge_controller.recharge, name="recharge"),
  path("recharge-bill", recharge_controller.recharge_bill, name="recharge_bill"),
 
 # Order
 path("recharge-order-summary/<int:order_id>", order_controller.recharge_order_summary, name="recharge-order-summary"),
 path("create-airtime-order", order_controller.create_airtime_order, name="create-airtime-order"),
 path("create-zesa-order", order_controller.create_zesa_order, name="create-zesa-order"),
 
#  Payment URLs
 path("payment/<int:order_id>", paypal_controller.paypal_payment, name="payment"),
 path("recharge-successful", payment_controller.recharge_successful, name="recharge-successful"),
 path("payment-done/<int:order_id>", payment_controller.recharge_successful, name="payment-done"),
path("payment-cancelled/<int:order_id>", payment_controller.recharge_failed, name="payment-cancelled"),
path("check-payment-status", payment_controller.check_payment_status, name="check-payment-status"),

# Paypal URLs
path("paypal-notify/<int:order_id>", paypal_controller.paypal_notify, name="paypal-notify"),

# Stripe URLs
path("get-stripe-session", stripe_controller.get_stripe_session, name="get-stripe-session"),
path("webhooks/stripe", stripe_controller.stripe_webhooks, name="stripe-webhooks"),

# General URLs
 path("remove-alerts", general_controller.remove_alerts, name="remove-alerts"),


]