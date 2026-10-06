import json

import pytest

from bidgo import pipeline
from bidgo.claude_extract import verify
from bidgo.ingest import ingest, resolves

EXPECTED = {
    "fremont-library-upgrade": "GO",
    "sjusd-lincoln-errcs": "HOLD",
    "fresno-jail-security": "NO-GO",
}


@pytest.fixture(scope="module")
def results(tmp_path_factory):
    out = tmp_path_factory.mktemp("out")
    return {name: pipeline.run(pipeline.OPPS / name, out=out) for name in EXPECTED} | {"_out": out}


@pytest.mark.parametrize("name,decision", EXPECTED.items())
def test_expected_decision(results, name, decision):
    result, _ = results[name]
    assert result["decision"] == decision


@pytest.mark.parametrize("name", EXPECTED)
def test_every_reason_and_check_cites_real_text(results, name):
    result, passages = results[name]
    assert result["reasons"]
    for check in result["checks"]:
        assert check["cites"], f"{check['check']} has no citation"
        for cite in check["cites"]:
            assert resolves(passages, cite), cite


@pytest.mark.parametrize("name", EXPECTED)
def test_every_extracted_fact_cites_real_text(results, name):
    result, passages = results[name]
    for field, fact in result["facts"].items():
        if isinstance(fact, dict) and "cite" in fact:
            assert resolves(passages, fact["cite"]), field


def test_hold_names_what_to_ask_for(results):
    result, _ = results["sjusd-lincoln-errcs"]
    checks = {r["check"] for r in result["reasons"]}
    assert {"Bid bond", "Missing Sheet T-201", "Missing Section 00 21 13"} <= checks


def test_nogo_reasons(results):
    result, _ = results["fresno-jail-security"]
    checks = {r["check"] for r in result["reasons"]}
    assert {"Service area", "Performance bond", "Liquidated damages"} <= checks


PASSAGES = ingest(pipeline.OPPS / "sjusd-lincoln-errcs")


def answer(value, pid, quote):
    return {"value": value, "passage_id": pid, "quote": quote}


def test_supported_claim_is_kept():
    facts, rejected = verify(PASSAGES, {"ld_per_day": answer("$750", "02-spec-excerpts.md:4", "$750 per calendar day")})
    assert facts["ld_per_day"]["value"] == 750 and not rejected


@pytest.mark.parametrize("claim,why", [
    # Model invents a 10% bid bond and cites the bid form, which only points to a missing section.
    (answer("10%", "05-bid-form.md:5", "Bid security: in the amount required by Section 00 21 13"), "does not state"),
    # Quote that is not in the cited line.
    (answer("10%", "05-bid-form.md:5", "Bid security: 10% bid bond"), "not in the cited passage"),
    # Passage id that does not exist.
    (answer("10%", "07-instructions.md:3", "bid bond of 10%"), "does not exist"),
])
def test_unsupported_claim_is_rejected(claim, why):
    facts, rejected = verify(PASSAGES, {"bid_bond_pct": claim})
    assert facts["bid_bond_pct"] is None
    assert why in rejected[0]["why"]


def test_approval_is_the_only_write_and_overrides_need_a_note(results):
    out = results["_out"]
    with pytest.raises(SystemExit):
        pipeline.approve("sjusd-lincoln-errcs", "Pat Lee", "GO", out=out)
    assert not (out / "approvals.jsonl").exists()
    e = pipeline.approve("sjusd-lincoln-errcs", "Pat Lee", "HOLD", "Asked district for T-201 and ITB", out=out)
    assert e["override"] is False
    rows = [json.loads(l) for l in (out / "approvals.jsonl").read_text().splitlines()]
    assert rows == [e]
