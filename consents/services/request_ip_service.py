# consents/services/request_ip_service.py

class RequestIPService:
    """
    Extract the real client IP address from a Django request.

    Supports common reverse proxy headers:
    - X-Forwarded-For
    - X-Real-IP
    - CF-Connecting-IP
    """

    @staticmethod
    def get_client_ip(request):

        if request is None:
            return None

        meta = getattr(request, "META", {})

        # ------------------------------------------------
        # Cloudflare
        # ------------------------------------------------

        ip = meta.get("HTTP_CF_CONNECTING_IP")

        if ip:
            return ip

        # ------------------------------------------------
        # Standard proxy header
        # ------------------------------------------------

        xff = meta.get("HTTP_X_FORWARDED_FOR")

        if xff:
            # XFF may contain multiple IPs
            # client, proxy1, proxy2
            parts = [p.strip() for p in xff.split(",") if p.strip()]
            if parts:
                return parts[0]

        # ------------------------------------------------
        # Nginx / reverse proxy
        # ------------------------------------------------

        ip = meta.get("HTTP_X_REAL_IP")

        if ip:
            return ip

        # ------------------------------------------------
        # Direct connection fallback
        # ------------------------------------------------

        return meta.get("REMOTE_ADDR")