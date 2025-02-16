import requests
import datetime

def fetch_crypto_price(symbol):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
    response = requests.get(url).json()
    return response.get(symbol, {}).get("usd", None)

def fetch_historical_prices(symbol):
    url = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart?vs_currency=usd&days=7&interval=daily"
    response = requests.get(url).json()
    prices = [price[1] for price in response.get("prices", [])]
    return prices

def calculate_sma(prices):
    return sum(prices) / len(prices) if prices else None

btc_price = fetch_crypto_price("bitcoin")
eth_price = fetch_crypto_price("ethereum")

btc_prices = fetch_historical_prices("bitcoin")
eth_prices = fetch_historical_prices("ethereum")

btc_sma = calculate_sma(btc_prices)
eth_sma = calculate_sma(eth_prices)

btc_trend = "📈 رو به رشد" if btc_price > btc_sma else "📉 رو به کاهش"
eth_trend = "📈 رو به رشد" if eth_price > eth_sma else "📉 رو به کاهش"

suggestion = "⏳ فعلاً خرید نکنید، روند نزولی است."
if btc_price > btc_sma and eth_price > eth_sma:
    suggestion = "✅ پیشنهاد: خرید **Bitcoin**" if (btc_price - btc_sma) > (eth_price - eth_sma) else "✅ پیشنهاد: خرید **Ethereum**"
elif btc_price > btc_sma:
    suggestion = "✅ پیشنهاد: خرید **Bitcoin**"
elif eth_price > eth_sma:
    suggestion = "✅ پیشنهاد: خرید **Ethereum**"

current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

readme_content = f"""# 📊 گزارش بازار کریپتو - {current_time}

| رمز ارز  | قیمت فعلی (USD) | میانگین ۷ روزه | وضعیت |
|----------|---------------|---------------|--------|
| Bitcoin  | ${btc_price}  | ${btc_sma:.2f} | {btc_trend} |
| Ethereum | ${eth_price}  | ${eth_sma:.2f} | {eth_trend} |

### 📢 نتیجه تحلیل:
{suggestion}

> ⚠️ این فقط یک تحلیل ساده است و نباید به عنوان توصیه مالی در نظر گرفته شود. همیشه تحقیقات خود را انجام دهید.

---

🚀 این داده‌ها هر ساعت یک‌بار به‌روزرسانی می‌شوند.
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)

print("✅ فایل README.md به‌روزرسانی شد.")
