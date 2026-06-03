from .models import RestaurantDetails

def restaurant_details(request):
    return {
        'rest_details': RestaurantDetails.objects.all().last()
    }
