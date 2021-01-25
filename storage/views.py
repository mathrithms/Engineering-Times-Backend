from django.shortcuts import render
from .forms import StoreForm
# Create your views here.


def store_view(request):
    context = {}
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

        else:
            context['form'] = form
    else:
        form = StoreForm()
        context['form'] = form

    return render(
        request,
        template_name='storage/store.html',
        context=context
    )
