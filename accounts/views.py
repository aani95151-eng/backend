from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ResisterSerializer,LoginSerializer
from rest_framework import status
#shamiseeme
class RegisterView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = ResisterSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Validation error',
                }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response({
                'data': serializer.data,
                'message': 'User registered successfully',
            }, status=status.HTTP_201_CREATED)
            

        except Exception as e:

            return Response({
                'data': {},
                'message': str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   


class LoginView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Validation error',
                }, status=status.HTTP_400_BAD_REQUEST)
            
            
            response_data = serializer.get_jwt_token(serializer.validated_data)
            return Response(response_data, status=status.HTTP_200_OK)
            

        except Exception as e:

            return Response({
                'data': {},
                'message': str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
     


            