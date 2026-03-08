import pytest
import sys

sys.path.append("/opt/ipintel")

from engine.investigation_engine import investigate_ip


def test_ipintel():

    result = investigate_ip("8.8.8.8")

    assert "risk_score" in result