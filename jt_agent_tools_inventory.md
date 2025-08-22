# 짬통 에이전트 (JT Agent) 도구 인벤토리
## 다음 담당자를 위한 완전한 마이그레이션 가이드

> **📋 이 문서의 목적**: 113개 도구를 7개 MCP 서버로 마이그레이션하는 완전한 로드맵

---

## 🚀 **마이그레이션 우선순위 (담당자 작업 순서)**

### **1단계: 핵심 서버 (금요일 밤)**
1. **news_sentiment** (24개 도구) - C01T001 포함, 기존 작업 연관성 ⭐
2. **stock_market_analysis** (27개 도구) - 가장 큰 서버, 핵심 기능 ⭐
3. **investment_account** (13개 도구) - 중간 규모 ⭐

### **2단계: 확장 서버 (토요일)**
4. **loan_management** (14개 도구)
5. **payment_management** (11개 도구)
6. **account_management** (6개 도구)
7. **macro_market_outlook** (18개 도구)

---

## 📁 **에이전트별 도구 매핑**

### 1. account_management_agent (계좌 관리)
- C02T001_tool
- C05T001_tool  
- C05T002_tool
- C05T003_tool
- C05T004_tool
- C05T005_tool
**총 6개 도구**

### 2. payment_management_agent (이체/자동이체 관리)
- C03T001_tool
- C03T002_tool
- C03T003_tool
- C04T001_tool
- C09T001_tool
- C09T002_tool
- C10T001_tool
- C10T002_tool
- C10T003_tool
- C10T004_tool
- C10T006_tool
**총 11개 도구**

### 3. loan_management_agent (대출 관리)
- C13T001_tool
- C13T002_tool
- C13T003_tool
- C13T004_tool
- C13T005_tool
- C13T006_tool
- C13T007_tool
- C13T008_tool
- C13T009_tool
- C14T001_tool
- C14T002_tool
- C14T003_tool
- C14T004_tool
- C14T005_tool
**총 14개 도구**

### 4. investment_account_agent (투자계좌/환율 관리)
- C11T001_tool
- C11T002_tool
- C11T003_tool
- C11T004_tool
- C11T005_tool
- C11T006_tool
- C11T007_tool
- C11T008_tool
- C11T009_tool
- C11T010_tool
- C11T011_tool
- C11T012_tool
- C11T013_tool
**총 13개 도구**

### 5. stock_market_analysis_agent (주식 시장 분석)
- C01T002_tool
- C01T006_tool
- C01T008_tool
- C01T011_tool
- C01T014_tool
- C01T015_tool
- C01T020_tool
- C01T022_tool
- C01T024_tool
- C01T025_tool
- C01T026_tool
- C01T027_tool
- C01T028_tool
- C01T029_tool
- C01T031_tool
- C01T032_tool
- C01T040_tool
- C01T041_tool
- C01T042_tool
- C01T045_tool
- C01T046_tool
- C01T047_tool
- C01T048_tool
- C01T053_tool
- C01T054_tool
- C01T058_tool
- C01T067_tool
**총 27개 도구**

### 6. macro_market_outlook_agent (매크로/시장 전망)
- C01T003_tool
- C01T009_tool
- C01T010_tool
- C01T012_tool
- C01T013_tool
- C01T016_tool
- C01T017_tool
- C01T021_tool
- C01T033_tool
- C01T034_tool
- C01T038_tool
- C01T052_tool
- C01T055_tool
- C01T056_tool
- C01T057_tool
- C01T062_tool
- C01T069_tool
- C01T070_tool
**총 18개 도구**

### 7. news_sentiment_agent (뉴스/감성 분석)
- C01T001_tool
- C01T004_tool
- C01T005_tool
- C01T007_tool
- C01T018_tool
- C01T019_tool
- C01T023_tool
- C01T030_tool
- C01T035_tool
- C01T036_tool
- C01T037_tool
- C01T039_tool
- C01T043_tool
- C01T044_tool
- C01T049_tool
- C01T050_tool
- C01T051_tool
- C01T059_tool
- C01T060_tool
- C01T061_tool
- C01T063_tool
- C01T065_tool
- C01T066_tool
- C01T068_tool
**총 24개 도구**

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

### **테스트 명령어**
```bash
# 개별 서버 테스트
mcp-eval generate-tasks --server mcp_servers/{agent_name}/server.py --num-tasks 10

# 다중 서버 테스트  
mcp-eval generate-tasks --servers \
  mcp_servers/news_sentiment/server.py \
  mcp_servers/stock_market_analysis/server.py \
  --num-tasks 50
```

---

## ⚡ **성공 기준**
- ✅ 각 서버가 독립적으로 실행 가능
- ✅ 모든 도구가 원본과 동일한 결과 반환
- ✅ MCPEval에서 시나리오 생성 가능
- ✅ 다중 서버 환경에서 크로스 도메인 시나리오 생성

**🎯 최종 목표**: 짬통 에이전트의 실제 사용 패턴을 MCPEval로 완벽 재현!
