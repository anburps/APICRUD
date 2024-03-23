from django.urls import path

from app import views



urlpatterns = [
    path('practice/<int:id>/',views.Gets.as_view(),name='Getmethod'),
    path('practice/',views.Gets.as_view(),name='Getmethod'),
    # path('practice/<int:id>/', views.PracticeDetailView.as_view(), name='practice-detail'),




    #concreate api
    
    path('blog/',views.createdata.as_view(),name='blog'),
    path('blog/<int:pk>/',views.SpecificDataRetrieveAPIView.as_view(),name='blogspecific'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]