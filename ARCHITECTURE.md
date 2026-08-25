# Architecture

## Responsibility boundary

The application may collect inputs and display state. ContentAgeCheck owns the bounded on-chain record, authorization rules, semantic consensus call, and consequential state transition. There is no hidden backend or autonomous source collector.

## State machine

Each item moves atomically from absent to a final stored band; items cannot be overwritten.

## Storage model

The contract stores owner, age guide, item descriptions, bands, submitters, and an item ID index. Text is line-ending-normalized and length-bounded before storage.

## Consensus boundary

The leader serializes only stored case data into canonical JSON and requests an exact JSON schema. Validators independently run the same prompt and normalization path. A validator accepts only an allowed, structurally valid value that exactly matches its own result. Exceptions and malformed model output fail closed.

## Authorization and invariants

Any address may classify a new item ID. Duplicate IDs and out-of-range inputs revert. Reads are public.

## Reuse and distinctness

One deployment can classify up to 250 items under the same guide. Deploy a new instance when the controlling guide changes.

This is a reusable many-item registry with a deterministic access predicate, not a one-case content label.
