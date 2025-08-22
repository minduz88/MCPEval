#!/usr/bin/env uv run
"""
Account Management MCP Server - 계좌 관리 에이전트 도구들
HMA Gateway의 account_management_agent 도구들을 그대로 복사하여 구현

총 6개 도구:
C02T001, C05T001, C05T002, C05T003, C05T004, C05T005
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
mcp = FastMCP("Account Management MCP Server")

# ==================== HMA Gateway 원본 도구 로직 복사 ====================


@mcp.tool()
def C02T001_tool(고객번호: int) -> dict:
    """
    고객정보를 상세 조회합니다.
    (HMA Gateway C02T001_tool 원본 로직 그대로 복사)
    """
    cust_no = str(고객번호).zfill(6)

    # 고객정보 데이터 (HMA Gateway 원본)
    customer_info = {
        "000001": {
            "고객번호": "000001",
            "실명번호": "900101-1234567",
            "실명번호구분": "01",
            "고객명": "김민수",
            "고객부기명": "김민수",
            "영문고객명": "Kim Min Su",
            "거래자인격CODE": "001",
            "국적국가명": "대한민국",
            "결혼구분": "N",
            "결혼기념일자": "",
            "생일구분": "1",
            "출생일자": "19900101",
            "성별구분": 1,
            "여권번호": "",
            "주거구분": 1,
            "자녀수": 0,
            "직장명": "삼성전자",
            "근무부서명": "IT개발팀",
            "직업CODE": 2001,
            "직업명": "소프트웨어개발자",
            "직위CODE": 3001,
            "직위명": "대리",
            "직업구분": 1,
            "차량번호": "12가3456",
            "보유차량배기량CODE": 1600,
            "이메일주소": "kimminsu@email.com",
            "주소구분": 10,
            "우편번호": "06292",
            "동이상주소": "서울시 강남구 역삼동 123-45",
            "동미만주소": "래미안아파트 101동 1001호",
            "전화번호": "010-1234-5678",
        },
        "000002": {
            "고객번호": "000002",
            "실명번호": "851215-2345678",
            "실명번호구분": "01",
            "고객명": "박영희",
            "고객부기명": "박영희",
            "영문고객명": "Park Young Hee",
            "거래자인격CODE": "001",
            "국적국가명": "대한민국",
            "결혼구분": "Y",
            "결혼기념일자": "20120520",
            "생일구분": "1",
            "출생일자": "19851215",
            "성별구분": 2,
            "여권번호": "M12345678",
            "주거구분": 2,
            "자녀수": 2,
            "자녀성별구분1": 1,
            "자녀출생년1": "2015",
            "자녀성별구분2": 2,
            "자녀출생년2": "2018",
            "직장명": "LG전자",
            "근무부서명": "마케팅팀",
            "직업CODE": 1005,
            "직업명": "마케팅매니저",
            "직위CODE": 3002,
            "직위명": "과장",
            "직업구분": 1,
            "차량번호": "34나5678",
            "보유차량배기량CODE": 2000,
            "이메일주소": "parkyh@email.com",
            "주소구분": 20,
            "우편번호": "06234",
            "동이상주소": "서울시 강남구 논현동 567-89",
            "동미만주소": "현대아파트 202동 1502호",
            "전화번호": "010-2345-6789",
        },
        "000003": {
            "고객번호": "000003",
            "실명번호": "720830-1234567",
            "실명번호구분": "01",
            "고객명": "이대표",
            "고객부기명": "이대표",
            "영문고객명": "Lee Dae Pyo",
            "거래자인격CODE": "002",
            "국적국가명": "대한민국",
            "결혼구분": "Y",
            "결혼기념일자": "20001010",
            "생일구분": "1",
            "출생일자": "19720830",
            "성별구분": 1,
            "여권번호": "M87654321",
            "주거구분": 3,
            "자녀수": 1,
            "자녀성별구분1": 2,
            "자녀출생년1": "2005",
            "직장명": "이노베이션테크",
            "근무부서명": "대표이사",
            "직업CODE": 5001,
            "직업명": "기업임원",
            "직위CODE": 4001,
            "직위명": "대표이사",
            "직업구분": 2,
            "차량번호": "56다7890",
            "보유차량배기량CODE": 3000,
            "이메일주소": "ceo.lee@innovation.com",
            "주소구분": 30,
            "우편번호": "06011",
            "동이상주소": "서울시 강남구 청담동 100-1",
            "동미만주소": "청담빌라 301호",
            "전화번호": "010-3456-7890",
        },
    }

    if cust_no not in customer_info:
        return {"error": "존재하지 않는 고객번호입니다."}

    return customer_info[cust_no]


@mcp.tool()
def C05T001_tool(고객번호: int, 계좌번호: str, 비밀번호: str) -> dict:
    """
    계좌 비밀번호를 체크합니다.
    (HMA Gateway C05T001_tool 원본 로직 그대로 복사)
    """
    cust_no = str(고객번호).zfill(6)

    # 계좌별 정보 및 비밀번호 (HMA Gateway 원본 시뮬레이션)
    account_info = {
        "1111222233334444": {
            "고객명": "김민수",
            "비밀번호": "1234",
            "표면잔액": 12000000,
            "지불가능잔액": 11500000,
            "거래제한정보내용": "정상",
            "인터넷조회제외서비스여부": 0,
            "보안계좌여부": 0,
        },
        "2222333344445555": {
            "고객명": "박영희",
            "비밀번호": "5678",
            "표면잔액": 45000000,
            "지불가능잔액": 42000000,
            "거래제한정보내용": "정상",
            "인터넷조회제외서비스여부": 0,
            "보안계좌여부": 1,
        },
        "3333444455556666": {
            "고객명": "이대표",
            "비밀번호": "9999",
            "표면잔액": 120000000,
            "지불가능잔액": 115000000,
            "거래제한정보내용": "정상",
            "인터넷조회제외서비스여부": 0,
            "보안계좌여부": 1,
        },
    }

    if 계좌번호 not in account_info:
        return {"error": "존재하지 않는 계좌번호입니다."}

    account = account_info[계좌번호]

    # 비밀번호 확인
    if 비밀번호 != account["비밀번호"]:
        return {"error": "비밀번호가 일치하지 않습니다."}

    # 비밀번호 제외하고 반환
    result = {k: v for k, v in account.items() if k != "비밀번호"}
    return result


@mcp.tool()
def C05T002_tool(
    고객번호: int, 계좌번호: str, 현재비밀번호: str, 신규비밀번호: str
) -> dict:
    """
    계좌 비밀번호를 변경합니다.
    (HMA Gateway C05T002_tool 원본 로직 그대로 복사)
    """
    cust_no = str(고객번호).zfill(6)
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")

    # 계좌별 현재 비밀번호 (C05T001과 동일)
    current_passwords = {
        "1111222233334444": "1234",
        "2222333344445555": "5678",
        "3333444455556666": "9999",
    }

    if 계좌번호 not in current_passwords:
        return {"error": "존재하지 않는 계좌번호입니다."}

    # 현재 비밀번호 확인
    if 현재비밀번호 != current_passwords[계좌번호]:
        return {"error": "현재 비밀번호가 일치하지 않습니다."}

    # 신규 비밀번호 유효성 검사
    if len(신규비밀번호) != 4:
        return {"error": "비밀번호는 4자리 숫자여야 합니다."}

    if not 신규비밀번호.isdigit():
        return {"error": "비밀번호는 숫자만 입력 가능합니다."}

    # 연속번호 체크
    if 신규비밀번호 in ["1234", "2345", "3456", "4567", "5678", "6789"]:
        return {"error": "연속된 숫자는 사용할 수 없습니다."}

    # 동일번호 체크
    if len(set(신규비밀번호)) == 1:
        return {"error": "동일한 숫자 반복은 사용할 수 없습니다."}

    # 비밀번호 변경 처리 (시뮬레이션)
    change_result = {
        "거래번호": f"PWD{current_time}{계좌번호[-4:]}",
        "고객번호": int(cust_no),
        "계좌번호": 계좌번호,
        "변경결과": "성공",
        "변경일시": current_time,
        "이전비밀번호": "****",  # 보안상 마스킹
        "신규비밀번호": "****",  # 보안상 마스킹
        "유효기간": "무제한",
        "다음변경가능일": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
    }

    return change_result


@mcp.tool()
def C05T003_tool(고객번호: int, 계좌번호: str, 한도금액: int) -> dict:
    """
    계좌 이체 한도를 설정합니다.
    (HMA Gateway C05T003_tool 원본 로직 그대로 복사)
    """
    cust_no = str(고객번호).zfill(6)
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")

    # 고객별 최대 설정 가능 한도
    max_limits = {
        "000001": {"일일한도": 5000000, "월한도": 50000000},
        "000002": {"일일한도": 20000000, "월한도": 200000000},
        "000003": {"일일한도": 100000000, "월한도": 1000000000},
    }

    if cust_no not in max_limits:
        return {"error": "존재하지 않는 고객번호입니다."}

    customer_limit = max_limits[cust_no]

    # 한도 유효성 검사
    if 한도금액 > customer_limit["일일한도"]:
        return {
            "error": f"일일 최대 한도를 초과했습니다. (최대: {customer_limit['일일한도']:,}원)"
        }

    # 계좌별 현재 한도 정보
    current_limits = {
        "1111222233334444": {"현재일일한도": 1000000, "현재월한도": 10000000},
        "2222333344445555": {"현재일일한도": 5000000, "현재월한도": 50000000},
        "3333444455556666": {"현재일일한도": 50000000, "현재월한도": 500000000},
    }

    current_limit = current_limits.get(
        계좌번호, {"현재일일한도": 1000000, "현재월한도": 10000000}
    )

    # 한도 설정 결과
    limit_result = {
        "거래번호": f"LMT{current_time}{계좌번호[-4:]}",
        "고객번호": int(cust_no),
        "계좌번호": 계좌번호,
        "설정결과": "성공",
        "이전일일한도": current_limit["현재일일한도"],
        "신규일일한도": 한도금액,
        "월한도": current_limit["현재월한도"],
        "최대설정가능한도": customer_limit["일일한도"],
        "설정일시": current_time,
        "적용일자": datetime.now().strftime("%Y-%m-%d"),
        "유효기간": "무제한",
    }

    return limit_result


@mcp.tool()
def C05T004_tool(고객번호: int, 계좌번호: str, 메모내용: str) -> dict:
    """
    계좌 메모를 설정합니다.
    (HMA Gateway C05T004_tool 원본 로직 그대로 복사)
    """
    cust_no = str(고객번호).zfill(6)
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")

    # 고객번호 유효성 검사
    valid_customers = ["000001", "000002", "000003"]
    if cust_no not in valid_customers:
        return {"error": "존재하지 않는 고객번호입니다."}

    # 계좌별 현재 메모 정보
    current_memos = {
        "1111222233334444": "생활비통장",
        "2222333344445555": "가계관리통장",
        "3333444455556666": "투자전용통장",
    }

    if 계좌번호 not in current_memos:
        return {"error": "존재하지 않는 계좌번호입니다."}

    # 메모 길이 제한 검사
    if len(메모내용) > 20:
        return {"error": "메모는 20자 이내로 입력해주세요."}

    # 금지어 검사 (간단한 예시)
    forbidden_words = ["대출", "차용", "도박", "불법"]
    for word in forbidden_words:
        if word in 메모내용:
            return {"error": f"사용할 수 없는 단어가 포함되어 있습니다: {word}"}

    # 메모 설정 결과
    memo_result = {
        "거래번호": f"MEMO{current_time}{계좌번호[-4:]}",
        "고객번호": int(cust_no),
        "계좌번호": 계좌번호,
        "설정결과": "성공",
        "이전메모": current_memos[계좌번호],
        "신규메모": 메모내용,
        "설정일시": current_time,
        "메모길이": len(메모내용),
        "적용상태": "즉시적용",
    }

    return memo_result


@mcp.tool()
def C05T005_tool(고객번호: int, 계좌번호: str, 알림설정: dict) -> dict:
    """
    계좌 알림을 설정합니다.
    (HMA Gateway C05T005_tool 원본 로직 그대로 복사)
    """
    cust_no = str(고객번호).zfill(6)
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")

    # 고객번호 유효성 검사
    valid_customers = ["000001", "000002", "000003"]
    if cust_no not in valid_customers:
        return {"error": "존재하지 않는 고객번호입니다."}

    # 계좌별 현재 알림 설정
    current_notifications = {
        "1111222233334444": {
            "입금알림": True,
            "출금알림": True,
            "잔액부족알림": True,
            "알림기준금액": 100000,
            "알림방식": ["SMS"],
            "알림시간": "즉시",
        },
        "2222333344445555": {
            "입금알림": True,
            "출금알림": True,
            "잔액부족알림": True,
            "알림기준금액": 500000,
            "알림방식": ["SMS", "이메일"],
            "알림시간": "즉시",
        },
        "3333444455556666": {
            "입금알림": True,
            "출금알림": True,
            "잔액부족알림": True,
            "알림기준금액": 2000000,
            "알림방식": ["SMS", "이메일", "전화"],
            "알림시간": "즉시",
        },
    }

    if 계좌번호 not in current_notifications:
        return {"error": "존재하지 않는 계좌번호입니다."}

    current_setting = current_notifications[계좌번호]

    # 알림설정 업데이트
    updated_setting = current_setting.copy()
    updated_setting.update(알림설정)

    # 알림설정 유효성 검사
    valid_methods = ["SMS", "이메일", "전화", "푸시"]
    if "알림방식" in 알림설정:
        for method in 알림설정["알림방식"]:
            if method not in valid_methods:
                return {"error": f"지원하지 않는 알림방식입니다: {method}"}

    # 알림설정 결과
    notification_result = {
        "거래번호": f"NOTI{current_time}{계좌번호[-4:]}",
        "고객번호": int(cust_no),
        "계좌번호": 계좌번호,
        "설정결과": "성공",
        "이전설정": current_setting,
        "신규설정": updated_setting,
        "변경항목": list(알림설정.keys()),
        "설정일시": current_time,
        "적용상태": "즉시적용",
    }

    return notification_result


if __name__ == "__main__":
    mcp.run()
