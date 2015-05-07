# -*- coding: latin-1 -*-

from principal.models import CoinHistory


def list_coin_history_traveller(id_traveller):
    coin_history = CoinHistory.objects.all().filter(traveller=id_traveller).order_by('-date')
    return coin_history
