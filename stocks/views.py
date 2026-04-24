import json
import yfinance as yf
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from .strategy import calc_indicators, generate_signal, run_backtest

POPULAR_STOCKS = [
    {'symbol': 'AAPL',  'name': 'Apple',          'flag': '🇺🇸'},
    {'symbol': 'MSFT',  'name': 'Microsoft',       'flag': '🇺🇸'},
    {'symbol': 'NVDA',  'name': 'NVIDIA',          'flag': '🇺🇸'},
    {'symbol': 'TSLA',  'name': 'Tesla',           'flag': '🇺🇸'},
    {'symbol': 'AMZN',  'name': 'Amazon',          'flag': '🇺🇸'},
    {'symbol': '005930.KS', 'name': '삼성전자',   'flag': '🇰🇷'},
    {'symbol': '000660.KS', 'name': 'SK하이닉스', 'flag': '🇰🇷'},
    {'symbol': '035420.KS', 'name': 'NAVER',       'flag': '🇰🇷'},
]

def stocks_index(request):
    symbol = request.GET.get('symbol', '').strip().upper()
    return render(request, 'stocks/index.html', {
        'popular': POPULAR_STOCKS,
        'query': symbol,
    })

def stock_analysis(request, symbol):
    symbol = symbol.upper()
    period = request.GET.get('period', '1y')

    try:
        ticker = yf.Ticker(symbol)
        info   = ticker.info or {}
        df     = ticker.history(period=period)

        if df.empty:
            return render(request, 'stocks/analysis.html', {
                'error': f"'{symbol}' 종목 데이터를 찾을 수 없습니다.",
                'symbol': symbol, 'popular': POPULAR_STOCKS,
            })

        df = calc_indicators(df)
        signal_data = generate_signal(df)
        backtest    = run_backtest(df)

        # 최근 2021년 이후 필터 (hw_4_4 / pjt02 F203)
        df_recent = df[df.index.year >= 2021].copy()

        # 월별 평균 종가 (pjt02 F205)
        monthly_avg = df_recent['Close'].resample('ME').mean().dropna()
        monthly_high = df_recent['High'].resample('ME').max().dropna()
        monthly_low  = df_recent['Low'].resample('ME').min().dropna()

        # 최고/최저 종가 (pjt02 F204)
        max_close = round(df_recent['Close'].max(), 2) if not df_recent.empty else 0
        min_close = round(df_recent['Close'].min(), 2) if not df_recent.empty else 0
        max_date  = df_recent['Close'].idxmax().strftime('%Y-%m-%d') if not df_recent.empty else '-'
        min_date  = df_recent['Close'].idxmin().strftime('%Y-%m-%d') if not df_recent.empty else '-'

        # Plotly 데이터
        recent_50 = df.tail(200)
        chart_data = {
            'dates':      recent_50.index.strftime('%Y-%m-%d').tolist(),
            'open':       [round(v,2) for v in recent_50['Open'].fillna(0).tolist()],
            'high':       [round(v,2) for v in recent_50['High'].fillna(0).tolist()],
            'low':        [round(v,2) for v in recent_50['Low'].fillna(0).tolist()],
            'close':      [round(v,2) for v in recent_50['Close'].fillna(0).tolist()],
            'volume':     [int(v) for v in recent_50['Volume'].fillna(0).tolist()],
            'ema10':      [round(v,2) if pd.notna(v) else None for v in recent_50['EMA_10'].tolist()],
            'ema20':      [round(v,2) if pd.notna(v) else None for v in recent_50['EMA_20'].tolist()],
            'ema50':      [round(v,2) if pd.notna(v) else None for v in recent_50['EMA_50'].tolist()],
            'rsi':        [round(v,2) if pd.notna(v) else None for v in recent_50['RSI'].tolist()],
            'macd':       [round(v,4) if pd.notna(v) else None for v in recent_50['MACD'].tolist()],
            'macd_sig':   [round(v,4) if pd.notna(v) else None for v in recent_50['MACD_signal'].tolist()],
            'adx':        [round(v,2) if pd.notna(v) else None for v in recent_50['ADX'].tolist()],
        }
        monthly_data = {
            'months': [d.strftime('%Y-%m') for d in monthly_avg.index],
            'avg':    [round(v,2) for v in monthly_avg.values],
            'high':   [round(v,2) for v in monthly_high.reindex(monthly_avg.index, method='nearest').values],
            'low':    [round(v,2) for v in monthly_low.reindex(monthly_avg.index, method='nearest').values],
        }

        last = df.iloc[-1]
        prev = df.iloc[-2]
        change = last['Close'] - prev['Close']
        change_pct = change / prev['Close'] * 100 if prev['Close'] else 0

        context = {
            'symbol': symbol,
            'name': info.get('longName') or info.get('shortName') or symbol,
            'period': period,
            'price': round(last['Close'], 2),
            'change': round(change, 2),
            'change_pct': round(change_pct, 2),
            'currency': info.get('currency', 'USD'),
            'market_cap': info.get('marketCap'),
            'signal': signal_data,
            'backtest': backtest,
            'chart_data': json.dumps(chart_data),
            'monthly_data': json.dumps(monthly_data),
            'max_close': max_close, 'max_date': max_date,
            'min_close': min_close, 'min_date': min_date,
            'popular': POPULAR_STOCKS,
        }
        return render(request, 'stocks/analysis.html', context)

    except Exception as e:
        return render(request, 'stocks/analysis.html', {
            'error': f'데이터 로드 중 오류가 발생했습니다: {str(e)}',
            'symbol': symbol, 'popular': POPULAR_STOCKS,
        })
