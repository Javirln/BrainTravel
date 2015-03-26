from principal.models import Payment, Traveller
from datetime import datetime



def save(payment):
    payment.save()


def create(id_traveller, amount):
    payment = Payment(traveller = Traveller.objects.get(id=id_traveller),
                      amount = amount,
                      date = datetime.now())
    return payment
    