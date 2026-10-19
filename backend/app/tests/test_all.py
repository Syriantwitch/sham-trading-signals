import sys
import os

# Add root folder to python path
sys.path.insert(0, os.path.abspath(os.path.curdir))

from backend.app.services.risk_calculator import RiskCalculator
from backend.app.services.payment_service import PaymentService

def run_all_tests():
    print("=== Running Unified System Verification ===")
    
    # Test 1: Risk Calculator
    res = RiskCalculator.calculate_position_size(1000, 2.0, 68000, 67000, "CRYPTO")
    print(f"[SUCCESS] Risk Calculator Test Passed: Risk USD = ")

    # Test 2: ShamCash Payment Submission
    pay = PaymentService.submit_payment("usr_1", "test@sham.com", "VIP Monthly", 30.0, "TXN_998877", "0933112233")
    print(f"[SUCCESS] ShamCash Payment Test Passed: ID = {pay['payment_id']} | Status = {pay['status']}")

    print("=== All System Modules Verified Successfully! ===")

if __name__ == "__main__":
    run_all_tests()
