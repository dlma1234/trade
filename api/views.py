from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated

from api.serializers import OrderSerializer
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

        
