from pathlib import Path
import json

CONTRACT = Path(__file__).resolve().parents[2] / "contracts" / "content_age_check.py"
SDK = "v0.2.16"
PROMPT = "independently assign the minimum audience band"
GUIDE = "EVERYONE is gentle content; SEVEN_PLUS allows mild peril; TEEN allows sustained threat; SIXTEEN_PLUS allows graphic injury; ADULT_ONLY covers explicit sexual content."


def deploy(vm, direct_deploy, alice):
    vm.sender = alice
    return direct_deploy(str(CONTRACT), GUIDE, sdk_version=SDK)


def test_multi_item_registry_and_access_rule(direct_vm, direct_deploy, direct_alice):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    direct_vm.mock_llm(PROMPT, json.dumps({"band": "TEEN"}))
    contract.classify_content("episode-7", "Heroes escape a burning station while enemies pursue them with weapons.")
    assert contract.get_item("episode-7")["band"] == "TEEN"
    assert contract.can_view("episode-7", 12) is False
    assert contract.can_view("episode-7", 13) is True
    leader = direct_vm._captured_validators[-1][0]
    assert direct_vm.run_validator(leader_result=leader) is True
    direct_vm.clear_mocks()
    direct_vm.mock_llm(PROMPT, json.dumps({"band": "EVERYONE"}))
    contract.classify_content("episode-1", "Friends prepare a picnic and solve a harmless missing-basket mystery together.")
    assert contract.get_state()["item_count"] == 2


def test_duplicate_id_and_invalid_band_fail_closed(direct_vm, direct_deploy, direct_alice):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    direct_vm.mock_llm(PROMPT, json.dumps({"band": "EVERYONE"}))
    contract.classify_content("pilot", "Friends plan a school fair and work together to decorate a community hall.")
    with direct_vm.expect_revert("item_already_classified"):
        contract.classify_content("pilot", "A different description that must not overwrite the original classification.")
    direct_vm.clear_mocks()
    direct_vm.mock_llm(PROMPT, json.dumps({"band": "TWELVE_PLUS"}))
    with direct_vm.expect_revert("invalid_band"):
        contract.classify_content("second", "A sufficiently detailed item description for classification by the stored guide.")

