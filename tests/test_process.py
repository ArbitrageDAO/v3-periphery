from scripts.helpful_scripts import find_contract, get_params,get_account,contract_from_abi,get_wallet
import sys


def test_postion():
    # Arrange
    from brownie.network import priority_fee
    priority_fee("2 gwei")
    print("test postion create ", file=sys.stderr)
    owner_account = get_account()
    find,postion_manager = contract_from_abi("NonfungiblePositionManager", "0x72c89c842cba0e119a0366B91CEe2480e0990e32")
    tx = postion_manager.mint("0x341189EDb1f3e14fFd7Bf06E61b16AB825d5b44A", "0xB6789e039a9607F3F71C09348d1e1e7b8A2344f8", 500, 1000, {"from": owner_account})
    tx.wait(1)


