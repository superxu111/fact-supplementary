# Supplementary Material — FaCT (ICEICT 2026, Paper ID 9466)

**FaCT: A Capacity-Matched, Same-Pool Re-examination of Type-Conditioned Temporal GNNs for Attack Detection**

This archive contains the complete experiment artifacts referenced by the paper: frozen
per-experiment result records, the append-only evidence ledger, all model and analysis
source code, run registrations, run logs, and sample score arrays. Everything here is
archived as the run record the paper cites — files are byte-preserved from the original
runs except for path echoes inside code (see "Processing disclosure" below).

## 1. Contents

```
.
├── code/                     # all model & analysis source (41 files)
│   ├── train-twin-arm.py             twin-arm trainer (full / homo / homoflows)
│   ├── pipeline-common.py            shared data pipeline
│   ├── run-protocol-grid.py          30/60-epoch protocol grid launcher
│   ├── ranking-inference.py          per-protocol inference + permutation tests
│   ├── logon-auc-aggregate.py        AUC caliber aggregation (E9)
│   ├── capacity-compensation-replay.py  w33 compensation replay
│   ├── clean-ablation.py             tw0 auxiliary-loss ablation
│   ├── evt-calibration.py            EVT / t-pivot calibration + G1/G3 gates
│   ├── pivot-identity-simulation.py  200k-draw pivot identity check
│   ├── window-level-readout.py       window-level CUSUM/EWMA/fixed readout
│   ├── hourly-readout.py             hourly aggregation readout
│   ├── calibration-certificate.py    four-specification calibration certificate
│   ├── sequential-sensitivity.py     one-sided threshold tightening
│   ├── granularity-analysis.py       edge→event granularity
│   ├── type-head-diagnosis.py        per-class type-head diagnosis
│   ├── memorization-frequency-baselines.py  UA / frequency baselines
│   ├── equivalence-bound-scan.py     AP equivalence-bound scan
│   ├── registry-layer.py             number-manifest construction
│   ├── verify-evidence-chain.py      three-gate evidence-chain verifier
│   ├── verify-score-reproduction.py  per-edge score reproduction (|Δ|<5e-4)
│   └── ...                           registry/bookkeeping utilities
├── tests/                    # unit tests (sequential readout, inference, keyscan, EVT)
├── scripts/                  # launcher utilities
├── results/
│   ├── sampling-protocols/   # ranking inference, AUC aggregate, grid closure
│   ├── threshold-calibration/# EVT calibration, spec curve, certificate, sensitivity,
│   │                         #   window & hourly readouts, pivot simulation
│   ├── capacity-parity/      # parameter recount, compensation replay, ablation,
│   │                         #   robustness spot-check
│   ├── granularity/          # edge→event granularity, type-head diagnosis
│   ├── baselines/            # UA & frequency baselines, equivalence scan
│   ├── cross-checks/         # score reproduction (|Δ| < 5e-4), delay-rule replay
│   ├── evidence-chain/       # append-only ledger (110 rows), latest audit,
│   │                         #   gate mutation score (8/8), number manifest
│   ├── criteria/             # frozen pre-registration criteria per experiment
│   ├── run-registrations/    # per-run registration JSONs (pool counts, protocol)
│   └── score-arrays/         # per-edge score arrays (numpy), representative samples
├── run-logs/                 # run logs (stdout), 27 files
└── NOTES.md                  # per-directory plain-language judgment notes
```

## 2. Paper claim → artifact map

| Paper claim (section) | Artifact |
|---|---|
| Twin arms, 0.819%/1.064% dual-caliber gap, dead 16-param embedding (II-A, Table I) | `results/capacity-parity/parameter-recount.json` |
| Identical pools: LOGON 131,235 / mixed 445,229, 277 positives (II-A, Table II) | `results/run-registrations/run-*-registration.json` |
| Table III main results, six protocols (IV-A) | `results/sampling-protocols/ranking-inference.json`, `logon-auc-aggregate.json` |
| AUC detectably worse, Holm-surviving 3/6 (Abstract, IV-A) | `results/sampling-protocols/logon-auc-aggregate.json` (`families.family_half1_logonAUC`) |
| Contamination-immunity flip, +0.29–0.33, p = 0.0005 (IV-C) | `results/sampling-protocols/ranking-inference.json` (`E2.families`), `protocol-grid-closure.json` (`grid_30ep`) |
| w33 compensation: in-band 3/3, signed gap 1/3 (IV-A) | `results/capacity-parity/capacity-compensation-replay.json` |
| tw0 clean ablation: −0.182/−0.162/+0.015, 2/3 in-band; E8b 3/3 (IV-A) | `results/capacity-parity/clean-ablation.json` |
| Measured ARL 8.7–9.4; τ = 3.0531/4.2068; G1 three-sentence audit (II-B, IV-B) | `results/threshold-calibration/evt-calibration-and-g1.json`, `pivot-identity-simulation.json` |
| Specification curve, k = 0/9, 0/9, 1/9, 4/9; S1↔S3 flip (II-B, IV-B, Fig. 2) | `results/threshold-calibration/specification-curve.json`, `calibration-certificate.json` |
| Family multiplicity corrected stance (5 raw → 3, 2 flips) (IV-B) | `results/threshold-calibration/calibration-certificate.json` (`family_multiplicity_stance_r3`) |
| Non-inferiority 9/9 & 7/9; κ = 1.3124/1.4616 (IV-B) | `results/threshold-calibration/sequential-sensitivity.json`, `evt-calibration-and-g1.json` |
| Hourly readout: 54.4% vs 4.4%, delays 49 h / 7 h (IV-B) | `results/threshold-calibration/hourly-readout.json` |
| Event-weighted AP 0.0061–0.0208; support 313,994 (IV-D) | `results/granularity/type-head-diagnosis.json`, `edge-event-granularity.json` |
| UA 0.00429 / frequency 0.00480 / 72.8% seen-in-train (IV-E) | `results/baselines/memorization-and-frequency-baselines.json` |
| 1pp equivalence bound, CI lower −0.00956 (IV-A) | `results/baselines/equivalence-bound-scan.json` |
| Score reproduction |Δ| < 5e-4 (III) | `results/cross-checks/score-reproduction-check.json` |
| Machine-verified ledger, mutation-tested gates 8/8 (I, II-B) | `results/evidence-chain/` (ledger, `gate-mutation-score.json`), `code/verify-evidence-chain.py` |
| E = N·q*; conformal α ≥ 1/(n+1) (II-B) | derivation stated in `results/threshold-calibration/NOTES.md` |
| GPD world gate never ran as designed; fails (II-B, disclosed) | `results/threshold-calibration/evt-calibration-and-g1.json` (`g1_synthetic`) |

## 3. How to run

Environment: Python 3.10; `torch` (GPU optional for training), `numpy`, `pandas`,
`scikit-learn`, `scipy`, `matplotlib`. Dataset: LANL comprehensive security events
(CC0, doi:10.17021/1179829); place under `data/raw/lanl/` and point the
`data/raw/lanl` path in `code/pipeline-common.py` / `code/train-twin-arm.py` at it.

```bash
# three-gate evidence-chain audit (no arguments = read-only; expect PASS)
# NOTE: the verifier was written for the original directory layout of the study
# (pre-registration-code directories); the latest audit snapshot is archived at
# results/evidence-chain/latest-audit.json (all three gates PASS, 110-row chain).
# In this reorganized view it reports structural path mismatches — see §4.
python3 code/verify-evidence-chain.py

# retrain one twin arm (example: homogenized arm, ratio-1 uniform negatives)
python3 code/train-twin-arm.py --arm homo --width 32 --neg-strategy uniform --neg-ratio 1

# ranking inference over the six-protocol grid, with permutation tests
python3 code/ranking-inference.py

# window-level calibration readout (fixed / CUSUM / EWMA at ARL0 = 100, 500)
python3 code/window-level-readout.py

# per-edge score reproduction against archived records (expect |Δ| < 5e-4)
python3 code/verify-score-reproduction.py
```

Output paths in the code are relative (`./results/...`); create the directories or
edit the single `BASE` constant at the top of each script.

## 4. Processing disclosure

- Directory and file names were reorganized from internal bookkeeping codes to
  functional names; `results/*/NOTES.md` files carry the plain-language judgment text
  copied verbatim from each record.
- Absolute server paths inside code were replaced with relative paths.
- The evidence ledger (`results/evidence-chain/evidence-ledger.jsonl`) is kept
  byte-identical to the runs; its `note` fields therefore still carry the original
  internal stage labels of the runs. The archived audit snapshot
  (`results/evidence-chain/latest-audit.json`) is the three-gate verdict produced
  on the original study layout (gate 1: 0 orphan files; gate 2: 31 manifest rows,
  0 FAIL; gate 3: 114-row chain intact, freeze-drift 50/50 files identical).
  Running the verifier inside this reorganized view reports structural path
  mismatches because the audit script resolves paths against the original
  directory names; every judgment record itself is byte-identical to the runs.
- `results/score-arrays/` contains representative per-edge score arrays
  (the uniform ratio-1 pair and the three calibration arms' benign arrays); the
  complete set of 60+ arrays is available from the authors on request.
