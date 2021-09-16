from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated

from api.serializers import OrderSerializer, StockSerializer
from api.services import TradeService


class OrderView(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = OrderSerializer(data=data)

        serializer.is_valid(raise_exception=True)
        input_data = serializer.data

        TradeService().create_order(
            user=request.user, 
            stock_id=input_data["stock_id"], 
            quantity=input_data["quantity"], 
            action=input_data["action"]
        )

        return Response(status=201)

    def get_total_value_by_user_and_stock(self, request, user_id, stock_id):
        total = TradeService().get_total_value_by_user_and_stock(
            user_id=user_id, stock_id=stock_id
        )
        return JsonResponse(total)


class StockView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        stock_name = request.query_params.get("name")
        
        stock = TradeService().get_stock_by_name(input_name=stock_name)

        serializer = StockSerializer(stock)
        response = JsonResponse(serializer.data)

        return JsonResponse(serializer.data)

        
