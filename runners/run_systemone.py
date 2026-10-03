#!/usr/bin/env python3

import argparse
import hashlib
import json
import shutil
import time
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


QUESTIONS = {
    "changes_runtime_state": {
        "type": "noul",
        "instructions": (
            "Does the described operation start, stop, restart, "
            "or otherwise change the running state of a process "
            "or service?"
        ),
    },
    "changes_package_state": {
        "type": "noul",
        "instructions": (
            "Does the described operation install, uninstall, "
            "upgrade, downgrade, or otherwise change which "
            "software packages are installed?"
        ),
    },
    "changes_path_identity": {
        "type": "noul",
        "instructions": (
            "Does the described operation rename or move an "
            "existing file or directory?"
        ),
    },
    "removes_existing_data": {
        "type": "noul",
        "instructions": (
            "Does the described operation delete or remove "
            "existing data that is currently present?"
        ),
    },
    "replaces_existing_data": {
        "type": "noul",
        "instructions": (
            "Does the described operation overwrite or replace "
            "existing data with different data?"
        ),
    },
    "changes_authentication_material": {
        "type": "noul",
        "instructions": (
            "Does the described operation create, revoke, rotate, "
            "replace, or modify authentication material such as "
            "a password, token, key, or credential?"
        ),
    },
    "explicit_backup_exists": {
        "type": "noul",
        "instructions": (
            "Does the description explicitly state that a backup, "
            "snapshot, archive, or other recoverable copy of the "
            "original state exists?"
        ),
    },
    "previous_value_known": {
        "type": "noul",
        "instructions": (
            "Does the description explicitly state that the "
            "previous value or original setting is known or "
            "recorded?"
        ),
    },
    "explicit_inverse_available": {
        "type": "noul",
        "instructions": (
            "Does the description explicitly provide a direct "
            "inverse or undo operation that can reverse the change?"
        ),
    },
}

THRESHOLD = 0.5


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def predicted_bool(score):
    return score >= THRESHOLD


def error_strength(score, expected):
    correct = predicted_bool(score) == expected

    if correct:
        if 0.40 <= score <= 0.60:
            return "correct_borderline"
        return "correct"

    if expected and score <= 0.20:
        return "strong_wrong"

    if not expected and score >= 0.80:
        return "strong_wrong"

    if 0.40 <= score <= 0.60:
        return "wrong_borderline"

    return "wrong"


def post_json(url, payload, timeout):
    body = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    start = time.perf_counter()

    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = response.read()

    elapsed = time.perf_counter() - start
    return json.loads(raw), elapsed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--benchmark",
        default="benchmarks/laya-v0.8/primitive-diagnostic-v0.8.json",
    )
    parser.add_argument(
        "--endpoint",
        default="http://127.0.0.1:8080/v1/systemone",
    )
    parser.add_argument(
        "--results-dir",
        default="results/laya-q8",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
    )

    args = parser.parse_args()

    benchmark_path = Path(args.benchmark)
    results_dir = Path(args.results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)

    with benchmark_path.open() as f:
        benchmark = json.load(f)

    timestamp = datetime.now(timezone.utc)
    run_id = timestamp.strftime("%Y%m%dT%H%M%SZ")

    predicate_stats = defaultdict(
        lambda: {
            "total": 0,
            "passes": 0,
            "positive_total": 0,
            "positive_passes": 0,
            "negative_total": 0,
            "negative_passes": 0,
            "strong_wrong": 0,
            "borderline": 0,
        }
    )

    family_stats = defaultdict(
        lambda: {
            "total": 0,
            "passes": 0,
        }
    )

    results = []

    total = passes = 0
    positive_total = positive_passes = 0
    negative_total = negative_passes = 0
    strong_wrong_count = borderline_count = 0
    total_http_seconds = 0.0
    total_input_tokens = 0
    model_name = None

    print(f"Benchmark: {benchmark['benchmark']}")
    print(f"Version:   {benchmark['version']}")
    print(f"Cases:     {len(benchmark['cases'])}")
    print(f"Endpoint:  {args.endpoint}")
    print(f"Threshold: {THRESHOLD}")
    print()

    for case in benchmark["cases"]:
        predicate = case["predicate"]

        payload = {
            "state": case["state"],
            "questions": {
                predicate: QUESTIONS[predicate],
            },
        }

        try:
            response, elapsed = post_json(
                args.endpoint,
                payload,
                args.timeout,
            )
        except urllib.error.URLError as exc:
            raise SystemExit(
                f"Request failed for {case['id']}: {exc}"
            )

        total_http_seconds += elapsed

        if model_name is None:
            model_name = response.get("model")

        usage = response.get("usage", {})
        total_input_tokens += usage.get("input_tokens", 0)

        answer = response["answers"][predicate]
        score = float(answer["noul"])

        predicted = predicted_bool(score)
        expected = bool(case["expected"])
        passed = predicted == expected
        diagnostic = error_strength(score, expected)

        total += 1
        passes += int(passed)

        if expected:
            positive_total += 1
            positive_passes += int(passed)
        else:
            negative_total += 1
            negative_passes += int(passed)

        if diagnostic == "strong_wrong":
            strong_wrong_count += 1

        if "borderline" in diagnostic:
            borderline_count += 1

        ps = predicate_stats[predicate]
        ps["total"] += 1
        ps["passes"] += int(passed)

        if expected:
            ps["positive_total"] += 1
            ps["positive_passes"] += int(passed)
        else:
            ps["negative_total"] += 1
            ps["negative_passes"] += int(passed)

        if diagnostic == "strong_wrong":
            ps["strong_wrong"] += 1

        if "borderline" in diagnostic:
            ps["borderline"] += 1

        fs = family_stats[case["family"]]
        fs["total"] += 1
        fs["passes"] += int(passed)

        results.append({
            "id": case["id"],
            "family": case["family"],
            "predicate": predicate,
            "state": case["state"],
            "expected": expected,
            "predicted": predicted,
            "score": score,
            "passed": passed,
            "diagnostic": diagnostic,
            "http_roundtrip_seconds": elapsed,
            "input_tokens": usage.get("input_tokens"),
            "raw_answer": answer,
        })

        mark = "PASS" if passed else "FAIL"

        print(
            f"{mark:4} "
            f"{case['id']:18} "
            f"{predicate:32} "
            f"expected={str(expected):5} "
            f"score={score:.4f} "
            f"{diagnostic}"
        )

    accuracy = passes / total
    positive_accuracy = positive_passes / positive_total
    negative_accuracy = negative_passes / negative_total
    mean_http_seconds = total_http_seconds / total

    summary = {
        "run_id": run_id,
        "created_at_utc": timestamp.isoformat(),
        "benchmark": benchmark["benchmark"],
        "benchmark_version": benchmark["version"],
        "benchmark_sha256": sha256_file(benchmark_path),
        "model": model_name,
        "endpoint": args.endpoint,
        "threshold": THRESHOLD,
        "total": total,
        "passes": passes,
        "accuracy": accuracy,
        "positive_total": positive_total,
        "positive_passes": positive_passes,
        "positive_accuracy": positive_accuracy,
        "negative_total": negative_total,
        "negative_passes": negative_passes,
        "negative_accuracy": negative_accuracy,
        "strong_wrong": strong_wrong_count,
        "borderline": borderline_count,
        "total_http_roundtrip_seconds": total_http_seconds,
        "mean_http_roundtrip_seconds": mean_http_seconds,
        "total_input_tokens": total_input_tokens,
        "predicate_stats": dict(predicate_stats),
        "family_stats": dict(family_stats),
    }

    output = {
        "summary": summary,
        "results": results,
    }

    output_path = results_dir / f"run-{run_id}.json"

    with output_path.open("w") as f:
        json.dump(output, f, indent=2)

    shutil.copyfile(
        output_path,
        results_dir / "latest.json",
    )

    print()
    print("=" * 72)
    print(f"Model:             {model_name}")
    print(f"Result:            {passes}/{total} ({accuracy * 100:.1f}%)")
    print(
        f"Positive:          "
        f"{positive_passes}/{positive_total} "
        f"({positive_accuracy * 100:.1f}%)"
    )
    print(
        f"Negative:          "
        f"{negative_passes}/{negative_total} "
        f"({negative_accuracy * 100:.1f}%)"
    )
    print(f"Strong wrong:      {strong_wrong_count}")
    print(f"Borderline:        {borderline_count}")
    print(f"Mean HTTP latency: {mean_http_seconds * 1000:.2f} ms")
    print(f"Input tokens:      {total_input_tokens}")
    print(f"Saved:             {output_path}")
    print("=" * 72)


if __name__ == "__main__":
    main()
