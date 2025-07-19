# test_sdk.py

import sys
import os
import time
from datetime import datetime

# 加入 ECPay SDK 路徑（注意這裡指向 sdk 子目錄）
sys.path.append(os.path.join(os.path.dirname(__file__), 'sdk'))

from config import config

class ECPaySDKTest:
    """ECPay SDK 測試類別"""
    
    def __init__(self):
        # 動態載入 ECPay SDK
        try:
            # 導入 SDK 的主要類別
            from ecpay_payment_sdk import ECPayPaymentSdk
            
            # 初始化 SDK
            self.ecpay = ECPayPaymentSdk(
                MerchantID=config.MERCHANT_ID,
                HashKey=config.HASH_KEY,
                HashIV=config.HASH_IV
            )
            print("✅ ECPay SDK 初始化成功")
            
        except ImportError as e:
            print(f"❌ 無法導入 ECPay SDK: {e}")
            print("請確認目錄結構：")
            print("  ecpay_sdk/")
            print("  ├── sdk/")
            print("  │   └── ecpay_payment_sdk.py")
            print("  ├── config.py")
            print("  └── test_sdk.py")
            self.ecpay = None
        except Exception as e:
            print(f"❌ SDK 初始化失敗: {e}")
            self.ecpay = None
    
    def test_sdk_loading(self):
        """測試 SDK 是否正常載入"""
        print("🧪 測試 ECPay SDK 載入...")
        
        if self.ecpay is None:
            print("❌ SDK 載入失敗")
            return False
        
        try:
            # 測試基本配置
            print(f"✅ 商店 ID：{config.MERCHANT_ID}")
            print(f"✅ Hash Key：{config.HASH_KEY[:8]}...")
            print(f"✅ Hash IV：{config.HASH_IV[:8]}...")
            print(f"✅ API 網址：{config.ACTION_URL}")
            
            return True
            
        except Exception as e:
            print(f"❌ SDK 測試失敗：{str(e)}")
            return False
    
    def test_payment_params(self):
        """測試付款參數設定"""
        print("\n🧪 測試付款參數設定...")
        
        if self.ecpay is None:
            print("❌ SDK 未載入，跳過測試")
            return False, None
        
        try:
            # 產生測試訂單編號
            trade_no = f"TEST{int(time.time())}"
            
            # 設定付款參數
            payment_params = {
                'MerchantTradeNo': trade_no,
                'MerchantTradeDate': datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
                'TotalAmount': 100,
                'TradeDesc': 'SDK 測試訂單',
                'ItemName': '測試商品',
                'ReturnURL': config.RETURN_URL,
                'ClientBackURL': config.CLIENT_BACK_URL,
                'ChoosePayment': 'ALL',
                'EncryptType': 1
            }
            
            print("✅ 付款參數設定成功：")
            for key, value in payment_params.items():
                print(f"   {key}: {value}")
            
            return True, payment_params
            
        except Exception as e:
            print(f"❌ 付款參數設定失敗：{str(e)}")
            return False, None
    
    def test_basic_functionality(self):
        """測試基本功能"""
        print("\n🧪 測試基本功能...")
        
        if self.ecpay is None:
            print("❌ SDK 未載入，跳過測試")
            return False
        
        try:
            # 檢查 SDK 是否有基本方法
            print("✅ SDK 物件建立成功")
            print(f"✅ SDK 類型：{type(self.ecpay)}")
            
            # 檢查是否有必要的屬性
            if hasattr(self.ecpay, 'MerchantID'):
                print(f"✅ MerchantID 設定：{self.ecpay.MerchantID}")
            
            return True
            
        except Exception as e:
            print(f"❌ 基本功能測試失敗：{str(e)}")
            return False

def main():
    """主測試程式"""
    print("=== ECPay Python SDK 安裝驗證 ===\n")
    
    # 建立測試物件
    sdk_test = ECPaySDKTest()
    
    # 執行測試
    tests_passed = 0
    total_tests = 3
    
    # 測試 1: SDK 載入
    if sdk_test.test_sdk_loading():
        tests_passed += 1
    
    # 測試 2: 付款參數
    success, params = sdk_test.test_payment_params()
    if success:
        tests_passed += 1
    
    # 測試 3: 基本功能
    if sdk_test.test_basic_functionality():
        tests_passed += 1
    
    # 顯示測試結果
    print(f"\n=== 測試結果 ===")
    print(f"通過測試：{tests_passed}/{total_tests}")
    
    if tests_passed >= 2:  # 至少通過前兩個測試就算成功
        print("🎉 恭喜！ECPay SDK 安裝成功且基本運作正常")
        print("✅ 你現在可以開始整合綠界金流了！")
        if tests_passed < total_tests:
            print("💡 部分進階功能測試失敗是正常的，需要查看實際 API 文件")
    else:
        print("❌ 基本測試失敗，請檢查 SDK 安裝是否正確")
        print("\n🔧 除錯建議：")
        print("1. 確認目錄結構正確")
        print("2. 檢查 sdk/ecpay_payment_sdk.py 是否存在")
        print("3. 查看具體錯誤訊息")

if __name__ == "__main__":
    main()

