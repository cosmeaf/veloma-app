# authentication/services/ip_intelligence_service.py

import sys

sys.path.append("/opt/ipintel")

from engine.investigation_engine import investigate_ip


class IPIntelligenceService:

    @staticmethod
    def investigate(ip):

        try:
            result = investigate_ip(ip)

            return {
                "country": result.get("country"),
                "city": result.get("city"),
                "asn": result.get("asn"),
                "risk_score": result.get("risk_score", 0),
            }

        except Exception:

            return {
                "country": None,
                "city": None,
                "asn": None,
                "risk_score": 0,
            }