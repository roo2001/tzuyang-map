import os
import json

def build_html_dashboard():
    coords_path = r"F:\Antigravity\Antigravity_data\workspace\01_작업_진행\122_쯔양_맛집_지도_시각화\tzuyang_restaurants_coords.json"
    html_out_path = r"F:\Antigravity\Antigravity_data\workspace\01_작업_진행\122_쯔양_맛집_지도_시각화\tzuyang_food_map.html"
    
    if not os.path.exists(coords_path):
        print(f"[ERROR] Geocoded data file not found: {coords_path}")
        return
        
    with open(coords_path, "r", encoding="utf-8") as f:
        restaurants_data = json.load(f)
        
    print(f"Loaded {len(restaurants_data)} geocoded restaurants. Generating HTML dashboard...")
    
    # HTML 및 CSS/JS 템플릿 정의 (세련된 밝은 테마 / Voyager Map 적용)
    html_template = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>쯔양 맛집 지도 & 리스트 대시보드</title>
    
    <!-- Pretendard 한글 폰트 -->
    <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css" />
    <!-- Leaflet.js CSS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
    <!-- Leaflet.markercluster CSS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.css" />
    <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.Default.css" />
    
    <style>
        :root {
            --bg-color: #f1f5f9;
            --sidebar-bg: rgba(255, 255, 255, 0.85);
            --card-bg: rgba(255, 255, 255, 0.7);
            --card-hover: rgba(255, 255, 255, 1);
            --border-color: rgba(15, 23, 42, 0.08);
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --accent-color: #4f46e5;
            --accent-gradient: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
            --naver-green: #03cf5d;
            --naver-gradient: linear-gradient(135deg, #03cf5d 0%, #029b45 100%);
            --youtube-red: #ff0000;
            --youtube-gradient: linear-gradient(135deg, #ff0000 0%, #cc0000 100%);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: "Pretendard Variable", Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-primary);
            height: 100vh;
            overflow: hidden;
            display: flex;
        }

        /* 전체 레이아웃 */
        .container {
            display: flex;
            width: 100%;
            height: 100vh;
        }

        /* 사이드바 */
        .sidebar {
            width: 420px;
            background-color: var(--sidebar-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-right: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            height: 100%;
            z-index: 1000;
            box-shadow: 5px 0 20px rgba(15, 23, 42, 0.05);
            transition: all 0.3s ease;
        }

        /* 사이드바 헤더 */
        .sidebar-header {
            padding: 24px;
            border-bottom: 1px solid var(--border-color);
            background: linear-gradient(to bottom, rgba(248, 250, 252, 0.5), transparent);
        }

        .logo-area {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 8px;
        }

        .logo-badge {
            background: var(--accent-gradient);
            color: white;
            font-size: 11px;
            font-weight: 700;
            padding: 4px 8px;
            border-radius: 6px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .sidebar-title {
            font-size: 20px;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: linear-gradient(135deg, #0f172a 40%, var(--text-secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .sidebar-subtitle {
            font-size: 13px;
            color: var(--text-secondary);
            margin-top: 4px;
        }

        /* 검색 및 필터 */
        .search-filter-section {
            padding: 20px 24px;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .search-box {
            position: relative;
            width: 100%;
        }

        .search-input {
            width: 100%;
            padding: 12px 16px 12px 42px;
            background-color: rgba(241, 245, 249, 0.8);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            color: var(--text-primary);
            font-size: 14px;
            transition: all 0.2s ease;
        }

        .search-input:focus {
            outline: none;
            border-color: #6366f1;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
            background-color: #ffffff;
        }

        .search-icon {
            position: absolute;
            left: 14px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-secondary);
            font-size: 16px;
            pointer-events: none;
        }

        .filter-group {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .filter-label {
            font-size: 12px;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* 카테고리 칩 목록 */
        .category-chips {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 4px;
        }

        .chip {
            padding: 6px 12px;
            background-color: rgba(241, 245, 249, 0.9);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .chip:hover {
            background-color: rgba(226, 232, 240, 1);
            color: var(--text-primary);
        }

        .chip.active {
            background: var(--accent-gradient);
            color: white;
            border-color: transparent;
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25);
        }

        /* 지역 선택 드롭다운 */
        .select-filter {
            width: 100%;
            padding: 10px 14px;
            background-color: rgba(241, 245, 249, 0.8);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            color: var(--text-primary);
            font-size: 13px;
            cursor: pointer;
            outline: none;
            transition: all 0.2s;
        }

        .select-filter:focus {
            border-color: #6366f1;
            background-color: #ffffff;
        }

        .select-filter option {
            background-color: #ffffff;
            color: var(--text-primary);
        }

        /* 리스트 카운터 */
        .list-meta {
            padding: 12px 24px;
            font-size: 12px;
            font-weight: 600;
            color: var(--text-secondary);
            border-bottom: 1px solid var(--border-color);
            background-color: rgba(241, 245, 249, 0.4);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .counter-badge {
            background-color: rgba(79, 70, 229, 0.1);
            color: #4f46e5;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 11px;
        }

        /* 식당 카드 리스트 */
        .restaurant-list {
            flex-grow: 1;
            overflow-y: auto;
            padding: 16px 24px;
            display: flex;
            flex-direction: column;
            gap: 14px;
        }

        /* 스크롤바 디자인 */
        .restaurant-list::-webkit-scrollbar {
            width: 6px;
        }

        .restaurant-list::-webkit-scrollbar-track {
            background: transparent;
        }

        .restaurant-list::-webkit-scrollbar-thumb {
            background: rgba(15, 23, 42, 0.08);
            border-radius: 4px;
        }

        .restaurant-list::-webkit-scrollbar-thumb:hover {
            background: rgba(15, 23, 42, 0.2);
        }

        /* 개별 식당 카드 */
        .restaurant-card {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 16px;
            cursor: pointer;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            flex-direction: column;
            gap: 8px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 10px rgba(15, 23, 42, 0.02);
            flex-shrink: 0 !important;
        }

        .restaurant-card::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            height: 100%;
            width: 4px;
            background: var(--accent-gradient);
            opacity: 0;
            transition: opacity 0.2s;
        }

        .restaurant-card:hover {
            background-color: var(--card-hover);
            transform: translateY(-2px);
            border-color: rgba(79, 70, 229, 0.25);
            box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
        }

        .restaurant-card:hover::before {
            opacity: 1;
        }

        .restaurant-card.active {
            background-color: rgba(79, 70, 229, 0.03);
            border-color: rgba(79, 70, 229, 0.4);
            box-shadow: 0 4px 15px rgba(79, 70, 229, 0.08);
        }

        .restaurant-card.active::before {
            opacity: 1;
        }

        .card-header-row {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 8px;
        }

        .card-title {
            font-size: 16px;
            font-weight: 700;
            color: var(--text-primary);
            line-height: 1.4;
            padding-bottom: 2px;
        }

        .card-category {
            background-color: rgba(15, 23, 42, 0.04);
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            font-size: 10px;
            font-weight: 700;
            padding: 2px 6px;
            border-radius: 4px;
            white-space: nowrap;
        }

        .card-address {
            font-size: 12.5px;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            gap: 4px;
        }

        .card-menu {
            font-size: 12.5px;
            color: #1e293b;
            background-color: rgba(15, 23, 42, 0.03);
            padding: 6px 8px;
            border-radius: 6px;
            border-left: 2px solid var(--accent-color);
            margin-top: 4px;
        }

        .card-comment {
            font-size: 12px;
            color: var(--text-secondary);
            line-height: 1.4;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            margin-top: 4px;
        }

        .card-actions {
            display: flex;
            gap: 8px;
            margin-top: 8px;
        }

        .card-btn {
            flex: 1;
            padding: 8px 10px;
            font-size: 11px;
            font-weight: 700;
            text-align: center;
            border-radius: 6px;
            text-decoration: none;
            cursor: pointer;
            transition: opacity 0.2s;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 4px;
        }

        .card-btn:hover {
            opacity: 0.9;
        }

        .btn-naver {
            background: linear-gradient(135deg, #03c75a 0%, #028a3e 100%) !important;
            color: #ffffff !important;
            font-weight: 800 !important;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.4);
            box-shadow: 0 2px 6px rgba(3, 199, 90, 0.2);
        }

        .btn-youtube {
            background: linear-gradient(135deg, #ff0000 0%, #cc0000 100%) !important;
            color: #ffffff !important;
            font-weight: 800 !important;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.4);
            box-shadow: 0 2px 6px rgba(255, 0, 0, 0.2);
        }

        /* 지도 영역 */
        #map {
            flex-grow: 1;
            height: 100vh;
        }

        /* 지도 팝업 커스텀 스타일 (밝은 테마에 맞추어 개편) */
        .leaflet-popup-content-wrapper {
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(15, 23, 42, 0.08);
            border-radius: 14px;
            color: var(--text-primary);
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.1);
            padding: 8px;
        }

        .leaflet-popup-tip {
            background: rgba(255, 255, 255, 0.98);
            border: 1px solid rgba(15, 23, 42, 0.08);
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.1);
        }

        .popup-container {
            display: flex;
            flex-direction: column;
            gap: 8px;
            max-width: 280px;
        }

        .popup-title {
            font-size: 16px;
            font-weight: 800;
            color: #0f172a;
            border-bottom: 1px solid rgba(15, 23, 42, 0.08);
            padding-bottom: 6px;
        }

        .popup-category {
            background-color: rgba(79, 70, 229, 0.08);
            color: #4f46e5;
            font-size: 10px;
            font-weight: 700;
            padding: 2px 6px;
            border-radius: 4px;
            margin-left: 6px;
            display: inline-block;
            vertical-align: middle;
        }

        .popup-item {
            font-size: 12px;
            color: var(--text-secondary);
            line-height: 1.4;
        }

        .popup-item strong {
            color: var(--text-primary);
        }

        .popup-menu {
            background-color: rgba(15, 23, 42, 0.03);
            border-left: 2px solid var(--accent-color);
            padding: 6px 8px;
            border-radius: 6px;
            color: #1e293b;
            font-size: 12px;
            margin: 4px 0;
        }

        .popup-comment {
            font-size: 11.5px;
            color: var(--text-secondary);
            font-style: italic;
            margin-top: 4px;
            border-top: 1px dashed rgba(15, 23, 42, 0.08);
            padding-top: 6px;
        }

        .popup-buttons {
            display: flex;
            gap: 8px;
            margin-top: 8px;
            border-top: 1px solid rgba(15, 23, 42, 0.08);
            padding-top: 8px;
        }

        .popup-btn {
            flex: 1;
            padding: 8px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            text-align: center;
            color: white;
            text-decoration: none;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 4px;
        }

        /* 클러스터 커스텀 디자인 (밝은 테마와 매치) */
        .marker-cluster-small {
            background-color: rgba(79, 70, 229, 0.2);
        }
        .marker-cluster-small div {
            background-color: rgba(79, 70, 229, 0.8);
            color: white;
            font-weight: 700;
        }
        .marker-cluster-medium {
            background-color: rgba(67, 56, 202, 0.2);
        }
        .marker-cluster-medium div {
            background-color: rgba(67, 56, 202, 0.8);
            color: white;
            font-weight: 700;
        }
        .marker-cluster-large {
            background-color: rgba(55, 48, 163, 0.2);
        }
        .marker-cluster-large div {
            background-color: rgba(55, 48, 163, 0.8);
            color: white;
            font-weight: 700;
        }

        /* 커스텀 마커 스타일 */
        .custom-div-icon {
            background: none;
            border: none;
        }
        .marker-pin {
            display: flex;
            align-items: center;
            justify-content: center;
            filter: drop-shadow(0px 2px 4px rgba(0,0,0,0.15));
            transition: all 0.2s ease;
        }
        .marker-pin:hover {
            transform: scale(1.25);
        }
        .marker-a {
            font-size: 26px;
        }
        .marker-b {
            font-size: 18px;
        }

        /* 모바일 뷰포트 (768px 미만) 최적화 */
        @media (max-width: 767px) {
            .container {
                flex-direction: column;
                height: 100vh !important;
                overflow: hidden;
            }
            .sidebar {
                width: 100% !important;
                height: calc(100vh - 64px) !important;
                display: flex;
            }
            #map {
                width: 100% !important;
                height: calc(100vh - 64px) !important;
                display: none; /* 기본 리스트 뷰 노출 */
            }
            .mobile-tabs {
                display: flex !important;
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                height: 64px;
                background: rgba(255, 255, 255, 0.85);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border-top: 1px solid rgba(15, 23, 42, 0.08);
                z-index: 9999;
                padding: 6px 12px;
                gap: 8px;
                justify-content: space-around;
                align-items: center;
                box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.03);
            }
            .tab-button {
                flex: 1;
                height: 48px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                border: none;
                background: transparent;
                color: var(--text-secondary);
                font-size: 11px;
                font-weight: 700;
                cursor: pointer;
                border-radius: 10px;
                transition: all 0.2s ease;
                gap: 2px;
            }
            .tab-button.active {
                color: #4f46e5;
                background-color: rgba(79, 70, 229, 0.06);
            }
            .tab-icon {
                font-size: 18px;
            }
            /* 모바일 스크롤 영역 및 입력 폼 방지 */
            .restaurant-list {
                padding-bottom: 90px !important;
            }
            .select-filter, .search-input {
                font-size: 14px !important; /* 모바일 인풋 포커스 줌 방지 */
            }
        }
        @media (min-width: 768px) {
            .mobile-tabs {
                display: none !important;
            }
        }

        /* 모바일 자연스러운 세로 스크롤 레이아웃 바인딩 */
        @media (max-width: 767px) {
            .container.mobile-scroll-mode {
                height: auto !important;
                min-height: 100vh !important;
                overflow-y: visible !important;
                overflow-x: hidden !important;
            }
            .container.mobile-scroll-mode .sidebar {
                height: auto !important;
                overflow-y: visible !important;
                display: flex !important;
            }
            .container.mobile-scroll-mode #map {
                display: none !important;
            }
        }
        /* 맵 마커 라벨 항상 표시 (v30) */
        .marker-label {
            background-color: rgba(255, 255, 255, 0.85);
            border: 1px solid #ccc;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
            font-weight: 600;
            color: #222;
            font-size: 11px;
            padding: 2px 5px;
            border-radius: 4px;
            white-space: nowrap;
        }
    </style>
    <link rel="manifest" href="manifest.json">
</head>
<body>

    <div class="container">
        
        <!-- 좌측 사이드바 -->
        <div class="sidebar">
            
            <div class="sidebar-header">
                <div class="logo-area">
                    <span class="logo-badge">M.A.G RAG</span>
                    <span class="sidebar-title">🍲 쯔양 맛집 지도</span>
                </div>
                <div class="sidebar-subtitle">
                    실시간 내비게이터(RUSH2001)
                </div>
            </div>
            
            <div class="search-filter-section">
                <!-- 검색창 -->
                <div class="search-box">
                    <span class="search-icon">🔍</span>
                    <input type="text" id="searchInput" class="search-input" placeholder="상호명, 메뉴, 주소 검색...">
                </div>
                
                <!-- 카테고리 필터 -->
                <div class="filter-group">
                    <span class="filter-label">음식 종류</span>
                    <select id="categorySelect" class="select-filter">
                        <option value="ALL">전체 음식</option>
                    </select>
                </div>
                
                <!-- 지역 필터 -->
                <div class="filter-group">
                    <span class="filter-label">지역 선택</span>
                    <select id="regionSelect" class="select-filter">
                        <option value="ALL">전국 전체</option>
                        <!-- 자바스크립트로 동적 로드 -->
                    </select>
                </div>
            </div>
            
            <!-- 리스트 메타 정보 -->
            <div class="list-meta">
                <span>정렬: 방송 순서</span>
                <div>
                    검색 결과: <span class="counter-badge" id="resultsCount">0</span>
                </div>
            </div>
            
            <!-- 맛집 리스트 스크롤 영역 -->
            <div class="restaurant-list" id="restaurantList">
                <!-- 맛집 카드가 동적으로 주입됩니다 -->
            </div>
            
        </div>
        
        <!-- 우측 지도 영역 -->
        <div id="map"></div>
        
    </div>

    <!-- 모바일 탭 바 (768px 미만 노출) -->
    <div class="mobile-tabs">
        <button id="tabList" class="tab-button active" onclick="switchTab('list')">
            <span class="tab-icon">📋</span>
            <span>목록 보기</span>
        </button>
        <button id="tabMap" class="tab-button" onclick="switchTab('map')">
            <span class="tab-icon">🗺️</span>
            <span>지도 보기</span>
        </button>
    </div>

    <!-- Leaflet.js -->
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
    <!-- Leaflet.markercluster -->
    <script src="https://unpkg.com/leaflet.markercluster@1.4.1/dist/leaflet.markercluster.js"></script>

    <script>
        // 파이썬 빌더에서 아래 변수에 데이터를 직접 바인딩합니다.
        const restaurants = {json_data_placeholder};
        
        let map;
        let markerCluster;
        let markersMap = new Map(); // id -> marker 객체 맵
        let currentFilter = { category: 'ALL', region: 'ALL', search: '' };
        
        // 1. 지도 초기화
        function initMap() {
        // 서울 중심부 기준 초기 뷰포트 및 세계지도 튕김 방지 옵션 주입
        map = L.map('map', {
            center: [36.2, 127.8], 
            zoom: 7,
            minZoom: 7, 
            maxZoom: 19,
            zoomControl: false // 커스텀 줌 버튼 위치 조정을 위해 비활성화
        });
            
            // 국토교통부 브이월드(Vworld) 한글 2D 지도 타일 교체 (한글화 100%)
            L.tileLayer('https://xdworld.vworld.kr/2d/Base/service/{z}/{x}/{y}.png', {
                attribution: '&copy; 국토교통부 브이월드 (Vworld)',
                maxZoom: 19
            }).addTo(map);
            
            // 줌 컨트롤 우측 상단으로 배치
            L.control.zoom({
                position: 'topright'
            }).addTo(map);
            
            markerCluster = L.markerClusterGroup({
                maxClusterRadius: 40,
                showCoverageOnHover: false
            });
            map.addLayer(markerCluster);
        }
        
        // 2. 필터 컨트롤 및 동적 옵션 세팅
        function initFilters() {
            const categories = new Set();
            const regions = new Set();
            
            restaurants.forEach(rest => {
                if (rest.category) categories.add(rest.category);
                const regionName = rest.region || rest.address.split(' ')[0];
                if (regionName) regions.add(regionName);
            });
            
            // 카테고리 드롭다운 렌더링
            const categorySelect = document.getElementById('categorySelect');
            categories.forEach(cat => {
                const opt = document.createElement('option');
                opt.value = cat;
                opt.textContent = cat;
                categorySelect.appendChild(opt);
            });
            
            categorySelect.onchange = (e) => {
                currentFilter.category = e.target.value;
                applyFilters();
            };
            
            // 지역 선택 드롭다운 렌더링
            const selectContainer = document.getElementById('regionSelect');
            const uniqueRegions = new Set();
            regions.forEach(reg => {
                const mainReg = reg.split(' ')[0];
                if (mainReg) uniqueRegions.add(mainReg);
            });
            
            // 가나다 순 정렬
            Array.from(uniqueRegions).sort().forEach(reg => {
                const opt = document.createElement('option');
                opt.value = reg;
                opt.textContent = reg;
                selectContainer.appendChild(opt);
            });
            
            selectContainer.onchange = (e) => {
                currentFilter.region = e.target.value;
                applyFilters();
            };
            
            // 검색바 입력 바인딩
            document.getElementById('searchInput').oninput = (e) => {
                currentFilter.search = e.target.value.toLowerCase().trim();
                applyFilters();
            };
        }
        
        // 3. 필터 적용 및 맵 마커/리스트 리로드
        function applyFilters() {
            const filtered = restaurants.filter(rest => {
                // A. 카테고리 매칭
                const matchCategory = currentFilter.category === 'ALL' || rest.category === currentFilter.category;
                
                // B. 지역 매칭
                const mainReg = rest.region ? rest.region.split(' ')[0] : rest.address.split(' ')[0];
                const matchRegion = currentFilter.region === 'ALL' || mainReg.includes(currentFilter.region);
                
                // C. 검색어 매칭
                const matchSearch = !currentFilter.search || 
                                    rest.name.toLowerCase().includes(currentFilter.search) ||
                                    rest.address.toLowerCase().includes(currentFilter.search) ||
                                    rest.main_menu.toLowerCase().includes(currentFilter.search) ||
                                    rest.comment.toLowerCase().includes(currentFilter.search);
                                    
                return matchCategory && matchRegion && matchSearch;
            });
            
            // 리스트 카운터 업데이트
            document.getElementById('resultsCount').textContent = filtered.length;
            
            // 리스트 뷰포트 업데이트
            renderList(filtered);
            
            // 지도 마커 갱신
            renderMarkers(filtered);
        }
        
        // 4. 좌측 리스트 렌더링
        function renderList(list) {
            const container = document.getElementById('restaurantList');
            container.innerHTML = '';
            
            if (list.length === 0) {
                container.innerHTML = '<div style="text-align:center; padding: 40px 0; color:var(--text-secondary); font-size:14px;">검색 조건에 맞는 맛집이 없습니다.</div>';
                return;
            }
            
            list.forEach(rest => {
                const id = rest.name.replace(/\s+/g, '-');
                const card = document.createElement('div');
                card.className = 'restaurant-card';
                card.id = `card-${id}`;
                
                card.innerHTML = `
                    <div class="card-header-row">
                        <div class="card-title">${rest.name}</div>
                        <span class="card-category">${rest.category}</span>
                    </div>
                    <div class="card-address">
                        📍 ${rest.address}
                    </div>
                    <div class="card-menu">
                        🍲 대표메뉴: ${rest.main_menu}
                    </div>
                    <div class="card-comment">
                        ${rest.comment}
                    </div>
                    <div class="card-actions">
                        <a href="${rest.naver_map_url}" target="_blank" class="card-btn btn-naver" onclick="event.stopPropagation();">
                            💚 네이버 지도
                        </a>
                        <a href="${rest.video_url}" target="_blank" class="card-btn btn-youtube" onclick="event.stopPropagation();">
                            🎥 유튜브 보기
                        </a>
                    </div>
                `;
                
                // 카드 클릭 이벤트
                card.onclick = () => {
                    document.querySelectorAll('.restaurant-card').forEach(c => c.classList.remove('active'));
                    card.classList.add('active');
                    
                    if (window.innerWidth < 768) {
                        switchTab('map', true); // 카드 클릭으로 인한 전환은 리셋 스킵
                    }
                    
                    if (rest.latitude && rest.longitude) {
                        map.flyTo([rest.latitude, rest.longitude], 16, {
                            animate: true,
                            duration: 1.2
                        });
                        
                        const marker = markersMap.get(rest.name);
                        if (marker) {
                            // 클러스터 그룹 내부에 숨겨진 마커를 안전하게 꺼내어 팝업 활성화
                            markerCluster.zoomToShowLayer(marker, () => {
                                marker.openPopup();
                            });
                        }
                    }
                };
                
                container.appendChild(card);
            });
        }
        
        // 5. 우측 맵 마커 렌더링
        function renderMarkers(list) {
            markerCluster.clearLayers();
            markersMap.clear();
            
            list.forEach(rest => {
                if (!rest.latitude || !rest.longitude) return;
                
                // 마커 아이콘 분기 (A그룹: 붉은별, B그룹: 파란원)
                let markerIcon;
                if (rest.group === 'A') {
                    markerIcon = L.divIcon({
                        html: '<div class="marker-pin marker-a">⭐</div>',
                        className: 'custom-div-icon',
                        iconSize: [30, 30],
                        iconAnchor: [15, 30]
                    });
                } else {
                    markerIcon = L.divIcon({
                        html: '<div class="marker-pin marker-b">🔵</div>',
                        className: 'custom-div-icon',
                        iconSize: [24, 24],
                        iconAnchor: [12, 24]
                    });
                }
                
                const marker = L.marker([rest.latitude, rest.longitude], { icon: markerIcon });
                
                // 마커 아래에 상호명 항상 표시 (v30)
                marker.bindTooltip(rest.name, {
                    permanent: true,
                    direction: 'bottom',
                    className: 'marker-label',
                    offset: [0, 5]
                });
                
                const popupContent = `
                    <div class="popup-container">
                        <div class="popup-title">
                            ${rest.name}
                            <span class="popup-category">${rest.category}</span>
                        </div>
                        <div class="popup-item">📌 <strong>주소:</strong> ${rest.address}</div>
                        <div class="popup-menu">🍲 <strong>대표메뉴:</strong> ${rest.main_menu}</div>
                        <div class="popup-item" style="font-size:11px;">🎥 <strong>방송명:</strong> ${rest.video_title}</div>
                        <div class="popup-comment">"${rest.comment}"</div>
                        <div class="popup-buttons">
                            <a href="${rest.naver_map_url}" target="_blank" class="popup-btn btn-naver">💚 네이버맵</a>
                            <a href="${rest.video_url}" target="_blank" class="popup-btn btn-youtube">🎥 유튜브</a>
                        </div>
                    </div>
                `;
                
                marker.bindPopup(popupContent, {
                    maxWidth: 300
                });
                
                marker.on('click', () => {
                    const cardId = `card-${rest.name.replace(/\s+/g, '-')}`;
                    const cardElement = document.getElementById(cardId);
                    
                    if (cardElement) {
                        document.querySelectorAll('.restaurant-card').forEach(c => c.classList.remove('active'));
                        cardElement.classList.add('active');
                        cardElement.scrollIntoView({
                            behavior: 'smooth',
                            block: 'center'
                        });
                    }
                });
                
                markerCluster.addLayer(marker);
                markersMap.set(rest.name, marker);
            });
            
            if (list.length > 0 && map) {
                const group = new L.featureGroup(Array.from(markersMap.values()));
                map.fitBounds(group.getBounds().pad(0.1));
            }
        }

        // 모바일 탭 스위처 (카드 클릭 시 지도 리셋 방지 인자 추가 및 모바일 세로 확장 스크롤 바인딩)
        function switchTab(tab, isCardClick = false) {
            const sidebar = document.querySelector('.sidebar');
            const mapEl = document.getElementById('map');
            const tabList = document.getElementById('tabList');
            const tabMap = document.getElementById('tabMap');
            const container = document.querySelector('.container');
            
            if (tab === 'list') {
                sidebar.style.display = 'flex';
                mapEl.style.display = 'none';
                tabList.classList.add('active');
                tabMap.classList.remove('active');
                
                // 모바일 뷰포트에서 세로 관성 스크롤 모드 개방
                if (window.innerWidth < 768) {
                    container.classList.add('mobile-scroll-mode');
                }
            } else if (tab === 'map') {
                sidebar.style.display = 'none';
                mapEl.style.display = 'block';
                tabList.classList.remove('active');
                tabMap.classList.add('active');
                
                // 모바일 뷰포트에서 전체화면 지도 뷰로 락인
                if (window.innerWidth < 768) {
                    container.classList.remove('mobile-scroll-mode');
                    mapEl.style.height = 'calc(100vh - 64px)';
                }
                
                setTimeout(() => {
                    map.invalidateSize();
                    // 카드 클릭 이동 시에는 7레벨 원복 리셋을 건너뜀 (레이스 컨디션 차단)
                    if (!isCardClick) {
                        map.setView([36.2, 127.8], 7);
                    }
                }, 100);
            }
        }

        window.onload = () => {
            initMap();
            initFilters();
            applyFilters();
            
            // 모바일 뷰 초기 상태 강제 세로 스크롤 바인딩
            if (window.innerWidth < 768) {
                switchTab('list');
            }
            
            // PWA 서비스 워커 등록
            if ('serviceWorker' in navigator) {
                navigator.serviceWorker.register('service-worker.js')
                    .then(reg => console.log('Service Worker registered successfully!', reg))
                    .catch(err => console.log('Service Worker registration failed: ', err));
            }
        };
    </script>
</body>
</html>
"""
    
    # JSON 플레이스홀더 치환
    json_str = json.dumps(restaurants_data, ensure_ascii=False)
    html_content = html_template.replace("{json_data_placeholder}", json_str)
    
    with open(html_out_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"[SUCCESS] Light theme dashboard generated at: {html_out_path}")

if __name__ == "__main__":
    build_html_dashboard()
