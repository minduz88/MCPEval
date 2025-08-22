#!/usr/bin/env uv run
"""
News Sentiment MCP Server - 뉴스/감성 분석 에이전트 도구들
HMA Gateway의 news_sentiment_agent 도구들을 그대로 복사하여 구현

총 24개 도구:
C01T001, C01T004, C01T005, C01T007, C01T018, C01T019, C01T023, C01T030,
C01T035, C01T036, C01T037, C01T039, C01T043, C01T044, C01T049, C01T050,
C01T051, C01T059, C01T060, C01T061, C01T063, C01T065, C01T066, C01T068
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
mcp = FastMCP("News Sentiment MCP Server")

# ==================== HMA Gateway 원본 도구 로직 복사 ====================


@mcp.tool()
def C01T001_tool(symbol: str) -> dict:
    """
    종목 코드에 해당하는 뉴스 감성 데이터를 반환합니다.
    (HMA Gateway C01T001_tool 원본 로직 그대로 복사)
    """
    # 현재 날짜를 YYYY-MM-DD 형식으로 가져오기
    current_date = datetime.now().strftime("%Y-%m-%d")

    # 종목별 뉴스 감성 데이터 (HMA Gateway 원본 데이터)
    sentiment_data = {
        "A035720": {  # LG전자
            "date": current_date,
            "symbol": "A035720",
            "score": 0.38,
            "sentiment": "긍정적",
            "keywords": ["AI 가전", "스마트홈", "신제품 출시", "기술 혁신"],
        },
        "A005930": {  # 삼성전자
            "date": current_date,
            "symbol": "A005930",
            "score": -0.12,
            "sentiment": "부정적",
            "keywords": ["반도체 수요 감소", "경기 침체", "수출 부진"],
        },
        "A000660": {  # SK하이닉스
            "date": current_date,
            "symbol": "A000660",
            "score": 0.25,
            "sentiment": "긍정적",
            "keywords": ["HBM", "AI메모리", "고성능반도체"],
        },
        "A010950": {  # SK하이닉스
            "date": current_date,
            "symbol": "A010950",
            "score": 0.42,
            "sentiment": "매우 긍정적",
            "keywords": ["HBM 수요 증가", "AI 메모리", "기술 우위"],
        },
        "A030200": {  # KT
            "date": current_date,
            "symbol": "A030200",
            "score": 0.15,
            "sentiment": "약간 긍정적",
            "keywords": ["5G 서비스", "클라우드 확장", "디지털 전환"],
        },
        "A051910": {  # LG화학
            "date": current_date,
            "symbol": "A051910",
            "score": 0.31,
            "sentiment": "긍정적",
            "keywords": ["배터리 수요 증가", "전기차 시장", "기술 개발"],
        },
        "A035420": {  # NAVER
            "date": current_date,
            "symbol": "A035420",
            "score": 0.28,
            "sentiment": "긍정적",
            "keywords": ["AI 검색", "챗봇 서비스", "플랫폼 확장"],
        },
        "A055550": {  # 신한지주
            "date": current_date,
            "symbol": "A055550",
            "score": 0.22,
            "sentiment": "긍정적",
            "keywords": ["AI 금융서비스", "디지털뱅킹", "핀테크 혁신"],
        },
        "A051900": {  # LG생활건강
            "date": current_date,
            "symbol": "A051900",
            "score": 0.18,
            "sentiment": "약간 긍정적",
            "keywords": ["뷰티 플랫폼", "개인화 서비스", "온라인 판매"],
        },
        "A068270": {  # 셀트리온
            "date": current_date,
            "symbol": "A068270",
            "score": 0.35,
            "sentiment": "긍정적",
            "keywords": ["신약 개발", "AI 바이오", "연구 성과"],
        },
    }

    # 요청된 종목의 감성 데이터 반환
    if symbol in sentiment_data:
        return sentiment_data[symbol]
    else:
        # 기본값 반환
        return {
            "date": current_date,
            "symbol": symbol,
            "score": 0.0,
            "sentiment": "중립",
            "keywords": [],
        }


@mcp.tool()
def C01T004_tool(symbol: str, start_date: str, end_date: str) -> dict:
    """
    특정 종목의 이슈 타임라인을 생성합니다.
    (HMA Gateway C01T004_tool 원본 로직 그대로 복사)
    """
    # 종목별 이슈 타임라인 데이터
    timeline_data = {
        "A035720": [  # LG전자
            {
                "date": "2025-02-10",
                "headline": "AI 가전 신제품 공개",
                "sentiment": 0.45,
            },
            {
                "date": "2025-03-15",
                "headline": "스마트홈 플랫폼 확장",
                "sentiment": 0.62,
            },
            {"date": "2025-05-20", "headline": "분기 실적 호조", "sentiment": 0.78},
        ],
        "A005930": [  # 삼성전자
            {
                "date": "2025-02-10",
                "headline": "반도체 수요 부진 우려",
                "sentiment": -0.35,
            },
            {"date": "2025-03-15", "headline": "메모리 가격 하락", "sentiment": -0.42},
            {
                "date": "2025-05-20",
                "headline": "AI 반도체 투자 발표",
                "sentiment": 0.28,
            },
        ],
        "A000660": [  # SK하이닉스
            {"date": "2025-02-10", "headline": "HBM 수요 증가", "sentiment": 0.55},
            {
                "date": "2025-03-15",
                "headline": "AI 메모리 기술 개발",
                "sentiment": 0.68,
            },
            {
                "date": "2025-05-20",
                "headline": "글로벌 파트너십 확대",
                "sentiment": 0.72,
            },
        ],
    }

    # 기본 타임라인 (종목이 없을 경우)
    default_timeline = [
        {"date": "2025-02-10", "headline": "일반적인 시장 동향", "sentiment": 0.0},
        {"date": "2025-03-15", "headline": "업계 관련 뉴스", "sentiment": 0.1},
        {"date": "2025-05-20", "headline": "분기 실적 발표", "sentiment": 0.2},
    ]

    timeline = timeline_data.get(symbol, default_timeline)

    return {"timeline": timeline}


@mcp.tool()
def C01T005_tool(symbol: str, sentiment_threshold: float = 0.5) -> dict:
    """
    종목의 감성 점수가 임계값을 초과하는지 확인합니다.
    (HMA Gateway C01T005_tool 원본 로직 그대로 복사)
    """
    # C01T001_tool과 동일한 감성 데이터 사용
    current_date = datetime.now().strftime("%Y-%m-%d")

    sentiment_data = {
        "A035720": 0.38,  # LG전자
        "A005930": -0.12,  # 삼성전자
        "A000660": 0.25,  # SK하이닉스
        "A010950": 0.42,  # SK하이닉스
        "A030200": 0.15,  # KT
        "A051910": 0.31,  # LG화학
        "A035420": 0.28,  # NAVER
        "A055550": 0.22,  # 신한지주
        "A051900": 0.18,  # LG생활건강
        "A068270": 0.35,  # 셀트리온
    }

    current_score = sentiment_data.get(symbol, 0.0)
    exceeds_threshold = abs(current_score) > sentiment_threshold

    return {
        "symbol": symbol,
        "current_score": current_score,
        "threshold": sentiment_threshold,
        "exceeds_threshold": exceeds_threshold,
        "date": current_date,
    }


@mcp.tool()
def C01T007_tool(symbols: List[str]) -> dict:
    """
    여러 종목의 감성 점수를 비교합니다.
    (HMA Gateway C01T007_tool 원본 로직 그대로 복사)
    """
    current_date = datetime.now().strftime("%Y-%m-%d")

    # 감성 데이터
    sentiment_data = {
        "A035720": {"score": 0.38, "sentiment": "긍정적"},  # LG전자
        "A005930": {"score": -0.12, "sentiment": "부정적"},  # 삼성전자
        "A000660": {"score": 0.25, "sentiment": "긍정적"},  # SK하이닉스
        "A010950": {"score": 0.42, "sentiment": "매우 긍정적"},  # SK하이닉스
        "A030200": {"score": 0.15, "sentiment": "약간 긍정적"},  # KT
        "A051910": {"score": 0.31, "sentiment": "긍정적"},  # LG화학
        "A035420": {"score": 0.28, "sentiment": "긍정적"},  # NAVER
        "A055550": {"score": 0.22, "sentiment": "긍정적"},  # 신한지주
        "A051900": {"score": 0.18, "sentiment": "약간 긍정적"},  # LG생활건강
        "A068270": {"score": 0.35, "sentiment": "긍정적"},  # 셀트리온
    }

    comparison_results = []
    for symbol in symbols:
        data = sentiment_data.get(symbol, {"score": 0.0, "sentiment": "중립"})
        comparison_results.append(
            {"symbol": symbol, "score": data["score"], "sentiment": data["sentiment"]}
        )

    # 점수 순으로 정렬
    comparison_results.sort(key=lambda x: x["score"], reverse=True)

    return {
        "comparison": comparison_results,
        "date": current_date,
        "total_symbols": len(symbols),
    }


@mcp.tool()
def C01T018_tool(symbol: str, news_count: int = 10) -> dict:
    """
    종목 관련 최신 뉴스를 조회합니다.
    (HMA Gateway C01T018_tool 원본 로직 그대로 복사)
    """
    current_date = datetime.now().strftime("%Y-%m-%d")

    # 종목별 뉴스 데이터
    news_data = {
        "A035720": [  # LG전자
            {
                "title": "LG전자, AI 가전 신제품 출시",
                "date": current_date,
                "sentiment": 0.45,
            },
            {
                "title": "스마트홈 시장 확장 전략 발표",
                "date": current_date,
                "sentiment": 0.38,
            },
            {
                "title": "IoT 기술 혁신으로 경쟁력 강화",
                "date": current_date,
                "sentiment": 0.42,
            },
        ],
        "A005930": [  # 삼성전자
            {
                "title": "반도체 수요 둔화 우려 확산",
                "date": current_date,
                "sentiment": -0.25,
            },
            {
                "title": "메모리 가격 하락세 지속",
                "date": current_date,
                "sentiment": -0.18,
            },
            {
                "title": "AI 반도체 투자 확대 계획",
                "date": current_date,
                "sentiment": 0.32,
            },
        ],
        "A000660": [  # SK하이닉스
            {
                "title": "HBM 수요 급증으로 실적 개선",
                "date": current_date,
                "sentiment": 0.55,
            },
            {"title": "AI 메모리 기술 선도", "date": current_date, "sentiment": 0.48},
            {"title": "글로벌 파트너십 강화", "date": current_date, "sentiment": 0.41},
        ],
    }

    # 기본 뉴스 (종목이 없을 경우)
    default_news = [
        {"title": "일반적인 시장 동향", "date": current_date, "sentiment": 0.0},
        {"title": "업계 관련 소식", "date": current_date, "sentiment": 0.1},
    ]

    news = news_data.get(symbol, default_news)

    return {
        "symbol": symbol,
        "news": news[:news_count],
        "total_count": len(news),
        "date": current_date,
    }


@mcp.tool()
def C01T019_tool(keyword: str, limit: int = 5) -> dict:
    """
    키워드로 뉴스를 검색합니다.
    (HMA Gateway C01T019_tool 원본 로직 그대로 복사)
    """
    current_date = datetime.now().strftime("%Y-%m-%d")

    # 키워드별 뉴스 데이터
    keyword_news = {
        "AI": [
            {"title": "AI 가전 시장 급성장", "symbol": "A035720", "sentiment": 0.45},
            {"title": "AI 반도체 투자 확대", "symbol": "A005930", "sentiment": 0.38},
            {"title": "AI 메모리 기술 혁신", "symbol": "A000660", "sentiment": 0.52},
            {"title": "AI 금융서비스 도입", "symbol": "A055550", "sentiment": 0.35},
            {"title": "AI 검색 플랫폼 강화", "symbol": "A035420", "sentiment": 0.42},
        ],
        "반도체": [
            {"title": "반도체 수요 회복 기대", "symbol": "A005930", "sentiment": 0.28},
            {
                "title": "메모리 반도체 가격 안정",
                "symbol": "A000660",
                "sentiment": 0.22,
            },
            {"title": "시스템반도체 투자 증가", "symbol": "A005930", "sentiment": 0.35},
        ],
        "전기차": [
            {
                "title": "전기차 배터리 수요 증가",
                "symbol": "A051910",
                "sentiment": 0.48,
            },
            {"title": "전기차 시장 확대", "symbol": "A035720", "sentiment": 0.35},
            {"title": "배터리 기술 혁신", "symbol": "A051910", "sentiment": 0.42},
        ],
    }

    # 기본 뉴스
    default_news = [
        {"title": "일반적인 시장 뉴스", "symbol": "MARKET", "sentiment": 0.0},
    ]

    news = keyword_news.get(keyword, default_news)

    return {
        "keyword": keyword,
        "news": news[:limit],
        "total_found": len(news),
        "date": current_date,
    }


@mcp.tool()
def C01T023_tool(symbol: str, days: int = 7) -> dict:
    """
    종목의 감성 변화 추이를 조회합니다.
    (HMA Gateway C01T023_tool 원본 로직 그대로 복사)
    """
    # 날짜 생성
    dates = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        dates.append(date)
    dates.reverse()

    # 종목별 감성 변화 데이터
    sentiment_trends = {
        "A035720": [0.25, 0.28, 0.32, 0.35, 0.38, 0.41, 0.38],  # LG전자
        "A005930": [-0.20, -0.18, -0.15, -0.12, -0.10, -0.08, -0.12],  # 삼성전자
        "A000660": [0.18, 0.20, 0.22, 0.25, 0.28, 0.30, 0.25],  # SK하이닉스
        "A010950": [0.35, 0.38, 0.40, 0.42, 0.45, 0.48, 0.42],  # SK하이닉스
    }

    # 기본 추이 (종목이 없을 경우)
    default_trend = [0.0] * days

    trend = sentiment_trends.get(symbol, default_trend)

    # 날짜와 감성 점수 매핑
    trend_data = []
    for i, date in enumerate(dates):
        if i < len(trend):
            trend_data.append({"date": date, "sentiment_score": trend[i]})

    return {
        "symbol": symbol,
        "period": f"{days}일",
        "trend": trend_data,
        "current_score": trend[-1] if trend else 0.0,
    }


@mcp.tool()
def C01T030_tool(keyword: str, top_n: int = 3) -> list:
    """
    특정 키워드와 연관된 종목 상위 N개를 반환합니다.
    (HMA Gateway C01T030_tool 원본 로직 그대로 복사)
    """
    # 키워드별 종목 데이터 (HMA Gateway 원본 데이터)
    keyword_data = {
        "AI": [
            {
                "symbol": "A055550",
                "name": "신한지주",
                "description": "AI 금융서비스, 디지털뱅킹",
            },
            {"symbol": "A030200", "name": "KT", "description": "AI 통신, 클라우드, 5G"},
            {
                "symbol": "A035720",
                "name": "LG전자",
                "description": "AI 가전, 스마트홈, IoT",
            },
            {
                "symbol": "A051910",
                "name": "LG화학",
                "description": "AI 배터리, 전기차 배터리",
            },
            {
                "symbol": "A035420",
                "name": "NAVER",
                "description": "AI 검색, 챗봇, AI 플랫폼",
            },
            {
                "symbol": "A005930",
                "name": "삼성전자",
                "description": "AI 반도체, 메모리, 시스템반도체",
            },
            {
                "symbol": "A010950",
                "name": "SK하이닉스",
                "description": "AI 메모리, HBM, DRAM",
            },
            {
                "symbol": "A068270",
                "name": "셀트리온",
                "description": "AI 신약개발, 바이오AI",
            },
        ],
        "인공지능": [
            {
                "symbol": "A055550",
                "name": "신한지주",
                "description": "AI 금융서비스, 디지털뱅킹",
            },
            {"symbol": "A030200", "name": "KT", "description": "AI 통신, 클라우드, 5G"},
            {
                "symbol": "A035720",
                "name": "LG전자",
                "description": "AI 가전, 스마트홈, IoT",
            },
            {
                "symbol": "A035420",
                "name": "NAVER",
                "description": "AI 검색, 챗봇, AI 플랫폼",
            },
            {
                "symbol": "A051910",
                "name": "LG화학",
                "description": "AI 배터리, 전기차 배터리",
            },
            {
                "symbol": "A005930",
                "name": "삼성전자",
                "description": "AI 반도체, 메모리, 시스템반도체",
            },
            {
                "symbol": "A010950",
                "name": "SK하이닉스",
                "description": "AI 메모리, HBM, DRAM",
            },
            {
                "symbol": "A068270",
                "name": "셀트리온",
                "description": "AI 신약개발, 바이오AI",
            },
        ],
        "반도체": [
            {
                "symbol": "A005930",
                "name": "삼성전자",
                "description": "메모리, 시스템반도체",
            },
            {
                "symbol": "A010950",
                "name": "SK하이닉스",
                "description": "메모리 반도체, HBM",
            },
            {"symbol": "A035720", "name": "LG전자", "description": "AI 반도체, IoT"},
            {
                "symbol": "A042700",
                "name": "한미반도체",
                "description": "반도체 장비, 테스트",
            },
            {"symbol": "A403870", "name": "HPSP", "description": "반도체 부품, 소재"},
            {
                "symbol": "A095570",
                "name": "AJ네트웍스",
                "description": "반도체 유통, 부품",
            },
        ],
        "전기차": [
            {"symbol": "A051910", "name": "LG화학", "description": "전기차 배터리"},
            {"symbol": "A000660", "name": "삼성전자", "description": "전기차 반도체"},
            {"symbol": "A035720", "name": "LG전자", "description": "전기차 부품"},
            {
                "symbol": "A096770",
                "name": "SK이노베이션",
                "description": "전기차 배터리, 에너지",
            },
            {
                "symbol": "A373220",
                "name": "LG에너지솔루션",
                "description": "전기차 배터리 전문",
            },
            {"symbol": "A005380", "name": "현대차", "description": "전기차 제조, 개발"},
        ],
    }

    # 키워드에 따른 데이터 선택 (기본값: AI)
    assets = keyword_data.get(keyword, keyword_data["AI"])

    # top_n에 맞게 종목 수 제한하여 반환
    return assets[:top_n]


# 나머지 도구들도 계속 구현...
# C01T035, C01T036, C01T037, C01T039, C01T043, C01T044, C01T049, C01T050,
# C01T051, C01T059, C01T060, C01T061, C01T063, C01T065, C01T066, C01T068


@mcp.tool()
def C01T035_tool(symbol: str, period: str = "1M") -> dict:
    """
    종목의 뉴스 볼륨 변화를 조회합니다.
    (HMA Gateway C01T035_tool 원본 로직 그대로 복사)
    """
    current_date = datetime.now().strftime("%Y-%m-%d")

    # 종목별 뉴스 볼륨 데이터
    volume_data = {
        "A035720": {"daily_avg": 15, "weekly_avg": 105, "monthly_avg": 450},  # LG전자
        "A005930": {"daily_avg": 25, "weekly_avg": 175, "monthly_avg": 750},  # 삼성전자
        "A000660": {
            "daily_avg": 18,
            "weekly_avg": 126,
            "monthly_avg": 540,
        },  # SK하이닉스
        "A010950": {
            "daily_avg": 12,
            "weekly_avg": 84,
            "monthly_avg": 360,
        },  # SK하이닉스
    }

    # 기본값
    default_volume = {"daily_avg": 5, "weekly_avg": 35, "monthly_avg": 150}

    volume = volume_data.get(symbol, default_volume)

    return {
        "symbol": symbol,
        "period": period,
        "volume_data": volume,
        "date": current_date,
    }


@mcp.tool()
def C01T036_tool(symbols: List[str], metric: str = "sentiment") -> dict:
    """
    여러 종목의 뉴스 메트릭을 비교합니다.
    (HMA Gateway C01T036_tool 원본 로직 그대로 복사)
    """
    current_date = datetime.now().strftime("%Y-%m-%d")

    # 종목별 메트릭 데이터
    metrics_data = {
        "A035720": {"sentiment": 0.38, "volume": 15, "impact": 0.65},  # LG전자
        "A005930": {"sentiment": -0.12, "volume": 25, "impact": 0.82},  # 삼성전자
        "A000660": {"sentiment": 0.25, "volume": 18, "impact": 0.71},  # SK하이닉스
        "A010950": {"sentiment": 0.42, "volume": 12, "impact": 0.58},  # SK하이닉스
    }

    comparison_results = []
    for symbol in symbols:
        data = metrics_data.get(symbol, {"sentiment": 0.0, "volume": 0, "impact": 0.0})
        comparison_results.append(
            {
                "symbol": symbol,
                "metric_value": data.get(metric, 0.0),
                "all_metrics": data,
            }
        )

    # 메트릭 값으로 정렬
    comparison_results.sort(key=lambda x: x["metric_value"], reverse=True)

    return {"metric": metric, "comparison": comparison_results, "date": current_date}


@mcp.tool()
def C01T037_tool(symbol: str, threshold: float = 0.3) -> dict:
    """
    종목의 뉴스 임팩트가 임계값을 초과하는지 확인합니다.
    (HMA Gateway C01T037_tool 원본 로직 그대로 복사)
    """
    current_date = datetime.now().strftime("%Y-%m-%d")

    # 종목별 뉴스 임팩트 데이터
    impact_data = {
        "A035720": 0.65,  # LG전자
        "A005930": 0.82,  # 삼성전자
        "A000660": 0.71,  # SK하이닉스
        "A010950": 0.58,  # SK하이닉스
        "A030200": 0.45,  # KT
        "A051910": 0.68,  # LG화학
    }

    current_impact = impact_data.get(symbol, 0.0)
    exceeds_threshold = current_impact > threshold

    return {
        "symbol": symbol,
        "current_impact": current_impact,
        "threshold": threshold,
        "exceeds_threshold": exceeds_threshold,
        "date": current_date,
    }


@mcp.tool()
def C01T039_tool(date: str, limit: int = 10) -> dict:
    """
    특정 날짜의 주요 뉴스를 조회합니다.
    (HMA Gateway C01T039_tool 원본 로직 그대로 복사)
    """
    # 날짜별 주요 뉴스 데이터
    daily_news = {
        "2025-01-15": [
            {"title": "AI 반도체 시장 급성장", "symbol": "A005930", "sentiment": 0.45},
            {
                "title": "전기차 배터리 수요 증가",
                "symbol": "A051910",
                "sentiment": 0.52,
            },
            {"title": "5G 서비스 확산", "symbol": "A030200", "sentiment": 0.38},
        ],
        "2025-01-16": [
            {
                "title": "메모리 반도체 가격 상승",
                "symbol": "A000660",
                "sentiment": 0.42,
            },
            {"title": "스마트홈 시장 확대", "symbol": "A035720", "sentiment": 0.35},
            {"title": "디지털뱅킹 혁신", "symbol": "A055550", "sentiment": 0.28},
        ],
    }

    # 기본 뉴스 (날짜가 없을 경우)
    default_news = [
        {"title": "일반적인 시장 동향", "symbol": "MARKET", "sentiment": 0.0},
    ]

    news = daily_news.get(date, default_news)

    return {"date": date, "news": news[:limit], "total_count": len(news)}


@mcp.tool()
def C01T043_tool(symbol: str, category: str = "all") -> dict:
    """
    종목의 뉴스를 카테고리별로 분류합니다.
    (HMA Gateway C01T043_tool 원본 로직 그대로 복사)
    """
    current_date = datetime.now().strftime("%Y-%m-%d")

    # 종목별 카테고리 뉴스 데이터
    categorized_news = {
        "A035720": {  # LG전자
            "technology": [
                {"title": "AI 가전 기술 혁신", "sentiment": 0.45},
                {"title": "스마트홈 플랫폼 개발", "sentiment": 0.38},
            ],
            "financial": [
                {"title": "분기 실적 발표", "sentiment": 0.32},
                {"title": "투자 계획 공개", "sentiment": 0.28},
            ],
            "market": [{"title": "시장 점유율 확대", "sentiment": 0.35}],
        },
        "A005930": {  # 삼성전자
            "technology": [
                {"title": "AI 반도체 개발", "sentiment": 0.42},
                {"title": "메모리 기술 혁신", "sentiment": 0.38},
            ],
            "financial": [
                {"title": "분기 실적 부진", "sentiment": -0.25},
                {"title": "투자 확대 계획", "sentiment": 0.22},
            ],
            "market": [{"title": "글로벌 경쟁 심화", "sentiment": -0.15}],
        },
    }

    # 기본 뉴스
    default_categorized = {
        "technology": [{"title": "일반 기술 뉴스", "sentiment": 0.0}],
        "financial": [{"title": "일반 재무 뉴스", "sentiment": 0.0}],
        "market": [{"title": "일반 시장 뉴스", "sentiment": 0.0}],
    }

    news_data = categorized_news.get(symbol, default_categorized)

    if category == "all":
        result = news_data
    else:
        result = {category: news_data.get(category, [])}

    return {
        "symbol": symbol,
        "category": category,
        "categorized_news": result,
        "date": current_date,
    }


@mcp.tool()
def C01T044_tool(symbols: List[str], start_date: str, end_date: str) -> dict:
    """
    여러 종목의 뉴스 감성을 기간별로 비교합니다.
    (HMA Gateway C01T044_tool 원본 로직 그대로 복사)
    """
    # 종목별 기간별 감성 데이터
    period_sentiment = {
        "A035720": {
            "avg_sentiment": 0.35,
            "positive_ratio": 0.68,
            "negative_ratio": 0.12,
        },
        "A005930": {
            "avg_sentiment": -0.08,
            "positive_ratio": 0.42,
            "negative_ratio": 0.38,
        },
        "A000660": {
            "avg_sentiment": 0.28,
            "positive_ratio": 0.65,
            "negative_ratio": 0.15,
        },
        "A010950": {
            "avg_sentiment": 0.42,
            "positive_ratio": 0.75,
            "negative_ratio": 0.08,
        },
    }

    comparison_results = []
    for symbol in symbols:
        data = period_sentiment.get(
            symbol, {"avg_sentiment": 0.0, "positive_ratio": 0.5, "negative_ratio": 0.5}
        )
        comparison_results.append({"symbol": symbol, "period_data": data})

    return {
        "symbols": symbols,
        "period": f"{start_date} ~ {end_date}",
        "comparison": comparison_results,
    }


@mcp.tool()
def C01T049_tool(symbol: str, source: str = "all") -> dict:
    """
    종목의 뉴스를 소스별로 분류합니다.
    (HMA Gateway C01T049_tool 원본 로직 그대로 복사)
    """
    current_date = datetime.now().strftime("%Y-%m-%d")

    # 종목별 소스별 뉴스 데이터
    source_news = {
        "A035720": {
            "financial": [
                {
                    "title": "LG전자 분기 실적 발표",
                    "sentiment": 0.35,
                    "source": "한국경제",
                },
                {"title": "AI 가전 매출 증가", "sentiment": 0.42, "source": "매일경제"},
            ],
            "tech": [
                {
                    "title": "스마트홈 기술 혁신",
                    "sentiment": 0.48,
                    "source": "전자신문",
                },
                {
                    "title": "IoT 플랫폼 확장",
                    "sentiment": 0.38,
                    "source": "디지털타임스",
                },
            ],
            "general": [
                {"title": "LG전자 신제품 출시", "sentiment": 0.32, "source": "연합뉴스"}
            ],
        }
    }

    # 기본 뉴스
    default_source_news = {
        "financial": [{"title": "일반 재무 뉴스", "sentiment": 0.0, "source": "일반"}],
        "tech": [{"title": "일반 기술 뉴스", "sentiment": 0.0, "source": "일반"}],
        "general": [{"title": "일반 뉴스", "sentiment": 0.0, "source": "일반"}],
    }

    news_data = source_news.get(symbol, default_source_news)

    if source == "all":
        result = news_data
    else:
        result = {source: news_data.get(source, [])}

    return {
        "symbol": symbol,
        "source": source,
        "source_news": result,
        "date": current_date,
    }


@mcp.tool()
def C01T050_tool(symbol: str, alert_threshold: float = 0.5) -> dict:
    """
    종목의 감성 점수 기반 알림을 설정합니다.
    (HMA Gateway C01T050_tool 원본 로직 그대로 복사)
    """
    current_date = datetime.now().strftime("%Y-%m-%d")

    # 현재 감성 점수 (C01T001과 동일한 데이터 사용)
    current_sentiments = {
        "A035720": 0.38,  # LG전자
        "A005930": -0.12,  # 삼성전자
        "A000660": 0.25,  # SK하이닉스
        "A010950": 0.42,  # SK하이닉스
        "A030200": 0.15,  # KT
        "A051910": 0.31,  # LG화학
    }

    current_score = current_sentiments.get(symbol, 0.0)
    should_alert = abs(current_score) >= alert_threshold

    alert_message = ""
    if should_alert:
        if current_score > 0:
            alert_message = (
                f"{symbol} 종목의 감성이 매우 긍정적입니다 (점수: {current_score})"
            )
        else:
            alert_message = (
                f"{symbol} 종목의 감성이 매우 부정적입니다 (점수: {current_score})"
            )

    return {
        "symbol": symbol,
        "current_score": current_score,
        "alert_threshold": alert_threshold,
        "should_alert": should_alert,
        "alert_message": alert_message,
        "date": current_date,
    }


@mcp.tool()
def C01T051_tool(keyword: str, date_range: int = 7) -> dict:
    """
    키워드의 뉴스 트렌드를 분석합니다.
    (HMA Gateway C01T051_tool 원본 로직 그대로 복사)
    """
    # 날짜 생성
    dates = []
    for i in range(date_range):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        dates.append(date)
    dates.reverse()

    # 키워드별 트렌드 데이터
    keyword_trends = {
        "AI": [12, 15, 18, 22, 28, 25, 30],
        "반도체": [8, 10, 12, 15, 18, 16, 20],
        "전기차": [6, 8, 10, 12, 15, 18, 22],
        "5G": [4, 5, 6, 8, 10, 12, 14],
    }

    # 기본 트렌드
    default_trend = [1] * date_range

    trend = keyword_trends.get(keyword, default_trend)

    # 날짜와 뉴스 수 매핑
    trend_data = []
    for i, date in enumerate(dates):
        if i < len(trend):
            trend_data.append({"date": date, "news_count": trend[i]})

    return {
        "keyword": keyword,
        "date_range": date_range,
        "trend": trend_data,
        "total_news": sum(trend),
    }


@mcp.tool()
def C01T059_tool(symbol: str, impact_threshold: float = 0.6) -> dict:
    """
    종목의 뉴스 임팩트 기반 투자 신호를 생성합니다.
    (HMA Gateway C01T059_tool 원본 로직 그대로 복사)
    """
    current_date = datetime.now().strftime("%Y-%m-%d")

    # 종목별 임팩트와 감성 데이터
    investment_data = {
        "A035720": {"impact": 0.65, "sentiment": 0.38, "volume": 15},  # LG전자
        "A005930": {"impact": 0.82, "sentiment": -0.12, "volume": 25},  # 삼성전자
        "A000660": {"impact": 0.71, "sentiment": 0.25, "volume": 18},  # SK하이닉스
        "A010950": {"impact": 0.58, "sentiment": 0.42, "volume": 12},  # SK하이닉스
    }

    data = investment_data.get(symbol, {"impact": 0.0, "sentiment": 0.0, "volume": 0})

    # 투자 신호 생성 로직
    signal = "HOLD"  # 기본값
    if data["impact"] >= impact_threshold:
        if data["sentiment"] > 0.3:
            signal = "BUY"
        elif data["sentiment"] < -0.3:
            signal = "SELL"

    return {
        "symbol": symbol,
        "investment_signal": signal,
        "impact": data["impact"],
        "sentiment": data["sentiment"],
        "volume": data["volume"],
        "impact_threshold": impact_threshold,
        "date": current_date,
    }


@mcp.tool()
def C01T060_tool(symbols: List[str], ranking_metric: str = "sentiment") -> dict:
    """
    여러 종목을 뉴스 메트릭으로 랭킹합니다.
    (HMA Gateway C01T060_tool 원본 로직 그대로 복사)
    """
    current_date = datetime.now().strftime("%Y-%m-%d")

    # 종목별 메트릭 데이터
    ranking_data = {
        "A035720": {"sentiment": 0.38, "impact": 0.65, "volume": 15},  # LG전자
        "A005930": {"sentiment": -0.12, "impact": 0.82, "volume": 25},  # 삼성전자
        "A000660": {"sentiment": 0.25, "impact": 0.71, "volume": 18},  # SK하이닉스
        "A010950": {"sentiment": 0.42, "impact": 0.58, "volume": 12},  # SK하이닉스
        "A030200": {"sentiment": 0.15, "impact": 0.45, "volume": 8},  # KT
        "A051910": {"sentiment": 0.31, "impact": 0.68, "volume": 14},  # LG화학
    }

    # 랭킹 계산
    ranking_results = []
    for symbol in symbols:
        data = ranking_data.get(symbol, {"sentiment": 0.0, "impact": 0.0, "volume": 0})
        ranking_results.append(
            {
                "symbol": symbol,
                "metric_value": data.get(ranking_metric, 0.0),
                "all_metrics": data,
            }
        )

    # 메트릭 값으로 정렬
    ranking_results.sort(key=lambda x: x["metric_value"], reverse=True)

    # 순위 추가
    for i, result in enumerate(ranking_results):
        result["rank"] = i + 1

    return {
        "ranking_metric": ranking_metric,
        "ranking": ranking_results,
        "total_symbols": len(symbols),
        "date": current_date,
    }


@mcp.tool()
def C01T061_tool(symbol: str, news_type: str = "positive") -> dict:
    """
    종목의 특정 타입 뉴스를 필터링합니다.
    (HMA Gateway C01T061_tool 원본 로직 그대로 복사)
    """
    current_date = datetime.now().strftime("%Y-%m-%d")

    # 종목별 뉴스 데이터
    news_by_type = {
        "A035720": {
            "positive": [
                {"title": "LG전자 AI 가전 혁신", "sentiment": 0.45},
                {"title": "스마트홈 시장 선도", "sentiment": 0.38},
                {"title": "기술 특허 증가", "sentiment": 0.42},
            ],
            "negative": [{"title": "경쟁 심화 우려", "sentiment": -0.25}],
            "neutral": [{"title": "일반적인 업계 동향", "sentiment": 0.05}],
        },
        "A005930": {
            "positive": [{"title": "AI 반도체 투자 확대", "sentiment": 0.32}],
            "negative": [
                {"title": "반도체 수요 감소", "sentiment": -0.35},
                {"title": "메모리 가격 하락", "sentiment": -0.28},
            ],
            "neutral": [{"title": "분기 실적 발표", "sentiment": 0.02}],
        },
    }

    # 기본 뉴스
    default_news = {
        "positive": [{"title": "일반적인 긍정 뉴스", "sentiment": 0.1}],
        "negative": [{"title": "일반적인 부정 뉴스", "sentiment": -0.1}],
        "neutral": [{"title": "일반적인 중립 뉴스", "sentiment": 0.0}],
    }

    symbol_news = news_by_type.get(symbol, default_news)
    filtered_news = symbol_news.get(news_type, [])

    return {
        "symbol": symbol,
        "news_type": news_type,
        "filtered_news": filtered_news,
        "count": len(filtered_news),
        "date": current_date,
    }


@mcp.tool()
def C01T063_tool(symbol: str, correlation_threshold: float = 0.7) -> dict:
    """
    종목과 뉴스 감성의 상관관계를 분석합니다.
    (HMA Gateway C01T063_tool 원본 로직 그대로 복사)
    """
    current_date = datetime.now().strftime("%Y-%m-%d")

    # 종목별 상관관계 데이터
    correlation_data = {
        "A035720": {
            "price_sentiment_corr": 0.75,
            "volume_sentiment_corr": 0.68,
        },  # LG전자
        "A005930": {
            "price_sentiment_corr": 0.82,
            "volume_sentiment_corr": 0.71,
        },  # 삼성전자
        "A000660": {
            "price_sentiment_corr": 0.78,
            "volume_sentiment_corr": 0.65,
        },  # SK하이닉스
        "A010950": {
            "price_sentiment_corr": 0.73,
            "volume_sentiment_corr": 0.69,
        },  # SK하이닉스
    }

    # 기본값
    default_corr = {"price_sentiment_corr": 0.5, "volume_sentiment_corr": 0.5}

    corr_data = correlation_data.get(symbol, default_corr)

    # 임계값 초과 여부 확인
    high_price_corr = corr_data["price_sentiment_corr"] >= correlation_threshold
    high_volume_corr = corr_data["volume_sentiment_corr"] >= correlation_threshold

    return {
        "symbol": symbol,
        "correlation_data": corr_data,
        "correlation_threshold": correlation_threshold,
        "high_price_correlation": high_price_corr,
        "high_volume_correlation": high_volume_corr,
        "date": current_date,
    }


@mcp.tool()
def C01T065_tool(symbols: List[str], sentiment_range: tuple = (-1.0, 1.0)) -> dict:
    """
    감성 점수 범위로 종목을 필터링합니다.
    (HMA Gateway C01T065_tool 원본 로직 그대로 복사)
    """
    current_date = datetime.now().strftime("%Y-%m-%d")

    # 종목별 감성 점수
    sentiment_scores = {
        "A035720": 0.38,  # LG전자
        "A005930": -0.12,  # 삼성전자
        "A000660": 0.25,  # SK하이닉스
        "A010950": 0.42,  # SK하이닉스
        "A030200": 0.15,  # KT
        "A051910": 0.31,  # LG화학
        "A035420": 0.28,  # NAVER
        "A055550": 0.22,  # 신한지주
        "A051900": 0.18,  # LG생활건강
        "A068270": 0.35,  # 셀트리온
    }

    min_score, max_score = sentiment_range

    # 범위 내 종목 필터링
    filtered_symbols = []
    for symbol in symbols:
        score = sentiment_scores.get(symbol, 0.0)
        if min_score <= score <= max_score:
            filtered_symbols.append({"symbol": symbol, "sentiment_score": score})

    # 점수 순으로 정렬
    filtered_symbols.sort(key=lambda x: x["sentiment_score"], reverse=True)

    return {
        "sentiment_range": sentiment_range,
        "input_symbols": symbols,
        "filtered_symbols": filtered_symbols,
        "filtered_count": len(filtered_symbols),
        "date": current_date,
    }


@mcp.tool()
def C01T066_tool(symbol: str, prediction_days: int = 7) -> dict:
    """
    종목의 뉴스 감성 기반 예측을 생성합니다.
    (HMA Gateway C01T066_tool 원본 로직 그대로 복사)
    """
    current_date = datetime.now().strftime("%Y-%m-%d")

    # 종목별 현재 감성 및 트렌드
    prediction_base = {
        "A035720": {"current": 0.38, "trend": 0.02},  # LG전자 - 상승 트렌드
        "A005930": {"current": -0.12, "trend": 0.01},  # 삼성전자 - 약간 상승
        "A000660": {"current": 0.25, "trend": 0.015},  # SK하이닉스 - 상승
        "A010950": {"current": 0.42, "trend": -0.005},  # SK하이닉스 - 약간 하락
    }

    # 기본값
    default_base = {"current": 0.0, "trend": 0.0}

    base = prediction_base.get(symbol, default_base)

    # 예측 데이터 생성
    predictions = []
    current_score = base["current"]

    for i in range(1, prediction_days + 1):
        # 트렌드에 약간의 랜덤성 추가
        predicted_score = current_score + (base["trend"] * i)
        # -1 ~ 1 범위로 제한
        predicted_score = max(-1.0, min(1.0, predicted_score))

        pred_date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
        predictions.append(
            {"date": pred_date, "predicted_sentiment": round(predicted_score, 3)}
        )

    return {
        "symbol": symbol,
        "current_sentiment": base["current"],
        "trend": base["trend"],
        "predictions": predictions,
        "prediction_days": prediction_days,
        "generated_date": current_date,
    }


@mcp.tool()
def C01T068_tool(symbol: str, benchmark_symbols: List[str]) -> dict:
    """
    종목의 뉴스 감성을 벤치마크 종목들과 비교합니다.
    (HMA Gateway C01T068_tool 원본 로직 그대로 복사)
    """
    current_date = datetime.now().strftime("%Y-%m-%d")

    # 종목별 감성 점수
    sentiment_scores = {
        "A035720": 0.38,  # LG전자
        "A005930": -0.12,  # 삼성전자
        "A000660": 0.25,  # SK하이닉스
        "A010950": 0.42,  # SK하이닉스
        "A030200": 0.15,  # KT
        "A051910": 0.31,  # LG화학
        "A035420": 0.28,  # NAVER
        "A055550": 0.22,  # 신한지주
    }

    target_score = sentiment_scores.get(symbol, 0.0)

    # 벤치마크 종목들의 감성 점수
    benchmark_data = []
    for bench_symbol in benchmark_symbols:
        bench_score = sentiment_scores.get(bench_symbol, 0.0)
        benchmark_data.append(
            {
                "symbol": bench_symbol,
                "sentiment_score": bench_score,
                "difference": target_score - bench_score,
            }
        )

    # 벤치마크 평균 계산
    benchmark_avg = (
        sum([data["sentiment_score"] for data in benchmark_data]) / len(benchmark_data)
        if benchmark_data
        else 0.0
    )

    # 상대적 성과 계산
    relative_performance = target_score - benchmark_avg

    return {
        "target_symbol": symbol,
        "target_sentiment": target_score,
        "benchmark_symbols": benchmark_symbols,
        "benchmark_data": benchmark_data,
        "benchmark_average": benchmark_avg,
        "relative_performance": relative_performance,
        "outperforming": relative_performance > 0,
        "date": current_date,
    }


if __name__ == "__main__":
    mcp.run()
