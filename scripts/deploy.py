from brownie import NonfungiblePositionManager,accounts, config, network
from scripts.helpful_scripts import (
    get_account,
    get_contract_address,
    get_params,
    find_contract,
    contract_from_abi
)
import time,json
from brownie.network import priority_fee
priority_fee("2 gwei")
json_contract = {}
def deploy_All():
    account = get_account()
    print("deploy NonfungiblePositionManager")
    factory = get_contract_address("factory")

    postion_manager = NonfungiblePositionManager.deploy(
        factory,
        "0x5F0D68e15E724A0027E0b26b64060c257d1906Fd",
        account,
        {"from": account},
    )
    
    if (config["networks"][network.show_active()].get("verify", False)):
        postion_manager.tx.wait(BLOCK_CONFIRMATIONS_FOR_VERIFICATION)
        NonfungiblePositionManager.publish_source(postion_manager)
    else: 
        postion_manager.tx.wait(1)
    json_contract["NonfungiblePositionManager"] = postion_manager.address


    print("deploy pool")
    BTC = get_contract_address("btc")
    USDC = get_contract_address("usdc")
    fee = get_params("fee")
    tickLower = get_params("tickLower")
    tickUpper = get_params("tickUpper")
    amount0Desired = 1000
    amount1Desired = 10000000000
    amount0Min = 0
    amount1Min = 0
    recipient = account
    deadline = 100000000000000000000
    
    find, btc_token =  contract_from_abi("IERC20Metadata", BTC);
    btc_token.approve(postion_manager.address, 1000000000000000, {"from": account})
    find, usdc_token =  contract_from_abi("IERC20Metadata", USDC);
    usdc_token.approve(postion_manager.address, 100000000000000, {"from": account})

    mintparams = (BTC,USDC, fee, tickLower, tickUpper, amount0Desired, amount1Desired, amount0Min, amount1Min, recipient, deadline)
    tx = postion_manager.mint(mintparams, {"from": account})
    tx.wait(1)
   
        


def main():
    deploy_All()
    save_file = get_params("save")
    with open(save_file, "w") as f:
        json.dump(json_contract, f, indent=4)
    return 0
