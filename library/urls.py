from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import AuthorViewSet,BookViewSet,BorrowViewSet
router = DefaultRouter()
router.register('authors',AuthorViewSet)
router.register('books',BookViewSet)
router.register('borrows',BorrowViewSet,basename='borrow')

urlpatterns = [
    path('',include(router.urls)),

]
