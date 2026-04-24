"""
PJT 01 - 날씨 API 데이터 수집
OpenWeatherMap API 활용
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY", "YOUR_API_KEY_HERE")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
CITY = "Seoul"


def get_weather_raw():
    """날씨 API 호출 → raw dict 반환"""
    params = {"q": CITY, "appid": API_KEY, "units": "metric", "lang": "kr"}
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()


def f101_print_keys(data):
    """F101: 응답 JSON의 Key 값만 출력"""
    print("=== F101: 날씨 데이터 Key 목록 ===")
    print(list(data.keys()))


def f102_extract_main_weather(data):
    """F102: main, weather 키 값을 딕셔너리로 추출"""
    print("\n=== F102: main, weather 추출 ===")
    result = {
        "main": data.get("main", {}),
        "weather": data.get("weather", [{}])[0],
    }
    print(result)
    return result


def f103_korean_keys(extracted):
    """F103: 추출한 키 값을 한글 키로 변환"""
    print("\n=== F103: 한글 키 변환 ===")
    main = extracted["main"]
    weather = extracted["weather"]
    result = {
        "온도": main.get("temp"),
        "체감온도": main.get("feels_like"),
        "최저기온": main.get("temp_min"),
        "최고기온": main.get("temp_max"),
        "습도": main.get("humidity"),
        "날씨상태": weather.get("description"),
    }
    print(result)
    return result


def f104_add_celsius(korean_data):
    """F104: 섭씨 온도 필드 추가 (API가 이미 metric이면 그대로, 아니면 변환)"""
    print("\n=== F104: 섭씨 온도 추가 ===")
    korean_data["섭씨온도"] = round(korean_data["온도"], 1)
    print(korean_data)
    return korean_data


if __name__ == "__main__":
    data = get_weather_raw()
    f101_print_keys(data)
    extracted = f102_extract_main_weather(data)
    korean = f103_korean_keys(extracted)
    f104_add_celsius(korean)
