from django.db.models import Q
from rest_framework import viewsets
from .models import Category, FAQ
from .serializers import CategorySerializer, FAQSerializer, FAQsWithCategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    pagination_class = None


class FAQsWithCategoriesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FAQsWithCategorySerializer
    pagination_class = None

    def get_queryset(self):
        search = self.request.query_params.get('search', '')
        queryset = Category.objects.prefetch_related('faqs')

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(faqs__question__icontains=search) |
                Q(faqs__answer__icontains=search)
            ).distinct()

        return queryset