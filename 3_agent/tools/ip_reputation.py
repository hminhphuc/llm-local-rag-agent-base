"""
Tool: check_ip_reputation

Mock blacklist nội bộ để demo agent tích hợp threat intelligence.

Production thay bằng API thật:
    - AbuseIPDB (free tier 1000 lookup/ngày): https://www.abuseipdb.com
    - VirusTotal:                              https://www.virustotal.com
    - AlienVault OTX (free):                   https://otx.alienvault.com
    - Shodan:                                  https://www.shodan.io

Cách thay (gợi ý vibe-coding):
    "Sửa check_ip_reputation để gọi AbuseIPDB API.
     Đọc key từ env ABUSEIPDB_KEY. Map response thành dict cũ."
"""

# ============================================================
# MOCK DATA — chỉ phục vụ demo
# ============================================================
# Vài IP test có sẵn để minh họa agent ra quyết định "IP độc hại thì sao".
# Các IP này nằm trong dải reserved (RFC5737) → an toàn dùng làm ví dụ.
_BLACKLIST = {
    "203.0.113.42": {
        "category": "C2 server",  # Command & Control của botnet
        "confidence": 95,
        "last_seen": "2026-05-28",
    },
    "198.51.100.7": {
        "category": "Brute force",
        "confidence": 87,
        "last_seen": "2026-05-29",
    },
    "192.0.2.100": {
        "category": "Phishing host",
        "confidence": 78,
        "last_seen": "2026-05-20",
    },
}


def check_ip_reputation(ip: str) -> dict:
    """Kiểm tra một địa chỉ IP có nằm trong blacklist (threat intelligence) không.

    Dùng khi user nhắc đến một địa chỉ IP cụ thể, cần biết IP đó
    có lịch sử độc hại không (C2, brute force, phishing, malware...).

    Args:
        ip: địa chỉ IPv4 dạng chuỗi, ví dụ '203.0.113.42'.

    Returns:
        Dict gồm:
            - ip:          IP đã kiểm tra
            - malicious:   True nếu có trong blacklist, False nếu không
            - category:    loại đe dọa (chỉ có khi malicious=True)
            - confidence:  độ tin cậy 0-100 (chỉ có khi malicious=True)
            - last_seen:   ngày phát hiện gần nhất (chỉ có khi malicious=True)
            - note:        ghi chú giải thích kết quả
    """
    if ip in _BLACKLIST:
        info = _BLACKLIST[ip]
        return {
            "ip": ip,
            "malicious": True,
            "category": info["category"],
            "confidence": info["confidence"],
            "last_seen": info["last_seen"],
            "note": "IP này nằm trong blacklist nội bộ.",
        }

    # Trả về malicious=False để agent biết IP "sạch" theo data ta có.
    # Lưu ý: không có trong blacklist ≠ chắc chắn an toàn — chỉ là không có
    # ghi nhận. Agent nên phản ánh điều này khi trả lời user.
    return {
        "ip": ip,
        "malicious": False,
        "note": "Không có ghi nhận tiêu cực trong blacklist nội bộ.",
    }
