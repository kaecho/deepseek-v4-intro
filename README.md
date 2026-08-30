---
title: DeepSeek V4 Pro introduction
emoji: 🐋
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 8080
pinned: false
license: mit
---

# DeepSeek V4 Pro 0813

Towards Highly Efficient Million-Token Context Intelligence

Read-only introduction to **DeepSeek-V4-Pro-0813**, the official V4-Pro release. It covers the MoE architecture, 1M context, reasoning effort levels, DSpark, and the agent benchmarks on the [model card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813). The page does not collect API keys or call the model.

## Model

| Specification | Value |
|:---|:---|
| Architecture | Mixture-of-Experts |
| Total parameters | 1.6T |
| Active parameters | 49B (3.1%) |
| Context length | 1,000,000 tokens |
| Pre-training data | 32T+ tokens |
| License | MIT |

0813 keeps the preview model structure and adds a DSpark speculative decoding module. Agentic scores are higher than DeepSeek-V4-Pro (Preview), especially in production-style tasks.

## Architecture

Hybrid attention (CSA + HCA). At 1M tokens this uses 27% of DeepSeek-V3.2 single-token FLOPs and 10% of the KV cache.

Manifold-Constrained Hyper-Connections (mHC) thicken residual paths. Muon is the pre-training optimizer.

## Reasoning

`reasoning_effort` is `low`, `high`, or `max`. There is no Jinja chat template; use the `encoding` folder on the Hub.

Recommended sampling: `temperature = 1.0`. Use `top_p = 0.95` for agents, `1.0` otherwise. For `high` and `max`, cap output at 384K tokens.

## Benchmarks (0813 vs preview)

From the official model card. Code-agent tasks used DeepSeek Harness (minimal), `reasoning_effort=max`, `temperature=1.0`, `top_p=0.95`.

| Benchmark | 0813 | Preview |
|:---|:---:|:---:|
| HLE (wo / w tools) | 42.7 / 60.0 | 37.7 / 48.2 |
| Terminal Bench 2.1 | 87.9 | 72.1 |
| NL2Repo | 61.5 | 38.5 |
| Cybergym | 83.3 | 52.7 |
| DeepSWE | 62.7 | 12.8 |
| Toolathlon-Verified | 74.1 | 55.9 |
| Agents' Last Exam | 25.7 | 16.5 |
| AutomationBench (Public) | 31.8 | 12.8 |
| DSBench-FullStack | 71.1 | 41.8 |
| DSBench-Hard | 67.2 | 31.1 |

DSBench-FullStack and DSBench-Hard are internal sets.

## Run

vLLM: `--speculative-config '{"method":"dspark","num_speculative_tokens":7,"draft_sample_method":"greedy"}'`

SGLang: `--speculative-algorithm DSPARK` (no separate draft model path)

Paper: [arXiv:2606.19348](https://arxiv.org/abs/2606.19348). Chat: [chat.deepseek.com](https://chat.deepseek.com/).

## License

MIT, DeepSeek-AI (2026).
