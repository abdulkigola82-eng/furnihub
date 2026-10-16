from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Product, Order


def home(request):
    products = Product.objects.filter(available=True)
    return render(request, "store/home.html", {"products": products})


@require_http_methods(["GET", "POST"])
def order_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id, available=True)

    if request.method == "POST":
        customer_name = request.POST.get("customer_name", "").strip()
        customer_phone = request.POST.get("customer_phone", "").strip()
        customer_address = request.POST.get("customer_address", "").strip()
        color = request.POST.get("color", "other")
        fabric = request.POST.get("fabric", "").strip()
        notes = request.POST.get("notes", "").strip()

        try:
            quantity = int(request.POST.get("quantity", "1"))
        except (TypeError, ValueError):
            quantity = 0

        valid_colors = {choice[0] for choice in Order.COLOR_CHOICES}

        if not customer_name or not customer_phone or not customer_address:
            messages.error(request, "Tafadhali jaza jina, simu na anwani.")
        elif len(customer_phone) > 20:
            messages.error(request, "Namba ya simu ni ndefu sana.")
        elif color not in valid_colors:
            messages.error(request, "Tafadhali chagua rangi sahihi.")
        elif not fabric:
            messages.error(request, "Tafadhali jaza aina ya kitambaa.")
        elif quantity < 1 or quantity > 100:
            messages.error(request, "Idadi lazima iwe kati ya 1 na 100.")
        else:
            order = Order.objects.create(
                product=product,
                customer_name=customer_name,
                customer_phone=customer_phone,
                customer_address=customer_address,
                color=color,
                fabric=fabric,
                quantity=quantity,
                unit_price=product.price,
                notes=notes,
            )
            request.session["last_order_id"] = order.id
            return redirect("order_success", order_id=order.id)

    return render(request, "store/order_form.html", {"product": product, "product_order_colors": Order.COLOR_CHOICES})


def order_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, "store/order_success.html", {"order": order})


def product_detail(request, product_id):
    product = get_object_or_404(
        Product,
        pk=product_id,
        available=True,
    )
    return render(
        request,
        "store/product_detail.html",
        {"product": product},
    )
