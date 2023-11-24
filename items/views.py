from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from items.models import Item
from items.serializers import ItemSerializer
from rest_framework import serializers
from rest_framework import status
from django.db.models import Sum

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def items(request):
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def summary(request):
    total_cost = Item.objects.aggregate(Sum('price'))['price__sum'] or 0

    count_of_items = Item.objects.count()

    return Response(f"There are {count_of_items} items in the basket with a total cost of £ {total_cost:.2f}")

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add(request):
    item = ItemSerializer(data=request.data)
    item_name = request.data["name"]
    if Item.objects.filter(name=item_name).exists():
        raise serializers.ValidationError(
            "Item with the same name already exists. Pleae use update"
        )

    if item.is_valid():
        item.save()
        return Response(item.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

    
@api_view(["PUT"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update(request, pk):
    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    item_name = request.data["name"]
    if Item.objects.filter(name=item_name).exclude(pk=pk).exists():
        raise serializers.ValidationError("Item with the same name already exists")

    item_serializer = ItemSerializer(item, data=request.data)
    if item_serializer.is_valid():
        item_serializer.save()
        return Response(item_serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete(request, pk):
    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
