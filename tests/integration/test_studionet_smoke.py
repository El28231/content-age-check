from pathlib import Path
import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address

GUIDE = "EVERYONE is gentle content; SEVEN_PLUS allows mild peril; TEEN allows sustained threat; SIXTEEN_PLUS allows graphic injury; ADULT_ONLY covers explicit sexual content."

@pytest.mark.integration
def test_studionet_content_registry(default_account):
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "content_age_check.py")
    deployed = factory.deploy_contract_tx(args=[GUIDE], account=default_account, wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(deployed)
    address = extract_contract_address(deployed)
    contract = factory.build_contract(address, account=default_account)
    classified = contract.classify_content(args=["episode-7", "Heroes escape a burning station while armed enemies pursue them through dark tunnels."]).transact(wait_transaction_status=TransactionStatus.FINALIZED)
    assert tx_execution_succeeded(classified)
    item = contract.get_item(args=["episode-7"]).call()
    assert item["band"] in ("EVERYONE", "SEVEN_PLUS", "TEEN", "SIXTEEN_PLUS", "ADULT_ONLY")
    print(f"STUDIONET_ADDRESS={address}")
    print(f"STUDIONET_DEPLOY_TX={deployed['hash']}")
    print(f"STUDIONET_WRITE_TX={classified['hash']}")
    print(f"STUDIONET_RESULT={item['band']}")

