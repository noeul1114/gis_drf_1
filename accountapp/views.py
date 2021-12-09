from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def hello_world(request):

    if request.method == 'POST':
        input_data = request.POST.get('input_data')

        return render(request, 'accountapp/hello_world.html', context={'message': input_data})

    return render(request, 'accountapp/hello_world.html')
