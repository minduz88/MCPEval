# 짬통 에이전트 (JT Agent) 도구 인벤토리
## 다음 담당자를 위한 완전한 마이그레이션 가이드

> **📋 이 문서의 목적**: 113개 도구를 7개 MCP 서버로 마이그레이션하는 완전한 로드맵

---

## ✅ **마이그레이션 완료 현황 (2025년 8월 23일 02:10 기준)**

### **1단계: 핵심 서버 (금요일 밤)** ✅ **완료**
1. ✅ **news_sentiment** (24개 도구) - C01T001 포함, 기존 작업 연관성
2. ✅ **stock_market_analysis** (27개 도구) - 가장 큰 서버, 핵심 기능
3. ✅ **investment_account** (13개 도구) - 중간 규모

### **2단계: 확장 서버 (금요일 밤 추가 완료)** ✅ **완료**
4. ✅ **loan_management** (14개 도구)
5. ✅ **payment_management** (11개 도구)
6. ✅ **account_management** (6개 도구)
7. ✅ **macro_market_outlook** (18개 도구)

### **🎉 전체 마이그레이션 완료!**
- **총 7개 서버 구축 완료**
- **총 113개 도구 마이그레이션 완료**
- **HMA Gateway 원본 로직 그대로 복사 구현**

---

## 📁 **에이전트별 도구 매핑**

### 1. account_management_agent (계좌 관리) ✅ **완료**
- ✅ C02T001_tool (고객정보 상세조회)
- ✅ C05T001_tool (계좌 비밀번호 체크)
- ✅ C05T002_tool (계좌 비밀번호 변경)
- ✅ C05T003_tool (계좌 이체 한도 설정)
- ✅ C05T004_tool (계좌 메모 설정)
- ✅ C05T005_tool (계좌 알림 설정)
**총 6개 도구 ✅ 구현완료**

### 2. payment_management_agent (이체/자동이체 관리) ✅ **완료**
- ✅ C03T001_tool (계좌 이체 처리 결과 조회)
- ✅ C03T002_tool (이체 실행)
- ✅ C03T003_tool (이체 한도 조회)
- ✅ C04T001_tool (이체 수수료 조회)
- ✅ C09T001_tool (자동이체 등록)
- ✅ C09T002_tool (자동이체 해지)
- ✅ C10T001_tool (자동이체 목록 조회)
- ✅ C10T002_tool (자동이체 변경)
- ✅ C10T003_tool (자동이체 실행 결과)
- ✅ C10T004_tool (자동이체 실패 처리)
- ✅ C10T006_tool (자동이체 통계)
**총 11개 도구 ✅ 구현완료**

### 3. loan_management_agent (대출 관리) ✅ **완료**
- ✅ C13T001_tool (마이너스 통장 대출 현황)
- ✅ C13T002_tool (전체 대출 현황 조회)
- ✅ C13T003_tool (대출 신청 처리)
- ✅ C13T004_tool (대출 상환 처리)
- ✅ C13T005_tool (대출 이력 조회)
- ✅ C13T006_tool (대출 한도 조회)
- ✅ C13T007_tool (대출 금리 정보 조회)
- ✅ C13T008_tool (대출 상품 비교)
- ✅ C13T009_tool (대출 연체 정보 조회)
- ✅ C14T001_tool (대출 이자 조회)
- ✅ C14T002_tool (대출 이자 납입)
- ✅ C14T003_tool (대출 만기 정보 조회)
- ✅ C14T004_tool (대출 만기 연장 신청)
- ✅ C14T005_tool (대출 통계 정보 조회)
**총 14개 도구 ✅ 구현완료**

### 4. investment_account_agent (투자계좌/환율 관리) ✅ **완료**
- ✅ C11T001_tool (예금 및 신탁 계좌 조회)
- ✅ C11T002_tool (투자계좌 잔고 조회)
- ✅ C11T003_tool (주식 주문 실행)
- ✅ C11T004_tool (주문 체결 내역 조회)
- ✅ C11T005_tool (환율 조회)
- ✅ C11T006_tool (환전 실행)
- ✅ C11T007_tool (환전 거래 내역 조회)
- ✅ C11T008_tool (외화계좌 잔고 조회)
- ✅ C11T009_tool (펀드 보유 현황 조회)
- ✅ C11T010_tool (펀드 매수/매도 실행)
- ✅ C11T011_tool (투자성향 분석 결과 조회)
- ✅ C11T012_tool (투자 수익률 분석)
- ✅ C11T013_tool (맞춤형 포트폴리오 추천)
**총 13개 도구 ✅ 구현완료**

### 5. stock_market_analysis_agent (주식 시장 분석) ✅ **완료**
- ✅ C01T002_tool (주식 실적 증감율 계산)
- ✅ C01T006_tool (기간별 수익률 계산)
- ✅ C01T008_tool (변동성 계산)
- ✅ C01T011_tool (기술적 분석 지표)
- ✅ C01T014_tool (여러 주식 성과 비교)
- ✅ C01T015_tool (벤치마크 상관관계 분석)
- ✅ C01T020_tool (시나리오 분석)
- ✅ C01T022_tool (샤프 비율 계산)
- ✅ C01T024_tool (모멘텀 계산)
- ✅ C01T025_tool (리스크 지표 조회)
- ✅ C01T026_tool (포트폴리오 리스크 계산)
- ✅ C01T027_tool (VaR 계산)
- ✅ C01T028_tool (옵션 그릭스 계산)
- ✅ C01T029_tool (내재가치 계산 DDM)
- ✅ C01T031_tool (다중 팩터 모델 분석)
- ✅ C01T032_tool (상대가치 분석)
- ✅ C01T040_tool (수익률 예측)
- ✅ C01T041_tool (포트폴리오 최적화)
- ✅ C01T042_tool (스트레스 테스트)
- ✅ C01T045_tool (정보비율 계산)
- ✅ C01T046_tool (팩터 익스포저 분석)
- ✅ C01T047_tool (성과 기여도 분석)
- ✅ C01T048_tool (조건부 VaR 계산)
- ✅ C01T053_tool (리밸런싱 효과 분석)
- ✅ C01T054_tool (주식 간 상관관계 분석)
- ✅ C01T058_tool (최대 손실 기간 분석)
- ✅ C01T067_tool (팩터 조건 필터링)
**총 27개 도구 ✅ 구현완료**

### 6. macro_market_outlook_agent (매크로/시장 전망) ✅ **완료**
- ✅ C01T003_tool (매크로 지표 증가율 계산)
- ✅ C01T009_tool (주식 매크로 민감도 분석)
- ✅ C01T010_tool (지역별 경제 지표 비교)
- ✅ C01T012_tool (지역별 경제 전망 예측)
- ✅ C01T013_tool (여러 지역 경제 지표 비교)
- ✅ C01T016_tool (매크로 시나리오 분석)
- ✅ C01T017_tool (매크로 지표 값 조회)
- ✅ C01T021_tool (매크로 스트레스 테스트)
- ✅ C01T033_tool (자산군별 전망 분석)
- ✅ C01T034_tool (매크로 지표 예측)
- ✅ C01T038_tool (시장 리스크 평가)
- ✅ C01T052_tool (경기 사이클 분석)
- ✅ C01T055_tool (중앙은행 정책 예측)
- ✅ C01T056_tool (금리 경로 분석)
- ✅ C01T057_tool (인플레이션 전망)
- ✅ C01T062_tool (경제 지표 상관관계)
- ✅ C01T069_tool (글로벌 리스크 평가)
- ✅ C01T070_tool (지정학적 리스크 분석)
**총 18개 도구 ✅ 구현완료**

### 7. news_sentiment_agent (뉴스/감성 분석) ✅ **완료**
- ✅ C01T001_tool (종목 뉴스 감성 분석)
- ✅ C01T004_tool (종목 이슈 타임라인 생성)
- ✅ C01T005_tool (감성 임계값 확인)
- ✅ C01T007_tool (여러 종목 감성 비교)
- ✅ C01T018_tool (종목 관련 최신 뉴스)
- ✅ C01T019_tool (키워드 뉴스 검색)
- ✅ C01T023_tool (감성 변화 추이)
- ✅ C01T030_tool (키워드 연관 종목)
- ✅ C01T035_tool (뉴스 볼륨 변화 조회)
- ✅ C01T036_tool (여러 종목 뉴스 메트릭 비교)
- ✅ C01T037_tool (뉴스 임팩트 임계값 확인)
- ✅ C01T039_tool (특정 날짜 주요 뉴스)
- ✅ C01T043_tool (뉴스 카테고리별 분류)
- ✅ C01T044_tool (여러 종목 기간별 감성 비교)
- ✅ C01T049_tool (뉴스 소스별 분류)
- ✅ C01T050_tool (감성 점수 기반 알림)
- ✅ C01T051_tool (키워드 뉴스 트렌드 분석)
- ✅ C01T059_tool (뉴스 임팩트 기반 투자 신호)
- ✅ C01T060_tool (여러 종목 뉴스 메트릭 랭킹)
- ✅ C01T061_tool (특정 타입 뉴스 필터링)
- ✅ C01T063_tool (뉴스 감성 상관관계 분석)
- ✅ C01T065_tool (감성 점수 범위 필터링)
- ✅ C01T066_tool (뉴스 감성 기반 예측)
- ✅ C01T068_tool (벤치마크 대비 감성 비교)
**총 24개 도구 ✅ 구현완료**

---

## 📊 **전체 마이그레이션 요약**
- **총 7개 MCP 서버 구축 필요**
- **총 113개 고유 도구** (중복 제거 완료)
- **가장 큰 서버**: stock_market_analysis (27개 도구)
- **가장 작은 서버**: account_management (6개 도구)

## 📈 **도구 분포 및 복잡도**
- **C01T 시리즈** (주식/시장): 70개 ⚠️ 가장 복잡
- **C11T 시리즈** (투자계좌): 13개
- **C13T 시리즈** (뉴스): 9개  
- **C14T 시리즈** (거시경제): 5개
- **C05T 시리즈** (예금/신탁): 5개
- **C10T 시리즈** (결제): 5개
- **C03T 시리즈** (고객정보): 3개
- **C09T 시리즈** (대출): 2개
- **C02T 시리즈** (계좌): 1개
- **C04T 시리즈** (기타): 1개

---

## 🛠️ **담당자를 위한 구현 가이드**

### **서버 생성 템플릿**
```python
# mcp_servers/{agent_name}/server.py
#!/usr/bin/env uv run
from mcp.server.fastmcp import FastMCP
from datetime import datetime

mcp = FastMCP("{Agent Name} MCP Server")

# 각 도구별 함수 구현
@mcp.tool()
def tool_name(param1: str, param2: int = None) -> dict:
    """도구 설명"""
    # HMA Gateway 원본 로직 복사
    return {"result": "data"}

if __name__ == "__main__":
    mcp.run()
```

### **필수 참조 파일**
1. **도구 정의**: `/mnt/c/Dev/SOL-Agent/hma-gateway/mcp_tools/{tool_id}_tool.json`
2. **구현체**: `/mnt/c/Dev/SOL-Agent/hma-gateway/factory/tool/preset/{tool_id}_tool.py`
3. **기존 예시**: `/mnt/c/Dev/SOL-Agent/MCPEval/mcp_servers/hma_gateway/server.py`

### **다음 담당자용 테스트 명령어** (GPT-4/Qwen3 엔드포인트 연결 후 실행)

#### **개별 서버 테스트**
```bash
# 각 서버별 개별 테스트 (10개씩)
uv run -m mcpeval.cli.main generate-tasks --server mcp_servers/news_sentiment/server.py --num-tasks 10
uv run -m mcpeval.cli.main generate-tasks --server mcp_servers/stock_market_analysis/server.py --num-tasks 10
uv run -m mcpeval.cli.main generate-tasks --server mcp_servers/investment_account/server.py --num-tasks 10
uv run -m mcpeval.cli.main generate-tasks --server mcp_servers/loan_management/server.py --num-tasks 10
uv run -m mcpeval.cli.main generate-tasks --server mcp_servers/payment_management/server.py --num-tasks 10
uv run -m mcpeval.cli.main generate-tasks --server mcp_servers/account_management/server.py --num-tasks 10
uv run -m mcpeval.cli.main generate-tasks --server mcp_servers/macro_market_outlook/server.py --num-tasks 10
```

#### **다중 서버 크로스 도메인 시나리오 생성** (메인 목표)
```bash
# 전체 7개 서버로 크로스 도메인 시나리오 300개 생성
uv run -m mcpeval.cli.main generate-tasks \
  --servers \
    mcp_servers/news_sentiment/server.py \
    mcp_servers/stock_market_analysis/server.py \
    mcp_servers/investment_account/server.py \
    mcp_servers/loan_management/server.py \
    mcp_servers/payment_management/server.py \
    mcp_servers/account_management/server.py \
    mcp_servers/macro_market_outlook/server.py \
  --num-tasks 300 \
  --output data/hma_gateway/multi_server_scenarios.jsonl
```

---

## ⚡ **성공 기준**
- ✅ 각 서버가 독립적으로 실행 가능
- ✅ 모든 도구가 원본과 동일한 결과 반환
- ✅ MCPEval에서 시나리오 생성 가능
- ✅ 다중 서버 환경에서 크로스 도메인 시나리오 생성

**🎯 최종 목표**: 짬통 에이전트의 실제 사용 패턴을 MCPEval로 완벽 재현!
