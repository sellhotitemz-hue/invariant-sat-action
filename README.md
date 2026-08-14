# 🛡️ Invariant SAT ZK Circuit Security Scanner

[![GitHub Actions Marketplace](https://img.shields.io/badge/Marketplace-Invariant%20SAT%20ZK%20Scanner-blue?logo=github)](https://github.com/marketplace)
[![Zero-IP Enclave Protected](https://img.shields.io/badge/Security-Zero--IP%20Enclave-green)](https://invariantsat.com)
[![License: Proprietary Commercial](https://img.shields.io/badge/License-Proprietary%20Commercial-red.svg)](#-license--terms)

Automated **Zero-Knowledge Circuit Soundness & Exploit Witness Scanner** for GitHub CI/CD pipelines.

Scans ZK circuits (Circom R1CS, SP1 zkVM AIR traces, Halo2 Plonkish matrices, Aztec Noir smart contracts) for **under-constrained signals** and **proof forgery vulnerabilities** before deploying code to production.

---

## 📖 COMPLETE USER & DEPLOYMENT GUIDE

### 🚀 Quickstart Workflow Integration

Add this step to your project's `.github/workflows/zk_security.yml` file:

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

      - name: Run Invariant SAT ZK Security Scan
        uses: sellhotitemz-hue/invariant-sat-action@v1.0.0
        with:
          r1cs_path: 'build/circuits/semaphore.r1cs'
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

---

## ⚡ ALL AVAILABLE FUNCTIONS & ADVANCED USAGE

### Function 1: Circom R1CS Circuit Soundness Audit
- **What it does**: Scans `.r1cs` circuit files for missing algebraic constraints ($x \cdot (1 - x) = 0$) and calculates system matrix rank over scalar field $\mathbb{F}_p$.
- **YAML Configuration**:
  ```yaml
  - uses: sellhotitemz-hue/invariant-sat-action@v1.0.0
    with:
      r1cs_path: 'circuits/multiplier.r1cs'
  ```

### Function 2: zkVM STARK AIR Trace LogUp Verifier (SP1 / RISC Zero)
- **What it does**: Audits STARK execution trace tables and LogUp multiset memory balance constraints across cycles.
- **YAML Configuration**:
  ```yaml
  - uses: sellhotitemz-hue/invariant-sat-action@v1.0.0
    with:
      r1cs_path: 'sp1_trace.air'
      api_url: 'https://invariant-sat-backend.onrender.com'
  ```

### Function 3: Plonkish Subgraph Slicing (Halo2 / Plonky3)
- **What it does**: Partitions multi-million gate constraint matrices into decoupled subgraphs for parallel linear algebra reduction.
- **YAML Configuration**:
  ```yaml
  - uses: sellhotitemz-hue/invariant-sat-action@v1.0.0
    with:
      r1cs_path: 'circuits/halo2_gate_matrix.json'
  ```

### Function 4: Aztec Noir Smart Contract AST Diagnostic
- **What it does**: Language Server Protocol (LSP) analysis for Aztec Noir smart contract code snippets, highlighting unconstrained private signals before compilation.

### Function 5: Custom Private Enclave Server & API Key
- **What it does**: Connects to your dedicated private enterprise server with custom SLA and auth credentials.
- **YAML Configuration**:
  ```yaml
  - uses: sellhotitemz-hue/invariant-sat-action@v1.0.0
    with:
      r1cs_path: 'circuits/private_vault.r1cs'
      api_url: 'https://invariant-sat-backend.onrender.com'
      api_key: ${{ secrets.INVARIANT_SAT_API_KEY }}
  ```

---

## 📊 Automated PR Security Comment Output

When a Pull Request is scanned, Invariant SAT automatically comments a detailed security verdict on the PR:

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

## 🔒 Security & Zero-IP Guarantee

This Action uses the **Zero-IP Client Architecture**:
- Your circuit files are processed client-side.
- Zero private keys or secret inputs are transmitted.
- Solver algorithms and C++ engines stay 100% private inside your remote Enclave API server.

---

## 📄 License & Terms

**Invariant SAT Proprietary Commercial License**. All rights reserved by Invariant SAT Platform. Client wrapper provided for GitHub CI/CD integration. Powered by [Invariant SAT Enclave Engine](https://invariant-sat-backend.onrender.com).
