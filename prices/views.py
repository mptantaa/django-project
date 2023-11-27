from django.shortcuts import render
from .models import Categories, Prices
from collections import OrderedDict
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from history.models import History
from .serializers import (
    PricesSerializer, 
    PricesRetriveUpdateSerializer, 
    PricesCreateSerializer,
    CategoriesSerializer,
    CategoriesRetriveUpdateSerializer,
    CategoriesCreateSerializer,
)
import json
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .permissions import CanModeratePrices, CanModerateCategories
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

def prices(request):
    categories = Categories.objects.all()
    prices_by_category = {}

    for category in categories:
        prices = Prices.objects.filter(category=category)
        prices_by_category[category] = prices
    return render(request, "prices/prices.html", {'prices_by_category': prices_by_category})

def create_in_history(user_id, prices_id, prices_data):
    fields_json = json.dumps(
        {'prices': prices_data}, ensure_ascii=False
    )
    History.objects.create(
        user_id=user_id,
        action=History.ADD_FLAG,
        date=timezone.now(),
        content_type=ContentType.objects.get_for_model(Prices),
        object_id=prices_id,
        fields_json=fields_json
    )
def edit_in_history(user_id, prices_id, prices_data):
    if prices_data:
        fields_json = json.dumps(
            {'prices': prices_data}, ensure_ascii=False
        )
        History.objects.create(
            user_id=user_id,
            action=History.EDIT_FLAG,
            date=timezone.now(),
            content_type=ContentType.objects.get_for_model(Prices),
            object_id=prices_id,
            fields_json=fields_json,
        )

def get_changes(before, after):
    changes = {}
    for key, value_after in after.items():
        value_before = before and before.get(key)
        if value_after != value_before:
            changes[key] = value_after
    return changes


class PricesPagination(PageNumberPagination):
    page_size = 10
    page_sizer_query_param = 'paginate_by'
    max_page_size = 20

    def get_paginated_response(self, data):
        return Response(
            OrderedDict([
                ('last_page', self.page.paginator.num_pages),
                *list(data.items()),
            ])
        )


class PricesViewSet(viewsets.ModelViewSet):
    serializer_class = PricesSerializer
    permission_classes = (CanModeratePrices,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'unit', 'category']
    pagination_class = PricesPagination
    http_method_names = ('get', 'post', 'put', 'delete')
    

    def get_queryset(self):
        return Prices.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create']:
            return PricesCreateSerializer
        if self.action in ['retrieve', 'partial_update']:
            return PricesRetriveUpdateSerializer
        return PricesSerializer
    
    def get_changes(before, after):
        changes = {}
        for key, value_after in after.items():
            value_before = before and before.get(key)
            if value_after != value_before:
                changes[key] = value_after
        return changes

    def list(self, request, *args, **kwargs):
        data = dict()
        queryset = self.filter_queryset(self.get_queryset())

        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')

        if min_price and max_price:
            queryset = Prices.objects.filter(
                Q(price__gte=min_price) & Q(price__lte=max_price)
            )

        page = self.paginate_queryset(queryset)
        
        if page is not None:
            price = self.get_serializer(page, many=True).data
        else:
            price = self.get_serializer(queryset, many=True).data
        
        data['price'] = price
        return self.get_paginated_response(data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        prev_data = self.get_serializer(instance).data
        data = request.data.copy()
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        price = serializer.data
        changes = get_changes(prev_data, price)
        edit_in_history(request.user.id, instance.id, changes)
        return Response(price)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        create_in_history(
            request.user.id,
            serializer.data['id'],
            {k: serializer.data[k] for k in serializer.data}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        price = self.get_object()
        self.perform_destroy(price)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST'], detail=True)
    def replace_price(self, request, pk=None):
        price = self.get_object()
        new_price = request.data.get('new_price')
        if new_price is not None:
            price.price = new_price
            price.save()
            return Response()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class CategoriesViewSet(viewsets.ModelViewSet):
    serializer_class = CategoriesSerializer
    permission_classes = (CanModerateCategories,)
    pagination_class = PricesPagination
    http_method_names = ('get', 'post', 'put', 'delete')
    

    def get_queryset(self):
        return Categories.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create']:
            return CategoriesCreateSerializer
        if self.action in ['retrieve', 'partial_update']:
            return CategoriesRetriveUpdateSerializer
        return CategoriesSerializer
    
    def get_changes(before, after):
        changes = {}
        for key, value_after in after.items():
            value_before = before and before.get(key)
            if value_after != value_before:
                changes[key] = value_after
        return changes

    def list(self, request, *args, **kwargs):
        data = dict()
        queryset = self.filter_queryset(self.get_queryset())

        search_query = request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query))

        page = self.paginate_queryset(queryset)
        
        if page is not None:
            category = self.get_serializer(page, many=True).data
        else:
            category = self.get_serializer(queryset, many=True).data
        
        data['category'] = category
        return self.get_paginated_response(data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        prev_data = self.get_serializer(instance).data
        data = request.data.copy()
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        category = serializer.data
        changes = get_changes(prev_data, category)
        edit_in_history(request.user.id, instance.id, changes)
        return Response(category)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        create_in_history(
            request.user.id,
            serializer.data['id'],
            {k: serializer.data[k] for k in serializer.data}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        price = self.get_object()
        self.perform_destroy(price)
        return Response(status=status.HTTP_204_NO_CONTENT)