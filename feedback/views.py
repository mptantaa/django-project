from django.shortcuts import render, redirect
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from collections import OrderedDict
from .forms import FeedbacksForm
from history.models import History
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Contacts, Feedbacks
from .serializers import FeedbacksSerializer
from .permissions import CanModerateFeedbacks
import json
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import FeedbacksSerializer, FeedbacksRetriveUpdateSerializer, FeedbacksCreateSerializer
from datetime import timedelta
from rest_framework.filters import SearchFilter

# Create your views here.
def feedback(request):
    error = ''
    if request.method == 'POST':
        form = FeedbacksForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else: 
            error = 'Ошибка при заполнении'
    form = FeedbacksForm
    contacts = Contacts.objects.all()
    return render(request, 'feedback/feedback.html', {'form': form, 'error': error, 'contacts': contacts})

def create_in_history(user_id, feedback_id, feedback_data):
    fields_json = json.dumps(
        {'feedback': feedback_data}, ensure_ascii=False
    )
    History.objects.create(
        user_id=user_id,
        action=History.ADD_FLAG,
        date=timezone.now(),
        content_type=ContentType.objects.get_for_model(Feedbacks),
        object_id=feedback_id,
        fields_json=fields_json
    )
def edit_in_history(user_id, feedback_id, feedback_data):
    if feedback_data:
        fields_json = json.dumps(
            {'feedbacks': feedback_data}, ensure_ascii=False
        )
        History.objects.create(
            user_id=user_id,
            action=History.EDIT_FLAG,
            date=timezone.now(),
            content_type=ContentType.objects.get_for_model(Feedbacks),
            object_id=feedback_id,
            fields_json=fields_json,
        )

def get_changes(before, after):
    changes = {}
    for key, value_after in after.items():
        value_before = before and before.get(key)
        if value_after != value_before:
            changes[key] = value_after
    return changes

class FeedbacksPagination(PageNumberPagination):
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
    
class FeedbacksViewSet(viewsets.ModelViewSet):
    serializer_class = FeedbacksSerializer
    permission_classes = (CanModerateFeedbacks,)
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name', 'phone']
    search_fields = ['name', 'message']
    pagination_class = FeedbacksPagination
    http_method_names = ('get', 'post', 'put', 'delete')
    

    def get_queryset(self):
        return Feedbacks.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create']:
            return FeedbacksCreateSerializer
        if self.action in ['retrieve', 'partial_update']:
            return FeedbacksRetriveUpdateSerializer
        return FeedbacksSerializer
    
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

        days = request.query_params.get('days', None)
        name_starts = request.query_params.get('name_starts', None)
        phone_have = request.query_params.get('phone_have', None)
        message = request.query_params.get('message', None)
        if (days != None and name_starts != None and phone_have != None and message != None):
            filter_date = timezone.now() - timedelta(days=int(days))
            queryset = self.filter_queryset(self.get_queryset()).filter(
                Q(created_at__gte=filter_date) &
                (Q(name__startswith=name_starts) | Q(phone__icontains=phone_have)) &
                ~Q(message__icontains=message)
            )
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            feedbacks = self.get_serializer(page, many=True).data
        else:
            feedbacks = self.get_serializer(queryset, many=True).data
        
        data['feedbacks'] = feedbacks
        return self.get_paginated_response(data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        prev_data = self.get_serializer(instance).data
        data = request.data.copy()
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        feedbacks = serializer.data
        changes = get_changes(prev_data, feedbacks)
        edit_in_history(request.user.id, instance.id, changes)
        return Response(feedbacks)

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
        feedbacks = self.get_object()
        self.perform_destroy(feedbacks)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'], detail=False)
    def filter_by_date(self, request):
        days = request.query_params.get('days', None)
        if days:
            filter_date = timezone.now() - timedelta(days=int(days))
            queryset = self.filter_queryset(self.get_queryset()).filter(created_at__gte=filter_date)
            feedbacks = self.get_serializer(queryset, many=True).data
            if feedbacks:
                return Response({'feedbacks': feedbacks})
            else:
                return Response({'error': 'not found'}, status=404)
        else:
            return Response({'error': 'Invalid date'}, status=status.HTTP_400_BAD_REQUEST)
