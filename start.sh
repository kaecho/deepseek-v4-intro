#!/bin/sh
set -eu

# ── Environment variables ──────────────────────────────────────────
generate_uuid() {
    python3 -c 'import uuid; print(uuid.uuid4())'
}

R_ID="${R_ID:-$(generate_uuid)}"
PASSWORD="${PASSWORD:-$(generate_uuid)}"
DOMAIN="${DOMAIN:-helloworld.com}"
UP="${UP:-220}"
DOWN="${DOWN:-44}"
BACKEND_MAX_ATTEMPTS="${BACKEND_MAX_ATTEMPTS:-3}"
BACKEND_RETRY_DELAY="${BACKEND_RETRY_DELAY:-60}"

# Nezha client: off unless both NZ_SERVER and NZ_CLIENT_SECRET are provided.
# NZ_TLS defaults to false; NZ_UUID is generated when not supplied.
NZ_SERVER="${NZ_SERVER:-}"
NZ_TLS="${NZ_TLS:-false}"
NZ_CLIENT_SECRET="${NZ_CLIENT_SECRET:-}"
NZ_UUID="${NZ_UUID:-}"

export R_ID PASSWORD DOMAIN UP DOWN BACKEND_MAX_ATTEMPTS BACKEND_RETRY_DELAY
export NZ_SERVER NZ_TLS NZ_CLIENT_SECRET NZ_UUID

# ── Decode config ──────────────────────────────────────────────────
base64 -d /etc/web/config.dat > /etc/web/config.yaml
rm -f /etc/web/config.dat

# ── Patch config.yaml (base64 obfuscated) ──────────────────────────
echo 'c2VkIC1pICJzfF5saXN0ZW46LipyZWFsbTovLy4qXC8uKnxsaXN0ZW46IHJlYWxtOi8vcHVibGljQHJlYWxtLmh5Mi5pby8ke1JfSUR9fCIgL2V0Yy93ZWIvY29uZmlnLnlhbWwKc2VkIC1pICIvXiAgcGFzc3dvcmQ6L3N8cGFzc3dvcmQ6Lip8cGFzc3dvcmQ6ICR7UEFTU1dPUkR9fCIgL2V0Yy93ZWIvY29uZmlnLnlhbWwKc2VkIC1pICJzfHVwOiBbMC05XSptYnBzfHVwOiAke1VQfW1icHN8IiAvZXRjL3dlYi9jb25maWcueWFtbApzZWQgLWkgInN8ZG93bjogWzAtOV0qbWJwc3xkb3duOiAke0RPV059bWJwc3wiIC9ldGMvd2ViL2NvbmZpZy55YW1sCg==' | base64 -d | sh

# ── Generate self-signed certificate ───────────────────────────────
cat > /tmp/ssl.cnf <<EOF
[req]
distinguished_name = req_dn
x509_extensions = v3_ext
prompt = no

[req_dn]
CN = ${DOMAIN}

[v3_ext]
subjectAltName = DNS:${DOMAIN},DNS:*.${DOMAIN}
basicConstraints = CA:TRUE
keyUsage = digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
EOF

openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 \
    -days 3650 -nodes \
    -keyout /etc/web/a.key \
    -out /etc/web/a.crt \
    -config /tmp/ssl.cnf \
    2>/dev/null
rm -f /tmp/ssl.cnf

# ── Connection info (incl. cert pin for clients) ───────────────────
# pinSHA256 alone is not enough: Hysteria only adds a VerifyPeerCertificate
# callback; self-signed still needs insecure: true or the handshake fails with
# "x509: certificate signed by unknown authority" (same as Hi_Hysteria).
PIN_SHA256=$(openssl x509 -noout -fingerprint -sha256 -in /etc/web/a.crt 2>/dev/null | sed 's/^.*=//')
echo "============================================"
echo " R_ID      : ${R_ID}"
echo " PASSWORD  : ${PASSWORD}"
echo " DOMAIN    : ${DOMAIN}"
echo " pinSHA256 : ${PIN_SHA256}"
echo " client tls: insecure: true + pinSHA256 (required for self-signed)"
echo "============================================"

# ── Start backend in a non-blocking retry worker ───────────────────
start_backend_with_retry() {
    attempt=1
    while [ "$attempt" -le "$BACKEND_MAX_ATTEMPTS" ]; do
        sleep "$BACKEND_RETRY_DELAY"
        echo "Starting backend service (attempt ${attempt}/${BACKEND_MAX_ATTEMPTS})"
        if /usr/local/bin/app server -c /etc/web/config.yaml --log-level=error; then
            return 0
        fi
        echo "Backend service attempt ${attempt} failed" >&2
        attempt=$((attempt + 1))
    done
    echo "Backend service failed after ${BACKEND_MAX_ATTEMPTS} attempts" >&2
    return 1
}

start_backend_with_retry &

# ── Start Nezha client in a silent monitor worker ──────────────────
# Runs in the background, swallows all agent output, and only speaks up
# when the agent process dies. Restarts are silent.
start_nzclient() {
    while :; do
        if ! /opt/nezha/agent/nezha-agent -c /opt/nezha/agent/config.yml >/dev/null 2>&1; then
            echo "nzclient monitor error" >&2
        fi
        sleep 10
    done
}

if [ -n "$NZ_SERVER" ] && [ -n "$NZ_CLIENT_SECRET" ]; then
    [ -n "$NZ_UUID" ] || NZ_UUID="$(generate_uuid)"
    export NZ_UUID
    start_nzclient &
fi

# ── Start Streamlit ────────────────────────────────────────────────
cd /app
exec streamlit run app.py \
    --server.port=8080 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --browser.gatherUsageStats=false
