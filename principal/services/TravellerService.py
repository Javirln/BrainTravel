# -*- coding: latin-1 -*-
from django.contrib.auth.models import Permission

from principal.models import Traveller


def create(form):
    
    res = Traveller(first_name=form.cleaned_data['first_name'],
                    email=form.cleaned_data['email'],
                    username=form.cleaned_data['email'])
    res.is_active = False
    return res


def save(traveller):
    traveller.save()
    #Es necesario guardar primero el traveller para poder asignar los permisos
    traveller.user_permissions.add(Permission.objects.get(codename="traveller"))


# author: Juane
def find_one(traveller_id):
    try:
        traveller = Traveller.objects.get(id=traveller_id)
    except Traveller.DoesNotExist:
        assert False

    return traveller


# author: Juane
def construct_password(traveller_id, form):
    traveller = find_one(traveller_id)
    assert traveller.has_perm('principal.traveller')
    assert str(form.cleaned_data['id']) == str(traveller.id)
    traveller.set_password(form.cleaned_data['password'])
    return traveller


# author: Juane
def construct_profile(traveller_id, form):
    traveller = find_one(traveller_id)
    assert traveller.has_perm('principal.traveller')
    assert str(form.cleaned_data['id']) == str(traveller.id)
    traveller.first_name = form.cleaned_data['first_name']
    traveller.last_name = form.cleaned_data['last_name']
    traveller.genre = form.cleaned_data['genre']
    if form.cleaned_data['photo_clear']:
        traveller.photo = "static/user_folder/default.jpg"
    elif form.cleaned_data['photo']:
        traveller.photo = form.cleaned_data['photo']
    return traveller