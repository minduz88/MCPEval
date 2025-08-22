# HMA Gateway → MCPEval 마이그레이션 프로젝트
## 다중 서버 크로스 도메인 시나리오 생성을 통한 Qwen3 모델 성능 향상

> **🎯 핵심 목표**: MCPEval 다중 서버로 짬통 에이전트 동작을 완벽 재현하여 크로스 도메인 시나리오 대량 생성

---

## 📋 **담당자 Quick Start 가이드**

### **즉시 시작 가능한 작업**
1. **도구 인벤토리 확인**: `jt_agent_tools_inventory.md` 파일 참조
2. **첫 번째 서버 구축**: `news_sentiment` 서버부터 시작 (24개 도구)
3. **기존 참조 코드**: `mcp_servers/hma_gateway/server.py` 참조

### **핵심 파일 위치**
- **도구 정의**: `/mnt/c/Dev/SOL-Agent/hma-gateway/mcp_tools/*.json`
- **도구 구현**: `/mnt/c/Dev/SOL-Agent/hma-gateway/factory/tool/preset/*.py`
- **MCPEval 서버**: `/mnt/c/Dev/SOL-Agent/MCPEval/mcp_servers/`

---

## 🎯 프로젝트 개요

### 목표
MCPEval을 활용하여 HMA Gateway의 "짬통 에이전트" 도구들로부터 다양한 금융 시나리오를 자동 생성하고, 이를 Few-shot 학습 데이터로 변환하여 Qwen3 모델의 사용자 요청 처리 능력을 향상시키는 지식 디스틸레이션 프로젝트

### 핵심 아이디어
```
기존 문제: 짬통 에이전트들은 시나리오가 없어서 적절한 처리 패턴을 모름
해결 방안: MCPEval = 시나리오 생성 엔진으로 활용
최종 목표: 생성된 시나리오를 RAG 기반 Few-shot으로 Qwen3에 주입
```

---

## 🏗️ 현재 HMA Gateway 구조 분석

### 기존 에이전트 구조
```
📦 HMA Gateway
├── 🎭 전문 에이전트들 (시나리오 기반)
│   ├── 특정 워크플로우용 에이전트
│   └── 잘 정의된 시나리오 보유
│
└── 🥫 짬통 에이전트 (JT Agent)
    ├── account_management_agent
    ├── payment_management_agent
    ├── loan_management_agent
    ├── investment_account_agent
    ├── stock_market_analysis_agent
    ├── macro_market_outlook_agent
    ├── news_sentiment_agent
    └── builtin:ragfaq
```

### 짬통 에이전트의 한계
- ❌ **시나리오 부재**: 구체적인 사용 패턴이 정의되지 않음
- ❌ **처리 패턴 불명확**: 사용자 요청에 대한 적절한 대응 방식 부족
- ❌ **예제 데이터 부족**: Few-shot 학습을 위한 참조 사례 없음

---

## 🚀 마이그레이션 전략 (에이전트별 분리 + 다중 서버)

### 🎯 **핵심 아이디어: MCPEval 다중 서버로 짬통 에이전트 동작 완벽 재현**

#### **기존 짬통 에이전트 동작**
```
사용자 요청 → JT Agent → 적절한 하위 에이전트 선택 → 해당 도구 실행
```

#### **MCPEval 다중 서버 구현**
```
사용자 요청 → MCPEval → 여러 서버의 모든 도구 접근 → 적절한 도구 조합 실행
```

### **Phase 1: 에이전트별 독립 MCP 서버 구축**
```
MCPEval/mcp_servers/
├── account_management/
│   └── server.py (6개 도구: C02T001, C05T001~C05T005)
├── payment_management/  
│   └── server.py (11개 도구: C03T001~C03T003, C04T001, C09T001~C09T002, C10T001~C10T004, C10T006)
├── loan_management/
│   └── server.py (14개 도구: C13T001~C13T009, C14T001~C14T005)
├── investment_account/
│   └── server.py (13개 도구: C11T001~C11T013)
├── stock_market_analysis/
│   └── server.py (27개 도구: C01T002, C01T006, C01T008, ...)
├── macro_market_outlook/
│   └── server.py (18개 도구: C01T003, C01T009, C01T010, ...)
├── news_sentiment/
│   └── server.py (24개 도구: C01T001, C01T004, C01T005, ...)
└── common/
    └── utils.py (공통 유틸리티 함수들)

총 7개 독립 서버 × 113개 고유 도구
```

### **Phase 2: MCPEval 다중 서버 시나리오 생성 엔진**
```
MCPEval Multi-Server Task Generation Pipeline:

# 크로스 도메인 시나리오 자동 생성
mcp-eval generate-tasks --servers \
  mcp_servers/stock_market_analysis/server.py \
  mcp_servers/investment_account/server.py \
  mcp_servers/news_sentiment/server.py \
  --num-tasks 200

생성 결과 예시:
{
  "name": "종합 투자 분석 및 감성 평가",
  "tool_calls": [
    {"tool_name": "C01T002_tool", "tool_parameters": {"symbol": "A005930"}},
    {"tool_name": "C01T001_tool", "tool_parameters": {"symbol": "A005930"}},
    {"tool_name": "C11T001_tool", "tool_parameters": {"account_id": "123456"}}
  ]
}
```

### **Phase 3: 실제 짬통 에이전트 사용 패턴 재현**
```
예상 생성 시나리오 타입들:

🔄 투자 + 뉴스 조합:
   주식 기술적 분석 + 뉴스 감성 분석 + 투자 의사결정

🔄 계좌 + 이체 조합:
   계좌 잔고 확인 + 자동이체 설정 + 이체 내역 조회

🔄 대출 + 투자 조합:
   대출 한도 확인 + 투자 상품 추천 + 리스크 평가

🔄 환율 + 투자 조합:
   환율 동향 분석 + 해외 투자 포트폴리오 + 환전 서비스

🔄 종합 금융 상담:
   모든 도메인을 아우르는 복합적 금융 서비스 시나리오
```

### Phase 3: Few-shot 데이터셋 구축
```
생성된 시나리오들을 Few-shot 형태로 변환:

{
  "user_request": "고객의 실제 요청",
  "tool_sequence": ["도구1", "도구2", "도구3"],
  "expected_response": "적절한 응답 패턴",
  "context": "금융 도메인 컨텍스트"
}
```

---

## 🔄 전체 워크플로우

### 데이터 생성 파이프라인
```
🔄 지식 디스틸레이션 파이프라인:

HMA Tools 
    ↓ (마이그레이션)
MCPEval MCP Servers
    ↓ (태스크 생성)
다양한 금융 시나리오들
    ↓ (품질 평가 & 선별)
고품질 시나리오 컬렉션
    ↓ (Few-shot 변환)
RAG 기반 예제 데이터셋
    ↓ (주입)
향상된 Qwen3 모델 성능
```

### 실행 단계
1. **도구 인벤토리 수집**
   - 각 에이전트별 사용 도구 매핑
   - 도구 간 의존성 분석

2. **MCP 서버 생성**
   - 에이전트별 독립 서버 구축
   - 도구 함수 마이그레이션

3. **대량 시나리오 생성**
   ```bash
   # 각 도메인별 시나리오 생성
   mcp-eval generate-tasks --server account_management --num-tasks 200
   mcp-eval generate-tasks --server investment_account --num-tasks 200
   # ... 모든 에이전트별 실행
   ```

4. **시나리오 품질 검증**
   ```bash
   # 생성된 태스크 검증
   mcp-eval verify-tasks --tasks-file generated_scenarios.jsonl
   ```

5. **Few-shot 데이터셋 구축**
   - 검증된 시나리오들 분석
   - 사용자 요청 패턴 추출
   - RAG용 임베딩 생성

6. **Qwen3 모델 성능 테스트**
   - Before/After 성능 비교
   - 실제 사용자 요청 처리 품질 측정

---

## 📊 예상 효과

### 정량적 효과
- **시나리오 생성량**: 에이전트당 100-200개 → 총 700-1400개 시나리오
- **커버리지 확대**: 기존 시나리오 대비 10-20배 증가
- **응답 품질**: 사용자 만족도 20-30% 향상 예상

### 정성적 효과
- ✅ **시나리오 부족 문제 해결**
- ✅ **자동화된 예제 생성 파이프라인**
- ✅ **모델 응답 일관성 향상**
- ✅ **새로운 사용 패턴 발견**

---

## 🛠️ 기술 스택

### 마이그레이션 도구
- **MCPEval**: 시나리오 생성 엔진
- **Python**: 도구 변환 스크립트
- **FastMCP**: MCP 서버 프레임워크

### 데이터 처리
- **Embedding**: 시나리오 벡터화
- **RAG**: 유사 시나리오 검색
- **Few-shot**: 컨텍스트 학습

---

## 📅 실행 계획

### Week 1: 인프라 구축
- [ ] 마이그레이션 스크립트 개발
- [ ] MCP 서버 템플릿 작성
- [ ] 첫 번째 에이전트 마이그레이션 테스트

### Week 2: 대량 마이그레이션
- [ ] 모든 짬통 에이전트 도구 마이그레이션
- [ ] MCPEval 통합 테스트
- [ ] 시나리오 생성 파이프라인 구축

### Week 3: 데이터 생성 및 검증
- [ ] 대량 시나리오 생성 (1000+ 개)
- [ ] 품질 평가 및 선별
- [ ] Few-shot 데이터셋 구축

### Week 4: 모델 통합 및 성능 측정
- [ ] RAG 시스템 구축
- [ ] Qwen3 모델 통합
- [ ] 성능 비교 및 최적화

---

## 🎉 기대 성과

이 프로젝트를 통해:
1. **MCPEval을 단순한 평가 도구에서 시나리오 생성 엔진으로 확장**
2. **HMA Gateway의 미완성 부분을 데이터 기반으로 보완**
3. **Qwen3 모델의 금융 도메인 처리 능력 대폭 향상**
4. **지속적인 시나리오 생성 및 개선 파이프라인 구축**

---

## 📝 참고사항

### 핵심 파일 위치
- **HMA 도구 정의**: `/mnt/c/Dev/SOL-Agent/hma-gateway/mcp_tools/`
- **도구 구현체**: `/mnt/c/Dev/SOL-Agent/hma-gateway/factory/tool/preset/`
- **MCPEval 서버**: `/mnt/c/Dev/SOL-Agent/MCPEval/mcp_servers/`

### 주요 명령어
```bash
# 시나리오 생성
mcp-eval generate-tasks --server [agent_name] --num-tasks 200

# 시나리오 검증  
mcp-eval verify-tasks --tasks-file scenarios.jsonl

# 성능 평가
mcp-eval evaluate --model-config qwen3.json
```

---

## 🚨 긴급 실행 계획 (주말 → 월요일)
## 고객 협의용 성능 비교 리포트 생성

---

### 🎯 주말 목표 (금요일 저녁 → 월요일 아침)

**최종 목표**: SOTA 모델(GPT-4.1)로 생성한 다양한 시나리오들을 **Qwen3 vs GPT-4**로 실행 비교하여 **고품질 성능 분석 리포트** 작성

#### 핵심 미션
```
🔥 고객 협의용 고품질 리포트 생성
📊 정량적 성능 비교 데이터 확보  
📈 Qwen3 모델의 강점/약점 명확화
💼 비즈니스 가치 입증 자료 완성
```

---

### 🔄 실행 워크플로우

#### **Phase 1: 에이전트별 MCP 서버 구축** (금요일 밤)
```bash
# 1단계: 핵심 에이전트 서버부터 구축 (우선순위 순)
# news_sentiment (24개 도구) - C01T001 포함, 기존 작업 연관성
# stock_market_analysis (27개 도구) - 가장 큰 서버, 핵심 기능
# investment_account (13개 도구) - 중간 규모

# 목표: 최소 3개 서버 구축 완료 (64개 도구 마이그레이션)
```

#### **Phase 2: 다중 서버 대량 시나리오 생성** (토요일 오전)
```bash
# SOTA 모델로 크로스 도메인 시나리오 생성
uv run -m mcpeval.cli.main generate-tasks \
  --servers \
    mcp_servers/news_sentiment/server.py \
    mcp_servers/stock_market_analysis/server.py \
    mcp_servers/investment_account/server.py \
  --model gpt-4.1-2025-04-14 \
  --num-tasks 300 \
  --prompt-file data/hma_gateway/task_generation_prompt.json \
  --output data/hma_gateway/multi_server_scenarios.jsonl

# 목표: 300+ 크로스 도메인 고품질 시나리오 확보
# 예상: 투자+뉴스, 주식분석+감성분석 등 복합 시나리오
```

#### **Phase 3: 다중 서버 시나리오 검증** (토요일 오후)
```bash
# 다중 서버 환경에서 시나리오 검증
uv run -m mcpeval.cli.main verify-tasks \
  --servers \
    mcp_servers/news_sentiment/server.py \
    mcp_servers/stock_market_analysis/server.py \
    mcp_servers/investment_account/server.py \
  --tasks-file data/hma_gateway/multi_server_scenarios.jsonl \
  --model gpt-4.1-2025-04-14 \
  --output data/hma_gateway/verified_multi_scenarios.jsonl

# 목표: 실행 가능한 크로스 도메인 시나리오 200+ 개 확보
```

#### **Phase 4: 다중 서버 이중 모델 성능 평가** (일요일)
```bash
# Qwen3 모델 다중 서버 성능 평가
uv run -m mcpeval.cli.main evaluate \
  --servers \
    mcp_servers/news_sentiment/server.py \
    mcp_servers/stock_market_analysis/server.py \
    mcp_servers/investment_account/server.py \
  --model-config data/hma_gateway/qwen3.json \
  --tasks-file data/hma_gateway/verified_multi_scenarios.jsonl \
  --output data/hma_gateway/qwen3_multi_server_results.json \
  --max-turns 10

# GPT-4 모델 다중 서버 성능 평가 (벤치마크)
uv run -m mcpeval.cli.main evaluate \
  --servers \
    mcp_servers/news_sentiment/server.py \
    mcp_servers/stock_market_analysis/server.py \
    mcp_servers/investment_account/server.py \
  --model-config data/hma_gateway/gpt-4o.json \
  --tasks-file data/hma_gateway/verified_multi_scenarios.jsonl \
  --output data/hma_gateway/gpt4_multi_server_results.json \
  --max-turns 10
```

#### **Phase 5: 다중 서버 심층 분석 및 리포트 생성** (일요일 밤~월요일 새벽)
```bash
# 다중 서버 환경에서 모델별 성능 분석
uv run -m mcpeval.cli.main analyze \
  --predictions data/hma_gateway/qwen3_multi_server_results.json \
  --ground-truth data/hma_gateway/verified_multi_scenarios.jsonl \
  --generate-report \
  --report-output data/hma_gateway/qwen3_multi_server_analysis.md

uv run -m mcpeval.cli.main analyze \
  --predictions data/hma_gateway/gpt4_multi_server_results.json \
  --ground-truth data/hma_gateway/verified_multi_scenarios.jsonl \
  --generate-report \
  --report-output data/hma_gateway/gpt4_multi_server_analysis.md

# 크로스 도메인 시나리오 특화 고품질 비교 리포트 작성
# 특별 분석: 도메인 간 협력 패턴, 복합 태스크 처리 능력
```

---

### 📊 분석 포인트 (다중 서버 크로스 도메인 특화)

#### **정량적 분석 지표**
1. **다중 도메인 도구 호출 정확도**
   - 크로스 도메인 도구 선택률 (%)
   - 도메인 간 협력 패턴 정확도 (%)
   - 불필요한 도구 호출 비율 (%)

2. **복합 시나리오 실행 성공률**
   - 단일 도메인 vs 다중 도메인 완료율 비교
   - 도메인 간 전환 성공률 (%)
   - 복잡도별 실행 시간 분석

3. **짬통 에이전트 패턴 재현도**
   - 실제 JT Agent 사용 패턴과의 유사도 (%)
   - 도메인 조합 다양성 지수
   - 사용자 요구사항 충족도 (크로스 도메인)

#### **정성적 분석 포인트**
1. **강점 영역 식별**
   - Qwen3이 GPT-4보다 우수한 시나리오 타입
   - 특정 금융 도메인에서의 전문성

2. **개선 필요 영역**
   - 실패 패턴 분석
   - 오류 유형별 분류
   - 개선 방향 제시

3. **비즈니스 가치**
   - 비용 효율성 (Qwen3 vs GPT-4)
   - 실제 업무 적용 가능성
   - ROI 추정

---

### 📈 고품질 리포트 구성 (고객 협의용)

#### **Executive Summary** (1페이지)
- 핵심 성과 지표 요약
- Qwen3 vs GPT-4 성능 비교 한눈에 보기
- 비즈니스 권장사항

#### **상세 성능 분석** (3-4페이지)
- 도메인별 성능 비교 차트
- 실패 케이스 분석 및 개선방안
- 구체적 사례 및 증빙자료

#### **기술적 인사이트** (2페이지)
- 모델 특성 비교
- 실제 운영 환경 고려사항
- 향후 개선 로드맵

#### **비즈니스 임팩트** (1페이지)
- 비용 절감 효과
- 서비스 품질 향상
- 경쟁 우위 확보 방안

---

### ⚡ 성공 기준

#### **리포트 품질 기준**
- ✅ **정량적 근거**: 150+ 시나리오 실행 결과 기반
- ✅ **시각적 완성도**: 차트, 그래프, 표를 활용한 직관적 표현
- ✅ **실무적 가치**: 실제 비즈니스 의사결정에 활용 가능한 인사이트
- ✅ **신뢰성**: 재현 가능한 실험 설계 및 투명한 방법론

#### **고객 협의 준비사항**
- 📊 **데이터 백업**: 모든 실험 결과 및 로그 보존
- 📋 **FAQ 준비**: 예상 질문에 대한 기술적 답변 준비
- 💡 **데모 시나리오**: 실시간 실행 가능한 대표 사례
- 🚀 **Next Steps**: 구체적인 후속 액션 플랜

---

### 🎯 월요일 아침 목표

**완성물**: 
1. **고품질 성능 비교 리포트** (10-15페이지)
2. **실행 가능한 데모 시나리오** (5-10개)
3. **정량적 성능 데이터** (JSON, CSV 형태)
4. **고객 프레젠테이션 자료** (PPT 또는 PDF)

**핵심 메시지**:
> *"Qwen3 모델이 특정 금융 도메인에서 GPT-4와 경쟁 가능한 성능을 보이며, 비용 효율적인 솔루션으로 활용 가능함을 실증적으로 입증"*

---

## ✅ **담당자 실행 체크리스트**

### **금요일 밤 (필수 완료)**
- [ ] `jt_agent_tools_inventory.md` 파일 숙지
- [ ] `news_sentiment` 서버 구축 (24개 도구)
- [ ] `stock_market_analysis` 서버 구축 (27개 도구) 
- [ ] `investment_account` 서버 구축 (13개 도구)
- [ ] 3개 서버 개별 테스트 완료

### **토요일 오전 (시나리오 생성)**
- [ ] 다중 서버 시나리오 생성 (300개 목표)
- [ ] 크로스 도메인 시나리오 검증
- [ ] 생성 품질 확인

### **토요일 오후~일요일 (성능 평가)**
- [ ] Qwen3 모델 평가 실행
- [ ] GPT-4 모델 평가 실행  
- [ ] 결과 데이터 수집 완료

### **일요일 밤~월요일 새벽 (리포트)**
- [ ] 성능 분석 실행
- [ ] 고품질 비교 리포트 작성
- [ ] 고객 협의 자료 준비

---

## 🚨 **긴급 연락처 및 참고사항**

### **핵심 파일 백업 위치**
- **메인 계획서**: `HMA_MCPEVAL_MIGRATION_PLAN.md`
- **도구 인벤토리**: `jt_agent_tools_inventory.md`
- **기존 서버 예시**: `mcp_servers/hma_gateway/server.py`

### **문제 발생시 대응**
1. **도구 구현 오류**: 원본 HMA Gateway 코드 직접 복사
2. **MCPEval 실행 오류**: 기존 4개 도구 서버로 테스트
3. **시나리오 생성 실패**: 단일 서버부터 점진적 확장

### **성공 지표**
- **최소 목표**: 200+ 검증된 시나리오
- **이상적 목표**: 300+ 크로스 도메인 시나리오
- **품질 기준**: 실행 성공률 80% 이상

---

*"다중 서버 크로스 도메인 시나리오 생성을 통한 혁신적 AI 모델 성능 향상 프로젝트"*
