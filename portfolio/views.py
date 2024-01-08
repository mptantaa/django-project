from django.shortcuts import render, get_object_or_404
from collections import OrderedDict
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from history.models import History
from .models import Portlofios
from .serializers import PortlofiosSerializer, PortlofiosRetriveUpdateSerializer, PortlofiosCreateSerializer
import json
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .permissions import CanModeratePortfolios
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.
def portfolio(request):
    portfolios = Portlofios.objects.all()
    return render(request, "portfolio/portfolio.html", {'portfolios': portfolios})

def portfolio_detail(request, object_id):
    object = get_object_or_404(Portlofios, pk=object_id)
    return render(request, 'portfolio/object.html', {'object': object})

def create_in_history(user_id, portfolio_id, portfolio_data):
    fields_json = json.dumps(
        {'portfolio': portfolio_data}, ensure_ascii=False
    )
    History.objects.create(
        user_id=user_id,
        action=History.ADD_FLAG,
        date=timezone.now(),
        content_type=ContentType.objects.get_for_model(Portlofios),
        object_id=portfolio_id,
        fields_json=fields_json
    )
def edit_in_history(user_id, portfolio_id, portfolio_data):
    if portfolio_data:
        fields_json = json.dumps(
            {'portfolio': portfolio_data}, ensure_ascii=False
        )
        History.objects.create(
            user_id=user_id,
            action=History.EDIT_FLAG,
            date=timezone.now(),
            content_type=ContentType.objects.get_for_model(Portlofios),
            object_id=portfolio_id,
            fields_json=fields_json,
        )

def get_changes(before, after):
    changes = {}
    for key, value_after in after.items():
        value_before = before and before.get(key)
        if value_after != value_before:
            changes[key] = value_after
    return changes


class PortlofiosPagination(PageNumberPagination):
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


class PortfoliosViewSet(viewsets.ModelViewSet):
    serializer_class = PortlofiosSerializer
    permission_classes = (CanModeratePortfolios,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'unit']
    pagination_class = PortlofiosPagination
    http_method_names = ('get', 'post', 'put', 'delete')
    

    def get_queryset(self):
        return Portlofios.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create']:
            return PortlofiosCreateSerializer
        if self.action in ['retrieve', 'partial_update']:
            return PortlofiosRetriveUpdateSerializer
        return PortlofiosSerializer
    
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
            portfolio = self.get_serializer(page, many=True).data
        else:
            portfolio = self.get_serializer(queryset, many=True).data
        
        data['portfolio'] = portfolio
        return self.get_paginated_response(data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        prev_data = self.get_serializer(instance).data
        data = request.data.copy()
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        portfolio = serializer.data
        changes = get_changes(prev_data, portfolio)
        edit_in_history(request.user.id, instance.id, changes)
        return Response(portfolio)

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
        portfolio = self.get_object()
        self.perform_destroy(portfolio)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST'], detail=True)
    def replace_description(self, request, pk=None):
        portfolio = self.get_object()
        new_description = request.data.get('new_description')
        if new_description is not None:
            portfolio.description = new_description
            portfolio.save()
            return Response()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    