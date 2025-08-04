def user_orders_count(request):
    orders_count = 0
    if request.user.is_authenticated:
        orders_count = request.user.order_set.count()

    return {"user_orders_count": orders_count}
