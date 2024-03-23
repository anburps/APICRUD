from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import RegisterData
from app.serializers import RegSerializer
from django.db.models import Q



from rest_framework.generics import (ListAPIView,
                                     CreateAPIView,
                                     RetrieveAPIView,
                                     DestroyAPIView)
from rest_framework.authentication import  BasicAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly

from django.contrib.auth import logout


from django.core.mail import send_mail
from django.conf import settings

#pagination
from rest_framework.pagination import PageNumberPagination
# Create your views here.

class Pagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100  


class Gets(APIView):
    pagination_class = Pagination
    def get(self, request):
        object = RegisterData.objects.all()
        search_query = request.query_params.get('search')
        
        if search_query:
            object = object.filter(
                Q(name__icontains=search_query) |
                Q(age__icontains=search_query))
                

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(object, request)
        
        serializ = RegSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializ.data)

    def post(self,request):
        serializ=RegSerializer(data= request.data)
        if serializ.is_valid():
            serializ.save()
            return Response(serializ.data,status=201)
        return Response(serializ.errors,status=400)
    
    def put(self,request, id):
        practice_object = RegisterData.objects.get(id=id)
        serializer = RegSerializer(practice_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request, id):
        practice_object = RegisterData.objects.get(id=id)
        serializer = RegSerializer(practice_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        practice_object = RegisterData.objects.get(id=id)
        practice_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# class listdata(ListAPIView):


#     serializer_class=RegSerializer
#     queryset=RegisterData.objects.all()
#     pagination_class = Pagination
#     authentication_classes = [BasicAuthentication]
#     permission_classes = [IsAuthenticated]
     
    

#     def get_queryset(self):
#         search = self.request.query_params.get("search")
#         if search:

#             return RegisterData.objects.filter(name__icontains=search)
#         return self.queryset
    

class createdata(CreateAPIView,ListAPIView):
    queryset=RegisterData.objects.all()
    pagination_class = Pagination
    serializer_class=RegSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]
    
    
    
    def perform_create(self, serializer):
        email=self.request.data.get("email")
        subject = 'New Data Created'
        message = f'A new RegisterData instance with name  was created.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email] 
        
        send_mail(subject, message, from_email, recipient_list)
        
        serializer.save(created_by=self.request.user)
    def get_queryset(self):
        search = self.request.query_params.get("search")
        if search:

           return RegisterData.objects.filter(name__icontains=search)
        return self.queryset
 
        
class SpecificDataRetrieveAPIView(RetrieveAPIView,DestroyAPIView):
    queryset = RegisterData.objects.all()
    serializer_class = RegSerializer
    lookup_field = 'pk' 



# class Deletedata(DestroyAPIView):

#     queryset=RegisterData.objects.all()
#     authentication_classes = [BasicAuthentication]
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     lookup_field = 'pk' 



class CustomLogoutView(APIView):
    authentication_classes = [BasicAuthentication]

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Logged out successfully."})

    def send_email_on_logout(self, email):
        subject = 'User Logged Out'
        message = 'You have been logged out of the system.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email] 
        send_mail(subject, message, from_email, recipient_list)
