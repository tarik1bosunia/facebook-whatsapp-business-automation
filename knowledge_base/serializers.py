from rest_framework import serializers
from .models import Category, FAQ


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'category']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class FAQsWithCategorySerializer(serializers.ModelSerializer):
    faqs = FAQSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'faqs']