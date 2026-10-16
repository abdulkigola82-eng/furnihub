from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods, require_POST

from .seller_forms import SellerRegistrationForm
from .seller_models import SellerProfile


@require_http_methods(["GET", "POST"])
def seller_register(request):
    if request.user.is_authenticated:
        try:
            request.user.seller_profile
        except SellerProfile.DoesNotExist:
            pass
        else:
            return redirect("seller_dashboard")

    if request.method == "POST":
        form = SellerRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            SellerProfile.objects.create(
                user=user,
                business_name=form.cleaned_data["business_name"],
                phone=form.cleaned_data["phone"],
                approved=False,
            )

            messages.success(
                request,
                "Usajili umekamilika. Subiri msimamizi aidhinishe akaunti yako.",
            )
            return redirect("seller_login")
    else:
        form = SellerRegistrationForm()

    return render(
        request,
        "store/seller_register.html",
        {"form": form},
    )


@require_http_methods(["GET", "POST"])
def seller_login(request):
    if request.user.is_authenticated:
        try:
            request.user.seller_profile
        except SellerProfile.DoesNotExist:
            return redirect("home")
        return redirect("seller_dashboard")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect("seller_dashboard")
    else:
        form = AuthenticationForm(request)

    return render(
        request,
        "store/seller_login.html",
        {"form": form},
    )


def seller_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("seller_login")

    try:
        profile = request.user.seller_profile
    except SellerProfile.DoesNotExist:
        messages.error(
            request,
            "Akaunti hii haina wasifu wa muuzaji. Tafadhali jisajili kama muuzaji.",
        )
        return redirect("home")

    return render(
        request,
        "store/seller_dashboard.html",
        {"seller": profile},
    )


@require_POST
def seller_logout(request):
    logout(request)
    return redirect("seller_login")


@require_http_methods(["GET", "POST"])
def seller_add_product(request):
    if not request.user.is_authenticated:
        return redirect("seller_login")

    try:
        profile = request.user.seller_profile
    except SellerProfile.DoesNotExist:
        messages.error(request, "Tafadhali jisajili kama muuzaji.")
        return redirect("home")

    if not profile.approved:
        messages.error(request, "Akaunti yako inasubiri idhini ya msimamizi.")
        return redirect("seller_dashboard")

    from .forms import SellerProductForm

    if request.method == "POST":
        form = SellerProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = profile
            product.save()
            messages.success(request, "Bidhaa imeongezwa kikamilifu.")
            return redirect("seller_dashboard")
    else:
        form = SellerProductForm()

    return render(
        request,
        "store/seller_add_product.html",
        {"form": form, "seller": profile},
    )
