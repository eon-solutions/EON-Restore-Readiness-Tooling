#!/usr/bin/env python3
import http.client
import re
import socket
import sys

if len(sys.argv) < 2:
    sys.exit("Usage: python3 aws_restore_check.py REGION [EXTRA_HOST ...]")

region = sys.argv[1]
if not re.fullmatch(r"[a-z]{2}(?:-[a-z]+)+-\d+", region) or region.startswith("cn-"):
    sys.exit("Supply a non-China AWS region, e.g. us-east-1")

hosts = [
    f"{service}.{region}.amazonaws.com"
    for service in ("s3", "sqs", "dynamodb")
] + sys.argv[2:]

failed = False
for host in hosts:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9.-]*", host):
        print(f"FAIL {host!r}: supply a hostname, not a URL")
        failed = True
        continue

    conn = http.client.HTTPSConnection(host, timeout=5)
    stage = "DNS"
    try:
        ips = sorted({
            a[4][0]
            for a in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
        })
        print(f"DNS  {host}: {', '.join(ips)}")

        stage = "TCP/TLS"
        conn.connect()

        stage = "HTTP"
        conn.request("GET", "/")
        response = conn.getresponse()
        print(f"PASS {host}:443 — HTTPS {response.status}")
    except Exception as exc:
        print(f"FAIL {host}:443 — {stage}: {exc}")
        failed = True
    finally:
        conn.close()

sys.exit(1 if failed else 0)