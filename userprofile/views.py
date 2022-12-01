from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, render,get_object_or_404,redirect
from django.urls import reverse
from userprofile.models import Address
from .forms import UserAddressForm
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from customerapp.forms import RegistrationForm
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

def edit_address(request,id):
    address=get_object_or_404(Address, id = id)
    address_form=UserAddressForm(request.POST or None,instance=address)
    if address_form.is_valid():
        address_form.save()
        return redirect('view_address')
    return render(request,'customerapp/add_address.html',
    {
        'form':address_form
    })


def delete_address(request,id):
    address=get_object_or_404(Address, id = id).delete()
    return redirect('view_address')

def edit_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    form=RegistrationForm(instance=user)
    if request.method =='POST':
        form=RegistrationForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('my_profile')

    
    return render(request,'customerapp/edit_details.html')