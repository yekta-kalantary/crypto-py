import requests
import json
from datetime import datetime

# دریافت اطلاعات قیمت از API کوین‌گکو
def fetch_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum",
        "vs_currencies": "usd",
    }
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else None

# به‌روزرسانی فایل README.md
def update_readme(data):
    if not data:
        return

    btc_price = data.get("bitcoin", {}).get("usd", "نامشخص")
    eth_price = data.get("ethereum", {}).get("usd", "نامشخص")

    recommendation = "🔹 **اتریوم بخرید!**" if eth_price / btc_price > 0.05 else "🔹 **بیت‌کوین بخرید!**"

    readme_content = f"""
# 🚀 گزارش قیمت ارزهای دیجیتال
این اطلاعات هر ساعت به‌روزرسانی می‌شود.

📅 **آخرین به‌روزرسانی:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC

| ارز دیجیتال | قیمت (دلار) |
|------------|------------|
| 🟠 بیت‌کوین | ${btc_price} |
| 🔵 اتریوم  | ${eth_price} |

💡 **توصیه:** {recommendation}

_(اطلاعات از **CoinGecko API** دریافت شده است.)_
    """

    with open("README.md", "w", encoding="utf-8") as file:
        file.write(readme_content)

if __name__ == "__main__":
    crypto_data = fetch_crypto_prices()
    update_readme(crypto_data)
