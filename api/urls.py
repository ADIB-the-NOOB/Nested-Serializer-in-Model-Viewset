from .views import StudentAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', StudentAPIView, basename='student')
urlpatterns = router.urls

# urlpatterns = [
    
# ]
