from django.shortcuts import render, redirect
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from django.conf import settings

def start_payment(request):
    tx = Transaction(WebpayOptions(
        commerce_code=settings.TRANSBANK['COMMERCE_CODE'],
        api_key=settings.TRANSBANK['API_KEY_SECRET'],
        integration_type=settings.TRANSBANK['MODO']
    ))

    amount = 10000  # Ejemplo de monto, puedes cambiar esto según tus necesidades
    buy_order = "orden12345"  # Número de orden único
    session_id = "sesion12345"  # ID de sesión
    return_url = request.build_absolute_uri('/payments/return/')

    response = tx.create(buy_order, session_id, amount, return_url)

    return redirect(response['url'] + '?token_ws=' + response['token'])

def return_from_payment(request):
    token = request.GET.get('token_ws')

    tx = Transaction(WebpayOptions(
        commerce_code=settings.TRANSBANK['COMMERCE_CODE'],
        api_key=settings.TRANSBANK['API_KEY_SECRET'],
        integration_type=settings.TRANSBANK['MODO']
    ))

    response = tx.commit(token)

    if response['response_code'] == 0:
        # El pago fue exitoso
        return redirect('/payments/finalize/?token_ws=' + token)
    else:
        # El pago falló
        return render(request, 'payments/failure.html', {'response': response})

def finalize_payment(request):
    token = request.GET.get('token_ws')

    tx = Transaction(WebpayOptions(
        commerce_code=settings.TRANSBANK['COMMERCE_CODE'],
        api_key=settings.TRANSBANK['API_KEY_SECRET'],
        integration_type=settings.TRANSBANK['MODO']
    ))

    response = tx.status(token)

    if response['status'] == 'AUTHORIZED':
        # El pago fue autorizado
        return render(request, 'payments/success.html', {'response': response})
    else:
        # El pago no fue autorizado
        return render(request, 'payments/failure.html', {'response': response})

def payment_button(request):
    return render(request, 'payments/payment_button.html')