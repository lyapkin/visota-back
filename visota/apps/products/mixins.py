from django.db.models import Q


class FilterMixin():
  def filter(self, queryset):
    query_params = self.request.query_params

    pks = query_params.getlist('pk')
    if pks is not None and len(pks) > 0:
        return queryset.filter(pk__in=pks)

    price_min = query_params.get('price_min')
    price_max = query_params.get('price_max')
    price_min_valid = True
    price_max_valid = True

    try:
        price_min = int(price_min)
    except:
        price_min_valid = False

    try:
        price_max = int(price_max)
    except:
        price_max_valid = False


    if price_max_valid and price_min_valid:
        queryset = queryset.filter(current_price__range=[price_min, price_max])
    elif price_max_valid:
        queryset = queryset.filter(current_price__lte=price_max)
    elif price_min_valid:
        queryset = queryset.filter(current_price__gte=price_min)

    searchline = query_params.get('search')
    searchline = searchline.strip() if isinstance(searchline, str) else None
    if searchline is not None:
        searchline = searchline.split()
        queryset = queryset.filter(*[Q(translations__name__icontains=q) for q in searchline])

    return queryset
