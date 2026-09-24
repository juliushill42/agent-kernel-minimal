# AgentKernel — Minimal Agent Execution Kernel

**T21-154** · `agentkernel-minimal-agent-execution-kernel`

A minimal deterministic task runtime built around explicit capabilities, queued task records, execution results, and tamper-evident local evidence.

## Implemented

The current capability table is explicit:

```text
read   allowed
write  allowed
net    denied
```

A submitted task records:

- task ID
- requested capability
- payload
- queued state

Execution reads the recorded task and emits a deterministic result record. The current proof result reports the serialized payload length.

Network capability requests fail before task execution.

State is stored in SQLite and linked through a SHA-256 record chain.

## Proof path

The shipped proof:

1. Submits a `read` task.
2. Executes it.
3. Attempts a `net` task and confirms denial.
4. Verifies record-chain integrity.

```bash
./boot154.sh verify
```

## Run

```bash
./boot154.sh doctor
./boot154.sh verify
./boot154.sh up
```

Default endpoint:

```text
http://127.0.0.1:8765
```

Routes:

```text
GET  /health
GET  /healthz
POST /proof
```

## Repository layout

```text
apps/web/               browser proof surface
services/api/engine.py  capability and execution logic
services/api/common.py  SQLite + SHA-256 record chain
services/api/server.py  local HTTP server
tests/test_proof.py     end-to-end proof
data/                   local state
boot154.sh              doctor / verify / up launcher
```

## Current boundary

This repository is intentionally minimal. It proves explicit capability gating, task/result state, denial behavior, and evidence-chain verification; it is not a general process sandbox.

## Ownership

Owner: Julius Cameron Hill / Titan Universal AI LLC  
Watermark: `":"`
