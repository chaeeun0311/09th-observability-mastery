"""
프로젝트명
---------
Observability Demo - 상품 조회 서비스 장애 분석

프로젝트 목적
------------
기존 모니터링(Monitoring)은 CPU, Memory, Error Count 등의
지표(Metrics)를 통해 '문제가 발생했다'는 사실을 알려준다.

관측 가능성(Observability)은
Metrics, Logs, Traces를 함께 활용하여
'왜 문제가 발생했는지'까지 추적할 수 있도록 한다.

데모 시나리오
-------------
사용자가 상품 조회 API(/product)를 호출한다.

Frontend
    ↓
Product API
    ↓
Database

Database 조회 시간이 랜덤하게 증가하도록 설정하여
실제 서비스에서 발생하는 응답 지연 상황을 재현한다.

관측 데이터
-----------
1. Metrics
   - API 응답시간
   - 요청 수
   - 에러율

2. Logs
   - 상품 조회 요청 로그
   - DB 지연 경고 로그

3. Traces
   - product_request Span
   - db_query Span

장애 발생 시 분석 흐름
--------------------
1. Metric에서 응답시간 증가 확인
2. Log에서 DB 지연 경고 확인
3. Trace에서 db_query 구간 병목 확인
4. 장애 원인 분석 완료

기대 효과
----------
- 장애 원인 파악 시간(MTTR) 단축
- 시스템 병목 지점 식별
- Observability 개념 이해

기술 스택
----------
- Python
- Flask
- OpenTelemetry
- Grafana Tempo (연동 가능)
- Loki (연동 가능)
- Prometheus (연동 가능)
"""

from flask import Flask
import logging
import random
import time

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter,
)

# ==================================================
# OpenTelemetry Tracing 설정
# ==================================================

trace.set_tracer_provider(TracerProvider())

tracer = trace.get_tracer(__name__)

span_processor = BatchSpanProcessor(
    OTLPSpanExporter(
        endpoint="http://localhost:4318/v1/traces"
    )
)

trace.get_tracer_provider().add_span_processor(
    span_processor
)

# ==================================================
# Logging 설정
# ==================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# ==================================================
# Flask Application
# ==================================================

app = Flask(__name__)


@app.route("/product")
def product():
    """
    상품 조회 API

    관측 포인트
    ----------
    product_request Span
        └─ db_query Span

    DB 응답시간을 랜덤하게 발생시켜
    장애 상황을 시뮬레이션한다.
    """

    with tracer.start_as_current_span("product_request"):

        logging.info("상품 조회 요청 수신")

        # 실제 DB 조회를 가정
        db_time = random.uniform(0.1, 3.0)

        with tracer.start_as_current_span("db_query"):

            time.sleep(db_time)

            # 2초 이상이면 지연 발생으로 간주
            if db_time > 2:
                logging.warning(
                    f"DB 응답 지연 발생 ({db_time:.2f}s)"
                )

        logging.info(
            f"상품 조회 완료 (DB 응답시간: {db_time:.2f}s)"
        )

        return {
            "status": "success",
            "db_time": round(db_time, 2)
        }


if __name__ == "__main__":
    logging.info("Observability Demo 시작")
    app.run(host="0.0.0.0", port=5000)