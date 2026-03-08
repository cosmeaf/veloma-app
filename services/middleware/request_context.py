import requests
import geoip2.database

from ipware import get_client_ip
from user_agents import parse

from django.conf import settings
from django.core.cache import cache


class RequestContextMiddleware:

    def __init__(self, get_response):

        self.get_response = get_response

        try:
            self.geo_reader = geoip2.database.Reader(settings.GEOIP_PATH)
        except Exception:
            self.geo_reader = None


    def __call__(self, request):

        ip, _ = get_client_ip(request)

        user_agent_string = request.META.get("HTTP_USER_AGENT", "")

        ua = parse(user_agent_string)

        browser = ua.browser.family
        os_name = ua.os.family
        device = "mobile" if ua.is_mobile else "desktop"

        geo = self.get_geo(ip)

        request.audit_context = {
            "ip": ip,
            "country": geo.get("country"),
            "city": geo.get("city"),
            "browser": browser,
            "os": os_name,
            "device": device
        }

        response = self.get_response(request)

        return response


    def get_geo(self, ip):

        if not ip:
            return {"country": None, "city": None}

        cache_key = f"geo:{ip}"

        cached = cache.get(cache_key)

        if cached:
            return cached

        geo = self.lookup_geoip(ip)

        if not geo["country"]:
            geo = self.lookup_api(ip)

        cache.set(cache_key, geo, 86400)

        return geo


    def lookup_geoip(self, ip):

        if not self.geo_reader:
            return {"country": None, "city": None}

        try:

            response = self.geo_reader.city(ip)

            return {
                "country": response.country.name,
                "city": response.city.name
            }

        except Exception:

            return {"country": None, "city": None}


    def lookup_api(self, ip):

        try:

            url = settings.GEOLOOKUP_API.format(ip=ip)

            r = requests.get(
                url,
                timeout=settings.GEOLOOKUP_TIMEOUT
            )

            data = r.json()

            return {
                "country": data.get("country_name"),
                "city": data.get("city")
            }

        except Exception:

            return {"country": None, "city": None}
        

# =====================================================
# HELPER PARA LOGIN
# =====================================================

def get_login_context(request):

    return getattr(
        request,
        "audit_context",
        {
            "ip": None,
            "country": None,
            "city": None,
            "browser": None,
            "os": None,
            "device": None,
        },
    )