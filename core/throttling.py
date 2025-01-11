from rest_framework.throttling import BaseThrottle
from rest_framework.exceptions import Throttled
from django.core.cache import cache
import time

class BlogAccessThrottle(BaseThrottle):
    def get_cache_key(self, request, view):
        # Determine user type: Unregistered, Free, or Paid
        if request.user.is_authenticated:
            user_type = "paid" if request.user.profile.is_paid else "free"
        else:
            user_type = "unregistered"

        # Use the user's ID or IP for anonymous users as the cache key
        return f"blog_access_{user_type}_{request.user.id if request.user.is_authenticated else self.get_ident(request)}"

    def allow_request(self, request, view):
        cache_key = self.get_cache_key(request, view)

        # Limits for different user types
        limits = {
            "unregistered": 3,
            "free": 10,
            "paid": float('inf'),  # No limit for paid users
        }

        # Determine user type
        if request.user.is_authenticated:
            user_type = "paid" if request.user.profile.is_paid else "free"
        else:
            user_type = "unregistered"

        # Paid users are always allowed
        if user_type == "paid":
            return True

        # Get access count from the cache
        access_data = cache.get(cache_key, (0, time.time()))
        access_count, first_access_time = access_data

        # Reset count if a month has passed
        one_month = 30 * 24 * 60 * 60  # seconds in a month
        if time.time() - first_access_time > one_month:
            access_count = 0
            first_access_time = time.time()

        # Check if access count exceeds the limit
        if access_count < limits[user_type]:
            # Increment the count and save to the cache
            cache.set(cache_key, (access_count + 1, first_access_time), timeout=one_month)
            return True
        
        # Raise a Throttled exception with a custom message
        if user_type == "unregistered":
            raise Throttled(detail="Access limit reached for unregistered users. Please register to get more access.")
        elif user_type == "free":
            raise Throttled(detail="Access limit reached for free users. Upgrade to a paid plan for unlimited access.")
        else:
            raise Throttled(detail="Request limit exceeded.")
        
        

    