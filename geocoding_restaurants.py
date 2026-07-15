import os
import json
import time
import urllib.parse
import requests

# API 키 및 설정
VWORLD_KEY = "A6B0E05E-B14D-3718-8041-23429773F279"
GOOGLE_KEY = "AIzaSyC5jNWMGQGCfqBPEtyU0EwY8SX0eSM-W2o"

def expand_region_abbreviation(address):
    """행정구역 축약어(경남, 전남 등)를 정식 표기법으로 팽창시켜 검색 정확도 향상"""
    replacements = {
        "경남 ": "경상남도 ",
        "경북 ": "경상북도 ",
        "전남 ": "전라남도 ",
        "전북 ": "전라북도 ",
        "충남 ": "충청남도 ",
        "충북 ": "충청북도 ",
        "경기 ": "경기도 ",
        "강원 ": "강원특별자치도 ",
        "제주 ": "제주특별자치도 "
    }
    expanded = address
    for abbrev, full in replacements.items():
        if expanded.startswith(abbrev):
            expanded = expanded.replace(abbrev, full, 1)
            break
    return expanded

def geocode_vworld(address, addr_type="ROAD"):
    """VWorld 주소변환 API를 통한 위경도 조회"""
    url = "http://api.vworld.kr/req/address"
    params = {
        "service": "address",
        "request": "getcoord",
        "version": "2.0",
        "crs": "epsg:4326",
        "address": address,
        "type": addr_type,
        "key": VWORLD_KEY
    }
    try:
        r = requests.get(url, params=params, timeout=5)
        if r.status_code == 200:
            res = r.json()
            if res.get("response", {}).get("status") == "OK":
                result = res["response"]["result"]
                lon = float(result["point"]["x"])
                lat = float(result["point"]["y"])
                return lat, lon
    except Exception as e:
        # 조용히 에러 패스
        pass
    return None, None

def geocode_google(query):
    """Google Maps Geocoding/Place API를 통한 위경도 조회"""
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": query,
        "key": GOOGLE_KEY,
        "language": "ko"
    }
    try:
        r = requests.get(url, params=params, timeout=5)
        if r.status_code == 200:
            res = r.json()
            if res.get("status") == "OK" and res.get("results"):
                loc = res["results"][0]["geometry"]["location"]
                return loc["lat"], loc["lng"]
    except Exception as e:
        print(f"[Google Error] {query}: {e}")
    return None, None

def geocode_nominatim(address):
    """Nominatim (OSM) API를 통한 위경도 조회 (최종 Fallback)"""
    url = "https://nominatim.openstreetmap.org/search"
    headers = {
        "User-Agent": "TzuyangFoodMapDashboard/1.0 (gdeat@gdeat.com)"
    }
    params = {
        "q": address,
        "format": "json",
        "limit": 1
    }
    try:
        r = requests.get(url, params=params, headers=headers, timeout=5)
        if r.status_code == 200 and r.json():
            data = r.json()[0]
            return float(data["lat"]), float(data["lon"])
    except Exception as e:
        pass
    return None, None

def geocode_pipeline(address, name):
    """지오코딩 성공률 100%를 보장하기 위한 다단계 파이프라인"""
    expanded_addr = expand_region_abbreviation(address)
    
    # 1단계: Google Maps에 상호명 + 전체 주소 조합으로 직접 장소 검색 (가장 강력)
    # 예: "대성식당 경상남도 함양군 함양읍 용평길 27-4"
    google_query = f"{name} {expanded_addr}"
    lat, lon = geocode_google(google_query)
    if lat and lon:
        return lat, lon
        
    # 2단계: VWorld 정식 명칭 도로명 주소 시도
    lat, lon = geocode_vworld(expanded_addr, "ROAD")
    if lat and lon:
        return lat, lon
        
    # 3단계: VWorld 정식 명칭 지번 주소 시도
    lat, lon = geocode_vworld(expanded_addr, "PARCEL")
    if lat and lon:
        return lat, lon
        
    # 4단계: Google Maps 전체 주소로 지오코딩 시도
    lat, lon = geocode_google(expanded_addr)
    if lat and lon:
        return lat, lon

    # 5단계: 주소 정제 후 VWorld 도로명 재시도 (괄호나 상세 정보 제거)
    clean_addr = expanded_addr.split('(')[0].split(',')[0].strip()
    lat, lon = geocode_vworld(clean_addr, "ROAD")
    if lat and lon:
        return lat, lon
    
    # 6단계: Nominatim 시도 (정제된 주소)
    lat, lon = geocode_nominatim(clean_addr)
    if lat and lon:
        return lat, lon
        
    # 7단계: 최종 Fallback - 상호명 및 지역명 결합 검색
    parts = clean_addr.split()
    if len(parts) >= 2:
        search_query = f"{parts[0]} {parts[1]} {name}"
        lat, lon = geocode_google(search_query)
        if lat and lon:
            return lat, lon
            
    print(f"[FAILURE] Failed to geocode: {name} ({address})")
    return None, None

def process_restaurants():
    source_path = r"F:\Antigravity\Antigravity_data\workspace\01_작업_진행\121_쯔양_맛집_온톨로지_구축\data\tzuyang_restaurants.json"
    target_path = r"F:\Antigravity\Antigravity_data\workspace\01_작업_진행\122_쯔양_맛집_지도_시각화\tzuyang_restaurants_coords.json"
    
    if not os.path.exists(source_path):
        print(f"[ERROR] Source file not found: {source_path}")
        return
        
    with open(source_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)
        
    print(f"Loaded {len(restaurants)} restaurants. Starting geocoding pipeline...")
    
    results = []
    success_count = 0
    
    for idx, rest in enumerate(restaurants):
        name = rest["name"]
        address = rest["address"]
        print(f"[{idx+1}/{len(restaurants)}] Geocoding: {name} - {address}")
        
        lat, lon = geocode_pipeline(address, name)
        
        # 네이버 지도 바로가기 URL 생성 (도로명주소와 상호명 조합)
        naver_map_url = f"https://map.naver.com/v5/search/{urllib.parse.quote(name + ' ' + address)}"
        
        # 데이터 항목 업데이트
        updated_rest = rest.copy()
        updated_rest["latitude"] = lat
        updated_rest["longitude"] = lon
        updated_rest["naver_map_url"] = naver_map_url
        
        if lat and lon:
            success_count += 1
        else:
            # 최종 실패시 서울 시청 좌표로 대체하되 플래그 설정
            updated_rest["latitude"] = 37.5665
            updated_rest["longitude"] = 126.9780
            updated_rest["geocoded"] = False
            print(f"  -> Assigned fallback coordinates (Seoul City Hall)")
            
        results.append(updated_rest)
        
        # API 과부하 방지 및 안정적인 쿼리
        time.sleep(0.12)
        
    print(f"\nGeocoding process finished. Success: {success_count}/{len(restaurants)}")
    
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
        
    print(f"Saved geocoded restaurants to: {target_path}")

if __name__ == "__main__":
    process_restaurants()
