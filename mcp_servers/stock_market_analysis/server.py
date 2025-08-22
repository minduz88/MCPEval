#!/usr/bin/env uv run
"""
Stock Market Analysis MCP Server - 주식 시장 분석 에이전트 도구들
HMA Gateway의 stock_market_analysis_agent 도구들을 그대로 복사하여 구현

총 27개 도구:
C01T002, C01T006, C01T008, C01T011, C01T014, C01T015, C01T020, C01T022,
C01T024, C01T025, C01T026, C01T027, C01T028, C01T029, C01T031, C01T032,
C01T040, C01T041, C01T042, C01T045, C01T046, C01T047, C01T048, C01T053,
C01T054, C01T058, C01T067
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
mcp = FastMCP("Stock Market Analysis MCP Server")

# ==================== HMA Gateway 원본 도구 로직 복사 ====================


@mcp.tool()
def C01T002_tool(symbol: str, metric: str, period: str, comparison: str) -> dict:
    """
    동일 주식의 실적 증감율을 계산합니다.
    (HMA Gateway C01T002_tool 원본 로직 그대로 복사)
    """
    # 종목별 실적 데이터 (예시)
    performance_data = {
        "A035720": {  # LG전자
            "revenue": {"current": 70000000, "previous": 65000000},
            "profit": {"current": 5000000, "previous": 4500000},
            "eps": {"current": 85000, "previous": 78000},
        },
        "A005930": {  # 삼성전자
            "revenue": {"current": 280000000, "previous": 275000000},
            "profit": {"current": 25000000, "previous": 22000000},
            "eps": {"current": 380000, "previous": 350000},
        },
        "A000660": {  # SK하이닉스
            "revenue": {"current": 45000000, "previous": 42000000},
            "profit": {"current": 3500000, "previous": 3200000},
            "eps": {"current": 48000, "previous": 44000},
        },
    }

    # 기본값
    default_data = {
        "revenue": {"current": 10000000, "previous": 9500000},
        "profit": {"current": 1000000, "previous": 950000},
        "eps": {"current": 12000, "previous": 11400},
    }

    data = performance_data.get(symbol, default_data)
    metric_data = data.get(metric, data["revenue"])

    current = metric_data["current"]
    previous = metric_data["previous"]

    # 성장률 계산
    if previous != 0:
        growth_rate = (current - previous) / previous
    else:
        growth_rate = 0.0

    return {
        "current": current,
        "previous": previous,
        "growth_rate": round(growth_rate, 4),
    }


@mcp.tool()
def C01T006_tool(symbol: str, start_date: str, end_date: str) -> dict:
    """
    주식의 기간별 수익률을 계산합니다.
    (HMA Gateway C01T006_tool 원본 로직 그대로 복사)
    """
    # 종목별 가격 데이터
    price_data = {
        "A035720": {"start_price": 85000, "end_price": 92000},  # LG전자
        "A005930": {"start_price": 72000, "end_price": 68000},  # 삼성전자
        "A000660": {"start_price": 125000, "end_price": 135000},  # SK하이닉스
        "A010950": {"start_price": 95000, "end_price": 105000},  # SK하이닉스
    }

    # 기본값
    default_price = {"start_price": 50000, "end_price": 52000}

    data = price_data.get(symbol, default_price)
    start_price = data["start_price"]
    end_price = data["end_price"]

    # 수익률 계산
    if start_price != 0:
        return_rate = (end_price - start_price) / start_price
    else:
        return_rate = 0.0

    return {
        "symbol": symbol,
        "start_date": start_date,
        "end_date": end_date,
        "start_price": start_price,
        "end_price": end_price,
        "return_rate": round(return_rate, 4),
        "return_percentage": round(return_rate * 100, 2),
    }


@mcp.tool()
def C01T008_tool(symbol: str, period: str = "1Y") -> dict:
    """
    주식의 변동성을 계산합니다.
    (HMA Gateway C01T008_tool 원본 로직 그대로 복사)
    """
    # 종목별 변동성 데이터
    volatility_data = {
        "A035720": {
            "daily": 0.025,
            "weekly": 0.055,
            "monthly": 0.12,
            "yearly": 0.28,
        },  # LG전자
        "A005930": {
            "daily": 0.022,
            "weekly": 0.048,
            "monthly": 0.10,
            "yearly": 0.24,
        },  # 삼성전자
        "A000660": {
            "daily": 0.035,
            "weekly": 0.075,
            "monthly": 0.16,
            "yearly": 0.38,
        },  # SK하이닉스
        "A010950": {
            "daily": 0.032,
            "weekly": 0.068,
            "monthly": 0.15,
            "yearly": 0.35,
        },  # SK하이닉스
    }

    # 기본값
    default_volatility = {
        "daily": 0.02,
        "weekly": 0.045,
        "monthly": 0.095,
        "yearly": 0.22,
    }

    vol_data = volatility_data.get(symbol, default_volatility)

    # 기간에 따른 변동성 선택
    period_mapping = {"1D": "daily", "1W": "weekly", "1M": "monthly", "1Y": "yearly"}

    vol_key = period_mapping.get(period, "yearly")
    volatility = vol_data[vol_key]

    return {
        "symbol": symbol,
        "period": period,
        "volatility": volatility,
        "volatility_percentage": round(volatility * 100, 2),
        "risk_level": (
            "높음" if volatility > 0.3 else "보통" if volatility > 0.15 else "낮음"
        ),
    }


@mcp.tool()
def C01T011_tool(symbol: str) -> dict:
    """
    주식의 기술적 분석 지표를 계산합니다.
    (HMA Gateway C01T011_tool 원본 로직 그대로 복사)
    """
    # 종목별 기술적 지표 데이터
    technical_data = {
        "A035720": {  # LG전자
            "rsi": 65.5,
            "macd": 0.85,
            "bollinger_upper": 95000,
            "bollinger_lower": 85000,
            "sma_20": 90000,
            "ema_12": 91500,
        },
        "A005930": {  # 삼성전자
            "rsi": 45.2,
            "macd": -0.32,
            "bollinger_upper": 75000,
            "bollinger_lower": 65000,
            "sma_20": 70000,
            "ema_12": 68500,
        },
        "A000660": {  # SK하이닉스
            "rsi": 72.8,
            "macd": 1.25,
            "bollinger_upper": 140000,
            "bollinger_lower": 125000,
            "sma_20": 132500,
            "ema_12": 134000,
        },
    }

    # 기본값
    default_technical = {
        "rsi": 50.0,
        "macd": 0.0,
        "bollinger_upper": 55000,
        "bollinger_lower": 45000,
        "sma_20": 50000,
        "ema_12": 50500,
    }

    data = technical_data.get(symbol, default_technical)

    # 매수/매도 신호 생성
    signals = []
    if data["rsi"] > 70:
        signals.append("과매수")
    elif data["rsi"] < 30:
        signals.append("과매도")

    if data["macd"] > 0:
        signals.append("상승추세")
    elif data["macd"] < 0:
        signals.append("하락추세")

    return {
        "symbol": symbol,
        "technical_indicators": data,
        "signals": signals,
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    }


@mcp.tool()
def C01T014_tool(symbols: List[str], metric: str = "price") -> dict:
    """
    여러 주식의 성과를 비교합니다.
    (HMA Gateway C01T014_tool 원본 로직 그대로 복사)
    """
    # 종목별 성과 데이터
    performance_data = {
        "A035720": {
            "price": 92000,
            "volume": 1500000,
            "market_cap": 55000000000,
            "return_1m": 0.08,
        },
        "A005930": {
            "price": 68000,
            "volume": 8500000,
            "market_cap": 405000000000,
            "return_1m": -0.05,
        },
        "A000660": {
            "price": 135000,
            "volume": 2200000,
            "market_cap": 98000000000,
            "return_1m": 0.12,
        },
        "A010950": {
            "price": 105000,
            "volume": 1800000,
            "market_cap": 76000000000,
            "return_1m": 0.15,
        },
    }

    comparison_results = []
    for symbol in symbols:
        data = performance_data.get(
            symbol,
            {
                "price": 50000,
                "volume": 1000000,
                "market_cap": 30000000000,
                "return_1m": 0.0,
            },
        )
        comparison_results.append(
            {"symbol": symbol, "metric_value": data.get(metric, 0), "all_metrics": data}
        )

    # 메트릭 값으로 정렬
    comparison_results.sort(key=lambda x: x["metric_value"], reverse=True)

    return {
        "metric": metric,
        "comparison": comparison_results,
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    }


@mcp.tool()
def C01T015_tool(symbol: str, benchmark: str = "KOSPI") -> dict:
    """
    주식과 벤치마크의 상관관계를 분석합니다.
    (HMA Gateway C01T015_tool 원본 로직 그대로 복사)
    """
    # 종목별 벤치마크 상관관계 데이터
    correlation_data = {
        "A035720": {"KOSPI": 0.75, "KOSDAQ": 0.68, "SECTOR": 0.82},  # LG전자
        "A005930": {"KOSPI": 0.85, "KOSDAQ": 0.72, "SECTOR": 0.88},  # 삼성전자
        "A000660": {"KOSPI": 0.78, "KOSDAQ": 0.71, "SECTOR": 0.85},  # SK하이닉스
        "A010950": {"KOSPI": 0.73, "KOSDAQ": 0.69, "SECTOR": 0.81},  # SK하이닉스
    }

    # 기본값
    default_corr = {"KOSPI": 0.65, "KOSDAQ": 0.60, "SECTOR": 0.70}

    corr_data = correlation_data.get(symbol, default_corr)
    correlation = corr_data.get(benchmark, 0.65)

    # 상관관계 해석
    if correlation > 0.8:
        interpretation = "매우 높은 상관관계"
    elif correlation > 0.6:
        interpretation = "높은 상관관계"
    elif correlation > 0.4:
        interpretation = "보통 상관관계"
    elif correlation > 0.2:
        interpretation = "낮은 상관관계"
    else:
        interpretation = "매우 낮은 상관관계"

    return {
        "symbol": symbol,
        "benchmark": benchmark,
        "correlation": correlation,
        "interpretation": interpretation,
        "all_correlations": corr_data,
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    }


@mcp.tool()
def C01T020_tool(symbol: str, scenario: str, impact_factor: float = 1.0) -> dict:
    """
    주식의 시나리오 분석을 수행합니다.
    (HMA Gateway C01T020_tool 원본 로직 그대로 복사)
    """
    current_date = datetime.now().strftime("%Y-%m-%d")

    # 종목별 현재 가격
    current_prices = {
        "A035720": 92000,  # LG전자
        "A005930": 68000,  # 삼성전자
        "A000660": 135000,  # SK하이닉스
        "A010950": 105000,  # SK하이닉스
    }

    current_price = current_prices.get(symbol, 50000)

    # 시나리오별 영향도
    scenario_impacts = {
        "bull_market": {"price_change": 0.20, "probability": 0.3},
        "bear_market": {"price_change": -0.25, "probability": 0.2},
        "recession": {"price_change": -0.35, "probability": 0.15},
        "recovery": {"price_change": 0.30, "probability": 0.25},
        "neutral": {"price_change": 0.0, "probability": 0.1},
    }

    # 시나리오 데이터 (기본값: neutral)
    scenario_data = scenario_impacts.get(scenario, scenario_impacts["neutral"])

    # 영향 팩터 적용
    adjusted_change = scenario_data["price_change"] * impact_factor
    projected_price = current_price * (1 + adjusted_change)

    return {
        "symbol": symbol,
        "scenario": scenario,
        "current_price": current_price,
        "projected_price": int(projected_price),
        "price_change_percentage": round(adjusted_change * 100, 2),
        "scenario_probability": scenario_data["probability"],
        "impact_factor": impact_factor,
        "analysis_date": current_date,
    }


@mcp.tool()
def C01T022_tool(symbol: str, period: str = "1Y") -> dict:
    """
    주식의 샤프 비율을 계산합니다.
    (HMA Gateway C01T022_tool 원본 로직 그대로 복사)
    """
    # 종목별 샤프 비율 데이터
    sharpe_data = {
        "A035720": {"1M": 1.25, "3M": 1.18, "6M": 1.32, "1Y": 1.45},  # LG전자
        "A005930": {"1M": 0.85, "3M": 0.92, "6M": 0.88, "1Y": 0.95},  # 삼성전자
        "A000660": {"1M": 1.65, "3M": 1.58, "6M": 1.72, "1Y": 1.68},  # SK하이닉스
        "A010950": {"1M": 1.48, "3M": 1.52, "6M": 1.55, "1Y": 1.62},  # SK하이닉스
    }

    # 기본값
    default_sharpe = {"1M": 1.0, "3M": 1.0, "6M": 1.0, "1Y": 1.0}

    symbol_data = sharpe_data.get(symbol, default_sharpe)
    sharpe_ratio = symbol_data.get(period, 1.0)

    # 샤프 비율 해석
    if sharpe_ratio > 2.0:
        performance = "매우 우수"
    elif sharpe_ratio > 1.5:
        performance = "우수"
    elif sharpe_ratio > 1.0:
        performance = "양호"
    elif sharpe_ratio > 0.5:
        performance = "보통"
    else:
        performance = "부진"

    return {
        "symbol": symbol,
        "period": period,
        "sharpe_ratio": sharpe_ratio,
        "performance_rating": performance,
        "all_periods": symbol_data,
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    }


@mcp.tool()
def C01T024_tool(symbol: str, lookback_days: int = 30) -> dict:
    """
    주식의 모멘텀을 계산합니다.
    (HMA Gateway C01T024_tool 원본 로직 그대로 복사)
    """
    # 종목별 모멘텀 데이터
    momentum_data = {
        "A035720": {"7d": 0.05, "14d": 0.08, "30d": 0.12, "60d": 0.18},  # LG전자
        "A005930": {"7d": -0.02, "14d": -0.03, "30d": -0.05, "60d": -0.08},  # 삼성전자
        "A000660": {"7d": 0.08, "14d": 0.12, "30d": 0.15, "60d": 0.22},  # SK하이닉스
        "A010950": {"7d": 0.06, "14d": 0.10, "30d": 0.14, "60d": 0.20},  # SK하이닉스
    }

    # 기본값
    default_momentum = {"7d": 0.0, "14d": 0.0, "30d": 0.0, "60d": 0.0}

    symbol_data = momentum_data.get(symbol, default_momentum)

    # 요청된 기간에 가장 가까운 데이터 선택
    if lookback_days <= 7:
        momentum = symbol_data["7d"]
        period_key = "7d"
    elif lookback_days <= 14:
        momentum = symbol_data["14d"]
        period_key = "14d"
    elif lookback_days <= 30:
        momentum = symbol_data["30d"]
        period_key = "30d"
    else:
        momentum = symbol_data["60d"]
        period_key = "60d"

    # 모멘텀 해석
    if momentum > 0.15:
        trend = "강한 상승"
    elif momentum > 0.05:
        trend = "상승"
    elif momentum > -0.05:
        trend = "횡보"
    elif momentum > -0.15:
        trend = "하락"
    else:
        trend = "강한 하락"

    return {
        "symbol": symbol,
        "lookback_days": lookback_days,
        "momentum": momentum,
        "momentum_percentage": round(momentum * 100, 2),
        "trend": trend,
        "all_periods": symbol_data,
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    }


@mcp.tool()
def C01T025_tool(symbol: str, period: str, end_date: str = None) -> dict:
    """
    개별 주식의 리스크 지표를 조회합니다.
    (HMA Gateway C01T025_tool 원본 로직 그대로 복사)
    """
    # 종목별 리스크 데이터 (HMA Gateway 원본 데이터)
    risk_data = {
        "A035720": {"beta": 1.05, "max_drawdown": -15.6, "VaR_95": -2.8},  # LG전자
        "A000660": {"beta": 1.12, "max_drawdown": -18.2, "VaR_95": -3.1},  # 삼성전자
        "A010950": {"beta": 1.35, "max_drawdown": -25.8, "VaR_95": -4.2},  # SK하이닉스
        "A066570": {"beta": 0.85, "max_drawdown": -12.4, "VaR_95": -2.1},  # KT
        "A051910": {"beta": 1.18, "max_drawdown": -20.5, "VaR_95": -3.5},  # LG화학
        "A035420": {"beta": 1.25, "max_drawdown": -22.3, "VaR_95": -3.8},  # NAVER
        "A051900": {"beta": 0.92, "max_drawdown": -14.7, "VaR_95": -2.4},  # LG생활건강
        "A068270": {"beta": 1.45, "max_drawdown": -28.9, "VaR_95": -4.8},  # 셀트리온
    }

    # 기본값 (종목이 없을 경우)
    default_risk = {"beta": 1.0, "max_drawdown": -15.0, "VaR_95": -2.5}

    # 해당 종목의 리스크 데이터 반환
    return risk_data.get(symbol, default_risk)


@mcp.tool()
def C01T026_tool(symbols: List[str], weights: List[float]) -> dict:
    """
    포트폴리오의 리스크를 계산합니다.
    (HMA Gateway C01T026_tool 원본 로직 그대로 복사)
    """
    # 종목별 개별 리스크 데이터 (C01T025와 동일)
    individual_risks = {
        "A035720": {"beta": 1.05, "volatility": 0.28},  # LG전자
        "A005930": {"beta": 1.12, "volatility": 0.24},  # 삼성전자
        "A000660": {"beta": 1.35, "volatility": 0.38},  # SK하이닉스
        "A010950": {"beta": 1.35, "volatility": 0.35},  # SK하이닉스
    }

    if len(symbols) != len(weights):
        return {"error": "종목 수와 가중치 수가 일치하지 않습니다"}

    # 가중치 정규화
    total_weight = sum(weights)
    if total_weight != 1.0:
        weights = [w / total_weight for w in weights]

    # 포트폴리오 베타 계산 (가중평균)
    portfolio_beta = 0.0
    portfolio_volatility = 0.0

    for symbol, weight in zip(symbols, weights):
        risk_data = individual_risks.get(symbol, {"beta": 1.0, "volatility": 0.25})
        portfolio_beta += risk_data["beta"] * weight
        portfolio_volatility += risk_data["volatility"] * weight  # 단순화된 계산

    # 포트폴리오 VaR 추정 (단순화)
    portfolio_var = portfolio_volatility * 2.33  # 95% 신뢰구간

    return {
        "symbols": symbols,
        "weights": weights,
        "portfolio_beta": round(portfolio_beta, 3),
        "portfolio_volatility": round(portfolio_volatility, 3),
        "portfolio_var_95": round(-portfolio_var, 3),
        "diversification_ratio": round(
            1
            - (
                portfolio_volatility
                / sum(
                    [
                        individual_risks.get(s, {"volatility": 0.25})["volatility"] * w
                        for s, w in zip(symbols, weights)
                    ]
                )
            ),
            3,
        ),
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    }


@mcp.tool()
def C01T027_tool(
    symbol: str, target_return: float, confidence_level: float = 0.95
) -> dict:
    """
    주식의 VaR (Value at Risk)를 계산합니다.
    (HMA Gateway C01T027_tool 원본 로직 그대로 복사)
    """
    # 종목별 VaR 관련 데이터
    var_data = {
        "A035720": {"daily_vol": 0.025, "expected_return": 0.0008},  # LG전자
        "A005930": {"daily_vol": 0.022, "expected_return": 0.0005},  # 삼성전자
        "A000660": {"daily_vol": 0.035, "expected_return": 0.0012},  # SK하이닉스
        "A010950": {"daily_vol": 0.032, "expected_return": 0.0010},  # SK하이닉스
    }

    # 기본값
    default_data = {"daily_vol": 0.025, "expected_return": 0.0006}

    data = var_data.get(symbol, default_data)

    # 신뢰구간에 따른 Z-score
    z_scores = {0.90: 1.28, 0.95: 1.65, 0.99: 2.33}

    z_score = z_scores.get(confidence_level, 1.65)

    # VaR 계산
    daily_var = (data["expected_return"] - z_score * data["daily_vol"]) * -1

    # 다양한 기간별 VaR 계산
    weekly_var = daily_var * (5**0.5)  # √5 (주 5일)
    monthly_var = daily_var * (21**0.5)  # √21 (월 21일)

    return {
        "symbol": symbol,
        "target_return": target_return,
        "confidence_level": confidence_level,
        "daily_var": round(daily_var, 4),
        "weekly_var": round(weekly_var, 4),
        "monthly_var": round(monthly_var, 4),
        "daily_volatility": data["daily_vol"],
        "expected_return": data["expected_return"],
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    }


@mcp.tool()
def C01T028_tool(
    symbol: str, option_type: str, strike_price: float, expiry_date: str
) -> dict:
    """
    옵션의 그릭스를 계산합니다.
    (HMA Gateway C01T028_tool 원본 로직 그대로 복사)
    """
    current_date = datetime.now().strftime("%Y-%m-%d")

    # 종목별 현재 가격 (옵션 계산용)
    current_prices = {
        "A035720": 92000,  # LG전자
        "A005930": 68000,  # 삼성전자
        "A000660": 135000,  # SK하이닉스
        "A010950": 105000,  # SK하이닉스
    }

    current_price = current_prices.get(symbol, 50000)

    # 단순화된 그릭스 계산 (실제로는 블랙-숄즈 모델 사용)
    # 현재가와 행사가의 차이에 따른 근사치
    moneyness = current_price / strike_price

    if option_type.upper() == "CALL":
        # 콜옵션 그릭스 (단순화)
        delta = 0.6 if moneyness > 1 else 0.4 if moneyness > 0.95 else 0.2
        gamma = 0.015 if 0.95 <= moneyness <= 1.05 else 0.008
        theta = -0.05 if moneyness > 0.9 else -0.02
        vega = 0.25 if 0.9 <= moneyness <= 1.1 else 0.15
        rho = 0.3 if moneyness > 1 else 0.1
    else:  # PUT
        # 풋옵션 그릭스 (단순화)
        delta = -0.4 if moneyness < 1 else -0.6 if moneyness < 1.05 else -0.8
        gamma = 0.015 if 0.95 <= moneyness <= 1.05 else 0.008
        theta = -0.04 if moneyness < 1.1 else -0.02
        vega = 0.25 if 0.9 <= moneyness <= 1.1 else 0.15
        rho = -0.2 if moneyness < 1 else -0.1

    return {
        "symbol": symbol,
        "option_type": option_type.upper(),
        "current_price": current_price,
        "strike_price": strike_price,
        "expiry_date": expiry_date,
        "moneyness": round(moneyness, 4),
        "greeks": {
            "delta": round(delta, 4),
            "gamma": round(gamma, 4),
            "theta": round(theta, 4),
            "vega": round(vega, 4),
            "rho": round(rho, 4),
        },
        "analysis_date": current_date,
    }


@mcp.tool()
def C01T029_tool(
    symbol: str, dividend_yield: float, growth_rate: float, discount_rate: float
) -> dict:
    """
    주식의 내재가치를 계산합니다 (DDM 모델).
    (HMA Gateway C01T029_tool 원본 로직 그대로 복사)
    """
    current_date = datetime.now().strftime("%Y-%m-%d")

    # 종목별 현재 가격
    current_prices = {
        "A035720": 92000,  # LG전자
        "A005930": 68000,  # 삼성전자
        "A000660": 135000,  # SK하이닉스
        "A010950": 105000,  # SK하이닉스
    }

    current_price = current_prices.get(symbol, 50000)

    # DDM (배당할인모델) 계산
    if discount_rate <= growth_rate:
        return {
            "error": "할인율이 성장률보다 커야 합니다",
            "symbol": symbol,
            "current_price": current_price,
        }

    # 내재가치 계산: D1 / (r - g)
    # D1 = 현재가격 * 배당수익률 * (1 + 성장률)
    next_dividend = current_price * (dividend_yield / 100) * (1 + growth_rate / 100)
    intrinsic_value = next_dividend / ((discount_rate / 100) - (growth_rate / 100))

    # 투자 판단
    price_ratio = current_price / intrinsic_value
    if price_ratio < 0.8:
        recommendation = "강력 매수"
    elif price_ratio < 0.9:
        recommendation = "매수"
    elif price_ratio < 1.1:
        recommendation = "보유"
    elif price_ratio < 1.2:
        recommendation = "매도"
    else:
        recommendation = "강력 매도"

    return {
        "symbol": symbol,
        "current_price": current_price,
        "intrinsic_value": round(intrinsic_value, 0),
        "price_ratio": round(price_ratio, 3),
        "upside_downside": round(
            (intrinsic_value - current_price) / current_price * 100, 2
        ),
        "recommendation": recommendation,
        "inputs": {
            "dividend_yield": dividend_yield,
            "growth_rate": growth_rate,
            "discount_rate": discount_rate,
        },
        "analysis_date": current_date,
    }


@mcp.tool()
def C01T031_tool(symbols: List[str], factors: List[str]) -> dict:
    """
    다중 팩터 모델로 주식을 분석합니다.
    (HMA Gateway C01T031_tool 원본 로직 그대로 복사)
    """
    # 종목별 팩터 데이터
    factor_data = {
        "A035720": {  # LG전자
            "value": 0.25,
            "growth": 0.35,
            "quality": 0.45,
            "momentum": 0.15,
            "size": -0.1,
            "volatility": -0.2,
            "profitability": 0.3,
        },
        "A005930": {  # 삼성전자
            "value": 0.15,
            "growth": 0.25,
            "quality": 0.55,
            "momentum": -0.05,
            "size": 0.4,
            "volatility": -0.15,
            "profitability": 0.4,
        },
        "A000660": {  # SK하이닉스
            "value": 0.35,
            "growth": 0.45,
            "quality": 0.25,
            "momentum": 0.25,
            "size": 0.1,
            "volatility": -0.3,
            "profitability": 0.2,
        },
        "A010950": {  # SK하이닉스
            "value": 0.30,
            "growth": 0.40,
            "quality": 0.30,
            "momentum": 0.20,
            "size": 0.05,
            "volatility": -0.25,
            "profitability": 0.25,
        },
    }

    analysis_results = []

    for symbol in symbols:
        symbol_factors = factor_data.get(symbol, {f: 0.0 for f in factors})

        # 요청된 팩터들의 점수
        factor_scores = {}
        composite_score = 0.0

        for factor in factors:
            score = symbol_factors.get(factor, 0.0)
            factor_scores[factor] = score
            composite_score += score

        # 평균 점수
        avg_score = composite_score / len(factors) if factors else 0.0

        # 등급 산정
        if avg_score > 0.3:
            rating = "A"
        elif avg_score > 0.1:
            rating = "B"
        elif avg_score > -0.1:
            rating = "C"
        elif avg_score > -0.3:
            rating = "D"
        else:
            rating = "F"

        analysis_results.append(
            {
                "symbol": symbol,
                "factor_scores": factor_scores,
                "composite_score": round(avg_score, 3),
                "rating": rating,
            }
        )

    # 복합점수로 정렬
    analysis_results.sort(key=lambda x: x["composite_score"], reverse=True)

    return {
        "factors": factors,
        "analysis_results": analysis_results,
        "top_performer": analysis_results[0]["symbol"] if analysis_results else None,
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    }


@mcp.tool()
def C01T032_tool(symbol: str, peer_symbols: List[str]) -> dict:
    """
    주식의 상대가치를 분석합니다.
    (HMA Gateway C01T032_tool 원본 로직 그대로 복사)
    """
    # 종목별 밸류에이션 데이터
    valuation_data = {
        "A035720": {"pe": 15.5, "pb": 1.2, "ps": 0.8, "ev_ebitda": 8.5},  # LG전자
        "A005930": {"pe": 12.8, "pb": 1.0, "ps": 1.5, "ev_ebitda": 7.2},  # 삼성전자
        "A000660": {"pe": 18.2, "pb": 1.5, "ps": 2.1, "ev_ebitda": 9.8},  # SK하이닉스
        "A010950": {"pe": 16.8, "pb": 1.4, "ps": 1.9, "ev_ebitda": 9.2},  # SK하이닉스
    }

    # 대상 종목 데이터
    target_data = valuation_data.get(
        symbol, {"pe": 15.0, "pb": 1.3, "ps": 1.2, "ev_ebitda": 8.0}
    )

    # 피어 그룹 데이터
    peer_data = []
    peer_averages = {"pe": 0, "pb": 0, "ps": 0, "ev_ebitda": 0}

    for peer in peer_symbols:
        peer_val = valuation_data.get(
            peer, {"pe": 15.0, "pb": 1.3, "ps": 1.2, "ev_ebitda": 8.0}
        )
        peer_data.append({"symbol": peer, "valuation": peer_val})

        # 평균 계산을 위한 누적
        for metric in peer_averages:
            peer_averages[metric] += peer_val[metric]

    # 피어 평균 계산
    if peer_symbols:
        for metric in peer_averages:
            peer_averages[metric] /= len(peer_symbols)

    # 상대가치 분석
    relative_valuation = {}
    for metric in ["pe", "pb", "ps", "ev_ebitda"]:
        if peer_averages[metric] != 0:
            relative_valuation[metric] = target_data[metric] / peer_averages[metric]
        else:
            relative_valuation[metric] = 1.0

    # 종합 판단
    avg_relative = sum(relative_valuation.values()) / len(relative_valuation)
    if avg_relative < 0.8:
        valuation_assessment = "저평가"
    elif avg_relative < 1.2:
        valuation_assessment = "적정평가"
    else:
        valuation_assessment = "고평가"

    return {
        "target_symbol": symbol,
        "target_valuation": target_data,
        "peer_symbols": peer_symbols,
        "peer_data": peer_data,
        "peer_averages": {k: round(v, 2) for k, v in peer_averages.items()},
        "relative_valuation": {k: round(v, 3) for k, v in relative_valuation.items()},
        "average_relative_multiple": round(avg_relative, 3),
        "valuation_assessment": valuation_assessment,
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    }


# 나머지 도구들 계속 구현...
# C01T040, C01T041, C01T042, C01T045, C01T046, C01T047, C01T048, C01T053, C01T054, C01T058, C01T067


@mcp.tool()
def C01T040_tool(symbol: str, forecast_period: int = 12) -> dict:
    """
    주식의 수익률을 예측합니다.
    (HMA Gateway C01T040_tool 원본 로직 그대로 복사)
    """
    current_date = datetime.now().strftime("%Y-%m-%d")

    # 종목별 예측 데이터
    forecast_data = {
        "A035720": {"trend": 0.008, "volatility": 0.025, "base_return": 0.12},  # LG전자
        "A005930": {
            "trend": 0.003,
            "volatility": 0.022,
            "base_return": 0.05,
        },  # 삼성전자
        "A000660": {
            "trend": 0.012,
            "volatility": 0.035,
            "base_return": 0.18,
        },  # SK하이닉스
        "A010950": {
            "trend": 0.010,
            "volatility": 0.032,
            "base_return": 0.15,
        },  # SK하이닉스
    }

    # 기본값
    default_data = {"trend": 0.005, "volatility": 0.025, "base_return": 0.08}

    data = forecast_data.get(symbol, default_data)

    # 월별 예측 수익률 생성
    monthly_forecasts = []
    cumulative_return = 0

    for month in range(1, forecast_period + 1):
        # 트렌드 + 약간의 변동성
        monthly_return = data["trend"] + (data["volatility"] * 0.5 * (month % 3 - 1))
        cumulative_return += monthly_return

        forecast_date = (datetime.now() + timedelta(days=month * 30)).strftime("%Y-%m")
        monthly_forecasts.append(
            {
                "month": forecast_date,
                "monthly_return": round(monthly_return, 4),
                "cumulative_return": round(cumulative_return, 4),
            }
        )

    # 신뢰구간 계산 (단순화)
    confidence_bands = {
        "upper_95": round(
            cumulative_return + 2 * data["volatility"] * (forecast_period**0.5), 4
        ),
        "lower_95": round(
            cumulative_return - 2 * data["volatility"] * (forecast_period**0.5), 4
        ),
        "upper_68": round(
            cumulative_return + data["volatility"] * (forecast_period**0.5), 4
        ),
        "lower_68": round(
            cumulative_return - data["volatility"] * (forecast_period**0.5), 4
        ),
    }

    return {
        "symbol": symbol,
        "forecast_period_months": forecast_period,
        "monthly_forecasts": monthly_forecasts,
        "total_expected_return": round(cumulative_return, 4),
        "confidence_bands": confidence_bands,
        "model_parameters": data,
        "forecast_date": current_date,
    }


@mcp.tool()
def C01T041_tool(
    symbols: List[str], optimization_method: str = "mean_variance"
) -> dict:
    """
    포트폴리오를 최적화합니다.
    (HMA Gateway C01T041_tool 원본 로직 그대로 복사)
    """
    # 종목별 기대수익률과 위험도
    asset_data = {
        "A035720": {
            "expected_return": 0.12,
            "volatility": 0.25,
            "sharpe": 1.2,
        },  # LG전자
        "A005930": {
            "expected_return": 0.08,
            "volatility": 0.20,
            "sharpe": 0.9,
        },  # 삼성전자
        "A000660": {
            "expected_return": 0.15,
            "volatility": 0.35,
            "sharpe": 1.1,
        },  # SK하이닉스
        "A010950": {
            "expected_return": 0.13,
            "volatility": 0.30,
            "sharpe": 1.0,
        },  # SK하이닉스
    }

    # 최적화 방법에 따른 가중치 계산
    if optimization_method == "equal_weight":
        # 동일가중
        weight = 1.0 / len(symbols)
        optimal_weights = [weight] * len(symbols)

    elif optimization_method == "risk_parity":
        # 리스크 패리티 (위험도 역비례)
        total_inv_vol = sum(
            [1 / asset_data.get(s, {"volatility": 0.25})["volatility"] for s in symbols]
        )
        optimal_weights = [
            (1 / asset_data.get(s, {"volatility": 0.25})["volatility"]) / total_inv_vol
            for s in symbols
        ]

    elif optimization_method == "max_sharpe":
        # 최대 샤프비율
        total_sharpe = sum(
            [asset_data.get(s, {"sharpe": 1.0})["sharpe"] for s in symbols]
        )
        optimal_weights = [
            asset_data.get(s, {"sharpe": 1.0})["sharpe"] / total_sharpe for s in symbols
        ]

    else:  # mean_variance (기본값)
        # 평균-분산 최적화 (단순화)
        returns = [
            asset_data.get(s, {"expected_return": 0.10})["expected_return"]
            for s in symbols
        ]
        vols = [asset_data.get(s, {"volatility": 0.25})["volatility"] for s in symbols]

        # 수익률/위험도 비율로 가중치 계산
        ratios = [r / v for r, v in zip(returns, vols)]
        total_ratio = sum(ratios)
        optimal_weights = [ratio / total_ratio for ratio in ratios]

    # 포트폴리오 성과 계산
    portfolio_return = sum(
        [
            asset_data.get(s, {"expected_return": 0.10})["expected_return"] * w
            for s, w in zip(symbols, optimal_weights)
        ]
    )

    portfolio_volatility = sum(
        [
            asset_data.get(s, {"volatility": 0.25})["volatility"] * w
            for s, w in zip(symbols, optimal_weights)
        ]
    )  # 단순화된 계산

    portfolio_sharpe = (
        portfolio_return / portfolio_volatility if portfolio_volatility > 0 else 0
    )

    # 결과 구성
    optimization_results = []
    for symbol, weight in zip(symbols, optimal_weights):
        asset_info = asset_data.get(
            symbol, {"expected_return": 0.10, "volatility": 0.25, "sharpe": 1.0}
        )
        optimization_results.append(
            {
                "symbol": symbol,
                "optimal_weight": round(weight, 4),
                "expected_return": asset_info["expected_return"],
                "volatility": asset_info["volatility"],
            }
        )

    return {
        "optimization_method": optimization_method,
        "symbols": symbols,
        "optimal_portfolio": optimization_results,
        "portfolio_metrics": {
            "expected_return": round(portfolio_return, 4),
            "volatility": round(portfolio_volatility, 4),
            "sharpe_ratio": round(portfolio_sharpe, 4),
        },
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    }


@mcp.tool()
def C01T042_tool(symbol: str, stress_scenarios: List[dict]) -> dict:
    """
    주식의 스트레스 테스트를 수행합니다.
    (HMA Gateway C01T042_tool 원본 로직 그대로 복사)
    """
    current_date = datetime.now().strftime("%Y-%m-%d")

    # 종목별 현재 가격
    current_prices = {
        "A035720": 92000,  # LG전자
        "A005930": 68000,  # 삼성전자
        "A000660": 135000,  # SK하이닉스
        "A010950": 105000,  # SK하이닉스
    }

    current_price = current_prices.get(symbol, 50000)

    # 기본 스트레스 시나리오 (사용자가 제공하지 않은 경우)
    default_scenarios = [
        {"name": "금융위기", "market_shock": -0.30, "sector_shock": -0.35},
        {"name": "경기침체", "market_shock": -0.20, "sector_shock": -0.25},
        {"name": "금리급등", "market_shock": -0.15, "sector_shock": -0.18},
        {"name": "지정학적위험", "market_shock": -0.12, "sector_shock": -0.15},
    ]

    scenarios_to_test = stress_scenarios if stress_scenarios else default_scenarios

    # 종목별 민감도 (베타 등)
    sensitivity_data = {
        "A035720": {"market_beta": 1.05, "sector_beta": 1.2},  # LG전자
        "A005930": {"market_beta": 1.12, "sector_beta": 1.1},  # 삼성전자
        "A000660": {"market_beta": 1.35, "sector_beta": 1.4},  # SK하이닉스
        "A010950": {"market_beta": 1.35, "sector_beta": 1.3},  # SK하이닉스
    }

    sensitivity = sensitivity_data.get(symbol, {"market_beta": 1.0, "sector_beta": 1.0})

    # 스트레스 테스트 실행
    stress_results = []

    for scenario in scenarios_to_test:
        # 시나리오 충격 계산
        market_impact = scenario.get("market_shock", 0) * sensitivity["market_beta"]
        sector_impact = scenario.get("sector_shock", 0) * sensitivity["sector_beta"]

        # 총 충격 (단순 합산)
        total_impact = market_impact + sector_impact

        # 스트레스 가격 계산
        stressed_price = current_price * (1 + total_impact)
        price_change = (stressed_price - current_price) / current_price

        stress_results.append(
            {
                "scenario_name": scenario.get("name", "Unknown"),
                "market_shock": scenario.get("market_shock", 0),
                "sector_shock": scenario.get("sector_shock", 0),
                "total_impact": round(total_impact, 4),
                "stressed_price": int(stressed_price),
                "price_change_percentage": round(price_change * 100, 2),
                "loss_amount": (
                    int(current_price - stressed_price)
                    if stressed_price < current_price
                    else 0
                ),
            }
        )

    # 최악 시나리오 식별
    worst_scenario = min(stress_results, key=lambda x: x["stressed_price"])

    return {
        "symbol": symbol,
        "current_price": current_price,
        "sensitivity": sensitivity,
        "stress_test_results": stress_results,
        "worst_case_scenario": worst_scenario,
        "max_potential_loss": worst_scenario["loss_amount"],
        "analysis_date": current_date,
    }


@mcp.tool()
def C01T045_tool(symbol: str, period: str = "1Y") -> dict:
    """
    주식의 정보비율을 계산합니다.
    (HMA Gateway C01T045_tool 원본 로직 그대로 복사)
    """
    # 종목별 정보비율 데이터
    info_ratio_data = {
        "A035720": {"1M": 0.85, "3M": 0.92, "6M": 0.88, "1Y": 0.95},  # LG전자
        "A005930": {"1M": 0.65, "3M": 0.72, "6M": 0.68, "1Y": 0.75},  # 삼성전자
        "A000660": {"1M": 1.25, "3M": 1.18, "6M": 1.32, "1Y": 1.28},  # SK하이닉스
        "A010950": {"1M": 1.08, "3M": 1.15, "6M": 1.12, "1Y": 1.18},  # SK하이닉스
    }

    # 기본값
    default_ratio = {"1M": 0.8, "3M": 0.8, "6M": 0.8, "1Y": 0.8}

    symbol_data = info_ratio_data.get(symbol, default_ratio)
    info_ratio = symbol_data.get(period, 0.8)

    # 벤치마크 대비 성과 데이터 (정보비율 계산에 사용된 데이터)
    benchmark_data = {
        "A035720": {"excess_return": 0.045, "tracking_error": 0.047},  # LG전자
        "A005930": {"excess_return": 0.032, "tracking_error": 0.043},  # 삼성전자
        "A000660": {"excess_return": 0.058, "tracking_error": 0.045},  # SK하이닉스
        "A010950": {"excess_return": 0.052, "tracking_error": 0.044},  # SK하이닉스
    }

    benchmark_info = benchmark_data.get(
        symbol, {"excess_return": 0.04, "tracking_error": 0.05}
    )

    # 정보비율 해석
    if info_ratio > 1.0:
        performance = "우수한 액티브 성과"
    elif info_ratio > 0.5:
        performance = "양호한 액티브 성과"
    elif info_ratio > 0:
        performance = "보통 액티브 성과"
    elif info_ratio > -0.5:
        performance = "부진한 액티브 성과"
    else:
        performance = "매우 부진한 액티브 성과"

    return {
        "symbol": symbol,
        "period": period,
        "information_ratio": info_ratio,
        "excess_return": benchmark_info["excess_return"],
        "tracking_error": benchmark_info["tracking_error"],
        "performance_assessment": performance,
        "all_periods": symbol_data,
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    }


@mcp.tool()
def C01T046_tool(symbol: str, factor_exposures: dict) -> dict:
    """
    주식의 팩터 익스포저를 분석합니다.
    (HMA Gateway C01T046_tool 원본 로직 그대로 복사)
    """
    # 종목별 팩터 익스포저 데이터
    exposure_data = {
        "A035720": {  # LG전자
            "market": 1.05,
            "size": -0.15,
            "value": 0.25,
            "momentum": 0.18,
            "quality": 0.35,
            "volatility": -0.22,
            "growth": 0.28,
            "dividend": 0.12,
        },
        "A005930": {  # 삼성전자
            "market": 1.12,
            "size": 0.45,
            "value": 0.18,
            "momentum": -0.08,
            "quality": 0.52,
            "volatility": -0.18,
            "growth": 0.22,
            "dividend": 0.25,
        },
        "A000660": {  # SK하이닉스
            "market": 1.35,
            "size": 0.08,
            "value": 0.32,
            "momentum": 0.28,
            "quality": 0.15,
            "volatility": -0.35,
            "growth": 0.42,
            "dividend": 0.05,
        },
        "A010950": {  # SK하이닉스
            "market": 1.35,
            "size": 0.05,
            "value": 0.28,
            "momentum": 0.25,
            "quality": 0.18,
            "volatility": -0.32,
            "growth": 0.38,
            "dividend": 0.08,
        },
    }

    # 기본값
    default_exposure = {
        "market": 1.0,
        "size": 0.0,
        "value": 0.0,
        "momentum": 0.0,
        "quality": 0.0,
        "volatility": 0.0,
        "growth": 0.0,
        "dividend": 0.0,
    }

    actual_exposures = exposure_data.get(symbol, default_exposure)

    # 요청된 팩터들과 실제 익스포저 비교
    exposure_analysis = {}
    risk_decomposition = {}
    total_risk = 0

    for factor, target_exposure in factor_exposures.items():
        actual_exposure = actual_exposures.get(factor, 0.0)
        exposure_diff = actual_exposure - target_exposure

        exposure_analysis[factor] = {
            "target_exposure": target_exposure,
            "actual_exposure": actual_exposure,
            "difference": round(exposure_diff, 4),
            "risk_contribution": round(
                abs(actual_exposure) * 0.1, 4
            ),  # 단순화된 리스크 기여도
        }

        total_risk += abs(actual_exposure) * 0.1

    # 팩터 집중도 계산
    concentration_score = sum([abs(exp) for exp in actual_exposures.values()]) / len(
        actual_exposures
    )

    return {
        "symbol": symbol,
        "factor_analysis": exposure_analysis,
        "actual_exposures": actual_exposures,
        "total_factor_risk": round(total_risk, 4),
        "concentration_score": round(concentration_score, 4),
        "diversification_level": (
            "낮음"
            if concentration_score > 0.5
            else "보통" if concentration_score > 0.3 else "높음"
        ),
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    }


@mcp.tool()
def C01T047_tool(symbols: List[str], start_date: str, end_date: str) -> dict:
    """
    포트폴리오의 성과 기여도를 분석합니다.
    (HMA Gateway C01T047_tool 원본 로직 그대로 복사)
    """
    # 종목별 성과 데이터
    performance_data = {
        "A035720": {"return": 0.08, "weight": 0.25, "benchmark_return": 0.06},  # LG전자
        "A005930": {
            "return": -0.05,
            "weight": 0.30,
            "benchmark_return": 0.02,
        },  # 삼성전자
        "A000660": {
            "return": 0.15,
            "weight": 0.25,
            "benchmark_return": 0.08,
        },  # SK하이닉스
        "A010950": {
            "return": 0.12,
            "weight": 0.20,
            "benchmark_return": 0.07,
        },  # SK하이닉스
    }

    contribution_analysis = []
    total_portfolio_return = 0
    total_benchmark_return = 0

    for symbol in symbols:
        data = performance_data.get(
            symbol,
            {"return": 0.05, "weight": 1.0 / len(symbols), "benchmark_return": 0.04},
        )

        # 성과 기여도 계산
        absolute_contribution = data["return"] * data["weight"]
        relative_contribution = (data["return"] - data["benchmark_return"]) * data[
            "weight"
        ]

        total_portfolio_return += absolute_contribution
        total_benchmark_return += data["benchmark_return"] * data["weight"]

        contribution_analysis.append(
            {
                "symbol": symbol,
                "weight": data["weight"],
                "return": data["return"],
                "benchmark_return": data["benchmark_return"],
                "absolute_contribution": round(absolute_contribution, 4),
                "relative_contribution": round(relative_contribution, 4),
                "excess_return": round(data["return"] - data["benchmark_return"], 4),
            }
        )

    # 기여도 순으로 정렬
    contribution_analysis.sort(key=lambda x: x["absolute_contribution"], reverse=True)

    # 포트폴리오 전체 성과
    portfolio_excess_return = total_portfolio_return - total_benchmark_return

    return {
        "period": f"{start_date} ~ {end_date}",
        "symbols": symbols,
        "contribution_analysis": contribution_analysis,
        "portfolio_summary": {
            "total_return": round(total_portfolio_return, 4),
            "benchmark_return": round(total_benchmark_return, 4),
            "excess_return": round(portfolio_excess_return, 4),
            "top_contributor": contribution_analysis[0]["symbol"],
            "worst_contributor": contribution_analysis[-1]["symbol"],
        },
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    }


@mcp.tool()
def C01T048_tool(symbol: str, confidence_levels: List[float] = [0.95, 0.99]) -> dict:
    """
    주식의 조건부 VaR (CVaR)를 계산합니다.
    (HMA Gateway C01T048_tool 원본 로직 그대로 복사)
    """
    # 종목별 리스크 데이터
    risk_data = {
        "A035720": {"daily_vol": 0.025, "skewness": -0.15, "kurtosis": 3.2},  # LG전자
        "A005930": {"daily_vol": 0.022, "skewness": -0.12, "kurtosis": 3.0},  # 삼성전자
        "A000660": {
            "daily_vol": 0.035,
            "skewness": -0.25,
            "kurtosis": 3.8,
        },  # SK하이닉스
        "A010950": {
            "daily_vol": 0.032,
            "skewness": -0.22,
            "kurtosis": 3.5,
        },  # SK하이닉스
    }

    # 기본값
    default_data = {"daily_vol": 0.025, "skewness": -0.15, "kurtosis": 3.2}

    data = risk_data.get(symbol, default_data)

    # CVaR 계산을 위한 Z-score (정규분포 근사)
    z_scores = {0.90: 1.28, 0.95: 1.65, 0.99: 2.33}

    cvar_results = []

    for confidence_level in confidence_levels:
        z_score = z_scores.get(confidence_level, 1.65)

        # VaR 계산 (정규분포 가정)
        var = z_score * data["daily_vol"]

        # CVaR 계산 (단순화된 공식)
        # CVaR ≈ VaR + (volatility / √(2π)) * exp(-z²/2) / (1-confidence_level)
        import math

        tail_expectation = (
            (data["daily_vol"] / math.sqrt(2 * math.pi))
            * math.exp(-(z_score**2) / 2)
            / (1 - confidence_level)
        )
        cvar = var + tail_expectation

        # 비대칭성 조정 (스큐니스 고려)
        skew_adjustment = data["skewness"] * (z_score**2 - 1) / 6
        adjusted_cvar = cvar + skew_adjustment * data["daily_vol"]

        cvar_results.append(
            {
                "confidence_level": confidence_level,
                "var": round(var, 4),
                "cvar": round(adjusted_cvar, 4),
                "tail_risk": round(adjusted_cvar - var, 4),
            }
        )

    # 다기간 CVaR (주간, 월간)
    multi_period_cvar = {}
    for result in cvar_results:
        confidence = result["confidence_level"]
        daily_cvar = result["cvar"]

        multi_period_cvar[confidence] = {
            "daily": daily_cvar,
            "weekly": round(daily_cvar * math.sqrt(5), 4),
            "monthly": round(daily_cvar * math.sqrt(21), 4),
        }

    return {
        "symbol": symbol,
        "risk_parameters": data,
        "cvar_analysis": cvar_results,
        "multi_period_cvar": multi_period_cvar,
        "worst_case_scenario": max(cvar_results, key=lambda x: x["cvar"]),
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    }


@mcp.tool()
def C01T053_tool(symbol: str, rebalance_frequency: str = "monthly") -> dict:
    """
    주식의 리밸런싱 효과를 분석합니다.
    (HMA Gateway C01T053_tool 원본 로직 그대로 복사)
    """
    # 종목별 리밸런싱 데이터
    rebalancing_data = {
        "A035720": {  # LG전자
            "monthly": {"excess_return": 0.008, "turnover": 0.15, "cost": 0.002},
            "quarterly": {"excess_return": 0.012, "turnover": 0.25, "cost": 0.004},
            "annually": {"excess_return": 0.018, "turnover": 0.45, "cost": 0.008},
        },
        "A005930": {  # 삼성전자
            "monthly": {"excess_return": 0.005, "turnover": 0.12, "cost": 0.0015},
            "quarterly": {"excess_return": 0.008, "turnover": 0.20, "cost": 0.003},
            "annually": {"excess_return": 0.015, "turnover": 0.38, "cost": 0.006},
        },
        "A000660": {  # SK하이닉스
            "monthly": {"excess_return": 0.012, "turnover": 0.22, "cost": 0.003},
            "quarterly": {"excess_return": 0.018, "turnover": 0.35, "cost": 0.005},
            "annually": {"excess_return": 0.025, "turnover": 0.58, "cost": 0.009},
        },
    }

    # 기본값
    default_data = {
        "monthly": {"excess_return": 0.006, "turnover": 0.15, "cost": 0.002},
        "quarterly": {"excess_return": 0.010, "turnover": 0.25, "cost": 0.004},
        "annually": {"excess_return": 0.016, "turnover": 0.40, "cost": 0.007},
    }

    symbol_data = rebalancing_data.get(symbol, default_data)

    # 요청된 빈도의 데이터
    freq_data = symbol_data.get(rebalance_frequency, symbol_data["monthly"])

    # 순 리밸런싱 효과 계산 (초과수익 - 비용)
    net_rebalancing_effect = freq_data["excess_return"] - freq_data["cost"]

    # 모든 빈도 비교
    frequency_comparison = []
    for freq, data in symbol_data.items():
        net_effect = data["excess_return"] - data["cost"]
        efficiency_ratio = net_effect / data["turnover"] if data["turnover"] > 0 else 0

        frequency_comparison.append(
            {
                "frequency": freq,
                "excess_return": data["excess_return"],
                "turnover": data["turnover"],
                "cost": data["cost"],
                "net_effect": round(net_effect, 4),
                "efficiency_ratio": round(efficiency_ratio, 4),
            }
        )

    # 최적 빈도 찾기 (순효과 기준)
    optimal_frequency = max(frequency_comparison, key=lambda x: x["net_effect"])

    return {
        "symbol": symbol,
        "rebalance_frequency": rebalance_frequency,
        "rebalancing_metrics": freq_data,
        "net_rebalancing_effect": round(net_rebalancing_effect, 4),
        "frequency_comparison": frequency_comparison,
        "optimal_frequency": optimal_frequency["frequency"],
        "optimal_net_effect": optimal_frequency["net_effect"],
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    }


@mcp.tool()
def C01T054_tool(symbols: List[str], correlation_threshold: float = 0.7) -> dict:
    """
    주식 간 상관관계를 분석합니다.
    (HMA Gateway C01T054_tool 원본 로직 그대로 복사)
    """
    # 종목 간 상관관계 매트릭스 (대칭 행렬)
    correlation_matrix = {
        ("A035720", "A005930"): 0.65,  # LG전자 - 삼성전자
        ("A035720", "A000660"): 0.58,  # LG전자 - SK하이닉스
        ("A035720", "A010950"): 0.55,  # LG전자 - SK하이닉스
        ("A005930", "A000660"): 0.72,  # 삼성전자 - SK하이닉스
        ("A005930", "A010950"): 0.68,  # 삼성전자 - SK하이닉스
        ("A000660", "A010950"): 0.85,  # SK하이닉스 - SK하이닉스
    }

    def get_correlation(sym1, sym2):
        if sym1 == sym2:
            return 1.0
        key = tuple(sorted([sym1, sym2]))
        return correlation_matrix.get(key, 0.5)  # 기본값 0.5

    # 상관관계 분석 결과
    correlation_analysis = []
    high_correlation_pairs = []

    for i, symbol1 in enumerate(symbols):
        for j, symbol2 in enumerate(symbols):
            if i < j:  # 중복 방지
                correlation = get_correlation(symbol1, symbol2)

                pair_analysis = {
                    "symbol1": symbol1,
                    "symbol2": symbol2,
                    "correlation": correlation,
                    "relationship_strength": (
                        "매우 강함"
                        if abs(correlation) > 0.8
                        else (
                            "강함"
                            if abs(correlation) > 0.6
                            else (
                                "보통"
                                if abs(correlation) > 0.4
                                else "약함" if abs(correlation) > 0.2 else "매우 약함"
                            )
                        )
                    ),
                }

                correlation_analysis.append(pair_analysis)

                # 높은 상관관계 페어 식별
                if abs(correlation) >= correlation_threshold:
                    high_correlation_pairs.append(pair_analysis)

    # 상관관계 매트릭스 생성
    correlation_matrix_result = {}
    for symbol1 in symbols:
        correlation_matrix_result[symbol1] = {}
        for symbol2 in symbols:
            correlation_matrix_result[symbol1][symbol2] = round(
                get_correlation(symbol1, symbol2), 3
            )

    # 다각화 점수 계산 (평균 상관관계의 역수)
    avg_correlation = (
        sum([abs(pair["correlation"]) for pair in correlation_analysis])
        / len(correlation_analysis)
        if correlation_analysis
        else 0
    )
    diversification_score = 1 - avg_correlation

    return {
        "symbols": symbols,
        "correlation_threshold": correlation_threshold,
        "correlation_matrix": correlation_matrix_result,
        "pairwise_analysis": correlation_analysis,
        "high_correlation_pairs": high_correlation_pairs,
        "portfolio_metrics": {
            "average_correlation": round(avg_correlation, 3),
            "diversification_score": round(diversification_score, 3),
            "diversification_level": (
                "높음"
                if diversification_score > 0.7
                else "보통" if diversification_score > 0.4 else "낮음"
            ),
        },
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    }


@mcp.tool()
def C01T058_tool(symbol: str, holding_period: int = 252) -> dict:
    """
    주식의 최대 손실 기간을 분석합니다.
    (HMA Gateway C01T058_tool 원본 로직 그대로 복사)
    """
    # 종목별 최대 손실 기간 데이터
    drawdown_data = {
        "A035720": {  # LG전자
            "max_drawdown": -0.285,
            "max_drawdown_duration": 45,
            "recovery_time": 67,
            "current_drawdown": -0.08,
            "peak_date": "2024-03-15",
            "trough_date": "2024-05-30",
        },
        "A005930": {  # 삼성전자
            "max_drawdown": -0.325,
            "max_drawdown_duration": 52,
            "recovery_time": 78,
            "current_drawdown": -0.12,
            "peak_date": "2024-02-20",
            "trough_date": "2024-06-15",
        },
        "A000660": {  # SK하이닉스
            "max_drawdown": -0.425,
            "max_drawdown_duration": 38,
            "recovery_time": 89,
            "current_drawdown": -0.05,
            "peak_date": "2024-01-10",
            "trough_date": "2024-04-25",
        },
        "A010950": {  # SK하이닉스
            "max_drawdown": -0.385,
            "max_drawdown_duration": 41,
            "recovery_time": 82,
            "current_drawdown": -0.03,
            "peak_date": "2024-01-25",
            "trough_date": "2024-05-10",
        },
    }

    # 기본값
    default_data = {
        "max_drawdown": -0.30,
        "max_drawdown_duration": 45,
        "recovery_time": 70,
        "current_drawdown": -0.05,
        "peak_date": "2024-03-01",
        "trough_date": "2024-05-15",
    }

    data = drawdown_data.get(symbol, default_data)

    # 보유기간 대비 분석
    max_dd_as_pct_of_holding = (data["max_drawdown_duration"] / holding_period) * 100
    recovery_as_pct_of_holding = (data["recovery_time"] / holding_period) * 100

    # 리스크 등급 산정
    if abs(data["max_drawdown"]) > 0.4:
        risk_level = "매우 높음"
    elif abs(data["max_drawdown"]) > 0.3:
        risk_level = "높음"
    elif abs(data["max_drawdown"]) > 0.2:
        risk_level = "보통"
    elif abs(data["max_drawdown"]) > 0.1:
        risk_level = "낮음"
    else:
        risk_level = "매우 낮음"

    # 현재 상태 분석
    if abs(data["current_drawdown"]) < 0.05:
        current_status = "양호"
    elif abs(data["current_drawdown"]) < 0.15:
        current_status = "주의"
    elif abs(data["current_drawdown"]) < 0.25:
        current_status = "경고"
    else:
        current_status = "위험"

    return {
        "symbol": symbol,
        "holding_period_days": holding_period,
        "drawdown_analysis": {
            "max_drawdown": data["max_drawdown"],
            "max_drawdown_percentage": round(data["max_drawdown"] * 100, 2),
            "max_drawdown_duration": data["max_drawdown_duration"],
            "recovery_time": data["recovery_time"],
            "peak_date": data["peak_date"],
            "trough_date": data["trough_date"],
        },
        "holding_period_analysis": {
            "drawdown_duration_pct": round(max_dd_as_pct_of_holding, 2),
            "recovery_time_pct": round(recovery_as_pct_of_holding, 2),
        },
        "current_status": {
            "current_drawdown": data["current_drawdown"],
            "current_drawdown_percentage": round(data["current_drawdown"] * 100, 2),
            "status": current_status,
        },
        "risk_assessment": {
            "risk_level": risk_level,
            "pain_index": round(
                abs(data["max_drawdown"]) * data["max_drawdown_duration"] / 100, 4
            ),
        },
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    }


@mcp.tool()
def C01T067_tool(filters: dict, universe: List[str], as_of_date: str = None) -> dict:
    """
    특정 팩터 조건으로 필터링된 주식 리스트를 반환합니다.
    (HMA Gateway C01T067_tool 원본 로직 그대로 복사)
    """
    current_date = as_of_date or datetime.now().strftime("%Y-%m-%d")

    # 종목별 팩터 데이터
    factor_data = {
        "A035720": {  # LG전자
            "sector": "전자",
            "market_cap": 55000000000,
            "pe_ratio": 15.5,
            "pb_ratio": 1.2,
            "roe": 0.08,
            "debt_ratio": 0.35,
            "dividend_yield": 0.02,
            "beta": 1.05,
            "momentum_1m": 0.08,
            "momentum_3m": 0.12,
            "quality_score": 0.75,
        },
        "A005930": {  # 삼성전자
            "sector": "반도체",
            "market_cap": 405000000000,
            "pe_ratio": 12.8,
            "pb_ratio": 1.0,
            "roe": 0.12,
            "debt_ratio": 0.28,
            "dividend_yield": 0.025,
            "beta": 1.12,
            "momentum_1m": -0.05,
            "momentum_3m": -0.02,
            "quality_score": 0.85,
        },
        "A000660": {  # SK하이닉스
            "sector": "반도체",
            "market_cap": 98000000000,
            "pe_ratio": 18.2,
            "pb_ratio": 1.5,
            "roe": 0.06,
            "debt_ratio": 0.42,
            "dividend_yield": 0.015,
            "beta": 1.35,
            "momentum_1m": 0.15,
            "momentum_3m": 0.22,
            "quality_score": 0.65,
        },
        "A010950": {  # SK하이닉스
            "sector": "반도체",
            "market_cap": 76000000000,
            "pe_ratio": 16.8,
            "pb_ratio": 1.4,
            "roe": 0.07,
            "debt_ratio": 0.38,
            "dividend_yield": 0.018,
            "beta": 1.35,
            "momentum_1m": 0.12,
            "momentum_3m": 0.18,
            "quality_score": 0.70,
        },
        "A030200": {  # KT
            "sector": "통신",
            "market_cap": 32000000000,
            "pe_ratio": 9.5,
            "pb_ratio": 0.8,
            "roe": 0.05,
            "debt_ratio": 0.55,
            "dividend_yield": 0.04,
            "beta": 0.85,
            "momentum_1m": 0.02,
            "momentum_3m": 0.05,
            "quality_score": 0.60,
        },
        "A051910": {  # LG화학
            "sector": "화학",
            "market_cap": 68000000000,
            "pe_ratio": 22.5,
            "pb_ratio": 1.8,
            "roe": 0.09,
            "debt_ratio": 0.48,
            "dividend_yield": 0.012,
            "beta": 1.18,
            "momentum_1m": 0.06,
            "momentum_3m": 0.08,
            "quality_score": 0.72,
        },
    }

    # 필터링 로직
    matched_symbols = []

    for symbol in universe:
        if symbol not in factor_data:
            continue

        symbol_data = factor_data[symbol]
        match = True

        # 각 필터 조건 확인
        for filter_key, filter_value in filters.items():
            if filter_key not in symbol_data:
                continue

            symbol_value = symbol_data[filter_key]

            # 필터 타입에 따른 처리
            if isinstance(filter_value, dict):
                # 범위 조건 (예: {"min": 10, "max": 20})
                if "min" in filter_value and symbol_value < filter_value["min"]:
                    match = False
                    break
                if "max" in filter_value and symbol_value > filter_value["max"]:
                    match = False
                    break
            elif isinstance(filter_value, list):
                # 리스트 조건 (예: ["반도체", "전자"])
                if symbol_value not in filter_value:
                    match = False
                    break
            else:
                # 직접 비교
                if symbol_value != filter_value:
                    match = False
                    break

        if match:
            matched_symbols.append(symbol)

    # 매칭된 종목들의 상세 정보
    matched_details = []
    for symbol in matched_symbols:
        matched_details.append({"symbol": symbol, "factor_data": factor_data[symbol]})

    return {
        "filters": filters,
        "universe": universe,
        "as_of_date": current_date,
        "matched_symbols": matched_symbols,
        "matched_count": len(matched_symbols),
        "matched_details": matched_details,
        "filter_success_rate": (
            round(len(matched_symbols) / len(universe) * 100, 2) if universe else 0
        ),
    }


if __name__ == "__main__":
    mcp.run()
