"""
주가 기술적 분석 모듈
이동평균, 추세 강도, 모멘텀 지표를 계산해 매매 신호를 생성합니다.
"""
import pandas as pd
import numpy as np

def calc_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """OHLCV DataFrame에 기술 지표를 추가해 반환합니다."""
    close = df['Close']
    high  = df['High']
    low   = df['Low']

    # 이동평균
    df['EMA_10'] = close.ewm(span=10, adjust=False).mean()
    df['EMA_20'] = close.ewm(span=20, adjust=False).mean()
    df['EMA_50'] = close.ewm(span=50, adjust=False).mean()

    # RSI
    delta = close.diff()
    gain  = delta.clip(lower=0).rolling(14).mean()
    loss  = (-delta.clip(upper=0)).rolling(14).mean()
    rs    = gain / loss.replace(0, np.nan)
    df['RSI'] = 100 - (100 / (1 + rs))

    # MACD
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    df['MACD']        = ema12 - ema26
    df['MACD_signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_hist']   = df['MACD'] - df['MACD_signal']

    # ADX (Average Directional Index)
    df = _calc_adx(df, high, low, close)

    # 볼린저 밴드
    sma20     = close.rolling(20).mean()
    std20     = close.rolling(20).std()
    df['BB_upper'] = sma20 + 2 * std20
    df['BB_lower'] = sma20 - 2 * std20
    df['BB_mid']   = sma20

    return df

def _calc_adx(df, high, low, close, period=14):
    tr  = pd.concat([high - low,
                     (high - close.shift()).abs(),
                     (low  - close.shift()).abs()], axis=1).max(axis=1)
    dm_plus  = (high - high.shift()).clip(lower=0)
    dm_minus = (low.shift() - low).clip(lower=0)
    dm_plus  = dm_plus.where(dm_plus > dm_minus, 0)
    dm_minus = dm_minus.where(dm_minus > dm_plus, 0)

    atr   = tr.rolling(period).mean()
    di_p  = 100 * dm_plus.rolling(period).mean() / atr.replace(0, np.nan)
    di_m  = 100 * dm_minus.rolling(period).mean() / atr.replace(0, np.nan)
    dx    = 100 * (di_p - di_m).abs() / (di_p + di_m).replace(0, np.nan)
    df['ADX']   = dx.rolling(period).mean()
    df['DI_plus']  = di_p
    df['DI_minus'] = di_m
    return df

def generate_signal(df: pd.DataFrame) -> dict:
    """최근 데이터를 기반으로 매매 신호를 생성합니다."""
    if len(df) < 50:
        return {'signal': 'HOLD', 'reason': '데이터 부족', 'strength': 0}

    last = df.iloc[-1]
    prev = df.iloc[-2]

    adx = last.get('ADX', 0) or 0
    ema10 = last.get('EMA_10', 0) or 0
    ema20 = last.get('EMA_20', 0) or 0
    ema50 = last.get('EMA_50', 0) or 0
    rsi   = last.get('RSI', 50) or 50
    macd  = last.get('MACD', 0) or 0
    macd_sig = last.get('MACD_signal', 0) or 0
    close = last.get('Close', 0) or 0

    score = 0
    reasons = []

    # 추세 강도 확인 (ADX > 25 → 강한 추세)
    if adx > 25:
        if ema10 > ema20 > ema50:
            score += 2
            reasons.append(f'강한 상승 추세 (ADX {adx:.1f})')
        elif ema10 < ema20 < ema50:
            score -= 2
            reasons.append(f'강한 하락 추세 (ADX {adx:.1f})')
    else:
        reasons.append(f'추세 약함 (ADX {adx:.1f})')

    # MACD 골든/데드크로스
    prev_macd = prev.get('MACD', 0) or 0
    prev_sig  = prev.get('MACD_signal', 0) or 0
    if prev_macd < prev_sig and macd > macd_sig:
        score += 2
        reasons.append('MACD 골든크로스')
    elif prev_macd > prev_sig and macd < macd_sig:
        score -= 2
        reasons.append('MACD 데드크로스')

    # RSI
    if rsi < 30:
        score += 1
        reasons.append(f'RSI 과매도 ({rsi:.1f})')
    elif rsi > 70:
        score -= 1
        reasons.append(f'RSI 과매수 ({rsi:.1f})')

    # EMA 크로스
    prev_ema10 = prev.get('EMA_10', 0) or 0
    prev_ema20 = prev.get('EMA_20', 0) or 0
    if prev_ema10 < prev_ema20 and ema10 > ema20:
        score += 1
        reasons.append('단기 이평 골든크로스')
    elif prev_ema10 > prev_ema20 and ema10 < ema20:
        score -= 1
        reasons.append('단기 이평 데드크로스')

    if score >= 2:
        signal = 'LONG'
    elif score <= -2:
        signal = 'SHORT'
    else:
        signal = 'HOLD'

    return {
        'signal': signal,
        'reason': ' / '.join(reasons) if reasons else '신호 없음',
        'strength': min(abs(score) / 4 * 100, 100),
        'adx': round(adx, 2),
        'rsi': round(rsi, 2),
        'ema10': round(ema10, 2),
        'ema20': round(ema20, 2),
        'score': score,
    }

def run_backtest(df: pd.DataFrame, initial_capital: float = 1_000_000) -> dict:
    """간단한 이동평균 크로스 전략 백테스트를 실행합니다."""
    df = df.copy()
    if len(df) < 30:
        return {'error': '데이터 부족'}

    df['signal_bt'] = 0
    df.loc[df['EMA_10'] > df['EMA_20'], 'signal_bt'] = 1
    df.loc[df['EMA_10'] < df['EMA_20'], 'signal_bt'] = -1

    capital  = initial_capital
    position = 0
    trades   = []
    buy_price = 0

    for i in range(1, len(df)):
        sig  = df['signal_bt'].iloc[i]
        prev_sig = df['signal_bt'].iloc[i-1]
        price = df['Close'].iloc[i]

        if prev_sig <= 0 and sig == 1 and capital > 0:
            position  = capital / price
            buy_price = price
            capital   = 0

        elif prev_sig == 1 and sig <= 0 and position > 0:
            capital  = position * price
            profit   = (price - buy_price) / buy_price * 100
            trades.append({'profit_pct': round(profit, 2)})
            position = 0

    if position > 0:
        capital = position * df['Close'].iloc[-1]

    final = capital
    total_return = (final - initial_capital) / initial_capital * 100
    win_trades   = [t for t in trades if t['profit_pct'] > 0]
    win_rate     = len(win_trades) / len(trades) * 100 if trades else 0

    return {
        'initial': initial_capital,
        'final': round(final),
        'total_return': round(total_return, 2),
        'trades': len(trades),
        'win_rate': round(win_rate, 1),
    }
