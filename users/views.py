from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import RegistrationForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('users/login/')
    else:
        form = RegistrationForm()

    return render(request, 'users/register.html', {'form': form})
