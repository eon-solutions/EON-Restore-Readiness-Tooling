#!/bin/sh
set -u

if [ "$#" -lt 1 ]; then
    echo "Usage: sh aws_restore_check.sh REGION [EXTRA_HOST ...]" >&2
    exit 2
fi

command -v curl >/dev/null 2>&1 || {
    echo "curl is required" >&2
    exit 2
}

region=$1
shift
case "$region" in
    ''|cn-*|*[!a-z0-9-]*|[!a-z]*)
        echo "Supply a non-China AWS region, e.g. us-east-1" >&2
        exit 2 ;;
esac

set -- "s3.$region.amazonaws.com" \
       "sqs.$region.amazonaws.com" \
       "dynamodb.$region.amazonaws.com" "$@"

failed=0
for host do
    case "$host" in
        ''|*[!A-Za-z0-9.-]*|[!A-Za-z0-9]*)
            echo "FAIL: supply a hostname, not a URL: $host"
            failed=1
            continue ;;
    esac

    if result=$(curl --noproxy '*' --silent --show-error \
        --connect-timeout 5 --max-time 10 --output /dev/null \
        --write-out 'HTTP %{http_code}, IP %{remote_ip}' \
        "https://$host/"); then
        echo "PASS $host:443 — $result"
    else
        echo "FAIL $host:443 — $result (see curl error above)"
        failed=1
    fi
done

exit "$failed"