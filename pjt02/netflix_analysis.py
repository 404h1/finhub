"""
PJT 02 - 넷플릭스 주가 데이터 분석
Pandas + Matplotlib 활용
Kaggle 데이터: archive/NFLX.csv 를 먼저 다운로드 후 실행
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 한글 폰트 설정 (Windows)
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False


def f202_load_data(filepath="archive/NFLX.csv"):
    """F202: CSV 읽기 + 필요 컬럼만 선택"""
    df = pd.read_csv(filepath, parse_dates=["Date"])
    df = df[["Date", "Open", "High", "Low", "Close"]]
    print("=== F202: 데이터 로드 완료 ===")
    print(df.head())
    return df


def f203_filter_after_2021(df):
    """F203: 2021년 이후 데이터 필터링"""
    df_filtered = df[df["Date"] >= "2021-01-01"].copy()
    print(f"\n=== F203: 2021년 이후 데이터 ({len(df_filtered)}행) ===")
    print(df_filtered.head())
    return df_filtered


def f204_max_min_close(df):
    """F204: 최고/최저 종가 추출"""
    max_close = df.loc[df["Close"].idxmax()]
    min_close = df.loc[df["Close"].idxmin()]
    print("\n=== F204: 최고/최저 종가 ===")
    print(f"최고 종가: ${max_close['Close']:.2f} ({max_close['Date'].date()})")
    print(f"최저 종가: ${min_close['Close']:.2f} ({min_close['Date'].date()})")
    return max_close, min_close


def f205_monthly_avg_close(df):
    """F205: 월별 평균 종가 계산 + 시각화"""
    df["YearMonth"] = df["Date"].dt.to_period("M")
    monthly = df.groupby("YearMonth")["Close"].mean().reset_index()
    monthly["YearMonth"] = monthly["YearMonth"].dt.to_timestamp()

    plt.figure(figsize=(12, 5))
    plt.bar(monthly["YearMonth"], monthly["Close"], color="#0d9488", alpha=0.8, width=20)
    plt.title("넷플릭스 월별 평균 종가 (2021년 이후)", fontsize=14, fontweight="bold")
    plt.xlabel("월")
    plt.ylabel("평균 종가 ($)")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("monthly_avg_close.png", dpi=150)
    plt.show()
    print("\n=== F205: 월별 평균 종가 차트 저장 완료 (monthly_avg_close.png) ===")
    return monthly


def f206_high_low_close_chart(df):
    """F206: 2022년 이후 High / Low / Close 3개 지표 시각화"""
    df_2022 = df[df["Date"] >= "2022-01-01"].copy()

    plt.figure(figsize=(14, 5))
    plt.plot(df_2022["Date"], df_2022["High"],  label="High",  color="#10b981", linewidth=1.2)
    plt.plot(df_2022["Date"], df_2022["Close"], label="Close", color="#0d9488", linewidth=1.5)
    plt.plot(df_2022["Date"], df_2022["Low"],   label="Low",   color="#f59e0b", linewidth=1.2)
    plt.title("넷플릭스 주가 (2022년 이후): High / Close / Low", fontsize=14, fontweight="bold")
    plt.xlabel("날짜")
    plt.ylabel("가격 ($)")
    plt.legend()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("high_low_close.png", dpi=150)
    plt.show()
    print("=== F206: High/Low/Close 차트 저장 완료 (high_low_close.png) ===")


if __name__ == "__main__":
    df = f202_load_data()
    df_2021 = f203_filter_after_2021(df)
    f204_max_min_close(df_2021)
    f205_monthly_avg_close(df_2021)
    f206_high_low_close_chart(df_2021)
