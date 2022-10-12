from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Contractor
from customuser.models import User_Account
from .forms import ContractorForm
from django.db import IntegrityError


@login_required(login_url='/signin/')
def contractors_list(request):

    user_account = User_Account.objects.get(owner=request.user)
    contractors = Contractor.objects.filter(user_account=user_account)

    if request.method == 'POST':
        form = ContractorForm(request.POST)
        if form.is_valid():
            form.instance.user_account = user_account

            try:
                form.save()
            except IntegrityError:
                form.add_error('contractor_name', 'Contractor with this name already exists')
    else:
        form = ContractorForm()

    context = {'contractors': contractors, 'form': form}

    return render(request, 'contractors/contractors.html', context)


@login_required(login_url='/signin/')
def contractor_edit(request, contr_uid):

    user_account = User_Account.objects.get(owner=request.user)
    contractor = Contractor.objects.get(user_account=user_account, uid=contr_uid)

    if request.method == 'POST':
        form = ContractorForm(request.POST, instance=contractor)
        if form.is_valid():

            try:
                form.save()
            except IntegrityError:
                form.add_error('contractor_name', 'Contractor with this name already exists')
            else:
                return redirect('contractors:contractor_edit', contractor.uid)

    else:
        form = ContractorForm(instance=contractor)

    context = {'contractor': contractor, 'form': form}

    return render(request, 'contractors/contractor_edit.html', context)


@login_required(login_url='/signin/')
def delete_contractor(request):
    if request.method == 'POST':
        Contractor.objects.filter(
            user_account=User_Account.objects.get(owner=request.user), uid=request.POST.get('uid')).delete()
        return JsonResponse({}, status=200)
