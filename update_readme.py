import requests
import json
from datetime import datetime

# دریافت اطلاعات قیمت از API کوین‌گکو برای ۵۰ ارز برتر
def fetch_top_crypto_prices():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
        "sparkline": False,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# محاسبه سبد سهام بر اساس وزن‌دهی ارزش بازار
def calculate_portfolio(data):
    if not data:
        return None

    # محاسبه کل ارزش بازار
    total_market_cap = sum(coin["market_cap"] for coin in data)

    # محاسبه وزن هر ارز در سبد (بر اساس ارزش بازار)
    for coin in data:
        coin["weight"] = (coin["market_cap"] / total_market_cap) * 100

    # انتخاب ۱۰ ارز برتر (بر اساس وزن)
    sorted_coins = sorted(data, key=lambda x: x["weight"], reverse=True)
    portfolio = sorted_coins[:10]  # انتخاب ۱۰ ارز برتر

    return portfolio

# به‌روزرسانی فایل README.md با سبد سهام پیشنهادی
def update_readme(portfolio):
    if not portfolio:
        return

    readme_content = f"""
# 🚀 سبد سهام پیشنهادی ارزهای دیجیتال
این اطلاعات هر ساعت به‌روزرسانی می‌شود.

📅 **آخرین به‌روزرسانی:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC

| ارز دیجیتال | قیمت (دلار) | وزن در سبد (%) |
|------------|------------|----------------|
"""

    for coin in portfolio:
        readme_content += f"| {coin['symbol'].upper()} | ${coin['current_price']} | {coin['weight']:.2f}% |\n"

    readme_content += """
💡 **توصیه:** این سبد بر اساس وزن‌دهی ارزش بازار پیشنهاد شده است.

_(اطلاعات از **CoinGecko API** دریافت شده است.)_
"""

    with open("README.md", "w", encoding="utf-8") as file:
        file.write(readme_content)

if __name__ == "__main__":
    crypto_data = fetch_top_crypto_prices()
    portfolio = calculate_portfolio(crypto_data)
    update_readme(portfolio)