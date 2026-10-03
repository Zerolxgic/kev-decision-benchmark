#!/usr/bin/env bash
set -euo pipefail

cd ~/AI-Training/Decision-Model-Lab/runtime/llama.cpp

exec ./build/bin/llama-server \
  -hf ggml-org/Kev-0.8B-GGUF:Q8_0 \
  --host 127.0.0.1 \
  --port 8080 \
  -ngl 0 \
  -np 1 \
  -c 512 \
  -b 128 \
  -ub 128 \
  -t 8 \
  -tb 8 \
  --cache-ram 0 \
  --no-cache-prompt \
  -ctxcp 0 \
  --poll 0 \
  --poll-batch 0
