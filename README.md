# 🛡️ Invariant SAT ZK Circuit Security Scanner

[![GitHub Actions Marketplace](https://img.shields.io/badge/Marketplace-Invariant%20SAT%20ZK%20Scanner-blue?logo=github)](https://github.com/marketplace)
[![Zero-IP Enclave Protected](https://img.shields.io/badge/Security-Zero--IP%20Enclave-green)](https://invariantsat.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Automated **Zero-Knowledge Circuit Soundness & Exploit Witness Scanner** for GitHub CI/CD pipelines.

Scans Circom R1CS circuits for **under-constrained signals** and **proof forgery vulnerabilities** before deploying code to production.

---

## 🚀 Quickstart Usage

Add this step to your `.github/workflows/zk_security.yml` file:

```yaml
name: ZK Circuit Security Audit
on:
  pull_request:
    branches: [ main, master ]

jobs:
  zk-security-scan:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Run Invariant SAT ZK Circuit Audit
        uses: sellhotitemz-hue/invariant-sat-action@v1.0.0
        with:
          r1cs_path: 'build/circuits/semaphore.r1cs'
          api_url: 'https://api.invariantsat.com'  # Or your custom API server URL
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

---

## ⚡ What It Does

When a developer submits a Pull Request, Invariant SAT automatically:

1. **Parses R1CS Circuit Constraints**: Evaluates constraint matrix system ranks over field prime $\mathbb{F}_p$.
2. **Detects Under-Constrained Signals**: Pinpoints signals missing upper or lower algebraic constraint bounds.
3. **Synthesizes Counterexample Witness Vectors**: Extracts concrete witness pairs $(w_1 \neq w_2)$ demonstrating proof forgery under identical public inputs.
4. **Posts Automated Security Reports**: Comments audit findings directly on the GitHub Pull Request.

---

## 📊 Example PR Comment Output

| Metric | Value |
| :--- | :--- |
| **Verdict** | `UNSOUND` ❌ |
| **Circuit Signals (N)** | `100` |
| **Constraints (M)** | `63` |
| **Under-Constrained Signals** | `9` |
| **Proof Execution Time** | `0.22 ms` |

#### 🚨 Concrete Counterexample Exploit Witness Pair:
```json
{
  "target_signal_name": "main.signal_92",
  "witness_1_value": 0,
  "witness_2_value": 1,
  "miter_equation": "(main.signal_92_1 - main.signal_92_2) * v = 1 (mod BN254_PRIME)"
}
```

---

## 🔒 Security & Privacy

This Action uses the **Zero-IP Client Architecture**:
- Your source code and circuit files are checked client-side.
- Zero private keys or secret inputs are transmitted.
- Requests are handled via encrypted HTTPS TLS.

---

## 📄 License
MIT License. Powered by [Invariant SAT Platform](https://invariantsat.com).
