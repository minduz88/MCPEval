#!/usr/bin/env uv run
"""
Loan Management MCP Server - 대출 관리 에이전트 도구들
HMA Gateway의 loan_management_agent 도구들을 그대로 복사하여 구현

총 14개 도구:
C13T001, C13T002, C13T003, C13T004, C13T005, C13T006, C13T007, C13T008,
C13T009, C14T001, C14T002, C14T003, C14T004, C14T005
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
mcp = FastMCP("Loan Management MCP Server")

# ==================== HMA Gateway 원본 도구 로직 복사 ====================

@mcp.tool()
def C13T001_tool(고객번호: int) -> dict:
    """
    마이너스 통장 대출 현황을 조회합니다.
    (HMA Gateway C13T001_tool 원본 로직 그대로 복사)
    """
    cust_no = str(고객번호).zfill(6)  # 6자리로 패딩

    # 고객번호로 user 매핑 (HMA Gateway 원본)
    user_mapping = {"000001": "user1", "000002": "user2", "000003": "user3"}

    if cust_no not in user_mapping:
        return {"error": "존재하지 않는 고객번호입니다."}

    user_key = user_mapping[cust_no]

    response_map = {
        "user1": {
            "계좌번호": "",
            "상품부기명": "",
            "원장잔액": 0,
            "고객명": "김민수",
            "지불가능잔액": 0,
            "신규일자": "",
            "계좌상태": 0,
            "대출한도금액": 0,
            "대출기일일자": "",
            "대출이율": 0,
            "지급정지여부": 0,
            "인감분실여부": 0,
            "통장분실여부": 0,
            "거래내역 목록": [],
        },
        "user2": {
            "계좌번호": "2222333344445555",
            "상품부기명": "신한마이너스통장대출",
            "원장잔액": 18000000,
            "고객명": "박영희",
            "지불가능잔액": 7000000,
            "신규일자": "2022-03-15",
            "계좌상태": 1,
            "대출한도금액": 25000000,
            "대출기일일자": "2027-03-15",
            "대출이율": 4.2,
            "지급정지여부": 0,
            "인감분실여부": 0,
            "통장분실여부": 0,
            "상품한글명": "신한 마이너스 통장 대출",
            "신용등급": "2등급",
            "담보유형": "신용",
            "거래내역 목록": [
                {
                    "거래일자": "2025-08-01",
                    "거래시각": "09:15:00",
                    "지급금액": "150000",
                    "입금금액": "0",
                    "거래주석내용": "대출이자 납입",
                    "잔액": 18000000,
                    "대출이자": 150000,
                },
                {
                    "거래일자": "2025-07-10",
                    "거래시각": "14:30:00",
                    "지급금액": "0",
                    "입금금액": "2000000",
                    "거래주석내용": "대출상환",
                    "잔액": 16000000,
                    "대출이자": 0,
                },
            ],
        },
        "user3": {
            "계좌번호": "3333444455556666",
            "상품부기명": "신한프라이빗한도대출",
            "원장잔액": 45000000,
            "고객명": "이대표",
            "지불가능잔액": 5000000,
            "신규일자": "2020-01-01",
            "계좌상태": 1,
            "대출한도금액": 50000000,
            "대출기일일자": "2030-01-01",
            "대출이율": 3.8,
            "지급정지여부": 0,
            "인감분실여부": 0,
            "통장분실여부": 0,
            "상품한글명": "신한 프라이빗 한도 대출",
            "신용등급": "1등급",
            "담보유형": "부동산",
            "담보평가액": 500000000,
            "LTV비율": 60.0,
            "거래내역 목록": [
                {
                    "거래일자": "2025-08-01",
                    "거래시각": "09:15:00",
                    "지급금액": "300000",
                    "입금금액": "0",
                    "거래주석내용": "대출이자 납입",
                    "잔액": 45000000,
                    "대출이자": 300000,
                },
                {
                    "거래일자": "2025-07-15",
                    "거래시각": "11:20:00",
                    "지급금액": "0",
                    "입금금액": "5000000",
                    "거래주석내용": "대출상환",
                    "잔액": 45000000,
                    "대출이자": 0,
                },
            ],
        },
    }

    return response_map[user_key]

@mcp.tool()
def C13T002_tool(고객번호: int, 대출종류: str = "전체") -> dict:
    """
    고객의 전체 대출 현황을 조회합니다.
    (HMA Gateway C13T002_tool 원본 로직 그대로 복사)
    """
    cust_no = str(고객번호).zfill(6)
    
    # 고객별 대출 현황 데이터 (HMA Gateway 원본)
    loan_status = {
        "000001": {
            "고객번호": int(cust_no),
            "고객명": "김민수",
            "총대출건수": 0,
            "총대출잔액": 0,
            "총대출한도": 0,
            "평균금리": 0.0,
            "신용등급": "3등급",
            "대출목록": []
        },
        "000002": {
            "고객번호": int(cust_no),
            "고객명": "박영희",
            "총대출건수": 2,
            "총대출잔액": 35000000,
            "총대출한도": 45000000,
            "평균금리": 4.5,
            "신용등급": "2등급",
            "대출목록": [
                {
                    "계좌번호": "2222333344445555",
                    "상품명": "신한마이너스통장대출",
                    "대출잔액": 18000000,
                    "대출한도": 25000000,
                    "대출금리": 4.2,
                    "대출종류": "한도대출",
                    "담보유형": "신용",
                    "만기일자": "2027-03-15"
                },
                {
                    "계좌번호": "2222333344445556",
                    "상품명": "신한주택담보대출",
                    "대출잔액": 17000000,
                    "대출한도": 20000000,
                    "대출금리": 4.8,
                    "대출종류": "담보대출",
                    "담보유형": "부동산",
                    "만기일자": "2030-05-20"
                }
            ]
        },
        "000003": {
            "고객번호": int(cust_no),
            "고객명": "이대표",
            "총대출건수": 3,
            "총대출잔액": 125000000,
            "총대출한도": 200000000,
            "평균금리": 3.2,
            "신용등급": "1등급",
            "대출목록": [
                {
                    "계좌번호": "3333444455556666",
                    "상품명": "신한프라이빗한도대출",
                    "대출잔액": 45000000,
                    "대출한도": 50000000,
                    "대출금리": 3.8,
                    "대출종류": "한도대출",
                    "담보유형": "부동산",
                    "만기일자": "2030-01-01"
                },
                {
                    "계좌번호": "3333444455556667",
                    "상품명": "신한기업운영자금대출",
                    "대출잔액": 50000000,
                    "대출한도": 80000000,
                    "대출금리": 2.8,
                    "대출종류": "운영자금",
                    "담보유형": "신용",
                    "만기일자": "2028-12-31"
                },
                {
                    "계좌번호": "3333444455556668",
                    "상품명": "신한부동산PF대출",
                    "대출잔액": 30000000,
                    "대출한도": 70000000,
                    "대출금리": 3.0,
                    "대출종류": "PF대출",
                    "담보유형": "부동산",
                    "만기일자": "2026-06-30"
                }
            ]
        }
    }
    
    if cust_no not in loan_status:
        return {"error": "존재하지 않는 고객번호입니다."}
    
    customer_loans = loan_status[cust_no]
    
    # 대출종류별 필터링
    if 대출종류 != "전체":
        filtered_loans = []
        for loan in customer_loans["대출목록"]:
            if loan["대출종류"] == 대출종류:
                filtered_loans.append(loan)
        
        # 필터링된 결과로 업데이트
        filtered_result = customer_loans.copy()
        filtered_result["대출목록"] = filtered_loans
        filtered_result["총대출건수"] = len(filtered_loans)
        filtered_result["총대출잔액"] = sum([loan["대출잔액"] for loan in filtered_loans])
        return filtered_result
    
    return customer_loans

@mcp.tool()
def C13T003_tool(고객번호: int, 대출금액: int, 대출기간: int, 대출종류: str = "신용대출") -> dict:
    """
    대출 신청을 처리합니다.
    (HMA Gateway C13T003_tool 원본 로직 그대로 복사)
    """
    cust_no = str(고객번호).zfill(6)
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # 고객번호 유효성 검사
    valid_customers = ["000001", "000002", "000003"]
    if cust_no not in valid_customers:
        return {"error": "존재하지 않는 고객번호입니다."}
    
    # 고객별 신용등급 및 한도 정보
    customer_info = {
        "000001": {"신용등급": "3등급", "최대한도": 30000000, "기준금리": 5.5},
        "000002": {"신용등급": "2등급", "최대한도": 50000000, "기준금리": 4.2},
        "000003": {"신용등급": "1등급", "최대한도": 100000000, "기준금리": 3.5}
    }
    
    customer = customer_info[cust_no]
    
    # 대출 가능 여부 심사
    if 대출금액 > customer["최대한도"]:
        return {
            "신청번호": f"LOAN{current_time}{cust_no[-3:]}",
            "심사결과": "거절",
            "거절사유": "신용한도 초과",
            "최대가능금액": customer["최대한도"],
            "신용등급": customer["신용등급"]
        }
    
    # 대출종류별 금리 조정
    interest_rate = customer["기준금리"]
    if 대출종류 == "담보대출":
        interest_rate -= 0.5  # 담보대출 우대금리
    elif 대출종류 == "마이너스통장":
        interest_rate += 0.3  # 한도대출 가산금리
    
    # 대출 승인
    application_no = f"LOAN{current_time}{cust_no[-3:]}"
    maturity_date = (datetime.now() + timedelta(days=대출기간 * 30)).strftime("%Y-%m-%d")
    
    return {
        "신청번호": application_no,
        "심사결과": "승인",
        "승인금액": 대출금액,
        "적용금리": round(interest_rate, 2),
        "대출기간": 대출기간,
        "만기일자": maturity_date,
        "월상환금액": int(대출금액 * (interest_rate / 100) / 12),
        "대출종류": 대출종류,
        "신용등급": customer["신용등급"],
        "실행예정일": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
    }

@mcp.tool()
def C13T004_tool(계좌번호: str, 상환금액: int, 상환방식: str = "원금균등") -> dict:
    """
    대출 상환을 처리합니다.
    (HMA Gateway C13T004_tool 원본 로직 그대로 복사)
    """
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # 계좌별 대출 정보 (시뮬레이션)
    loan_accounts = {
        "2222333344445555": {
            "고객명": "박영희",
            "상품명": "신한마이너스통장대출",
            "현재잔액": 18000000,
            "대출금리": 4.2,
            "월이자": 63000
        },
        "3333444455556666": {
            "고객명": "이대표",
            "상품명": "신한프라이빗한도대출",
            "현재잔액": 45000000,
            "대출금리": 3.8,
            "월이자": 142500
        }
    }
    
    if 계좌번호 not in loan_accounts:
        return {"error": "존재하지 않는 계좌번호입니다."}
    
    loan_info = loan_accounts[계좌번호]
    
    # 상환 후 잔액 계산
    remaining_balance = max(0, loan_info["현재잔액"] - 상환금액)
    
    # 거래번호 생성
    transaction_no = f"RPY{current_time}{계좌번호[-4:]}"
    
    # 상환 처리 결과
    repayment_result = {
        "거래번호": transaction_no,
        "계좌번호": 계좌번호,
        "고객명": loan_info["고객명"],
        "상품명": loan_info["상품명"],
        "상환금액": 상환금액,
        "상환전잔액": loan_info["현재잔액"],
        "상환후잔액": remaining_balance,
        "상환방식": 상환방식,
        "처리일시": current_time,
        "처리상태": "완료"
    }
    
    # 전액상환 여부 확인
    if remaining_balance == 0:
        repayment_result["상환구분"] = "전액상환"
        repayment_result["계좌상태"] = "해지"
    else:
        repayment_result["상환구분"] = "일부상환"
        repayment_result["계좌상태"] = "정상"
        repayment_result["다음이자납입일"] = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    
    return repayment_result

@mcp.tool()
def C13T005_tool(고객번호: int, 대출종류: str = "전체", 조회기간: int = 12) -> dict:
    """
    대출 이력을 조회합니다.
    (HMA Gateway C13T005_tool 원본 로직 그대로 복사)
    """
    cust_no = str(고객번호).zfill(6)
    
    # 고객별 대출 이력 데이터
    loan_history = {
        "000001": {
            "고객번호": int(cust_no),
            "고객명": "김민수",
            "조회기간": f"{조회기간}개월",
            "총거래건수": 0,
            "대출이력": []
        },
        "000002": {
            "고객번호": int(cust_no),
            "고객명": "박영희",
            "조회기간": f"{조회기간}개월",
            "총거래건수": 5,
            "대출이력": [
                {
                    "거래일자": "2024-12-15",
                    "거래구분": "대출실행",
                    "상품명": "신한마이너스통장대출",
                    "거래금액": 20000000,
                    "거래후잔액": 20000000,
                    "금리": 4.2,
                    "비고": "한도대출 신규"
                },
                {
                    "거래일자": "2025-01-15",
                    "거래구분": "이자납입",
                    "상품명": "신한마이너스통장대출",
                    "거래금액": 70000,
                    "거래후잔액": 20000000,
                    "금리": 4.2,
                    "비고": "정기이자납입"
                },
                {
                    "거래일자": "2025-03-20",
                    "거래구분": "일부상환",
                    "상품명": "신한마이너스통장대출",
                    "거래금액": 2000000,
                    "거래후잔액": 18000000,
                    "금리": 4.2,
                    "비고": "원금일부상환"
                }
            ]
        },
        "000003": {
            "고객번호": int(cust_no),
            "고객명": "이대표",
            "조회기간": f"{조회기간}개월",
            "총거래건수": 8,
            "대출이력": [
                {
                    "거래일자": "2024-06-01",
                    "거래구분": "대출실행",
                    "상품명": "신한프라이빗한도대출",
                    "거래금액": 50000000,
                    "거래후잔액": 50000000,
                    "금리": 3.8,
                    "비고": "부동산담보대출"
                },
                {
                    "거래일자": "2024-09-15",
                    "거래구분": "일부상환",
                    "상품명": "신한프라이빗한도대출",
                    "거래금액": 5000000,
                    "거래후잔액": 45000000,
                    "금리": 3.8,
                    "비고": "원금일부상환"
                },
                {
                    "거래일자": "2024-11-30",
                    "거래구분": "대출실행",
                    "상품명": "신한기업운영자금대출",
                    "거래금액": 50000000,
                    "거래후잔액": 50000000,
                    "금리": 2.8,
                    "비고": "운영자금대출"
                }
            ]
        }
    }
    
    if cust_no not in loan_history:
        return {"error": "존재하지 않는 고객번호입니다."}
    
    customer_history = loan_history[cust_no]
    
    # 대출종류별 필터링
    if 대출종류 != "전체":
        filtered_history = []
        for record in customer_history["대출이력"]:
            if 대출종류 in record["상품명"]:
                filtered_history.append(record)
        
        filtered_result = customer_history.copy()
        filtered_result["대출이력"] = filtered_history
        filtered_result["총거래건수"] = len(filtered_history)
        return filtered_result
    
    return customer_history

@mcp.tool()
def C13T006_tool(고객번호: int) -> dict:
    """
    대출 한도를 조회합니다.
    (HMA Gateway C13T006_tool 원본 로직 그대로 복사)
    """
    cust_no = str(고객번호).zfill(6)
    
    # 고객별 대출 한도 정보
    loan_limits = {
        "000001": {
            "고객번호": int(cust_no),
            "고객명": "김민수",
            "신용등급": "3등급",
            "연소득": 45000000,
            "총한도": 30000000,
            "사용한도": 0,
            "가용한도": 30000000,
            "한도상세": {
                "신용대출한도": 20000000,
                "마이너스통장한도": 10000000,
                "담보대출한도": 0,
                "카드론한도": 5000000
            },
            "한도산정기준": {
                "소득배수": 0.67,
                "신용점수": 650,
                "기존대출": 0,
                "담보가치": 0
            }
        },
        "000002": {
            "고객번호": int(cust_no),
            "고객명": "박영희",
            "신용등급": "2등급",
            "연소득": 80000000,
            "총한도": 50000000,
            "사용한도": 35000000,
            "가용한도": 15000000,
            "한도상세": {
                "신용대출한도": 30000000,
                "마이너스통장한도": 20000000,
                "담보대출한도": 50000000,
                "카드론한도": 10000000
            },
            "한도산정기준": {
                "소득배수": 0.625,
                "신용점수": 750,
                "기존대출": 35000000,
                "담보가치": 200000000
            }
        },
        "000003": {
            "고객번호": int(cust_no),
            "고객명": "이대표",
            "신용등급": "1등급",
            "연소득": 300000000,
            "총한도": 200000000,
            "사용한도": 125000000,
            "가용한도": 75000000,
            "한도상세": {
                "신용대출한도": 100000000,
                "마이너스통장한도": 50000000,
                "담보대출한도": 500000000,
                "카드론한도": 20000000
            },
            "한도산정기준": {
                "소득배수": 0.67,
                "신용점수": 950,
                "기존대출": 125000000,
                "담보가치": 800000000
            },
            "특별서비스": {
                "프라이빗뱅킹": "가능",
                "전담PB": "김상담",
                "우대금리": 0.5
            }
        }
    }
    
    if cust_no not in loan_limits:
        return {"error": "존재하지 않는 고객번호입니다."}
    
    return loan_limits[cust_no]

@mcp.tool()
def C13T007_tool(고객번호: int, 계좌번호: str = None) -> dict:
    """
    대출 금리 정보를 조회합니다.
    (HMA Gateway C13T007_tool 원본 로직 그대로 복사)
    """
    cust_no = str(고객번호).zfill(6)
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # 고객별 대출 금리 정보
    interest_rates = {
        "000001": {
            "고객번호": int(cust_no),
            "고객명": "김민수",
            "신용등급": "3등급",
            "기준금리": 5.5,
            "우대금리": 0.0,
            "최종적용금리": 5.5,
            "대출계좌목록": []
        },
        "000002": {
            "고객번호": int(cust_no),
            "고객명": "박영희",
            "신용등급": "2등급",
            "기준금리": 4.5,
            "우대금리": 0.3,
            "최종적용금리": 4.2,
            "대출계좌목록": [
                {
                    "계좌번호": "2222333344445555",
                    "상품명": "신한마이너스통장대출",
                    "현재금리": 4.2,
                    "기준금리": 4.5,
                    "가산금리": 0.0,
                    "우대금리": -0.3,
                    "금리유형": "변동금리",
                    "금리조정주기": "3개월",
                    "다음조정일": "2025-09-15"
                }
            ]
        },
        "000003": {
            "고객번호": int(cust_no),
            "고객명": "이대표",
            "신용등급": "1등급",
            "기준금리": 3.5,
            "우대금리": 0.5,
            "최종적용금리": 3.0,
            "대출계좌목록": [
                {
                    "계좌번호": "3333444455556666",
                    "상품명": "신한프라이빗한도대출",
                    "현재금리": 3.8,
                    "기준금리": 4.0,
                    "가산금리": 0.3,
                    "우대금리": -0.5,
                    "금리유형": "변동금리",
                    "금리조정주기": "1개월",
                    "다음조정일": "2025-09-01"
                },
                {
                    "계좌번호": "3333444455556667",
                    "상품명": "신한기업운영자금대출",
                    "현재금리": 2.8,
                    "기준금리": 3.5,
                    "가산금리": -0.2,
                    "우대금리": -0.5,
                    "금리유형": "고정금리",
                    "금리조정주기": "해당없음",
                    "다음조정일": "해당없음"
                }
            ]
        }
    }
    
    if cust_no not in interest_rates:
        return {"error": "존재하지 않는 고객번호입니다."}
    
    customer_rates = interest_rates[cust_no]
    
    # 특정 계좌번호 조회
    if 계좌번호:
        for account in customer_rates["대출계좌목록"]:
            if account["계좌번호"] == 계좌번호:
                return {
                    "고객번호": customer_rates["고객번호"],
                    "계좌정보": account,
                    "조회일자": current_date
                }
        return {"error": "해당 계좌번호를 찾을 수 없습니다."}
    
    # 전체 금리 정보 반환
    customer_rates["조회일자"] = current_date
    return customer_rates

@mcp.tool()
def C13T008_tool(고객번호: int, 대출종류: str, 대출금액: int, 대출기간: int) -> dict:
    """
    대출 상품을 비교합니다.
    (HMA Gateway C13T008_tool 원본 로직 그대로 복사)
    """
    cust_no = str(고객번호).zfill(6)
    
    # 고객번호 유효성 검사
    valid_customers = ["000001", "000002", "000003"]
    if cust_no not in valid_customers:
        return {"error": "존재하지 않는 고객번호입니다."}
    
    # 고객별 신용등급
    customer_grades = {
        "000001": "3등급",
        "000002": "2등급", 
        "000003": "1등급"
    }
    
    credit_grade = customer_grades[cust_no]
    
    # 대출종류별 상품 정보
    loan_products = {
        "신용대출": [
            {
                "상품명": "신한 일반신용대출",
                "기준금리": 5.5 if credit_grade == "3등급" else 4.5 if credit_grade == "2등급" else 3.5,
                "최대한도": 30000000 if credit_grade == "3등급" else 50000000 if credit_grade == "2등급" else 100000000,
                "최대기간": 60,
                "중도상환수수료": 1.5,
                "특징": "간편한 온라인 신청, 빠른 심사"
            },
            {
                "상품명": "신한 직장인신용대출",
                "기준금리": 5.0 if credit_grade == "3등급" else 4.0 if credit_grade == "2등급" else 3.0,
                "최대한도": 50000000 if credit_grade == "3등급" else 80000000 if credit_grade == "2등급" else 150000000,
                "최대기간": 84,
                "중도상환수수료": 1.0,
                "특징": "직장인 전용, 우대금리 적용"
            }
        ],
        "담보대출": [
            {
                "상품명": "신한 주택담보대출",
                "기준금리": 4.0,
                "최대한도": 500000000,
                "최대기간": 360,
                "중도상환수수료": 0.5,
                "특징": "주택담보, 장기상환 가능"
            },
            {
                "상품명": "신한 아파트담보대출",
                "기준금리": 3.8,
                "최대한도": 800000000,
                "최대기간": 420,
                "중도상환수수료": 0.3,
                "특징": "아파트 전용, 최저금리"
            }
        ],
        "마이너스통장": [
            {
                "상품명": "신한 마이너스통장",
                "기준금리": 4.5 if credit_grade == "3등급" else 3.8 if credit_grade == "2등급" else 3.2,
                "최대한도": 20000000 if credit_grade == "3등급" else 30000000 if credit_grade == "2등급" else 50000000,
                "최대기간": 12,
                "중도상환수수료": 0.0,
                "특징": "필요시 언제든 사용, 이자는 사용분만"
            }
        ]
    }
    
    if 대출종류 not in loan_products:
        return {"error": f"지원하지 않는 대출종류입니다: {대출종류}"}
    
    products = loan_products[대출종류]
    
    # 각 상품별 상세 비교 정보 생성
    comparison_results = []
    
    for product in products:
        # 월상환금액 계산 (원리금균등상환 기준)
        monthly_rate = product["기준금리"] / 100 / 12
        if monthly_rate > 0:
            monthly_payment = int(대출금액 * monthly_rate * (1 + monthly_rate)**대출기간 / ((1 + monthly_rate)**대출기간 - 1))
        else:
            monthly_payment = int(대출금액 / 대출기간)
        
        # 총이자 계산
        total_interest = (monthly_payment * 대출기간) - 대출금액
        
        # 승인 가능성 평가
        approval_possibility = "높음"
        if 대출금액 > product["최대한도"]:
            approval_possibility = "낮음"
        elif 대출기간 > product["최대기간"]:
            approval_possibility = "보통"
        
        comparison_results.append({
            "상품명": product["상품명"],
            "적용금리": product["기준금리"],
            "월상환금액": monthly_payment,
            "총이자금액": max(0, total_interest),
            "중도상환수수료율": product["중도상환수수료"],
            "최대한도": product["최대한도"],
            "최대기간": product["최대기간"],
            "승인가능성": approval_possibility,
            "상품특징": product["특징"]
        })
    
    # 금리 순으로 정렬
    comparison_results.sort(key=lambda x: x["적용금리"])
    
    return {
        "고객번호": int(cust_no),
        "신용등급": credit_grade,
        "요청조건": {
            "대출종류": 대출종류,
            "대출금액": 대출금액,
            "대출기간": 대출기간
        },
        "상품비교결과": comparison_results,
        "추천상품": comparison_results[0]["상품명"] if comparison_results else None,
        "비교일자": datetime.now().strftime("%Y-%m-%d")
    }

@mcp.tool()
def C13T009_tool(고객번호: int, 연체일수: int = 0) -> dict:
    """
    대출 연체 정보를 조회합니다.
    (HMA Gateway C13T009_tool 원본 로직 그대로 복사)
    """
    cust_no = str(고객번호).zfill(6)
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # 고객별 연체 정보
    delinquency_info = {
        "000001": {
            "고객번호": int(cust_no),
            "고객명": "김민수",
            "총연체건수": 0,
            "총연체금액": 0,
            "연체계좌목록": []
        },
        "000002": {
            "고객번호": int(cust_no),
            "고객명": "박영희",
            "총연체건수": 1,
            "총연체금액": 150000,
            "연체계좌목록": [
                {
                    "계좌번호": "2222333344445556",
                    "상품명": "신한주택담보대출",
                    "연체일수": 15,
                    "연체원금": 0,
                    "연체이자": 150000,
                    "연체시작일": "2025-07-15",
                    "연체사유": "이자납입 지연",
                    "연체등급": "요주의"
                }
            ]
        },
        "000003": {
            "고객번호": int(cust_no),
            "고객명": "이대표",
            "총연체건수": 0,
            "총연체금액": 0,
            "연체계좌목록": []
        }
    }
    
    if cust_no not in delinquency_info:
        return {"error": "존재하지 않는 고객번호입니다."}
    
    customer_delinquency = delinquency_info[cust_no]
    
    # 연체일수별 필터링
    if 연체일수 > 0:
        filtered_accounts = []
        for account in customer_delinquency["연체계좌목록"]:
            if account["연체일수"] >= 연체일수:
                filtered_accounts.append(account)
        
        filtered_result = customer_delinquency.copy()
        filtered_result["연체계좌목록"] = filtered_accounts
        filtered_result["총연체건수"] = len(filtered_accounts)
        filtered_result["총연체금액"] = sum([acc["연체이자"] + acc["연체원금"] for acc in filtered_accounts])
        filtered_result["조회조건"] = f"{연체일수}일 이상 연체"
        filtered_result["조회일자"] = current_date
        return filtered_result
    
    customer_delinquency["조회일자"] = current_date
    return customer_delinquency

# C14T 시리즈 도구들 (5개)

@mcp.tool()
def C14T001_tool(여신계좌번호: str) -> dict:
    """
    대출 이자 조회를 수행합니다.
    (HMA Gateway C14T001_tool 원본 로직 그대로 복사)
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # 계좌별 이자 정보
    interest_info = {
        "2222333344445555": {
            "계좌번호": "2222333344445555",
            "고객명": "박영희",
            "상품명": "신한마이너스통장대출",
            "대출잔액": 18000000,
            "적용금리": 4.2,
            "정상이자": 63000,
            "연체이자": 0,
            "총이자": 63000,
            "이자계산기간": "2025-07-01~2025-07-31",
            "다음이자납입일": "2025-08-31",
            "이자납입방식": "매월후취"
        },
        "3333444455556666": {
            "계좌번호": "3333444455556666",
            "고객명": "이대표",
            "상품명": "신한프라이빗한도대출",
            "대출잔액": 45000000,
            "적용금리": 3.8,
            "정상이자": 142500,
            "연체이자": 0,
            "총이자": 142500,
            "이자계산기간": "2025-07-01~2025-07-31",
            "다음이자납입일": "2025-08-01",
            "이자납입방식": "매월후취"
        }
    }
    
    if 여신계좌번호 not in interest_info:
        return {"error": "존재하지 않는 계좌번호입니다."}
    
    account_interest = interest_info[여신계좌번호]
    account_interest["조회일자"] = current_date
    
    return account_interest

@mcp.tool()
def C14T002_tool(여신계좌번호: str, 이자수입종료일자: str, 연동계좌번호: str, 거래금액: int) -> dict:
    """
    대출 이자 납입을 실행합니다.
    (HMA Gateway C14T002_tool 원본 로직 그대로 복사)
    """
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # 계좌별 이자 정보 (C14T001과 동일)
    interest_accounts = {
        "2222333344445555": {
            "정상이자합계금액": 63000,
            "연체이자합계금액": 0,
            "대출잔액": 18000000
        },
        "3333444455556666": {
            "정상이자합계금액": 142500,
            "연체이자합계금액": 0,
            "대출잔액": 45000000
        }
    }
    
    if 여신계좌번호 not in interest_accounts:
        return {"error": "존재하지 않는 계좌번호입니다."}
    
    account_info = interest_accounts[여신계좌번호]
    
    # 이자 납입 처리
    total_interest = account_info["정상이자합계금액"] + account_info["연체이자합계금액"]
    
    if 거래금액 < total_interest:
        return {"error": f"이자 부족: 필요금액 {total_interest}원, 납입금액 {거래금액}원"}
    
    # 연동계좌 잔액 차감 (시뮬레이션)
    remaining_balance = 거래금액 - total_interest
    
    # 다음 이자납입일 계산 (1개월 후)
    next_payment_date = (datetime.now() + timedelta(days=30)).strftime("%Y%m%d")
    
    return {
        "이자수입종료일자": 이자수입종료일자,
        "후대출잔액": account_info["대출잔액"],
        "거래금액": 거래금액,
        "정상이자합계금액": account_info["정상이자합계금액"],
        "연체이자합계금액": account_info["연체이자합계금액"],
        "연동지급후유동성잔액": remaining_balance,
        "다음이자납입일자": next_payment_date,
        "처리일시": current_time,
        "처리상태": "완료"
    }

@mcp.tool()
def C14T003_tool(고객번호: int, 대출종류: str = "전체") -> dict:
    """
    대출 만기 정보를 조회합니다.
    (HMA Gateway C14T003_tool 원본 로직 그대로 복사)
    """
    cust_no = str(고객번호).zfill(6)
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # 고객별 대출 만기 정보
    maturity_info = {
        "000001": {
            "고객번호": int(cust_no),
            "고객명": "김민수",
            "만기도래대출건수": 0,
            "만기대출목록": []
        },
        "000002": {
            "고객번호": int(cust_no),
            "고객명": "박영희",
            "만기도래대출건수": 1,
            "만기대출목록": [
                {
                    "계좌번호": "2222333344445555",
                    "상품명": "신한마이너스통장대출",
                    "만기일자": "2027-03-15",
                    "잔여일수": 456,
                    "대출잔액": 18000000,
                    "만기구분": "정상",
                    "연장가능여부": "가능",
                    "자동연장여부": "설정"
                }
            ]
        },
        "000003": {
            "고객번호": int(cust_no),
            "고객명": "이대표",
            "만기도래대출건수": 2,
            "만기대출목록": [
                {
                    "계좌번호": "3333444455556668",
                    "상품명": "신한부동산PF대출",
                    "만기일자": "2026-06-30",
                    "잔여일수": 156,
                    "대출잔액": 30000000,
                    "만기구분": "만기임박",
                    "연장가능여부": "가능",
                    "자동연장여부": "미설정"
                },
                {
                    "계좌번호": "3333444455556667",
                    "상품명": "신한기업운영자금대출",
                    "만기일자": "2028-12-31",
                    "잔여일수": 1095,
                    "대출잔액": 50000000,
                    "만기구분": "정상",
                    "연장가능여부": "가능",
                    "자동연장여부": "설정"
                }
            ]
        }
    }
    
    if cust_no not in maturity_info:
        return {"error": "존재하지 않는 고객번호입니다."}
    
    customer_maturity = maturity_info[cust_no]
    
    # 대출종류별 필터링
    if 대출종류 != "전체":
        filtered_loans = []
        for loan in customer_maturity["만기대출목록"]:
            if 대출종류 in loan["상품명"]:
                filtered_loans.append(loan)
        
        filtered_result = customer_maturity.copy()
        filtered_result["만기대출목록"] = filtered_loans
        filtered_result["만기도래대출건수"] = len(filtered_loans)
        filtered_result["조회조건"] = 대출종류
        filtered_result["조회일자"] = current_date
        return filtered_result
    
    customer_maturity["조회일자"] = current_date
    return customer_maturity

@mcp.tool()
def C14T004_tool(계좌번호: str, 연장기간: int, 연장사유: str = "운영자금") -> dict:
    """
    대출 만기 연장을 신청합니다.
    (HMA Gateway C14T004_tool 원본 로직 그대로 복사)
    """
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # 계좌별 연장 가능 정보
    extension_info = {
        "2222333344445555": {
            "고객명": "박영희",
            "상품명": "신한마이너스통장대출",
            "현재만기일": "2027-03-15",
            "최대연장기간": 24,
            "연장수수료": 50000,
            "연장가능여부": True
        },
        "3333444455556666": {
            "고객명": "이대표",
            "상품명": "신한프라이빗한도대출",
            "현재만기일": "2030-01-01",
            "최대연장기간": 36,
            "연장수수료": 100000,
            "연장가능여부": True
        },
        "3333444455556668": {
            "고객명": "이대표",
            "상품명": "신한부동산PF대출",
            "현재만기일": "2026-06-30",
            "최대연장기간": 12,
            "연장수수료": 200000,
            "연장가능여부": True
        }
    }
    
    if 계좌번호 not in extension_info:
        return {"error": "존재하지 않는 계좌번호입니다."}
    
    account_info = extension_info[계좌번호]
    
    # 연장 가능 여부 확인
    if not account_info["연장가능여부"]:
        return {"error": "연장이 불가능한 계좌입니다."}
    
    if 연장기간 > account_info["최대연장기간"]:
        return {"error": f"최대 연장 가능 기간을 초과했습니다. (최대: {account_info['최대연장기간']}개월)"}
    
    # 새로운 만기일 계산
    current_maturity = datetime.strptime(account_info["현재만기일"], "%Y-%m-%d")
    new_maturity = current_maturity + timedelta(days=연장기간 * 30)
    
    # 연장 신청 결과
    extension_result = {
        "신청번호": f"EXT{current_time}{계좌번호[-4:]}",
        "계좌번호": 계좌번호,
        "고객명": account_info["고객명"],
        "상품명": account_info["상품명"],
        "현재만기일": account_info["현재만기일"],
        "연장기간": 연장기간,
        "신규만기일": new_maturity.strftime("%Y-%m-%d"),
        "연장사유": 연장사유,
        "연장수수료": account_info["연장수수료"],
        "신청상태": "승인",
        "신청일시": current_time,
        "적용예정일": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    }
    
    return extension_result

@mcp.tool()
def C14T005_tool(고객번호: int, 기간: str = "1년") -> dict:
    """
    대출 통계 정보를 조회합니다.
    (HMA Gateway C14T005_tool 원본 로직 그대로 복사)
    """
    cust_no = str(고객번호).zfill(6)
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # 고객별 대출 통계 정보
    loan_statistics = {
        "000001": {
            "고객번호": int(cust_no),
            "고객명": "김민수",
            "분석기간": 기간,
            "대출이용통계": {
                "총대출실행건수": 0,
                "총대출실행금액": 0,
                "평균대출금액": 0,
                "총상환금액": 0,
                "총이자납입금액": 0,
                "평균이용기간": 0
            },
            "월별통계": []
        },
        "000002": {
            "고객번호": int(cust_no),
            "고객명": "박영희",
            "분석기간": 기간,
            "대출이용통계": {
                "총대출실행건수": 3,
                "총대출실행금액": 37000000,
                "평균대출금액": 12333333,
                "총상환금액": 2000000,
                "총이자납입금액": 850000,
                "평균이용기간": 18
            },
            "월별통계": [
                {"월": "2024-12", "대출실행": 20000000, "상환금액": 0, "이자납입": 0},
                {"월": "2025-01", "대출실행": 0, "상환금액": 0, "이자납입": 70000},
                {"월": "2025-02", "대출실행": 0, "상환금액": 0, "이자납입": 70000},
                {"월": "2025-03", "대출실행": 0, "상환금액": 2000000, "이자납입": 70000},
                {"월": "2025-04", "대출실행": 17000000, "상환금액": 0, "이자납입": 210000},
                {"월": "2025-05", "대출실행": 0, "상환금액": 0, "이자납입": 210000},
                {"월": "2025-06", "대출실행": 0, "상환금액": 0, "이자납입": 210000},
                {"월": "2025-07", "대출실행": 0, "상환금액": 0, "이자납입": 210000}
            ]
        },
        "000003": {
            "고객번호": int(cust_no),
            "고객명": "이대표",
            "분석기간": 기간,
            "대출이용통계": {
                "총대출실행건수": 6,
                "총대출실행금액": 180000000,
                "평균대출금액": 30000000,
                "총상환금액": 15000000,
                "총이자납입금액": 3200000,
                "평균이용기간": 24
            },
            "월별통계": [
                {"월": "2024-06", "대출실행": 50000000, "상환금액": 0, "이자납입": 0},
                {"월": "2024-07", "대출실행": 0, "상환금액": 0, "이자납입": 190000},
                {"월": "2024-08", "대출실행": 0, "상환금액": 0, "이자납입": 190000},
                {"월": "2024-09", "대출실행": 0, "상환금액": 5000000, "이자납입": 190000},
                {"월": "2024-10", "대출실행": 0, "상환금액": 0, "이자납입": 171000},
                {"월": "2024-11", "대출실행": 50000000, "상환금액": 0, "이자납입": 171000},
                {"월": "2024-12", "대출실행": 30000000, "상환금액": 0, "이자납입": 288000},
                {"월": "2025-01", "대출실행": 50000000, "상환금액": 10000000, "이자납입": 425000}
            ]
        }
    }
    
    if cust_no not in loan_statistics:
        return {"error": "존재하지 않는 고객번호입니다."}
    
    customer_stats = loan_statistics[cust_no]
    customer_stats["조회일자"] = current_date
    
    # 추가 분석 지표 계산
    stats = customer_stats["대출이용통계"]
    if stats["총대출실행건수"] > 0:
        customer_stats["분석지표"] = {
            "대출이용빈도": round(stats["총대출실행건수"] / 12, 2),  # 월평균 대출 건수
            "상환비율": round(stats["총상환금액"] / stats["총대출실행금액"] * 100, 2) if stats["총대출실행금액"] > 0 else 0,
            "이자부담률": round(stats["총이자납입금액"] / stats["총대출실행금액"] * 100, 2) if stats["총대출실행금액"] > 0 else 0,
            "평균월이자": round(stats["총이자납입금액"] / 12, 0)
        }
    
    return customer_stats

if __name__ == "__main__":
    mcp.run()
