from django.http import JsonResponse

def remove_alerts(request):
    
    if 'success_messages' in request.session.keys():
        del request.session['success_messages']
        
    if 'error_messages' in request.session.keys():
        del request.session['error_messages']
        
    return JsonResponse({"status": "success", "message": "Alerts removed"})

