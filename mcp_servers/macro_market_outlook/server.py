#!/usr/bin/env uv run
"""
Macro Market Outlook MCP Server - 매크로/시장 전망 에이전트 도구들
HMA Gateway의 macro_market_outlook_agent 도구들을 그대로 복사하여 구현

총 18개 도구:
C01T003, C01T009, C01T010, C01T012, C01T013, C01T016, C01T017, C01T021,
C01T033, C01T034, C01T038, C01T052, C01T055, C01T056, C01T057, C01T062,
C01T069, C01T070
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MCP 서버 초기화
mcp = FastMCP("Macro Market Outlook MCP Server")

# ==================== HMA Gateway 원본 도구 로직 복사 ====================


@mcp.tool()
def C01T003_tool(indicator: str, region: str, period: str, comparison: str) -> dict:
    """
    매크로 지표의 전년동기비/전월대비 증가율을 계산합니다.
    (HMA Gateway C01T003_tool 원본 로직 그대로 복사)
    """
    # 지표별 지역별 증가율 데이터
    growth_data = {
        "환율": {
            "미국": {"전년동기비": 0.023, "전월대비": 0.015, "전분기대비": 0.018},
            "유럽": {"전년동기비": 0.031, "전월대비": 0.022, "전분기대비": 0.025},
            "일본": {"전년동기비": -0.012, "전월대비": -0.008, "전분기대비": -0.010},
        },
        "금리": {
            "미국": {"전년동기비": 0.125, "전월대비": 0.025, "전분기대비": 0.075},
            "유럽": {"전년동기비": 0.085, "전월대비": 0.015, "전분기대비": 0.045},
            "일본": {"전년동기비": 0.005, "전월대비": 0.000, "전분기대비": 0.002},
        },
        "물가": {
            "미국": {"전년동기비": 0.034, "전월대비": 0.003, "전분기대비": 0.012},
            "유럽": {"전년동기비": 0.028, "전월대비": 0.002, "전분기대비": 0.008},
            "일본": {"전년동기비": 0.015, "전월대비": 0.001, "전분기대비": 0.004},
        },
        "GDP": {
            "미국": {"전년동기비": 0.025, "전월대비": 0.006, "전분기대비": 0.018},
            "유럽": {"전년동기비": 0.018, "전월대비": 0.004, "전분기대비": 0.012},
            "일본": {"전년동기비": 0.012, "전월대비": 0.003, "전분기대비": 0.008},
        },
    }

    # 기본값
    default_growth = {"전년동기비": 0.02, "전월대비": 0.005, "전분기대비": 0.015}

    # 지표와 지역에 따른 데이터 선택
    indicator_data = growth_data.get(
        indicator,
        {"미국": default_growth, "유럽": default_growth, "일본": default_growth},
    )
    region_data = indicator_data.get(region, default_growth)

    # 비교 기준에 따른 증가율 선택
    growth_rate = region_data.get(comparison, 0.02)

    return {"growth_rate": growth_rate}


@mcp.tool()
def C01T009_tool(symbol: str, factors: List[str]) -> dict:
    """
    주식의 매크로 민감도를 분석합니다.
    (HMA Gateway C01T009_tool 원본 로직 그대로 복사)
    """
    # 종목별 매크로 팩터 민감도 데이터
    macro_sensitivity = {
        "A035720": {  # LG전자
            "금리": -0.15,
            "환율": 0.25,
            "유가": -0.08,
            "GDP": 0.35,
            "인플레이션": -0.12,
            "실업률": -0.18,
            "소비자신뢰지수": 0.22,
        },
        "A005930": {  # 삼성전자
            "금리": -0.18,
            "환율": 0.45,
            "유가": -0.05,
            "GDP": 0.28,
            "인플레이션": -0.08,
            "실업률": -0.15,
            "소비자신뢰지수": 0.18,
        },
        "A000660": {  # SK하이닉스
            "금리": -0.25,
            "환율": 0.55,
            "유가": -0.12,
            "GDP": 0.42,
            "인플레이션": -0.15,
            "실업률": -0.22,
            "소비자신뢰지수": 0.28,
        },
        "A010950": {  # SK하이닉스
            "금리": -0.22,
            "환율": 0.52,
            "유가": -0.10,
            "GDP": 0.38,
            "인플레이션": -0.13,
            "실업률": -0.20,
            "소비자신뢰지수": 0.25,
        },
    }

    # 기본값
    default_sensitivity = {
        "금리": -0.15,
        "환율": 0.30,
        "유가": -0.08,
        "GDP": 0.25,
        "인플레이션": -0.10,
        "실업률": -0.15,
        "소비자신뢰지수": 0.20,
    }

    symbol_data = macro_sensitivity.get(symbol, default_sensitivity)

    # 요청된 팩터들의 민감도
    factor_analysis = {}
    total_sensitivity = 0

    for factor in factors:
        sensitivity = symbol_data.get(factor, 0.0)
        factor_analysis[factor] = {
            "sensitivity": sensitivity,
            "impact_level": (
                "높음"
                if abs(sensitivity) > 0.3
                else "보통" if abs(sensitivity) > 0.15 else "낮음"
            ),
            "direction": (
                "양의 상관관계"
                if sensitivity > 0
                else "음의 상관관계" if sensitivity < 0 else "무관"
            ),
        }
        total_sensitivity += abs(sensitivity)

    # 전체 매크로 민감도 평가
    overall_sensitivity = total_sensitivity / len(factors) if factors else 0

    return {
        "symbol": symbol,
        "analyzed_factors": factors,
        "factor_analysis": factor_analysis,
        "overall_macro_sensitivity": round(overall_sensitivity, 3),
        "sensitivity_level": (
            "매우 높음"
            if overall_sensitivity > 0.4
            else (
                "높음"
                if overall_sensitivity > 0.25
                else "보통" if overall_sensitivity > 0.15 else "낮음"
            )
        ),
        "all_available_factors": list(symbol_data.keys()),
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    }


@mcp.tool()
def C01T010_tool(region: str, indicators: List[str]) -> dict:
    """
    지역별 경제 지표를 비교합니다.
    (HMA Gateway C01T010_tool 원본 로직 그대로 복사)
    """
    # 지역별 경제 지표 데이터
    economic_indicators = {
        "미국": {
            "GDP성장률": 2.5,
            "인플레이션": 3.4,
            "실업률": 3.8,
            "기준금리": 5.25,
            "소비자신뢰지수": 105.2,
            "제조업PMI": 52.8,
            "서비스업PMI": 54.1,
        },
        "유럽": {
            "GDP성장률": 1.8,
            "인플레이션": 2.9,
            "실업률": 6.2,
            "기준금리": 4.0,
            "소비자신뢰지수": 98.5,
            "제조업PMI": 48.2,
            "서비스업PMI": 51.3,
        },
        "일본": {
            "GDP성장률": 1.2,
            "인플레이션": 1.8,
            "실업률": 2.5,
            "기준금리": -0.1,
            "소비자신뢰지수": 88.7,
            "제조업PMI": 49.5,
            "서비스업PMI": 50.8,
        },
        "중국": {
            "GDP성장률": 5.2,
            "인플레이션": 2.1,
            "실업률": 5.1,
            "기준금리": 3.45,
            "소비자신뢰지수": 92.3,
            "제조업PMI": 51.2,
            "서비스업PMI": 52.6,
        },
        "한국": {
            "GDP성장률": 2.8,
            "인플레이션": 2.6,
            "실업률": 2.9,
            "기준금리": 3.5,
            "소비자신뢰지수": 95.8,
            "제조업PMI": 50.9,
            "서비스업PMI": 52.1,
        },
    }

    if region not in economic_indicators:
        return {"error": f"지원하지 않는 지역입니다: {region}"}

    region_data = economic_indicators[region]

    # 요청된 지표들의 데이터
    indicator_results = {}
    for indicator in indicators:
        if indicator in region_data:
            value = region_data[indicator]

            # 지표별 평가 기준
            if indicator == "GDP성장률":
                assessment = (
                    "양호" if value > 2.0 else "보통" if value > 1.0 else "부진"
                )
            elif indicator == "인플레이션":
                assessment = (
                    "안정"
                    if 1.5 <= value <= 3.0
                    else "주의" if value > 3.0 else "디플레이션위험"
                )
            elif indicator == "실업률":
                assessment = (
                    "양호" if value < 4.0 else "보통" if value < 6.0 else "부진"
                )
            elif indicator == "기준금리":
                assessment = (
                    "완화적" if value < 2.0 else "중립적" if value < 4.0 else "긴축적"
                )
            else:
                assessment = "양호" if value > 50 else "부진"

            indicator_results[indicator] = {
                "value": value,
                "assessment": assessment,
                "unit": (
                    "%"
                    if indicator in ["GDP성장률", "인플레이션", "실업률", "기준금리"]
                    else "포인트"
                ),
            }
        else:
            indicator_results[indicator] = {"error": "해당 지표 데이터 없음"}

    # 전체 경제 상황 평가
    positive_indicators = sum(
        [
            1
            for ind, data in indicator_results.items()
            if isinstance(data, dict) and data.get("assessment") in ["양호", "안정"]
        ]
    )
    total_indicators = len(
        [
            ind
            for ind, data in indicator_results.items()
            if isinstance(data, dict) and "value" in data
        ]
    )

    if total_indicators > 0:
        economic_health_score = positive_indicators / total_indicators
        if economic_health_score > 0.7:
            overall_assessment = "양호"
        elif economic_health_score > 0.4:
            overall_assessment = "보통"
        else:
            overall_assessment = "부진"
    else:
        overall_assessment = "데이터 부족"

    return {
        "region": region,
        "analyzed_indicators": indicators,
        "indicator_results": indicator_results,
        "overall_assessment": overall_assessment,
        "economic_health_score": (
            round(economic_health_score, 3) if total_indicators > 0 else 0
        ),
        "available_indicators": list(region_data.keys()),
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    }


@mcp.tool()
def C01T012_tool(region: str, forecast_period: int = 12) -> dict:
    """
    지역별 경제 전망을 예측합니다.
    (HMA Gateway C01T012_tool 원본 로직 그대로 복사)
    """
    # 지역별 경제 전망 데이터
    economic_forecasts = {
        "미국": {
            "GDP성장률": {"current": 2.5, "forecast": [2.3, 2.1, 2.0, 1.9]},
            "인플레이션": {"current": 3.4, "forecast": [3.2, 3.0, 2.8, 2.6]},
            "기준금리": {"current": 5.25, "forecast": [5.0, 4.75, 4.5, 4.25]},
            "실업률": {"current": 3.8, "forecast": [3.9, 4.0, 4.1, 4.2]},
        },
        "유럽": {
            "GDP성장률": {"current": 1.8, "forecast": [1.6, 1.5, 1.4, 1.3]},
            "인플레이션": {"current": 2.9, "forecast": [2.7, 2.5, 2.3, 2.1]},
            "기준금리": {"current": 4.0, "forecast": [3.75, 3.5, 3.25, 3.0]},
            "실업률": {"current": 6.2, "forecast": [6.3, 6.4, 6.5, 6.6]},
        },
        "일본": {
            "GDP성장률": {"current": 1.2, "forecast": [1.1, 1.0, 0.9, 0.8]},
            "인플레이션": {"current": 1.8, "forecast": [1.6, 1.4, 1.2, 1.0]},
            "기준금리": {"current": -0.1, "forecast": [0.0, 0.1, 0.2, 0.3]},
            "실업률": {"current": 2.5, "forecast": [2.6, 2.7, 2.8, 2.9]},
        },
        "한국": {
            "GDP성장률": {"current": 2.8, "forecast": [2.6, 2.4, 2.2, 2.0]},
            "인플레이션": {"current": 2.6, "forecast": [2.4, 2.2, 2.0, 1.8]},
            "기준금리": {"current": 3.5, "forecast": [3.25, 3.0, 2.75, 2.5]},
            "실업률": {"current": 2.9, "forecast": [3.0, 3.1, 3.2, 3.3]},
        },
    }

    if region not in economic_forecasts:
        return {"error": f"지원하지 않는 지역입니다: {region}"}

    region_forecasts = economic_forecasts[region]

    # 월별 예측 데이터 생성
    monthly_forecasts = []

    for month in range(1, min(forecast_period + 1, 13)):  # 최대 12개월
        forecast_date = (datetime.now() + timedelta(days=month * 30)).strftime("%Y-%m")

        month_data = {"month": forecast_date}

        for indicator, data in region_forecasts.items():
            # 분기별 예측값을 월별로 보간
            quarter_index = min((month - 1) // 3, len(data["forecast"]) - 1)
            forecast_value = data["forecast"][quarter_index]

            month_data[indicator] = forecast_value

        monthly_forecasts.append(month_data)

    # 경제 전망 요약
    forecast_summary = {}
    for indicator, data in region_forecasts.items():
        current_value = data["current"]
        end_forecast = data["forecast"][-1]
        change = end_forecast - current_value

        forecast_summary[indicator] = {
            "current": current_value,
            "forecast_end": end_forecast,
            "expected_change": round(change, 3),
            "trend": "상승" if change > 0 else "하락" if change < 0 else "횡보",
        }

    return {
        "region": region,
        "forecast_period_months": forecast_period,
        "monthly_forecasts": monthly_forecasts,
        "forecast_summary": forecast_summary,
        "forecast_date": datetime.now().strftime("%Y-%m-%d"),
    }


@mcp.tool()
def C01T013_tool(indicators: List[str], regions: List[str]) -> dict:
    """
    여러 지역의 경제 지표를 비교합니다.
    (HMA Gateway C01T013_tool 원본 로직 그대로 복사)
    """
    # C01T010과 동일한 경제 지표 데이터 사용
    economic_indicators = {
        "미국": {
            "GDP성장률": 2.5,
            "인플레이션": 3.4,
            "실업률": 3.8,
            "기준금리": 5.25,
            "소비자신뢰지수": 105.2,
            "제조업PMI": 52.8,
            "서비스업PMI": 54.1,
        },
        "유럽": {
            "GDP성장률": 1.8,
            "인플레이션": 2.9,
            "실업률": 6.2,
            "기준금리": 4.0,
            "소비자신뢰지수": 98.5,
            "제조업PMI": 48.2,
            "서비스업PMI": 51.3,
        },
        "일본": {
            "GDP성장률": 1.2,
            "인플레이션": 1.8,
            "실업률": 2.5,
            "기준금리": -0.1,
            "소비자신뢰지수": 88.7,
            "제조업PMI": 49.5,
            "서비스업PMI": 50.8,
        },
        "중국": {
            "GDP성장률": 5.2,
            "인플레이션": 2.1,
            "실업률": 5.1,
            "기준금리": 3.45,
            "소비자신뢰지수": 92.3,
            "제조업PMI": 51.2,
            "서비스업PMI": 52.6,
        },
        "한국": {
            "GDP성장률": 2.8,
            "인플레이션": 2.6,
            "실업률": 2.9,
            "기준금리": 3.5,
            "소비자신뢰지수": 95.8,
            "제조업PMI": 50.9,
            "서비스업PMI": 52.1,
        },
    }

    # 지표별 지역 비교
    indicator_comparison = {}

    for indicator in indicators:
        region_values = {}
        values = []

        for region in regions:
            if (
                region in economic_indicators
                and indicator in economic_indicators[region]
            ):
                value = economic_indicators[region][indicator]
                region_values[region] = value
                values.append(value)
            else:
                region_values[region] = None

        # 통계 계산
        if values:
            avg_value = sum(values) / len(values)
            max_region = max(
                region_values,
                key=lambda x: (
                    region_values[x] if region_values[x] is not None else -float("inf")
                ),
            )
            min_region = min(
                region_values,
                key=lambda x: (
                    region_values[x] if region_values[x] is not None else float("inf")
                ),
            )

            indicator_comparison[indicator] = {
                "region_values": region_values,
                "average": round(avg_value, 2),
                "highest_region": max_region,
                "highest_value": region_values[max_region],
                "lowest_region": min_region,
                "lowest_value": region_values[min_region],
                "spread": round(
                    region_values[max_region] - region_values[min_region], 2
                ),
            }
        else:
            indicator_comparison[indicator] = {"error": "데이터 없음"}

    # 지역별 종합 평가
    region_rankings = []
    for region in regions:
        if region in economic_indicators:
            region_score = 0
            valid_indicators = 0

            for indicator in indicators:
                if indicator in economic_indicators[region]:
                    value = economic_indicators[region][indicator]
                    # 지표별 정규화 점수 (간단한 방식)
                    if indicator in [
                        "GDP성장률",
                        "소비자신뢰지수",
                        "제조업PMI",
                        "서비스업PMI",
                    ]:
                        # 높을수록 좋은 지표
                        normalized_score = min(100, max(0, value * 20))
                    else:
                        # 낮을수록 좋은 지표 (실업률, 인플레이션)
                        normalized_score = min(100, max(0, 100 - value * 15))

                    region_score += normalized_score
                    valid_indicators += 1

            if valid_indicators > 0:
                average_score = region_score / valid_indicators
                region_rankings.append(
                    {
                        "region": region,
                        "composite_score": round(average_score, 1),
                        "ranking": 0,  # 나중에 설정
                    }
                )

    # 랭킹 설정
    region_rankings.sort(key=lambda x: x["composite_score"], reverse=True)
    for i, region_data in enumerate(region_rankings):
        region_data["ranking"] = i + 1

    return {
        "compared_indicators": indicators,
        "compared_regions": regions,
        "indicator_comparison": indicator_comparison,
        "region_rankings": region_rankings,
        "best_performing_region": (
            region_rankings[0]["region"] if region_rankings else None
        ),
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    }


@mcp.tool()
def C01T016_tool(symbol: str, scenario: str) -> dict:
    """
    매크로 시나리오 분석을 수행합니다.
    (HMA Gateway C01T016_tool 원본 로직 그대로 복사)
    """
    # 매크로 시나리오별 영향도
    macro_scenarios = {
        "금리인상": {
            "description": "기준금리 1%p 인상 시나리오",
            "macro_changes": {"기준금리": 1.0, "환율": 0.5, "인플레이션": -0.2},
            "sector_impacts": {
                "금융": 0.15,
                "부동산": -0.25,
                "건설": -0.20,
                "소비재": -0.10,
                "기술": -0.05,
                "에너지": 0.0,
                "헬스케어": -0.03,
            },
        },
        "환율급등": {
            "description": "원/달러 환율 10% 상승 시나리오",
            "macro_changes": {"환율": 10.0, "인플레이션": 0.5, "수출": 5.0},
            "sector_impacts": {
                "수출": 0.20,
                "반도체": 0.25,
                "조선": 0.18,
                "화학": 0.15,
                "소비재": -0.08,
                "서비스": -0.05,
                "건설": -0.03,
            },
        },
        "경기침체": {
            "description": "글로벌 경기침체 시나리오",
            "macro_changes": {"GDP성장률": -1.5, "실업률": 2.0, "소비": -3.0},
            "sector_impacts": {
                "소비재": -0.30,
                "서비스": -0.25,
                "건설": -0.35,
                "금융": -0.20,
                "기술": -0.15,
                "헬스케어": -0.05,
                "유틸리티": 0.05,
            },
        },
        "인플레이션": {
            "description": "인플레이션 급등 시나리오",
            "macro_changes": {"인플레이션": 2.0, "기준금리": 1.5, "소비": -1.0},
            "sector_impacts": {
                "에너지": 0.25,
                "원자재": 0.30,
                "금융": 0.10,
                "부동산": 0.15,
                "소비재": -0.15,
                "기술": -0.08,
                "서비스": -0.12,
            },
        },
    }

    if scenario not in macro_scenarios:
        return {"error": f"지원하지 않는 시나리오입니다: {scenario}"}

    scenario_data = macro_scenarios[scenario]

    # 종목별 섹터 매핑
    symbol_sectors = {
        "A035720": "기술",  # LG전자
        "A005930": "반도체",  # 삼성전자
        "A000660": "반도체",  # SK하이닉스
        "A010950": "반도체",  # SK하이닉스
        "A030200": "서비스",  # KT
        "A051910": "화학",  # LG화학
        "A035420": "기술",  # NAVER
        "A055550": "금융",  # 신한지주
        "A068270": "헬스케어",  # 셀트리온
    }

    symbol_sector = symbol_sectors.get(symbol, "기타")
    sector_impact = scenario_data["sector_impacts"].get(symbol_sector, 0.0)

    # 종목별 현재가 (시나리오 분석용)
    current_prices = {
        "A035720": 92000,  # LG전자
        "A005930": 68000,  # 삼성전자
        "A000660": 135000,  # SK하이닉스
        "A010950": 105000,  # SK하이닉스
    }

    current_price = current_prices.get(symbol, 50000)

    # 시나리오 영향 계산
    scenario_price = current_price * (1 + sector_impact)
    price_change = (scenario_price - current_price) / current_price * 100

    # 리스크 평가
    if abs(sector_impact) > 0.2:
        risk_level = "높음"
    elif abs(sector_impact) > 0.1:
        risk_level = "보통"
    else:
        risk_level = "낮음"

    return {
        "symbol": symbol,
        "scenario": scenario,
        "scenario_description": scenario_data["description"],
        "symbol_sector": symbol_sector,
        "macro_changes": scenario_data["macro_changes"],
        "sector_impact": sector_impact,
        "price_analysis": {
            "current_price": current_price,
            "scenario_price": int(scenario_price),
            "price_change_percentage": round(price_change, 2),
            "absolute_change": int(scenario_price - current_price),
        },
        "risk_assessment": {
            "risk_level": risk_level,
            "impact_direction": (
                "긍정적"
                if sector_impact > 0
                else "부정적" if sector_impact < 0 else "중립적"
            ),
        },
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    }


@mcp.tool()
def C01T017_tool(indicator: str, region: str, start_date: str, end_date: str) -> dict:
    """
    지정한 날짜 범위 내 매크로 지표 값을 조회합니다.
    (HMA Gateway C01T017_tool 원본 로직 그대로 복사)
    """
    # 달러 환율 변동 데이터 (HMA Gateway 원본 데이터)
    usd_exchange_rate_data = [
        {"date": "2024-01-31", "value": 1.2},
        {"date": "2024-02-29", "value": 1.4},
        {"date": "2024-03-31", "value": 1.8},
        {"date": "2024-04-30", "value": 2.0},
        {"date": "2024-05-31", "value": 2.1},
        {"date": "2024-06-30", "value": 2.3},
        {"date": "2024-07-31", "value": 2.5},
        {"date": "2024-08-31", "value": 2.7},
        {"date": "2024-09-30", "value": 2.9},
        {"date": "2024-10-31", "value": 3.1},
        {"date": "2024-11-30", "value": 3.3},
        {"date": "2024-12-31", "value": 3.5},
        {"date": "2025-01-31", "value": 3.7},
        {"date": "2025-02-28", "value": 3.9},
        {"date": "2025-03-31", "value": 4.1},
        {"date": "2025-04-30", "value": 4.3},
        {"date": "2025-05-31", "value": 4.5},
        {"date": "2025-06-30", "value": 4.7},
        {"date": "2025-07-31", "value": 4.9},
        {"date": "2025-08-05", "value": 5.1},
    ]

    # 유로 환율 변동 데이터
    eur_exchange_rate_data = [
        {"date": "2024-01-31", "value": 1.1},
        {"date": "2024-02-29", "value": 1.3},
        {"date": "2024-03-31", "value": 1.6},
        {"date": "2024-04-30", "value": 1.8},
        {"date": "2024-05-31", "value": 2.0},
        {"date": "2024-06-30", "value": 2.2},
        {"date": "2024-07-31", "value": 2.4},
        {"date": "2024-08-31", "value": 2.6},
        {"date": "2024-09-30", "value": 2.8},
        {"date": "2024-10-31", "value": 3.0},
        {"date": "2024-11-30", "value": 3.2},
        {"date": "2024-12-31", "value": 3.4},
        {"date": "2025-01-31", "value": 3.6},
        {"date": "2025-02-28", "value": 3.8},
        {"date": "2025-03-31", "value": 4.0},
        {"date": "2025-04-30", "value": 4.2},
        {"date": "2025-05-31", "value": 4.4},
        {"date": "2025-06-30", "value": 4.6},
        {"date": "2025-07-31", "value": 4.8},
        {"date": "2025-08-05", "value": 5.0},
    ]

    # 일본 엔 환율 변동 데이터
    jpy_exchange_rate_data = [
        {"date": "2024-01-31", "value": 0.8},
        {"date": "2024-02-29", "value": 1.0},
        {"date": "2024-03-31", "value": 1.2},
        {"date": "2024-04-30", "value": 1.4},
        {"date": "2024-05-31", "value": 1.6},
        {"date": "2024-06-30", "value": 1.8},
        {"date": "2024-07-31", "value": 2.0},
        {"date": "2024-08-31", "value": 2.2},
        {"date": "2024-09-30", "value": 2.4},
        {"date": "2024-10-31", "value": 2.6},
        {"date": "2024-11-30", "value": 2.8},
        {"date": "2024-12-31", "value": 3.0},
        {"date": "2025-01-31", "value": 3.2},
        {"date": "2025-02-28", "value": 3.4},
        {"date": "2025-03-31", "value": 3.6},
        {"date": "2025-04-30", "value": 3.8},
        {"date": "2025-05-31", "value": 4.0},
        {"date": "2025-06-30", "value": 4.2},
        {"date": "2025-07-31", "value": 4.4},
        {"date": "2025-08-05", "value": 4.6},
    ]

    # 지표와 지역에 따른 데이터 선택
    if indicator == "환율":
        if region == "미국":
            data = usd_exchange_rate_data
        elif region == "유럽":
            data = eur_exchange_rate_data
        elif region == "일본":
            data = jpy_exchange_rate_data
        else:
            data = usd_exchange_rate_data  # 기본값
    else:
        # 다른 지표의 경우 기본 데이터 반환
        data = [{"date": "2025-08-05", "value": 1.0}]

    # 날짜 범위에 따른 필터링
    filtered_data = []
    for item in data:
        if start_date <= item["date"] <= end_date:
            filtered_data.append(item)

    return {
        "data": filtered_data,
        "indicator": indicator,
        "region": region,
        "period": f"{start_date} ~ {end_date}",
        "total_count": len(filtered_data),
    }


@mcp.tool()
def C01T021_tool(region: str, stress_level: str = "중간") -> dict:
    """
    매크로 스트레스 테스트를 수행합니다.
    (HMA Gateway C01T021_tool 원본 로직 그대로 복사)
    """
    # 스트레스 시나리오 정의
    stress_scenarios = {
        "약함": {
            "금리충격": 0.5,
            "환율충격": 5.0,
            "GDP충격": -0.5,
            "인플레이션충격": 0.5,
            "실업률충격": 0.5,
        },
        "중간": {
            "금리충격": 1.0,
            "환율충격": 10.0,
            "GDP충격": -1.0,
            "인플레이션충격": 1.0,
            "실업률충격": 1.0,
        },
        "강함": {
            "금리충격": 2.0,
            "환율충격": 20.0,
            "GDP충격": -2.0,
            "인플레이션충격": 2.0,
            "실업률충격": 2.0,
        },
    }

    if stress_level not in stress_scenarios:
        return {"error": f"지원하지 않는 스트레스 레벨입니다: {stress_level}"}

    stress_shocks = stress_scenarios[stress_level]

    # 지역별 현재 경제 지표 (C01T010과 동일)
    current_indicators = {
        "미국": {"GDP성장률": 2.5, "인플레이션": 3.4, "실업률": 3.8, "기준금리": 5.25},
        "유럽": {"GDP성장률": 1.8, "인플레이션": 2.9, "실업률": 6.2, "기준금리": 4.0},
        "일본": {"GDP성장률": 1.2, "인플레이션": 1.8, "실업률": 2.5, "기준금리": -0.1},
        "한국": {"GDP성장률": 2.8, "인플레이션": 2.6, "실업률": 2.9, "기준금리": 3.5},
    }

    if region not in current_indicators:
        return {"error": f"지원하지 않는 지역입니다: {region}"}

    current_data = current_indicators[region]

    # 스트레스 테스트 결과 계산
    stressed_indicators = {}

    for indicator, current_value in current_data.items():
        if indicator == "GDP성장률":
            stressed_value = current_value + stress_shocks["GDP충격"]
        elif indicator == "인플레이션":
            stressed_value = current_value + stress_shocks["인플레이션충격"]
        elif indicator == "실업률":
            stressed_value = current_value + stress_shocks["실업률충격"]
        elif indicator == "기준금리":
            stressed_value = current_value + stress_shocks["금리충격"]
        else:
            stressed_value = current_value

        change = stressed_value - current_value
        change_percentage = (change / current_value * 100) if current_value != 0 else 0

        stressed_indicators[indicator] = {
            "current_value": current_value,
            "stressed_value": round(stressed_value, 2),
            "absolute_change": round(change, 2),
            "percentage_change": round(change_percentage, 2),
        }

    # 전체 경제 충격 평가
    total_impact_score = (
        abs(stress_shocks["GDP충격"]) * 0.3
        + abs(stress_shocks["인플레이션충격"]) * 0.2
        + abs(stress_shocks["실업률충격"]) * 0.2
        + abs(stress_shocks["금리충격"]) * 0.3
    )

    if total_impact_score > 1.5:
        impact_severity = "심각"
    elif total_impact_score > 1.0:
        impact_severity = "보통"
    else:
        impact_severity = "경미"

    return {
        "region": region,
        "stress_level": stress_level,
        "stress_scenario": stress_shocks,
        "stressed_indicators": stressed_indicators,
        "impact_assessment": {
            "total_impact_score": round(total_impact_score, 3),
            "impact_severity": impact_severity,
            "most_affected_indicator": max(
                stressed_indicators.keys(),
                key=lambda x: abs(stressed_indicators[x]["percentage_change"]),
            ),
        },
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    }


@mcp.tool()
def C01T033_tool(asset_class: str, time_horizon: str = "1Y") -> dict:
    """
    자산군별 전망을 분석합니다.
    (HMA Gateway C01T033_tool 원본 로직 그대로 복사)
    """
    # 자산군별 전망 데이터
    asset_outlooks = {
        "주식": {
            "1M": {"수익률예상": 2.1, "변동성예상": 15.2, "신뢰도": 0.65},
            "3M": {"수익률예상": 5.8, "변동성예상": 18.5, "신뢰도": 0.72},
            "6M": {"수익률예상": 8.5, "변동성예상": 22.1, "신뢰도": 0.68},
            "1Y": {"수익률예상": 12.3, "변동성예상": 25.8, "신뢰도": 0.63},
        },
        "채권": {
            "1M": {"수익률예상": 0.8, "변동성예상": 3.2, "신뢰도": 0.85},
            "3M": {"수익률예상": 2.1, "변동성예상": 4.8, "신뢰도": 0.82},
            "6M": {"수익률예상": 3.5, "변동성예상": 6.2, "신뢰도": 0.78},
            "1Y": {"수익률예상": 4.2, "변동성예상": 8.5, "신뢰도": 0.75},
        },
        "부동산": {
            "1M": {"수익률예상": 0.5, "변동성예상": 2.1, "신뢰도": 0.70},
            "3M": {"수익률예상": 1.2, "변동성예상": 3.5, "신뢰도": 0.68},
            "6M": {"수익률예상": 2.8, "변동성예상": 5.8, "신뢰도": 0.65},
            "1Y": {"수익률예상": 5.5, "변동성예상": 8.2, "신뢰도": 0.62},
        },
        "원자재": {
            "1M": {"수익률예상": 3.2, "변동성예상": 25.5, "신뢰도": 0.45},
            "3M": {"수익률예상": 6.8, "변동성예상": 32.1, "신뢰도": 0.42},
            "6M": {"수익률예상": 8.5, "변동성예상": 38.5, "신뢰도": 0.38},
            "1Y": {"수익률예상": 10.2, "변동성예상": 42.8, "신뢰도": 0.35},
        },
        "현금": {
            "1M": {"수익률예상": 0.3, "변동성예상": 0.1, "신뢰도": 0.95},
            "3M": {"수익률예상": 0.9, "변동성예상": 0.2, "신뢰도": 0.95},
            "6M": {"수익률예상": 1.8, "변동성예상": 0.3, "신뢰도": 0.95},
            "1Y": {"수익률예상": 3.5, "변동성예상": 0.5, "신뢰도": 0.95},
        },
    }

    if asset_class not in asset_outlooks:
        return {"error": f"지원하지 않는 자산군입니다: {asset_class}"}

    asset_data = asset_outlooks[asset_class]

    # 요청된 기간의 전망
    outlook_data = asset_data.get(time_horizon, asset_data["1Y"])

    # 샤프 비율 계산
    if outlook_data["변동성예상"] > 0:
        sharpe_ratio = outlook_data["수익률예상"] / outlook_data["변동성예상"]
    else:
        sharpe_ratio = 0

    # 투자 추천도 계산
    risk_adjusted_return = outlook_data["수익률예상"] * outlook_data["신뢰도"]

    if risk_adjusted_return > 8.0:
        recommendation = "적극 투자"
    elif risk_adjusted_return > 5.0:
        recommendation = "투자 권장"
    elif risk_adjusted_return > 2.0:
        recommendation = "신중 투자"
    else:
        recommendation = "투자 비권장"

    # 모든 기간 비교
    all_horizons = {}
    for horizon, data in asset_data.items():
        all_horizons[horizon] = {
            "예상수익률": data["수익률예상"],
            "예상변동성": data["변동성예상"],
            "샤프비율": (
                round(data["수익률예상"] / data["변동성예상"], 3)
                if data["변동성예상"] > 0
                else 0
            ),
        }

    return {
        "asset_class": asset_class,
        "time_horizon": time_horizon,
        "outlook": outlook_data,
        "performance_metrics": {
            "sharpe_ratio": round(sharpe_ratio, 3),
            "risk_adjusted_return": round(risk_adjusted_return, 2),
            "risk_level": (
                "높음"
                if outlook_data["변동성예상"] > 20
                else "보통" if outlook_data["변동성예상"] > 10 else "낮음"
            ),
        },
        "investment_recommendation": recommendation,
        "all_time_horizons": all_horizons,
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    }


@mcp.tool()
def C01T034_tool(indicators: List[str], forecast_months: int = 6) -> dict:
    """
    매크로 지표를 예측합니다.
    (HMA Gateway C01T034_tool 원본 로직 그대로 복사)
    """
    # 지표별 현재값과 예측 트렌드
    indicator_forecasts = {
        "GDP성장률": {"current": 2.8, "trend": -0.05, "volatility": 0.3},
        "인플레이션": {"current": 2.6, "trend": -0.03, "volatility": 0.2},
        "실업률": {"current": 2.9, "trend": 0.02, "volatility": 0.15},
        "기준금리": {"current": 3.5, "trend": -0.08, "volatility": 0.25},
        "환율": {"current": 1340.5, "trend": 2.5, "volatility": 25.0},
        "소비자신뢰지수": {"current": 95.8, "trend": -0.5, "volatility": 3.2},
    }

    forecast_results = {}

    for indicator in indicators:
        if indicator not in indicator_forecasts:
            forecast_results[indicator] = {"error": "지원하지 않는 지표"}
            continue

        data = indicator_forecasts[indicator]

        # 월별 예측 생성
        monthly_forecasts = []
        current_value = data["current"]

        for month in range(1, forecast_months + 1):
            # 트렌드 + 약간의 변동성
            forecast_value = (
                current_value
                + (data["trend"] * month)
                + (data["volatility"] * 0.1 * (month % 3 - 1))
            )

            forecast_date = (datetime.now() + timedelta(days=month * 30)).strftime(
                "%Y-%m"
            )
            monthly_forecasts.append(
                {"month": forecast_date, "forecast_value": round(forecast_value, 2)}
            )

        # 신뢰구간 계산
        final_forecast = monthly_forecasts[-1]["forecast_value"]
        confidence_interval = data["volatility"] * (forecast_months**0.5)

        forecast_results[indicator] = {
            "current_value": data["current"],
            "monthly_forecasts": monthly_forecasts,
            "final_forecast": final_forecast,
            "trend": (
                "상승" if data["trend"] > 0 else "하락" if data["trend"] < 0 else "횡보"
            ),
            "confidence_interval": {
                "upper": round(final_forecast + confidence_interval, 2),
                "lower": round(final_forecast - confidence_interval, 2),
            },
            "forecast_reliability": (
                "높음"
                if data["volatility"] < 0.2
                else "보통" if data["volatility"] < 0.5 else "낮음"
            ),
        }

    return {
        "indicators": indicators,
        "forecast_period_months": forecast_months,
        "forecast_results": forecast_results,
        "forecast_date": datetime.now().strftime("%Y-%m-%d"),
    }


if __name__ == "__main__":
    mcp.run()
