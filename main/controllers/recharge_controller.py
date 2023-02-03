


from main.models import Package, Setting
from django.shortcuts import render
from main.libraries.hot_recharge import HotRechargeZW
from django.http import JsonResponse
from app_utils.helpers import get_page_seo

try:
    zwl_rate = int(Setting.objects.get(name="USD_TO_ZWL_RATE").value)
except Setting.DoesNotExist:
    zwl_rate = 120

def check_zesa_customer(request):
    if request.method == "POST":
        meter_number = request.POST.get('meter_number')
        status = ""
        
        try:
            hot_recharge = HotRechargeZW()
            response = hot_recharge.checkZesaCustomer(meter_number)
            status = "success"
        except Exception as e:
            status = "fail"
            response = e.__str__()
        
        return JsonResponse({
            "status" :status,
            "data"   : response
        })

def recharge(request):
    packages = Package.objects.all()
    page_seo = get_page_seo("recharge")
    
    for package in packages:
        package.zwl_amount = package.package_price * zwl_rate
    
    return render(request, 'main/recharge.html', {
        'packages': packages,
        'seo': page_seo
    })
    
def recharge_bill(request):
    page_seo = get_page_seo("recharge_bill")
    return render(request, 'main/bill/rechargebill.html', {
        'packages': Package.objects.all(), 
        'seo': page_seo
    })