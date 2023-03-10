from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from market.models import Car, Order, Payment


def show_cars(request: HttpRequest) -> HttpResponse:
    context = {
        "cars": Car.objects.all()
    }
    return render(request, "cars.html", context)


def audi_purchase(request: HttpRequest, id_: int) -> HttpResponse:
    car = Car.objects.filter(id=id_).first()

    if request.method == "POST":
        order = Order.objects.create(
            car=car,
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
        )

        # добавил здесь payment = ...
        # чтобы показать, как получить созданный объект
        # он сейчас не используется, но вы должны его использовать
        payment = Payment.objects.create(
            order=order,
            amount=order.car.price,
            # credit_card=request.POST.get("credit_card"),
        )
        return HttpResponseRedirect(f"/payment_form/{payment.id}")

    return render(request, "purchase_form.html", {"car": car})


def payment(request:HttpRequest, payment_id_: int) -> HttpResponse:
    payment = Payment.objects.filter(id=payment_id_).first()
    if request.method == "POST":
        payment.credit_card = request.POST.get("credit_card")
        payment.save(update_fields=["credit_card"])
        return HttpResponseRedirect(f"/")
    return render(request, "payment_form.html", {"car" : payment.order.car}) #, {"car": car}