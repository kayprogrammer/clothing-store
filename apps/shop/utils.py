def get_session_key(request):
    if not request.user.is_authenticated:
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
        return session_key
    return None


def sort_products(request, products):
    filter_value = request.GET.get("filter")
    if filter_value and (filter_value == "featured" or filter_value == "flash_deals"):
        filter_data = {filter_value: True}
        products = products.filter(**filter_data)
    return products


def sort_filter_value(request, context):
    filter_value = request.GET.get("filter")
    context["filter_value"] = filter_value
    if filter_value:
        context["post_param"] = f"&filter={filter_value}"
    return context
