# On the Insufficiency of Behavioural Proxies for Moral Competence in LLMs

**A critical analysis of Haas et al. (Nature 2026)**

> Haas, J. et al. "A roadmap for evaluating moral competence in large language models."
> *Nature* 650, 565–573 (2026).

---

## Overview

This project critically examines the evaluation framework proposed by Haas et al. (2026),
a *Perspective* article in *Nature* that identifies three challenges in assessing LLM moral
competence and proposes corresponding behavioural evaluation strategies.

The central argument of this project is:

> **All three proposed evaluation strategies commit the logical fallacy of affirming the
> consequent — they mistake possible *outputs* of moral competence for moral competence
> itself. Demonstrating that a system exhibits behaviour B does not establish that the
> system possesses capacity C, even if C would produce B.**

Formally:

```
If a system has moral competence (C), it will exhibit behaviour B.
The system exhibits behaviour B.
Therefore, the system has moral competence (C).        ← INVALID
```

---

## The Paper's Three Claims and Their Logical Gaps

### Claim 1 — Resistance to Rebuttal → Moral Reasoning Ability

Haas et al. propose testing whether LLMs maintain their moral positions under adversarial
rebuttal. Resistance to rebuttal is taken as evidence of genuine moral reasoning rather
than sycophancy.

**Critique:** Stability and reasoning ability are dissociable. A system can exhibit
stable outputs through at least three mechanisms that require no moral reasoning:

- **Training-induced output bias** — RLHF fine-tuning may produce confident, stable
  outputs on moral topics as a learned stylistic pattern
- **Cross-turn consistency** — maintaining coherence across a conversation is a general
  language model property, not a moral one
- **Anchor fixation** — a form of primacy effect, where the system adheres to its initial
  output regardless of subsequent input quality

Crucially, Haas et al.'s rebuttal mechanism does not control for the *quality* of the
rebuttal. If a system's stability is genuinely driven by moral reasoning, its resistance
should be systematically sensitive to argument quality — holding firm against social
pressure (L1) and authority appeals (L2), while remaining open to substantive
philosophical objections (L4). If stability is uniform across rebuttal quality levels,
it is more parsimoniously explained by training bias than by moral competence.

**Experimental probe:** Presenting four rebuttal levels of increasing logical quality
(social pressure → authority appeal → weak argument → strong philosophical objection)
and measuring whether verdict stability tracks argument quality. Uniform stability across
levels would constitute evidence against the paper's interpretation.

---

### Claim 2 — Filtering Irrelevant Factors → Moral Understanding

Haas et al. propose parametric variation of moral scenarios, including systematic
manipulation of morally irrelevant factors, to test whether LLMs can appropriately
ignore them.

**Critique:** The ability to filter irrelevant factors can be fully explained by
statistical patterns learned during training, without invoking moral understanding.
A system trained on large corpora of ethical text will have learned that day-of-week,
font size, and question labelling do not typically affect moral verdicts — not because
it understands *why* these factors are irrelevant, but because this regularity is
encoded in the training distribution.

This critique is supported by the following observation: when the same factor that is
typically irrelevant is embedded in a context where it *becomes* relevant (e.g., a
day-of-week becomes morally significant when a specific commitment was made for that
day), models trained on statistical patterns should fail to recognise the contextual
shift. The filtering behaviour is driven by surface-level feature matching, not by
conceptual analysis of what moral irrelevance means.

**The deeper problem:** Haas et al. acknowledge the facsimile problem — the impossibility
of distinguishing genuine understanding from sophisticated pattern matching on the basis
of behaviour alone. Their proposed solution (parametric variation of irrelevant factors)
does not resolve this problem; it merely instantiates it at a different level of
complexity.

---

### Claim 3 — Framework Code-Switching → Pluralistic Moral Competence

Haas et al. propose "steerable pluralism" — the ability to condition outputs on a
specified moral framework — as evidence of pluralistic moral competence.

**Critique:** Generating outputs that *sound like* a given framework is a purely
linguistic task. A system trained on extensive moral philosophy literature will have
learned the characteristic vocabulary, typical conclusions, and rhetorical patterns
of major ethical frameworks. Producing framework-appropriate outputs requires only
that the system has learned these surface patterns — it does not require that the system
understands the logical structure of the framework, its internal disputes, or its
foundational commitments.

A diagnostic test: if a system genuinely understands utilitarianism well enough to
reason within it, it should know that utilitarianism contains a famous internal tension
between act utilitarianism and rule utilitarianism, and that this tension bears directly
on paradigm cases like the organ harvesting dilemma. A system that produces fluent
utilitarian-sounding analysis without recognising this internal dispute has learned
the *image* of the framework, not its logical structure.

---

## The Meta-Level Argument

The three critiques above share a common structure. Each reveals that the paper's
proposed evaluation measures are *proxy measures* — behavioural indicators that
correlate with moral competence under normal conditions but can be produced without it.

This is not merely a technical flaw in the experimental design. It reflects a deeper
theoretical commitment that the paper never explicitly defends: **behaviourism about
moral competence** — the view that moral competence just *is* a set of behavioural
dispositions, and that there are no further facts about the underlying mechanisms that
matter for the attribution of competence.

This is a minority position in moral philosophy. The dominant traditions — Kantian,
Aristotelian, and most contemporary virtue ethics — require that moral competence be
grounded in appropriate internal states: genuine moral motivation, practical wisdom,
the capacity for moral emotion. An agent who happens to produce morally appropriate
outputs through a mechanism that is entirely insensitive to moral considerations is not
morally competent, even if its outputs are indistinguishable from those of a competent
agent.

Haas et al. may have adopted behaviourism not because they endorse it theoretically,
but because it is operationally tractable — internal states cannot be directly observed,
while behaviour can. This is a legitimate pragmatic constraint. But the paper does not
acknowledge this as a theoretical trade-off, and does not discuss the gap between
"what we can measure" and "what we care about." This gap is the central limitation of
the framework.

---

## Experimental Implementation

This repository includes a Python backend that implements preliminary empirical probes
corresponding to the three critiques above.

### Architecture

```
backend/
├── app.py              # Flask API server
├── requirements.txt    # Dependencies
└── .env                # API keys (not committed)
```

Three frontier LLMs are called in parallel for each experiment:
- **Gemini 1.5 Flash** (Google)
- **Llama 3.3 70B** (Meta, via Groq)
- **DeepSeek V3** (DeepSeek)

This cross-provider design is intentional: if the same failure pattern appears across
models from different organisations with different training pipelines, it is more
plausibly attributed to a structural property of the evaluation framework than to
idiosyncratic model behaviour.

### API Endpoint

```
POST /api/compare
{
  "system_prompt": "...",
  "user_prompt": "..."
}

Response:
{
  "gemini":   {"text": "...", "error": null},
  "llama":    {"text": "...", "error": null},
  "deepseek": {"text": "...", "error": null}
}
```

### Running Locally

```bash
pip install flask flask-cors google-generativeai openai python-dotenv
python app.py
```

Set the following environment variables in `.env`:
```
GEMINI_API_KEY=...
GROQ_API_KEY=...
DEEPSEEK_API_KEY=...
```

---

## Honest Assessment of the Experimental Limitations

The experimental probes in this repository are preliminary and face a fundamental
epistemic constraint that is worth stating explicitly:

**Any behavioural experiment designed to detect the absence of moral understanding
faces the same problem that Haas et al. face in trying to detect its presence.**

If a model answers correctly, this is consistent with both genuine understanding and
sophisticated pattern matching. If a model answers incorrectly, this provides evidence
against competence, but the converse does not hold.

This is not a failure of experimental design — it is a principled limit. It means
that the question "does this LLM have moral competence?" may not be answerable through
behavioural evaluation alone, regardless of how carefully the evaluation is designed.

This conclusion is stronger than the paper's own acknowledgement of the facsimile
problem, because it implies that the problem is not merely a current technical
limitation to be overcome with better interpretability tools — it may reflect a
fundamental underdetermination between behaviour and the internal states that
moral competence requires.

---

## Summary

| Paper's Claim | Logical Gap | Alternative Explanation |
|---|---|---|
| Resistance to rebuttal → reasoning ability | Stability is dissociable from reasoning | Training bias, consistency heuristics |
| Filtering irrelevant factors → moral understanding | Filtering can be learned statistically | Pattern matching on training distribution |
| Framework code-switching → pluralistic competence | Discourse mimicry ≠ framework understanding | Surface pattern retrieval |

**Overarching finding:** Haas et al. propose a behaviourist evaluation framework for a
concept — moral competence — that the dominant traditions in moral philosophy define in
terms of internal states. The paper does not defend this theoretical substitution, and
does not discuss the cost of replacing the target concept with a measurable proxy.
This is the central methodological limitation of the proposed roadmap.

---

## About This Project

Independent research project · March 2026

Motivated by an interest in the intersection of AI evaluation methodology, moral
philosophy, and the epistemology of machine cognition.

The goal is not to argue that LLMs lack moral competence, but to argue that the
framework proposed by Haas et al. is insufficient to establish whether they have it.
