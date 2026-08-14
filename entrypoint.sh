#!/usr/bin/env bash
set -e

echo "================================================================================"
echo "          INVARIANT SAT ZERO-IP ENCLAVE — GITHUB ACTION SCANNER"
echo "================================================================================"

API_URL="${INPUT_API_URL:-http://localhost:8080}"
R1CS_PATH="${INPUT_R1CS_PATH}"
API_KEY="${INPUT_API_KEY}"
GH_TOKEN="${INPUT_GITHUB_TOKEN}"

MD_OUTPUT_FILE="/tmp/invariant_report.md"
JSON_OUTPUT_FILE="/tmp/invariant_report.json"

CMD_ARGS="--api-url ${API_URL} --markdown ${MD_OUTPUT_FILE} --json ${JSON_OUTPUT_FILE}"

if [ -n "$R1CS_PATH" ]; then
    CMD_ARGS="${CMD_ARGS} --r1cs ${R1CS_PATH}"
else
    CMD_ARGS="${CMD_ARGS} --zk-demo"
fi

if [ -n "$API_KEY" ]; then
    CMD_ARGS="${CMD_ARGS} --api-key ${API_KEY}"
fi

echo "[*] Querying private Invariant SAT API Server enclave at: ${API_URL}..."
python /app/enterprise_client.py ${CMD_ARGS}

echo ""
if [ -f "${MD_OUTPUT_FILE}" ]; then
    echo "[+] Verification output report generated:"
    cat "${MD_OUTPUT_FILE}"
fi

# Post PR Comment on GitHub Actions if GITHUB_EVENT_PATH and GH_TOKEN exist
if [ -f "$GITHUB_EVENT_PATH" ] && [ -n "$GH_TOKEN" ]; then
    PR_NUMBER=$(jq -r ".pull_request.number // empty" "$GITHUB_EVENT_PATH")
    COMMENTS_URL=$(jq -r ".pull_request.comments_url // empty" "$GITHUB_EVENT_PATH")

    if [ -n "$PR_NUMBER" ] && [ -n "$COMMENTS_URL" ] && [ -f "${MD_OUTPUT_FILE}" ]; then
        echo ""
        echo "[+] Posting automated security analysis report to GitHub Pull Request #${PR_NUMBER}..."
        
        COMMENT_BODY=$(jq -Rs . < "${MD_OUTPUT_FILE}")
        PAYLOAD=$(jq -n --arg body "$COMMENT_BODY" '{body: $body}')

        curl -s -S -X POST \
            -H "Authorization: Bearer ${GH_TOKEN}" \
            -H "Accept: application/vnd.github.v3+json" \
            -H "Content-Type: application/json" \
            "${COMMENTS_URL}" \
            -d "{\"body\": $(cat ${MD_OUTPUT_FILE} | jq -s -R .)}" \
            > /dev/null || echo "[!] Warning: Could not post comment to PR automatically."
    fi
fi

echo ""
echo "================================================================================"
echo "  [✓] INVARIANT SAT SCAN COMPLETE — ZERO IP EXPOSED"
echo "================================================================================"
