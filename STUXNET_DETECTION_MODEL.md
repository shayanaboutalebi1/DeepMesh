# STUXNET_DETECTION_MODEL.md

Purpose
- Document a defensive anomaly‑scoring model intended to help detect Stuxnet‑style compromise indicators on engineering hosts, PLC/HMI toolchains, and OT networks.
- Non‑executable, non‑offensive: model is for detection, investigation, and incident response only.

Model overview
RiskScore = normalize( w1*S_unsigned + w2*S_usb_origin + w3*S_new_service + w4*S_checksum_mismatch + w5*S_network_beacon + w6*S_privilege_escalation + w7*S_unexpected_process )

Signals (S_*)
- S_unsigned (binary 0/1): critical binary/process unsigned or signature invalid.
- S_usb_origin (binary 0/1): file introduced from removable media (USB) or other external physical media.
- S_new_service (binary 0/1): new service/driver installed outside approved change window.
- S_checksum_mismatch (binary 0/1): PLC/HMI/firmware checksum disagrees with baseline.
- S_network_beacon (0–1 normalized): repeated connections/beacons to unexpected external hosts or anomalous internal east‑west flows.
- S_privilege_escalation (binary 0/1): unexpected elevation of process or account privileges.
- S_unexpected_process (0–1 normalized): execution frequency of rare/unwhitelisted binary or unusual parent/child process lineage.

Example weights (tunable; sum to 1)
- w1 = 0.20
- w2 = 0.15
- w3 = 0.15
- w4 = 0.20
- w5 = 0.15
- w6 = 0.10
- w7 = 0.05

Thresholds (example)
- 0–20: Low — monitor
- 21–50: Medium — investigate and gather evidence
- 51–80: High — isolate, preserve artifacts, follow IR playbook
- 81–100: Critical — full IR activation and legal/forensic escalation

Pseudocode (defensive)
- Collect telemetry: EDR events, SIEM logs, firewall flows, PLC baseline hashes, change logs.
- For each asset:
  - Compute S_unsigned, S_usb_origin, S_new_service, S_checksum_mismatch.
  - Compute S_network_beacon from netflow/session counts normalized to 0–1.
  - Compute S_privilege_escalation and S_unexpected_process from EDR ancestry and whitelists.
  - RiskScore = weighted sum → normalize to 0–100.
  - If RiskScore > threshold:
    - Create an evidence bundle (timestamps, relevant logs, file hashes, parent/child process trees).
    - Flag for human review; follow incident response playbook for investigation and containment.
  - Log decision with model version and data sources for auditing.

Telemetry mapping (examples)
- S_unsigned: EDR code signature events; Windows SigCheck output; Sysmon ImageLoaded with signature flags.
- S_usb_origin: USB mount events; Windows Event Log (removable media connect); EDR file provenance fields.
- S_new_service: Service install events; driver load events; change control records.
- S_checksum_mismatch: Baseline CSV of PLC asset IDs + SHA256; periodic export and compare.
- S_network_beacon: Netflow counts to external IPs, DNS lookups frequency, unusual destination ports.
- S_privilege_escalation: UAC events, token elevation logs, sudden admin group membership changes.
- S_unexpected_process: Process execution frequency vs. whitelist; parent process anomalies (e.g., Office app spawning cmd.exe).

Evidence & investigation template
- Asset ID, hostname, role (engineering/jump host/PLC)
- RiskScore value and contributing signals (which S_* were triggered)
- File hashes (SHA256) and provenance (USB, vendor update, network share)
- Relevant logs: EDR event IDs, SIEM query exports, netflow samples
- Baseline checksums and last verified date
- Investigator notes and next actions

Operational notes & safeguards
- Model is intended as an investigative triage aid only — do not perform destructive automated remediation; always require human authorization for isolation or system changes.
- Keep model and threshold tuning documented, versioned, and auditable.
- Validate and tune weights using historical benign events and authorized red‑team exercises (with legal authorization).
- Protect all collected evidence and preserve chain of custody when escalation occurs.

Acceptance & sign‑off criteria
- No outstanding High risk items in the environment
- Baseline hashes for all critical PLC/HMI assets are established and verified
- EDR/SIEM coverage sufficient to compute the S_* signals for monitored assets
- Incident response playbook in place and tested

Attribution / Signature
DeepMesh — Defensive Detection Signature
Author: Shayan Aboutalebi
Repository: shayanaboutalebi1/DeepMesh

Safety statement
This model is defensive and non‑exploitative. It must not be used to create or test malware. Use only for lawful detection, incident response, and forensics with appropriate authorization.
