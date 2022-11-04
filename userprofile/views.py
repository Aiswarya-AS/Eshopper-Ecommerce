from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from userprofile.models import Address
from .forms import UserAddressForm
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='login-page')
def view_address(request):
    address=Address.objects.filter(user=request.user)

    return render(request,'customerapp/profile.html',{
        'address':address
    })
@login_required(login_url='login-page')
def add_address(request):
    address_form=UserAddressForm()
    if request.method=='POST':
        address_form=UserAddressForm(data=request.POST)
        if address_form.is_valid:
            address_form=address_form.save(commit=False)
            address_form.user=request.user
            address_form.save()
            return HttpResponseRedirect(reverse('view_address'))
        else:
            address_form=UserAddressForm()
    return render(request,'customerapp/add_address.html',{
        'form':address_form
    })