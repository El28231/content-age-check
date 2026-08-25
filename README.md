# Content Age Check

Maintains a multi-item content-rating registry and converts each consensus rating into a deterministic minimum-age access check.

## Core workflow

- The owner deploys one project-specific age guide.
- Callers register uniquely identified content descriptions.
- Validators assign one of five fixed audience bands under that guide.
- Applications query the stored band or call can_view with a viewer age.

## Reuse model

One deployment can classify up to 250 items under the same guide. Deploy a new instance when the controlling guide changes.

## Why GenLayer

Mapping a description to a prose age guide is semantic, while enforcing the resulting minimum age is deterministic. GenLayer handles the judgment once and stores an auditable band for later application checks.

## Evidence and source boundary

The stored age guide and submitted description are the only classification evidence. No jurisdictional rating database or outside legal rule is consulted.

## Safety boundary

Descriptions may omit material content. The result is project guidance, not statutory age verification or a legal rating. The contract holds no funds, has no upgrade hook, and never treats a model result as real-world certification.

## Verify locally

```text
python -m pip install -r requirements.txt
genvm-lint check contracts/content_age_check.py
genvm-lint typecheck contracts/content_age_check.py
pytest tests/direct -q
python tests/run_glsim.py --no-browser --seed 210821
gltest tests/integration/test_glsim_consensus.py -q --network localnet
```

Run the last two commands in separate terminals. The opt-in live test uses a dedicated StudioNet key outside this repository:

```text
gltest tests/integration/test_studionet_smoke.py -q -s --network studionet
```

Never commit a populated .env file, private key, keystore, or wallet password.

## Repository map

- contracts: deployable Intelligent Contract
- tests/direct: hardened direct-mode state, authorization, malformed-output, and validator tests
- tests/integration: five-validator GLSim and live StudioNet flows
- deployments: public deployment and transaction evidence only
- SOURCE_POLICY.md: evidence authority, collection, provenance, freshness, and privacy
- AUDIT.md: review-readiness checks and residual limitations
