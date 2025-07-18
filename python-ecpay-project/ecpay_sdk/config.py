# config.py

class ECPayConfig:
    """綠界金流設定"""
    
    # 測試環境設定
    TEST_MODE = True
    
    # 測試商店資訊（綠界提供的測試參數）
    MERCHANT_ID = '2000132'
    HASH_KEY = '5294y06JbISpM5x9'
    HASH_IV = 'v77hoKGq4kWxNNIS'
    
    # API 網址
    if TEST_MODE:
        ACTION_URL = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'
        QUERY_URL = 'https://payment-stage.ecpay.com.tw/Cashier/QueryTradeInfo/V5'
    else:
        ACTION_URL = 'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5'
        QUERY_URL = 'https://payment.ecpay.com.tw/Cashier/QueryTradeInfo/V5'
    
    # 回傳網址（請改成你的網域）
    RETURN_URL = 'http://your-domain.com/payment/return'
    NOTIFY_URL = 'http://your-domain.com/payment/notify'
    CLIENT_BACK_URL = 'http://your-domain.com'

# 匯出設定
config = ECPayConfig()

