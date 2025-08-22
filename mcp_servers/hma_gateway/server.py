#!/usr/bin/env uv run
"""
HMA Gateway MCP Server - 실제 도구 연동 (간단 버전)

이 서버는 HMA Gateway의 실제 도구 로직을 복사해서 사용.
복잡한 의존성 문제를 피하기 위해 핵심 로직만 독립적으로 구현.
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MCP 서버 초기화
mcp = FastMCP("HMA Gateway Real Tools")

# ==================== 실제 HMA Gateway 도구 로직 복사 ====================


def real_C01T001_tool(symbol: str, session_info: dict = None):
    """
    종목 코드에 해당하는 뉴스 감성 데이터를 반환.
    (HMA Gateway C01T001_tool 로직 복사)
    """
    # 현재 날짜를 YYYY-MM-DD 형식으로 가져오기
    current_date = datetime.now().strftime("%Y-%m-%d")

    # 종목별 뉴스 감성 데이터 (실제 HMA Gateway 데이터)
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


def real_C01T025_tool(symbol, period="3M", end_date=None, session_info=None):
    """
    개별 주식의 리스크 지표를 조회.
    (HMA Gateway C01T025_tool 로직 복사)
    """
    # 종목별 리스크 데이터
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
    result = risk_data.get(symbol, default_risk)
    result.update(
        {
            "symbol": symbol,
            "period": period,
            "analysis_date": datetime.now().strftime("%Y-%m-%d"),
        }
    )
    return result


def real_C11T001_tool(고객번호, 만기도래계좌조회여부=None, session_info=None):
    """
    예금 및 신탁 계좌 조회
    (HMA Gateway C11T001_tool 로직 복사)
    """
    cust_no = str(고객번호).zfill(6)  # 6자리로 패딩

    # 고객번호로 user 매핑
    user_mapping = {"000001": "user1", "000002": "user2", "000003": "user3"}

    if cust_no not in user_mapping:
        return {"error": "존재하지 않는 고객번호입니다."}

    user_key = user_mapping[cust_no]

    response_map = {
        "user1": {
            "누적금액": 12000000.0,
            "예금종류": 1,
            "현수신계좌상태": 10,
            "계좌번호": "1111222233334444",
            "예금신규일자": "20240301",
            "예적금만기일자": "20260301",
            "계좌잔액": 12000000.0,
            "지불가능잔액": 11500000.0,
            "거래통지기준금액": 100000.0,
            "상품부기명": "신한S라인통장",
            "상품한글명": "신한 S-라인 통장",
            "입출금잔액": 12000000.0,
            "납입원금수익률": 1.1,
            "총계좌수": 1,
            "계좌별명": "생활비통장",
            "개설지점명": "강남지점",
        },
        "user2": {
            "누적금액": 45000000.0,
            "예금종류": 2,
            "현수신계좌상태": 10,
            "계좌번호": "2222333344445555",
            "예금신규일자": "20200815",
            "예적금만기일자": "20260815",
            "계좌잔액": 45000000.0,
            "지불가능잔액": 42000000.0,
            "거래통지기준금액": 500000.0,
            "상품부기명": "신한플러스통장",
            "상품한글명": "신한 플러스 통장",
            "입출금잔액": 45000000.0,
            "납입원금수익률": 1.2,
            "총계좌수": 3,
            "계좌별명": "가계관리통장",
            "개설지점명": "역삼지점",
            "VIP등급": "골드",
            "우대이율": 0.1,
        },
        "user3": {
            "누적금액": 120000000.0,
            "예금종류": 3,
            "현수신계좌상태": 10,
            "계좌번호": "3333444455556666",
            "예금신규일자": "20180101",
            "예적금만기일자": "20270101",
            "계좌잔액": 120000000.0,
            "지불가능잔액": 115000000.0,
            "거래통지기준금액": 2000000.0,
            "상품부기명": "신한프라이빗통장",
            "상품한글명": "신한 프라이빗 뱅킹 통장",
            "입출금잔액": 120000000.0,
            "납입원금수익률": 1.3,
            "총계좌수": 5,
            "계좌별명": "투자전용통장",
            "개설지점명": "강남PB센터",
            "VIP등급": "프라이빗",
            "우대이율": 0.3,
            "전담PB": "김상담",
            "자산관리한도": 500000000,
        },
    }

    return response_map.get(user_key, {"error": "고객 정보를 찾을 수 없습니다."})


def real_C05T004_tool(고객번호, session_info=None):
    """
    고객번호를 통해 전체 계좌 정보를 조회 (간단 버전)
    """
    customer_id = str(고객번호).zfill(6)

    # 간단한 계좌 데이터
    account_data = {
        "000001": {
            "고객번호": "000001",
            "고객명": "김고객",
            "총잔액": 12000000,
            "출금가능금액": 11500000,
            "계좌정보목록": [
                {
                    "계좌ID": "ACC000001001",
                    "계좌종류": "보통예금",
                    "계좌번호": "1111-2222-3333-4444",
                    "계좌명": "생활비통장",
                    "만기일자": "2026-03-01",
                    "계좌잔액": 12000000,
                    "계좌상태": "정상",
                    "출금가능": 11500000,
                }
            ],
        },
        "000002": {
            "고객번호": "000002",
            "고객명": "이고객",
            "총잔액": 45000000,
            "출금가능금액": 42000000,
            "계좌정보목록": [
                {
                    "계좌ID": "ACC000002001",
                    "계좌종류": "정기예금",
                    "계좌번호": "2222-3333-4444-5555",
                    "계좌명": "가계관리통장",
                    "만기일자": "2026-08-15",
                    "계좌잔액": 45000000,
                    "계좌상태": "정상",
                    "출금가능": 42000000,
                }
            ],
        },
        "000003": {
            "고객번호": "000003",
            "고객명": "박고객",
            "총잔액": 120000000,
            "출금가능금액": 115000000,
            "계좌정보목록": [
                {
                    "계좌ID": "ACC000003001",
                    "계좌종류": "프라이빗뱅킹",
                    "계좌번호": "3333-4444-5555-6666",
                    "계좌명": "투자전용통장",
                    "만기일자": "2027-01-01",
                    "계좌잔액": 120000000,
                    "계좌상태": "정상",
                    "출금가능": 115000000,
                }
            ],
        },
    }

    if customer_id in account_data:
        return account_data[customer_id]
    else:
        return {"error": "존재하지 않는 고객번호입니다."}


# ==================== MCP 도구 래퍼들 ====================


@mcp.tool()
def stock_news_sentiment_analysis(symbol: str) -> Dict[str, Any]:
    """
    종목 코드에 해당하는 뉴스 감성 데이터를 반환.

    Args:
        symbol: 종목 코드 (예: A035720, A005930)

    Returns:
        dict: 종목의 뉴스 감성 분석 결과
    """
    try:
        result = real_C01T001_tool(symbol=symbol, session_info=None)
        logger.info(f"C01T001_tool 성공: {symbol} -> {result}")
        return result
    except Exception as e:
        logger.error(f"C01T001_tool 실패: {e}")
        return {"error": str(e), "symbol": symbol}


@mcp.tool()
def stock_risk_indicators(
    symbol: str, period: str = "3M", end_date: Optional[str] = None
) -> Dict[str, Any]:
    """
    개별 주식의 리스크 지표를 조회.

    Args:
        symbol: 주식 종목 코드
        period: 분석 기간 (1D, 1W, 1M, 3M, 6M, 1Y)
        end_date: 종료일자 (YYYY-MM-DD 형식)

    Returns:
        dict: 리스크 지표 정보
    """
    try:
        result = real_C01T025_tool(
            symbol=symbol, period=period, end_date=end_date, session_info=None
        )
        logger.info(f"C01T025_tool 성공: {symbol} -> {result}")
        return result
    except Exception as e:
        logger.error(f"C01T025_tool 실패: {e}")
        return {"error": str(e), "symbol": symbol, "period": period}


@mcp.tool()
def get_customer_accounts(customer_number: str) -> Dict[str, Any]:
    """
    고객번호를 통해 전체 계좌 정보를 조회.

    Args:
        customer_number: 조회할 고객의 번호 (6자리)

    Returns:
        dict: 고객의 계좌 정보
    """
    try:
        result = real_C05T004_tool(고객번호=customer_number, session_info=None)
        logger.info(f"C05T004_tool 성공: {customer_number} -> {result}")
        return result
    except Exception as e:
        logger.error(f"C05T004_tool 실패: {e}")
        return {"error": str(e), "customer_number": customer_number}


@mcp.tool()
def get_deposit_trust_accounts(
    customer_number: int, maturity_filter: Optional[str] = None
) -> Dict[str, Any]:
    """
    예금 및 신탁 계좌를 조회.

    Args:
        customer_number: 고객번호
        maturity_filter: 만기도래계좌조회여부

    Returns:
        dict: 예금 및 신탁 계좌 정보
    """
    try:
        result = real_C11T001_tool(
            고객번호=customer_number,
            만기도래계좌조회여부=maturity_filter,
            session_info=None,
        )
        logger.info(f"C11T001_tool 성공: {customer_number} -> {result}")
        return result
    except Exception as e:
        logger.error(f"C11T001_tool 실패: {e}")
        return {"error": str(e), "customer_number": customer_number}


# ==================== 서버 실행 ====================

if __name__ == "__main__":
    logger.info("HMA Gateway MCP Server (Real Tools) 시작 중...")
    logger.info("실제 HMA Gateway 도구 로직을 사용")

    # 서버 실행
    mcp.run()
