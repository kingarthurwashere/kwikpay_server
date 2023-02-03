from celery import shared_task



@shared_task(name='send_welcome_user_mail')
def tsk_send_welcome_message(username, user_email, scheme, host):
    send_welcome_user_mail(username, user_email, scheme, host)
    return "Email sent to {}".format(username)

@shared_task(name='send_reset_user_mail')
def tsk_send_password_reset(request, user_id, email):
    send_password_reset_mail(request, user_id, email)
    return "Reset email sent!"