from django.http import HttpResponse
from django.shortcuts import render, redirect
from food.models import Food


def index(request):

    #return render(request, 'index.html')
    if request.method == 'POST':
        Food.objects.create(text=request.POST['item_text'])
        return redirect('/')

    items = Food.objects.all()
    return render(request, 'index.html', {'items': items})
    '''
    food = Food()
    food.name = request.POST.get('item_text', '')
    food.save()

    return render(request, 'index.html', {
        'new_item_text': request.POST.get('item_text', ''),
    })
    '''
