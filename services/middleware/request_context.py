import requests
import geoip2.database
import ipaddress

from ipware import get_client_ip
from user_agents import parse

from django.conf import settings
from django.core.cache import cache


class RequestContextMiddleware:

    GEO_CACHE_TTL = 21600  # 6h

    def __init__(self, get_response):

        self.get_response = get_response

        try:
            self.geo_reader = geoip2.database.Reader(
                f"{settings.GEOIP_PATH}/GeoLite2-City.mmdb"
            )
        except Exception:
            self.geo_reader = None


    def __call__(self, request):

        ip, is_routable = get_client_ip(request)

        ip = self.normalize_ip(ip)

        ua_string = request.META.get("HTTP_USER_AGENT", "")

        ua = parse(ua_string)

        geo = self.get_geo(ip)

        request.audit_context = {

            # -----------------------------
            # NETWORK
            # -----------------------------

            "ip": ip,
            "is_routable": is_routable,

            # -----------------------------
            # GEO
            # -----------------------------

            "country": geo.get("country"),
            "country_code": geo.get("country_code"),
            "city": geo.get("city"),
            "region": geo.get("region"),

            "latitude": geo.get("latitude"),
            "longitude": geo.get("longitude"),
            "timezone": geo.get("timezone"),

            # -----------------------------
            # DEVICE
            # -----------------------------

            "browser": ua.browser.family,
            "browser_version": ua.browser.version_string,

            "os": ua.os.family,
            "os_version": ua.os.version_string,

            "device": (
                "mobile" if ua.is_mobile else
                "tablet" if ua.is_tablet else
                "desktop"
            ),

            "device_family": ua.device.family,

            "user_agent": ua_string,

            # -----------------------------
            # UA FLAGS
            # -----------------------------

            "is_mobile": ua.is_mobile,
            "is_tablet": ua.is_tablet,
            "is_pc": ua.is_pc,
            "is_bot": ua.is_bot,

            # -----------------------------
            # REQUEST
            # -----------------------------

            "method": request.method,
            "path": request.path,
            "referer": request.META.get("HTTP_REFERER"),
            "accept_language": request.META.get("HTTP_ACCEPT_LANGUAGE"),
        }

        return self.get_response(request)


    def normalize_ip(self, ip):

        if not ip:
            return None

        try:
            return str(ipaddress.ip_address(ip))
        except Exception:
            return ip


    def get_geo(self, ip):

        if not ip:
            return self.empty_geo()

        cache_key = f"geo:{ip}"

        cached = cache.get(cache_key)

        if cached:
            return cached

        geo = self.lookup_geoip(ip)

        if not geo["country"]:
            geo = self.lookup_api(ip)

        cache.set(cache_key, geo, self.GEO_CACHE_TTL)

        return geo


    def empty_geo(self):

        return {
            "country": None,
            "country_code": None,
            "city": None,
            "region": None,
            "latitude": None,
            "longitude": None,
            "timezone": None
        }


    def lookup_geoip(self, ip):

        if not self.geo_reader:
            return self.empty_geo()

        try:

            response = self.geo_reader.city(ip)

            return {

                "country": response.country.name,
                "country_code": response.country.iso_code,

                "city": response.city.name,
                "region": response.subdivisions.most_specific.name,

                "latitude": response.location.latitude,
                "longitude": response.location.longitude,

                "timezone": response.location.time_zone
            }

        except Exception:

            return self.empty_geo()


    def lookup_api(self, ip):

        try:

            url = settings.GEOLOOKUP_API.format(ip=ip)

            r = requests.get(
                url,
                timeout=1.5
            )

            data = r.json()

            return {

                "country": data.get("country_name"),
                "country_code": data.get("country"),

                "city": data.get("city"),
                "region": data.get("region"),

                "latitude": data.get("latitude"),
                "longitude": data.get("longitude"),

                "timezone": data.get("timezone")
            }

        except Exception:

            return self.empty_geo()


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
            "country_code": None,
            "city": None,
            "region": None,
            "latitude": None,
            "longitude": None,
            "timezone": None,
            "browser": None,
            "browser_version": None,
            "os": None,
            "os_version": None,
            "device": None,
            "device_family": None,
            "user_agent": None,
            "is_mobile": None,
            "is_tablet": None,
            "is_pc": None,
            "is_bot": None,
            "method": None,
            "path": None,
            "referer": None,
            "accept_language": None,
        },
    )