# -*- coding: utf-8 -*-
# 전국/서울/대전/인천/부산/대구/울산/광주 교통사망사고 시각화 Flask 서버

from flask import Flask, render_template, jsonify, Response, request
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium
from folium.plugins import MarkerCluster
import os, sys

# ==============================
# 1) 경로: 반드시 "실제 존재하는 경로"로 수정하세요
# ==============================
CSV_PATH = r"C:\work\텐트메이커1기\project\사망교통사고정보(2022년).csv"   # ← 정확한 파일명
SIG_SHP  = r"C:\Users\user\Downloads\시군구\SIG.shp"
CTP_SHP  = r"C:\Users\user\Downloads\시도 (1)\CTPRVN.shp"

for p in [CSV_PATH, SIG_SHP, CTP_SHP]:
    if not os.path.exists(p):
        raise FileNotFoundError(f"경로가 존재하지 않습니다: {p}")

# ==============================
# 2) Flask 기본
# ==============================
app = Flask(__name__, template_folder="templates", static_folder="static")
os.makedirs(os.path.join("static", "map"), exist_ok=True)

# ==============================
# 3) 공통 유틸
# ==============================
def popup_from_row(row, extra=None):
    pairs = [
        ("발생년", row.get("발생년")),
        ("발생년월일시", row.get("발생년월일시")),
        ("주야", row.get("주야")),
        ("요일", row.get("요일")),
        ("사망자수", row.get("사망자수")),
        ("부상자수", row.get("부상자수")),
        ("발생지시도", row.get("발생지시도")),
        ("발생지시군구", row.get("발생지시군구")),
        ("사고유형_대분류", row.get("사고유형_대분류")),
        ("사고유형_중분류", row.get("사고유형_중분류")),
        ("도로형태_대분류", row.get("도로형태_대분류")),
        ("도로형태", row.get("도로형태")),
        ("가해자법규위반", row.get("가해자법규위반")),
        ("가해자_당사자종별", row.get("가해자_당사자종별")),
        ("피해자_당사자종별", row.get("피해자_당사자종별")),
    ]
    if extra:
        pairs += extra
    html = "<b>사고 정보</b><br>" + "<br>".join(
        f"<b>{k}:</b> {v}" for k, v in pairs if pd.notna(v)
    )
    return folium.Popup(html, max_width=420)

def build_map_boundary_points(ctp_gdf, merged_gdf, acc_gdf, center, outfile, boundary_name):
    m = folium.Map(location=center, zoom_start=11, tiles="OpenStreetMap")

    # 시/도 외곽선
    folium.GeoJson(
        ctp_gdf,
        name=f"{boundary_name} 외곽선",
        style_function=lambda x: {"fillColor": "transparent", "color": "black", "weight": 2.0, "fillOpacity": 0},
    ).add_to(m)

    # 구/군 경계 + 툴팁
    label_col = "SIG_KOR_NM" if "SIG_KOR_NM" in merged_gdf.columns else ("구명" if "구명" in merged_gdf.columns else None)
    fields = [c for c in [label_col, "사망사고발생건수"] if c]
    aliases = (["지역:", "사망사고발생건수:"] if label_col else ["사망사고발생건수:"])
    folium.GeoJson(
        merged_gdf,
        name=f"{boundary_name} 경계",
        style_function=lambda x: {"fillColor": "transparent", "color": "blue", "weight": 1.2, "fillOpacity": 0},
        tooltip=folium.GeoJsonTooltip(fields=fields, aliases=aliases, localize=True),
    ).add_to(m)

    # 사고 지점 마커
    for _, r in acc_gdf.iterrows():
        folium.Marker(
            [r["위도"], r["경도"]],
            popup=popup_from_row(r),
            icon=folium.Icon(color="red", icon="info-sign"),
        ).add_to(m)

    folium.LayerControl().add_to(m)
    out_path = os.path.join("static", "map", outfile)
    m.save(out_path)
    return out_path

# ==============================
# 4) 데이터 로드 & 공간 전처리
# ==============================
def load_all():
    # CSV
    df = pd.read_csv(CSV_PATH, encoding="euc-kr")
    # 날짜/연도
    df["발생년월일시"] = pd.to_datetime(df.get("발생년월일시"), errors="coerce")
    if "발생년" not in df.columns:
        df["발생년"] = df["발생년월일시"].dt.year

    # 좌표
    df["위도"] = pd.to_numeric(df.get("위도"), errors="coerce")
    df["경도"] = pd.to_numeric(df.get("경도"), errors="coerce")
    df = df.dropna(subset=["위도", "경도"]).copy()

    # SHP
    gdf_sig = gpd.read_file(SIG_SHP, encoding="euc-kr")
    gdf_ctp = gpd.read_file(CTP_SHP, encoding="euc-kr")
    if gdf_sig.crs != gdf_ctp.crs:
        gdf_ctp = gdf_ctp.to_crs(gdf_sig.crs)

    # 시군구에 시도명 부여
    gdf_sig_ctp = gpd.sjoin(
        gdf_sig,
        gdf_ctp[["CTP_KOR_NM", "geometry"]],
        how="left",
        predicate="intersects"
    )

    # 사고 포인트 (WGS84)
    geo_df = gpd.GeoDataFrame(
        df.copy(),
        geometry=[Point(xy) for xy in zip(df["경도"], df["위도"])],
        crs="EPSG:4326"
    )

    # 전국 (시도 Choropleth용)
    gdf_ctp_4326 = gdf_ctp.to_crs(geo_df.crs)
    nation_acc = gpd.sjoin(
        geo_df, gdf_ctp_4326[["CTP_KOR_NM", "geometry"]], how="inner", predicate="intersects"
    ).rename(columns={"CTP_KOR_NM": "시도명"})
    ctp_counts = nation_acc["시도명"].value_counts().rename_axis("시도명").reset_index(name="사망사고발생건수")
    ctp_with_count = gdf_ctp_4326.merge(ctp_counts, left_on="CTP_KOR_NM", right_on="시도명", how="left")
    ctp_with_count["사망사고발생건수"] = ctp_with_count["사망사고발생건수"].fillna(0).astype(int)

    # 도시 생성 함수
    def make_city(ctp_name, districts, center, outfile):
        ctp = gdf_ctp[gdf_ctp["CTP_KOR_NM"] == ctp_name].copy().to_crs(geo_df.crs)
        acc = gpd.sjoin(geo_df, ctp, how="inner", predicate="intersects")
        counts = acc.groupby("발생지시군구").size().reset_index(name="사망사고발생건수")
        counts["발생지시군구"] = counts["발생지시군구"].astype(str).str.strip()

        gdf_city = gdf_sig_ctp[
            (gdf_sig_ctp["CTP_KOR_NM"] == ctp_name) &
            (gdf_sig_ctp["SIG_KOR_NM"].isin(districts))
        ].copy()
        gdf_city["SIG_KOR_NM"] = gdf_city["SIG_KOR_NM"].astype(str).str.strip()

        merged = gdf_city.merge(counts, left_on="SIG_KOR_NM", right_on="발생지시군구", how="left") \
                         .drop(columns=["발생지시군구"], errors="ignore") \
                         .fillna({"사망사고발생건수": 0})
        # 지도 저장 (정적)
        build_map_boundary_points(ctp, merged, acc, center, outfile, ctp_name)
        return acc.drop(columns=["geometry"], errors="ignore"), merged, ctp

    # 서울
    seoul_dists = ["강남구","강동구","강북구","강서구","관악구","광진구","구로구","금천구","노원구",
                   "도봉구","동대문구","동작구","마포구","서대문구","서초구","성동구","성북구",
                   "송파구","양천구","영등포구","용산구","은평구","종로구","중구","중랑구"]
    SEOUL_ACC, SEOUL_GDF, SEOUL_CTP = make_city("서울특별시", seoul_dists, [37.5665,126.9780], "seoul_map.html")

    # 대전
    daejeon_dists = ["동구","중구","서구","유성구","대덕구"]
    DAEJEON_ACC, DAEJEON_GDF, DAEJEON_CTP = make_city("대전광역시", daejeon_dists, [36.3504,127.3845], "daejeon_map.html")

    # 인천
    incheon_dists = ["중구","동구","미추홀구","연수구","남동구","부평구","계양구","서구","강화군","옹진군"]
    INCHEON_ACC, INCHEON_GDF, INCHEON_CTP = make_city("인천광역시", incheon_dists, [37.4563,126.7052], "incheon_map.html")

    # ★ 부산/대구/울산/광주 추가
    busan_dists = ["중구","서구","동구","영도구","부산진구","동래구","남구","북구","강서구","해운대구","사하구","금정구","연제구","수영구","사상구","기장군"]
    BUSAN_ACC, BUSAN_GDF, BUSAN_CTP = make_city("부산광역시", busan_dists, [35.1796,129.0756], "busan_map.html")

    daegu_dists = ["중구","동구","서구","남구","북구","수성구","달서구","달성군"]
    DAEGU_ACC, DAEGU_GDF, DAEGU_CTP = make_city("대구광역시", daegu_dists, [35.8714,128.6014], "daegu_map.html")

    ulsan_dists = ["중구","남구","동구","북구","울주군"]
    ULSAN_ACC, ULSAN_GDF, ULSAN_CTP = make_city("울산광역시", ulsan_dists, [35.5384,129.3114], "ulsan_map.html")

    gwangju_dists = ["동구","서구","남구","북구","광산구"]
    GWANGJU_ACC, GWANGJU_GDF, GWANGJU_CTP = make_city("광주광역시", gwangju_dists, [35.1595,126.8526], "gwangju_map.html")

    # 전국 Choropleth 지도 저장
    def build_total():
        m = folium.Map(location=[36.5, 127.8], zoom_start=7, tiles="OpenStreetMap")
        folium.Choropleth(
            geo_data=ctp_with_count.to_json(),
            data=ctp_with_count,
            columns=["시도명", "사망사고발생건수"],
            key_on="feature.properties.시도명",
            fill_opacity=0.7, line_opacity=0.6, line_weight=0.8,
            legend_name="시도별 사망사고 발생건수 (건)",
        ).add_to(m)
        folium.GeoJson(
            ctp_with_count,
            name="시도 경계/툴팁",
            style_function=lambda x: {"fillColor": "transparent", "color": "black", "weight": 1.0, "fillOpacity": 0},
            tooltip=folium.GeoJsonTooltip(fields=["시도명", "사망사고발생건수"], aliases=["시도:", "사망사고발생건수:"], localize=True),
        ).add_to(m)
        cluster = MarkerCluster(name="사고 지점(클러스터)").add_to(m)
        for _, r in nation_acc.iterrows():
            folium.Marker(
                [r["위도"], r["경도"]],
                popup=popup_from_row(r, extra=[("시도명(공간조인)", r.get("시도명"))]),
                icon=folium.Icon(icon="info-sign"),
            ).add_to(cluster)
        folium.LayerControl().add_to(m)
        out_path = os.path.join("static", "map", "total_map.html")
        m.save(out_path)
        return out_path

    TOTAL_MAP = build_total()

    # 도시별 차트/지표용(geometry 제거)
    def to_plain(gdf): return gdf.drop(columns=["geometry"], errors="ignore").copy()

    return {
        "DF": df,
        "NATION_ACC": to_plain(nation_acc),
        "CTP_WITH_COUNT": ctp_with_count,
        "TOTAL_MAP": TOTAL_MAP,

        "SEOUL_ACC": to_plain(SEOUL_ACC), "SEOUL_GDF": SEOUL_GDF, "SEOUL_CTP": SEOUL_CTP,
        "DAEJEON_ACC": to_plain(DAEJEON_ACC), "DAEJEON_GDF": DAEJEON_GDF, "DAEJEON_CTP": DAEJEON_CTP,
        "INCHEON_ACC": to_plain(INCHEON_ACC), "INCHEON_GDF": INCHEON_GDF, "INCHEON_CTP": INCHEON_CTP,

        "BUSAN_ACC": to_plain(BUSAN_ACC), "BUSAN_GDF": BUSAN_GDF, "BUSAN_CTP": BUSAN_CTP,
        "DAEGU_ACC": to_plain(DAEGU_ACC), "DAEGU_GDF": DAEGU_GDF, "DAEGU_CTP": DAEGU_CTP,
        "ULSAN_ACC": to_plain(ULSAN_ACC), "ULSAN_GDF": ULSAN_GDF, "ULSAN_CTP": ULSAN_CTP,
        "GWANGJU_ACC": to_plain(GWANGJU_ACC), "GWANGJU_GDF": GWANGJU_GDF, "GWANGJU_CTP": GWANGJU_CTP,
    }

# ==============================
# 5) 데이터 준비 (서버 기동 시 1회)
# ==============================
DATA = load_all()

# ==============================
# 6) API (요약/분석)
# ==============================
def get_city_df(city):
    city = (city or "seoul").lower()
    return {
        "national": DATA["DF"],
        "seoul":    DATA["SEOUL_ACC"],
        "daejeon":  DATA["DAEJEON_ACC"],
        "incheon":  DATA["INCHEON_ACC"],
        "busan":    DATA["BUSAN_ACC"],
        "daegu":    DATA["DAEGU_ACC"],
        "ulsan":    DATA["ULSAN_ACC"],
        "gwangju":  DATA["GWANGJU_ACC"],
    }.get(city, DATA["SEOUL_ACC"])

def summary_stats(city="seoul"):
    X = get_city_df(city)
    deaths = pd.to_numeric(X.get("사망자수"), errors="coerce").fillna(0).sum() if "사망자수" in X.columns else 0
    injuries = pd.to_numeric(X.get("부상자수"), errors="coerce").fillna(0).sum() if "부상자수" in X.columns else 0
    return {"accidents": int(len(X)), "deaths": int(deaths), "injuries": int(injuries)}

@app.route("/api/summary")
def api_summary():
    return jsonify(summary_stats(request.args.get("city")))

@app.route("/api/violation")
def api_violation():
    X = get_city_df(request.args.get("city"))
    s = X.get("가해자법규위반")
    return jsonify({} if s is None else s.value_counts().to_dict())

@app.route("/api/roadtype")
def api_roadtype():
    X = get_city_df(request.args.get("city"))
    s = X.get("도로형태_대분류")
    return jsonify({} if s is None else s.value_counts().to_dict())

@app.route("/api/victim_death")
def api_victim_death():
    X = get_city_df(request.args.get("city"))
    if "피해자_당사자종별" not in X.columns or "사망자수" not in X.columns: return jsonify({})
    d = X.groupby("피해자_당사자종별")["사망자수"].sum(min_count=1).fillna(0).sort_values(ascending=False).to_dict()
    return jsonify(d)

@app.route("/api/offender_death")
def api_offender_death():
    X = get_city_df(request.args.get("city"))
    if "가해자_당사자종별" not in X.columns or "사망자수" not in X.columns: return jsonify({})
    d = X.groupby("가해자_당사자종별")["사망자수"].sum(min_count=1).fillna(0).sort_values(ascending=False).to_dict()
    return jsonify(d)

@app.route("/api/hourly")
def api_hourly():
    X = get_city_df(request.args.get("city")).copy()
    X["발생년월일시"] = pd.to_datetime(X.get("발생년월일시"), errors="coerce")
    X["hour"] = X["발생년월일시"].dt.hour
    d = X["hour"].value_counts().sort_index().to_dict()
    return jsonify(d)

@app.route("/api/daynight")
def api_daynight():
    X = get_city_df(request.args.get("city"))
    s = X.get("주야")
    return jsonify({} if s is None else s.value_counts().to_dict())

@app.route("/api/commute")
def api_commute():
    X = get_city_df(request.args.get("city")).copy()
    X["발생년월일시"] = pd.to_datetime(X.get("발생년월일시"), errors="coerce")
    X["hour"] = X["발생년월일시"].dt.hour
    def tag(h):
        if pd.isna(h): return None
        h = int(h)
        if 7 <= h <= 9: return "출근(07~09)"
        if 17 <= h <= 19: return "퇴근(17~19)"
        return None
    X["출퇴근구분"] = X["hour"].apply(tag)
    X = X.dropna(subset=["출퇴근구분"])
    return jsonify(X["출퇴근구분"].value_counts().to_dict())

@app.route("/api/district_counts")
def api_district_counts():
    # 간단히: 지도 툴팁용 집계는 city DF에서 발생지시군구 기준 카운트
    X = get_city_df(request.args.get("city"))
    s = X.get("발생지시군구")
    return jsonify({} if s is None else s.value_counts().to_dict())

# ==============================
# 7) HTML
# ==============================
@app.route("/")
def home():
    return render_template("index.html")

# (선택) 별도 템플릿 필요 시 추가 가능
@app.route("/total")
def total_page():
    return Response(status=404)

# ==============================
# 8) 실행
# ==============================
if __name__ == "__main__":
    app.run(debug=True)
