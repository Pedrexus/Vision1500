from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from registration.forms import UpdateMyUserForm
from registration.models import MyUser
from .forms import PictureForm
from .models import Picture


@login_required
def user_home(request):
    return render(request, 'analysis/home.html')


@login_required
def user_data(request):
    data = {'this_user': request.user, 'user_model': MyUser}

    return render(request, 'analysis/data.html', data)


@login_required
def user_data_update(request):
    user = request.user
    form = UpdateMyUserForm(request.POST or None, instance=user)

    if form.is_valid():
        user.save()
        return redirect('user_data')

    data = {'this_user': user, 'form': form}
    return render(request, 'analysis/data_form.html', data)


@login_required
def user_pictures(request):
    data = {'my_pictures': Picture.objects.filter(user=request.user),
            'media_url': settings.MEDIA_URL}

    return render(request, 'analysis/pictures.html', data)


@login_required
def user_pictures_create(request):
    form = PictureForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        pic = form.save(commit=False)

        # preenchimento de campos baseado em dados de contexto:
        pic.user = request.user
        pic.save()

        return redirect('user_pics')

    return render(request, 'analysis/picture_form.html', {'pic_form': form})


def user_pictures_update(request, pic_id):
    pic = get_object_or_404(Picture, pk=pic_id)
    form = PictureForm(request.POST or None, request.FILES or None,
                       instance=pic)

    if form.is_valid():
        pic.save()
        return redirect('user_pics')

    return render(request, 'analysis/picture_form.html', {'pic_form': form})


def user_pictures_delete(request, pic_id):
    pic = get_object_or_404(Picture, pk=pic_id)
    if request.method == 'POST':
        pic.delete()
        return redirect('user_pics')

    return render(request, 'analysis/picture_delete.html',
                  {'this_pic': pic, 'media_url': settings.MEDIA_URL})


def user_pictures_report(request, pic_id):
    pass
