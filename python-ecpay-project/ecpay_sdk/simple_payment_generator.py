#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import time
import hashlib
import urllib.parse
from datetime import datetime

class SimplePaymentGenerator:
    """簡單的付款頁面生成器"""
    
    def __init__(self):
        # 綠界測試環境參數
        self.merchant_id = '2000132'
        self.hash_key = '5294y06JbISpM5x9'
        self.hash_iv = 'v77hoKGq4kWxNNIS'
        self.action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'
    
    def generate_trade_no(self):
        """產生唯一訂單編號"""
        return f"TEST{int(time.time())}"
    
    def generate_check_mac_value(self, params):
        """產生綠界 CheckMacValue - 正確版本"""
        
        # 步驟1: 移除空值和 CheckMacValue
        filtered_params = {}
        for key, value in params.items():
            if key != 'CheckMacValue' and value is not None and str(value).strip() != '':
                filtered_params[key] = str(value)
        
        # 步驟2: 按 key 排序（區分大小寫）
        sorted_params = sorted(filtered_params.items())
        
        # 步驟3: 組合成查詢字串
        query_string = '&'.join([f'{key}={value}' for key, value in sorted_params])
        
        # 步驟4: 前後加上 HashKey 和 HashIV
        raw_string = f"HashKey={self.hash_key}&{query_string}&HashIV={self.hash_iv}"
        
        # 步驟5: URL encode
        encoded_string = urllib.parse.quote_plus(raw_string)
        
        # 步驟6: 轉小寫
        encoded_string = encoded_string.lower()
        
        # 步驟7: SHA256 加密並轉大寫
        check_mac_value = hashlib.sha256(encoded_string.encode('utf-8')).hexdigest().upper()
        
        print(f"🔍 Debug 資訊：")
        print(f"   過濾參數：{filtered_params}")
        print(f"   查詢字串：{query_string}")
        print(f"   原始字串：{raw_string}")
        print(f"   編碼字串：{encoded_string}")
        print(f"   CheckMacValue：{check_mac_value}")
        
        return check_mac_value
    
    def create_payment_page(self, item_name="Python課程", amount=100, choose_payment="ALL"):
        """建立付款頁面"""
        
        print("=== 綠界付款頁面生成器 ===")
        print(f"📝 商品名稱：{item_name}")
        print(f"💰 付款金額：NT$ {amount}")
        print(f"💳 付款方式：{choose_payment}")
        
        # 產生訂單編號
        trade_no = self.generate_trade_no()
        
        # 準備 ECPay API 參數
        payment_params = {
            'MerchantID': self.merchant_id,
            'MerchantTradeNo': trade_no,
            'MerchantTradeDate': datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
            'PaymentType': 'aio',
            'TotalAmount': str(amount),
            'TradeDesc': item_name,  # 簡化描述，避免複雜中文
            'ItemName': item_name,
            'ReturnURL': 'https://www.ecpay.com.tw/return_url.php',
            'ChoosePayment': choose_payment,
            'EncryptType': '1'
        }
        
        # 產生 CheckMacValue
        check_mac_value = self.generate_check_mac_value(payment_params)
        payment_params['CheckMacValue'] = check_mac_value
        
        # 生成 HTML 表單
        html_content = self.generate_html_form(trade_no, payment_params, item_name, amount)
        
        # 儲存 HTML 檔案
        filename = f'payment_{trade_no}.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ 付款頁面已生成：{filename}")
        print("🚀 請開啟 HTML 檔案進行付款測試")
        
        return filename
    
    def generate_html_form(self, trade_no, payment_params, item_name, amount):
        """生成 HTML 表單"""
        
        hidden_fields = ''
        for key, value in payment_params.items():
            # HTML 需要轉義特殊字元
            escaped_value = str(value).replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
            hidden_fields += f'        <input type="hidden" name="{key}" value="{escaped_value}">\n'
        
        html_template = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>綠界付款 - {item_name}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            text-align: center;
            background-color: #f5f5f5;
            padding: 20px;
        }}
        .payment-box {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .submit-btn {{
            background-color: #28a745;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 5px;
            font-size: 18px;
            cursor: pointer;
            margin-top: 20px;
        }}
        .submit-btn:hover {{
            background-color: #218838;
        }}
        .info {{
            background-color: #e9ecef;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .debug {{
            background-color: #fff3cd;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            font-size: 12px;
            text-align: left;
            word-break: break-all;
        }}
    </style>
</head>
<body>
    <div class="payment-box">
        <h1>🛒 綠界付款確認</h1>
        
        <div class="info">
            <h3>📋 訂單資訊</h3>
            <p><strong>訂單編號：</strong>{trade_no}</p>
            <p><strong>商品名稱：</strong>{item_name}</p>
            <p><strong>金額：</strong>NT$ {amount}</p>
        </div>
        
        <form method="post" action="{self.action_url}">
{hidden_fields}
            <input type="submit" value="前往綠界付款" class="submit-btn">
        </form>
        
        <div class="info">
            <h4>💡 測試說明</h4>
            <p>這是綠界測試環境</p>
            <p><strong>測試卡號：</strong>4311-9522-2222-2222</p>
            <p><strong>安全碼：</strong>任意三碼數字</p>
        </div>
        
        <div class="debug">
            <h4>🔍 除錯資訊</h4>
            <p><strong>CheckMacValue：</strong>{payment_params['CheckMacValue']}</p>
        </div>
    </div>
</body>
</html>"""
        
        return html_template

def main():
    """主程式"""
    generator = SimplePaymentGenerator()
    
    # 使用簡單的英文測試，避免中文編碼問題
    print("測試用固定參數（避免中文編碼問題）：")
    
    try:
        # 生成付款頁面 - 使用簡單的英文
        filename = generator.create_payment_page("Test Product", 100, "Credit")
        
    except Exception as e:
        print(f"❌ 發生錯誤：{e}")

if __name__ == "__main__":
    main()
