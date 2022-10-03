from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from .models import Contractor
from customuser.models import User_Account


@login_required(login_url='/signin/')
def contractors_list(request):

    user_account = User_Account.objects.get(owner=request.user)

    if request.method == 'POST':
        contractor_name = request.POST.get('contractor_name')
        try:
            new_contractor = Contractor.objects.create(contractor_name=contractor_name, user_account=user_account)
        except Exception:
            pass
        return redirect('contractors:contractors')
    else:
        contractors = Contractor.objects.filter(user_account=user_account)
        return render(request, 'contractors/contractors.html', {'contractors': contractors})


@login_required(login_url='/signin/')
def delete_contractor(request):
    if request.method == 'POST':
        contractor_uid = request.POST.get('uid')
        user_account = User_Account.objects.get(owner=request.user)

        contractor = Contractor.objects.filter(user_account=user_account, uid=contractor_uid)

        if contractor:
            contractor[0].delete()
            return JsonResponse({}, status=200)
        else:
            return HttpResponseRedirect('/bad_request/')


@login_required(login_url='/signin/')
def contractor_edit(request, contr_uid):

    user_account = User_Account.objects.filter(owner=request.user)[0]
    contractor = Contractor.objects.filter(user_account=user_account, uid=contr_uid)

    if request.method == 'POST':
        contractor_name = request.POST.get('contractor_name')
        contractor.update(contractor_name=contractor_name)
        return HttpResponseRedirect(f'/contractors/{contr_uid}/')
    else:
        return render(request, 'contractors/contractor_edit.html', {'contractor': contractor[0]})
