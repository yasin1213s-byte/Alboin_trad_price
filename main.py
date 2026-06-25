import requests
import os

# خواندن لیست آیتم‌ها از فایل
with open('items.txt', 'r') as f:
    items = [line.strip() for line in f if line.strip()]

def get_best_price(item_id):
    # چک کردن تمام شهرها (بازار بزرگ آلبین)
    url = f"https://www.albion-online-data.com/api/v2/stats/prices/{item_id}.json?locations=Martlock,Lymhurst,Bridgewatch,FortSterling,Thetford"
    try:
        response = requests.get(url).json()
        # فیلتر کردن قیمت‌های صفر و پیدا کردن ارزان‌ترین
        prices = [item['sell_price_min'] for item in response if item['sell_price_min'] > 0]
        if prices:
            return min(prices)
        return "ناموجود"
    except:
        return "خطا"

token = os.environ['TELEGRAM_BOT_TOKEN']
chat_id = os.environ['CHAT_ID']

report = "📊 گزارش لحظه‌ای بازار آلبین:\n\n"
for item in items:
    price = get_best_price(item)
    report += f"🔹 {item}: {price} سیلور\n"

url_send = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={report}"
requests.get(url_send)
