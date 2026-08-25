from __future__ import annotations
import json
from pathlib import Path
from gltest import get_contract_factory, get_validator_factory
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address

PROMPT = "independently assign the minimum audience band"
GUIDE = "EVERYONE is gentle content; SEVEN_PLUS allows mild peril; TEEN allows sustained threat; SIXTEEN_PLUS allows graphic injury; ADULT_ONLY covers explicit sexual content."

def context():
    validators = get_validator_factory().batch_create_mock_validators(5, mock_llm_response={"nondet_exec_prompt": {PROMPT: json.dumps({"band": "TEEN"})}})
    return {"validators": [v.to_dict() for v in validators]}

def test_five_validator_content_registry():
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "content_age_check.py")
    deployed = factory.deploy_contract_tx(args=[GUIDE], wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(deployed)
    contract = factory.build_contract(extract_contract_address(deployed))
    classified = contract.classify_content(args=["episode-7", "Heroes escape a burning station while armed enemies pursue them through dark tunnels."]).transact(transaction_context=context(), wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(classified)
    assert contract.get_item(args=["episode-7"]).call()["band"] == "TEEN"
    assert contract.can_view(args=["episode-7", 13]).call() is True

