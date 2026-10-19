import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from backend.app.services.risk_calculator import RiskCalculator

def test_master_init():
    print("=== Testing Master Setup & Risk Calculator ===")
    
    # Test Crypto Risk Calculation ( balance, 2% risk)
    btc_calc = RiskCalculator.calculate_position_size(
        account_balance=1000, 
        risk_percentage=2.0, 
        entry_price=68000, 
        stop_loss_price=67000, 
        asset_type="CRYPTO"
    )
    print(f"[Crypto Calc] Risk USD:  | Units: {btc_calc['recommended_units']}")

    # Test Gold Risk Calculation ( balance, 1.5% risk)
    gold_calc = RiskCalculator.calculate_position_size(
        account_balance=2000, 
        risk_percentage=1.5, 
        entry_price=2700, 
        stop_loss_price=2685, 
        asset_type="GOLD"
    )
    print(f"[Gold Calc] Risk USD:  | Lot Size: {gold_calc['recommended_lot_size']}")

    print("=== Master Setup Verification Completed Successfully ===")

if __name__ == "__main__":
    test_master_init()
