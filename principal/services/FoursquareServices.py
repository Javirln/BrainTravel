# -*- coding: latin-1 -*-

import foursquare

from principal.models import Category


_client_id = "TWYKUP301GVPHIAHBPYFQQT0PJGZ0O2B24HQ3RUGLUFSLP1E"
_client_secret = "TDNQ441CNLDJZKC3UJYDERT2MNDWN1E2CX1550CW1OXPEST2"
client = None


def init_fs():
    # Construct the client object
    global client
    client = foursquare.Foursquare(client_id=_client_id, client_secret=_client_secret)


def categories_initializer():
    """This functions belongs to populate_db but since there is no instance
     of Foursquare there, this function will be used."""
    categories = client.venues.categories()
    Category.objects.all().delete()
    for row in categories['categories']:
        cat = Category(
            id_foursquare=row['id'],
            name=row['pluralName']
        )
        cat.save()
        for child in row['categories']:
            cat1 = Category(
                id_foursquare=child['id'],
                name=child['pluralName']
            )
            cat1.save()
            for grand_child in child['categories']:
                cat2 = Category(
                    id_foursquare=grand_child['id'],
                    name=grand_child['pluralName']
                )
                cat2.save()


# devuelve: un dict,con una lista llamada groups, que contiene un dict, qe contiene lista llamada items ordenada x rating
def search_by_category(city, category):
    # A term to be searched against a venue's tips, category, etc.
    response = client.venues.explore(params={'near': city, 'query': category})
    print(response)


# devuelve lista ordenada por rating (hay que asegurarse mas)
def search_by_section(city, section):
    # section = One of food, drinks, coffee, shops, arts, outdoors, sights, trending or specials, nextVenues
    # (venues frequently visited after a given venue)
    # or topPicks (a mix of recommendations generated without a query from the user).
    response = client.venues.explore(params={'near': city, 'section': section})
    print(response)
