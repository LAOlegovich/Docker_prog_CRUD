from rest_framework import serializers
from .models import Product,StockProduct,Stock
from django.db import IntegrityError
from rest_framework.exceptions import APIException, ValidationError
from rest_framework import status


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title','description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product','quantity','price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address','positions']

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # addr = validated_data.pop('address')
        # if Stock.objects.filter(address = addr).exists():
        #     return Stock.objects.filter(address = addr)
        # else:
            
       
        # создаем склад по его параметрам
        #stock = super().create(validated_data)

        stock = Stock.objects.create(**validated_data)
                                             
        for position in positions:
            product = position['product']
            quantity = position['quantity']
            price = position['price']
            StockProduct.objects.create(product = product,  stock = stock,
                                            quantity = quantity, 
                                            price = price)
                                                                                                                       
        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        for position in positions:
            product = position['product']
            quantity = position['quantity']
            price = position['price']
            stock_product = StockProduct.objects.filter(stock = stock, product = product)

            if stock_product.exists():
                dictionary = dict(quantity = stock_product.get().quantity + quantity,
                                 price = price)
            else:
                dictionary = dict(quantity = quantity, price = price)

            StockProduct.objects.update_or_create(stock = stock, product = product,
                                                  defaults = dictionary)
                

       
        return stock
