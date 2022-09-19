from django.shortcuts import render


def invoice(request):
    return render(request, 'invoice/invoice.html', {})
