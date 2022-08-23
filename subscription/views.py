from django.shortcuts import render
from django.contrib import messages


def subscription_view(request):
    return render(request, 'subscription/subscription.html', {})
