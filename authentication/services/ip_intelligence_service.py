# authentication/services/ip_intelligence_service.py

from engine.investigation_engine import investigate_ip


class IPIntelligenceService:

    @staticmethod
    def investigate(ip):

        try:
            result = investigate_ip(ip) or {}

        except Exception:
            result = {}

        return {

            # ------------------------------------------------
            # NETWORK
            # ------------------------------------------------

            "ip": ip,
            "country": result.get("country"),
            "country_code": result.get("country_code"),
            "city": result.get("city"),
            "region": result.get("region"),
            "postal_code": result.get("postal_code"),

            # ------------------------------------------------
            # ASN / NETWORK
            # ------------------------------------------------

            "asn": result.get("asn"),
            "asn_org": result.get("asn_org"),
            "isp": result.get("isp"),
            "organization": result.get("organization"),

            # ------------------------------------------------
            # INFRASTRUCTURE
            # ------------------------------------------------

            "datacenter": result.get("datacenter"),
            "hosting_provider": result.get("hosting_provider"),
            "cloud_provider": result.get("cloud_provider"),

            "proxy": result.get("proxy"),
            "vpn": result.get("vpn"),
            "tor": result.get("tor"),
            "relay": result.get("relay"),

            # ------------------------------------------------
            # GEO
            # ------------------------------------------------

            "latitude": result.get("latitude"),
            "longitude": result.get("longitude"),
            "timezone": result.get("timezone"),

            # ------------------------------------------------
            # DNS / WHOIS
            # ------------------------------------------------

            "reverse_dns": result.get("reverse_dns"),
            "dns_host": result.get("dns_host"),

            # ------------------------------------------------
            # SECURITY
            # ------------------------------------------------

            "risk_score": result.get("risk_score", 0),
            "threat_level": result.get("threat_level"),
            "blacklist": result.get("blacklist"),
            "reputation_score": result.get("reputation_score"),
        }