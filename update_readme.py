import requests
import numpy as np
from datetime import datetime

# دریافت داده‌های تاریخی قیمت برای تحلیل (داده‌های ساعتی در ۷ روز گذشته)
def fetch_historical_data(coin_id, days=7):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days,
        "interval": "hourly"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()['prices']
    return None

# محاسبه اندیکاتورهای تکنیکال
def calculate_technical_indicators(prices):
    closing_prices = [price[1] for price in prices]
    
    # محاسبه EMA 20 و EMA 50
    ema20 = np.mean(closing_prices[-20:]) if len(closing_prices) >= 20 else 0
    ema50 = np.mean(closing_prices[-50:]) if len(closing_prices) >= 50 else 0
    
    # محاسبه RSI
    deltas = np.diff(closing_prices)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    
    avg_gain = np.mean(gains[-14:]) if len(gains) >= 14 else 0
    avg_loss = np.mean(losses[-14:]) if len(losses) >= 14 else 0
    
    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    rsi = 100 - (100 / (1 + rs)) if avg_loss != 0 else 50
    
    # محاسبه MACD
    ema12 = np.mean(closing_prices[-12:])
    ema26 = np.mean(closing_prices[-26:])
    macd = ema12 - ema26

    # روند یک هفته‌ای
    weekly_trend = (closing_prices[-1] - closing_prices[0]) / closing_prices[0] * 100
    
    return {
        'ema20': ema20,
        'ema50': ema50,
        'rsi': rsi,
        'macd': macd,
        'weekly_trend': weekly_trend,
        'current_price': closing_prices[-1]
    }

# محاسبه امتیاز ترکیبی
def calculate_composite_score(coin_data):
    score = 0
    
    # 1. روند صعودی بر اساس EMA
    if coin_data['ema20'] > coin_data['ema50']:
        score += 25
    
    # 2. وضعیت RSI (۳۰ تا ۷۰ مناسب)
    if 30 < coin_data['rsi'] < 70:
        score += 20
    elif coin_data['rsi'] < 30:
        score += 30  # اشباع فروش

    # 3. قدرت MACD
    if coin_data['macd'] > 0:
        score += 15
    
    # 4. روند هفتگی
    if coin_data['weekly_trend'] > 5:  # افزایش بیش از ۵٪ در یک هفته
        score += 25

    return score

# تحلیل ۵۰ رمزارز برتر
def analyze_top_coins():
    base_data = requests.get(
        "https://api.coingecko.com/api/v3/coins/markets",
        params={"vs_currency": "usd", "per_page": 50, "order": "market_cap_desc"}
    ).json()
    
    portfolio = []
    
    for coin in base_data:
        try:
            historical_data = fetch_historical_data(coin['id'])
            if not historical_data:
                continue
                
            indicators = calculate_technical_indicators(historical_data)
            score = calculate_composite_score(indicators)
            
            portfolio.append({
                "name": coin['name'],
                "symbol": coin['symbol'],
                "score": score,
                "price": indicators['current_price'],
                "rsi": indicators['rsi'],
                "macd": indicators['macd'],
                "weekly_trend": indicators['weekly_trend']
            })
            
        except Exception as e:
            print(f"Error analyzing {coin['name']}: {str(e)}")
    
    top_portfolio = sorted(portfolio, key=lambda x: x['score'], reverse=True)[:10]
    
    # تخصیص درصد هر ارز در سبد
    total_score = sum(coin["score"] for coin in top_portfolio)
    for coin in top_portfolio:
        coin["allocation"] = round((coin["score"] / total_score) * 100, 2) if total_score > 0 else 0
    
    return top_portfolio

# ایجاد گزارش سبد پیشنهادی
def update_readme(portfolio):
    content = f"""## 🚀 سبد پیشنهادی ارزهای دیجیتال
📅 آخرین بروزرسانی: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC

| ارز | نماد | قیمت | امتیاز | RSI | MACD | روند هفتگی | درصد تخصیص |
|-----|------|-------|--------|-----|------|-----------|------------|
"""
    
    for coin in portfolio:
        content += f"| {coin['name']} | {coin['symbol'].upper()} | ${coin['price']} | {coin['score']} | {coin['rsi']:.1f} | {coin['macd']:.2f} | {coin['weekly_trend']:.2f}% | {coin['allocation']}% |\n"
    
    content += "\n### معیارهای انتخاب:\n"
    content += "1. **روند صعودی بر اساس EMA**\n2. **RSI متعادل (۳۰ تا ۷۰)**\n3. **MACD مثبت**\n4. **روند هفتگی مثبت بالای ۵٪**"

    with open("README.md", "w") as f:
        f.write(content)

if __name__ == "__main__":
    top_coins = analyze_top_coins()
    update_readme(top_coins)
