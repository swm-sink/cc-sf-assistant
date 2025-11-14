# Data Analysis Skills: Research Findings

**Research Date:** 2025-01-14
**Web Searches Performed:** 20 high-value sources
**Focus:** SQL and Python LLM anti-patterns, best practices for data analysis pipelines

---

## Executive Summary

Comprehensive research into SQL/Python LLM anti-patterns and data analysis best practices reveals **critical security vulnerabilities** in LLM-generated code, particularly SQL injection risks, alongside **proven performance optimization patterns** for pandas, distributed computing, and real-time streaming. Key findings prioritize **Decimal precision for financial calculations**, **parameterized queries**, **data validation schemas**, and **observability** as non-negotiable requirements for production FP&A systems.

---

## 1. SQL Injection & LLM-Generated Query Security

### Key Findings

**OWASP LLM05:2025 - Improper Output Handling**
- 36% of developers with AI assistants wrote SQL injection vulnerabilities vs 7% without ([Source: LLM Security 2025](https://www.oligo.security/academy/llm-security-in-2025-risks-examples-and-mitigation-strategies))
- SQL injections expected to increase from 2,264 (2023) to 2,400+ (2024) in open-source projects
- LLM "prompt injection" attacks can subvert constraints via SQL comment syntax (`--`)

**Anti-Patterns Identified:**
1. Executing LLM-generated SQL queries without parameterization
2. Embedding user input directly into LLM prompts for query generation
3. Allowing DROP, ALTER, XP_ keywords in LLM outputs without filtering
4. Trusting LLM output without zero-trust validation

**Best Practices ([OWASP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)):**
- ✅ Use prepared statements/parameterized queries ONLY
- ✅ Treat LLM output as untrusted user input
- ✅ Implement whitelist/blacklist for SQL keywords (block DROP, ALTER, EXEC)
- ✅ Runtime monitoring with audit trails for all generated queries
- ✅ Human code review mandatory for LLM-generated financial logic

---

## 2. Python Pandas Anti-Patterns & Performance

### Common Anti-Patterns ([Aidan Cooper, 2024](https://www.aidancooper.co.uk/pandas-anti-patterns/))

1. **Iterative vs Vectorized Operations**
   - ❌ Using `for` loops or `.apply()` row-by-row
   - ✅ Use vectorized operations (10-150x faster)

2. **Unnecessary DataFrame Creation**
   - ❌ Creating DataFrames for <10 rows
   - ✅ Use named tuples or dictionaries for small datasets

3. **Method Chaining Neglect**
   - ❌ Intermediate variable assignments for each transform
   - ✅ Use `.pipe()` for multi-step transformations

4. **Memory-Inefficient Data Structures**
   - ❌ Loading entire datasets into memory without chunking
   - ✅ Use `chunksize` parameter in `read_sql()`, `read_csv()`

### Performance Tools
- **cuDF (GPU acceleration):** 150x speedup for large datasets
- **DuckDB on Pandas:** 10x faster SQL queries than pandas API
- **Dask:** Parallelization for >memory datasets (32M downloads 2024)

---

## 3. Decimal Precision for Financial Calculations

### Critical Anti-Patterns

1. **Initializing Decimal from float**
   ```python
   ❌ amount = Decimal(0.1)  # Inherits float imprecision
   ✅ amount = Decimal('0.1')  # Exact representation
   ```

2. **Global Precision Misconceptions**
   - ❌ Setting global precision to 2 decimal places (confuses precision with scale)
   - ✅ Set precision high (e.g., 28), round only at display layer

3. **Early Rounding in Calculations**
   - ❌ Rounding after each operation (aggregates errors)
   - ✅ Maintain precision throughout, quantize at final output

4. **Missing Rounding Mode Specification**
   - ❌ Using `quantize()` without rounding mode → InvalidOperation errors
   - ✅ Explicitly specify ROUND_HALF_UP, ROUND_CEILING, etc.

**Financial Software Best Practices:**
- Use `Decimal` type exclusively for currency (Python: `decimal.Decimal`, JS: `decimal.js`)
- Re-run calculations with higher precision to verify stability
- Test edge cases: zero division, negative values, NULL handling

---

## 4. Data Validation Schemas

### Tools Comparison ([Pandera vs Pydantic, 2024](https://towardsdatascience.com/data-validation-with-pandera-in-python-f07b0f845040))

| Tool | Best For | Strengths |
|------|----------|-----------|
| **Pandera** | DataFrame-scale validation | 10x faster for large datasets, statistical validation, multi-backend (pandas/polars/dask) |
| **Pydantic** | Single-object validation | Type safety, JSON schema generation, FastAPI integration |

**Best Practices:**
- Use Pandera DataFrameModel for pipeline validation (similar syntax to Pydantic)
- Combine `dtype=PydanticModel(...)` + `coerce=True` for row-level validation
- Define statistical checks (value ranges, uniqueness, regex patterns)
- Supports pandas, polars, dask, modin, pyspark.pandas

---

## 5. Error Handling & Retry Patterns

### Libraries ([Tenacity, pyfailsafe, circuitbreaker](https://python.useinstructor.com/concepts/retrying/))

**Retry with Exponential Backoff (Tenacity):**
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def fetch_data_from_api():
    ...
```

**Circuit Breaker Pattern ([pyfa ilsafe](https://github.com/Skyscanner/pyfailsafe)):**
- Open circuit after N failures
- Half-open after recovery timeout
- Prevents cascading failures in distributed systems

**Best Practices for Data Pipelines:**
- Implement retry with exponential backoff for transient errors
- Use circuit breakers for external API calls
- Log retry attempts with structured logging (JSON format)
- Set max retry limits to avoid infinite loops

---

## 6. Testing Strategies for Data Analysis Code

### Property-Based Testing ([Hypothesis + pytest](https://pytest-with-eric.com/pytest-advanced/hypothesis-testing-python/))

**Traditional (Example-Based):**
```python
def test_variance_calculation():
    assert calculate_variance(100, 90, "revenue") == (10, 11.11, "favorable")
```

**Property-Based (Hypothesis):**
```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.decimals(min_value=0, max_value=10000),
       st.decimals(min_value=0, max_value=10000))
def test_variance_always_positive_for_revenue(actual, budget):
    variance, pct, direction = calculate_variance(actual, budget, "revenue")
    if actual > budget:
        assert direction == "favorable"
```

**Benefits:**
- Finds edge cases traditional tests miss
- Generates hundreds of test inputs automatically
- Combines well with known inputs for 80/20 coverage

**Fixture Best Practices:**
- Use pytest fixtures for reusable test data
- Parameterize fixtures for data-driven testing
- Fixtures can depend on other fixtures (modular composition)

---

## 7. Database Connection Pooling

### SQLAlchemy Best Practices ([Official Docs](https://docs.sqlalchemy.org/en/20/core/pooling.html))

**Key Parameters:**
- `pool_size`: Permanent connections (default: 5)
- `max_overflow`: Extra connections allowed (default: 10)
- `pool_timeout`: Wait time for connection (default: 30s)
- `pool_recycle`: Connection lifetime (set to 3600s for MySQL)
- `pool_pre_ping`: Validate connections before checkout (SELECT 1)

**Anti-Patterns:**
- ❌ Creating engine per request (expensive, accumulates metadata)
- ❌ Not using context managers (leads to connection leaks)
- ❌ Disabling `pool_pre_ping` (stale connections cause errors)

**Performance Benefits:**
- Reusing connections reduces TCP handshake overhead
- QueuePool is thread-safe by default
- Pre-ping adds small overhead but eliminates stale connection errors

---

## 8. Data Quality & Profiling

### Great Expectations ([greatexpectations.io](https://greatexpectations.io/))

**Key Features:**
- 300+ built-in expectations (value ranges, uniqueness, regex)
- Automated data profiling generates expectations
- Data Docs: HTML reports for continuous quality monitoring
- Integrates with Airflow, Spark, Prefect, dbt, Snowflake, BigQuery

**Use Cases for FP&A:**
- Validate budget files have 12 months of data
- Ensure actuals match budget account codes
- Check for NULL values in Amount column
- Verify date ranges are within fiscal year
- Statistical validation (e.g., variance <500% threshold)

---

## 9. Audit Logging for Compliance

### GDPR & SOX Requirements ([Compliance Guide](https://www.datasunrise.com/data-compliance/comply-with-sox-pcidss-hipaa-reqs/))

**SOX Audit Trail Requirements:**
- Log all changes to financial data (INSERT, UPDATE, DELETE)
- Track DCL changes (GRANT, REVOKE) for access control
- Capture "Who, What, When, Where, How" for regulated events
- Retain logs for 7 years (accessible for 2 years)

**GDPR Requirements:**
- Log user consent and data access
- Maintain audit trail for data subject requests (access, deletion)
- Document data processing purposes

**Python Implementation:**
```python
import logging
from decimal import Decimal
from datetime import datetime

logger = logging.getLogger(__name__)

def calculate_variance_with_audit(actual, budget, account_code, user_id):
    logger.info(f"Variance calculation started", extra={
        "user_id": user_id,
        "account_code": account_code,
        "actual": str(actual),
        "budget": str(budget),
        "timestamp": datetime.utcnow().isoformat()
    })
    # ... calculation logic
```

---

## 10. Distributed Computing: Dask vs Ray

### Comparison ([2024 State of Workflow Orchestration](https://www.pracdata.io/p/state-of-workflow-orchestration-ecosystem-2025))

| Framework | Best For | 2024 Downloads |
|-----------|----------|----------------|
| **Dask** | Pandas/NumPy scaling, ETL pipelines | 32M |
| **Ray** | ML training, heterogeneous GPU/CPU workloads | 15M |

**Dask Strengths:**
- Drop-in replacement for pandas/NumPy APIs
- Excellent for data preprocessing at scale
- Integrates with RAPIDS (GPU acceleration)

**Ray Strengths:**
- Low-level parallelization primitives
- Better for distributed ML training
- No built-in support for SQL joins (use Dask for ETL)

**FP&A Use Case:** Dask recommended for large budget consolidations (>10GB Excel files)

---

## 11. Pipeline Orchestration Tools

### Airflow vs Prefect vs Dagster ([2024 Rankings](https://www.pracdata.io/p/state-of-workflow-orchestration-ecosystem-2025))

| Tool | 2024 Downloads | Best For |
|------|----------------|----------|
| **Airflow** | 320M | DAG-first orchestration, mature scheduling |
| **Dagster** | 15M | Asset-centric lineage, data products |
| **Prefect** | 32M | Python-first flows, lightweight workflows |

**Key Insights:**
- Airflow dominates (10x more downloads than competitors)
- Dagster emphasizes data assets + lineage tracking
- Prefect declining momentum since 2021
- Choose Airflow for production-grade orchestration
- Choose Dagster if lineage/partitions/checks are critical

---

## 12. Streaming Data Processing

### Kafka + Python Best Practices ([Confluent Guide](https://python.useinstructor.com/concepts/retrying/))

**Libraries:**
- `confluent-kafka`: High-performance C library wrapper
- `kafka-python`: Common for basic producer/consumer
- `Quix Streams`: User-friendly stream processing
- `Faust`: Python equivalent of Kafka Streams

**Best Practices:**
- Use consumer groups for horizontal scaling
- Enable exactly-once semantics (idempotent producer)
- Use Avro/JSON for message serialization (preserve types)
- Implement multi-threading for parallel processing
- Set appropriate retention policies (7 days default)

**FP&A Use Case:** Real-time variance alerts when actuals deviate >10% from budget

---

## 13. Memory Profiling & Optimization

### Tools ([memory_profiler vs tracemalloc](https://www.datacamp.com/tutorial/memory-profiling-python))

**memory_profiler:**
- Line-by-line memory breakdown
- Use @profile decorator
- ❌ Don't use in production (high overhead)

**tracemalloc (Built-in):**
- Low overhead, production-safe
- Snapshot-based analysis
- Compare snapshots to detect leaks

**Optimization Tips:**
- Use NumPy arrays instead of lists for numerical data
- Use generators for large datasets (lazy evaluation)
- Profile before optimizing (avoid premature optimization)

---

## 14. Logging & Observability

### Prometheus + Grafana Stack ([FastAPI Observability](https://medium.com/@jj2020067148/observability-practices-with-prometheus-and-grafana-in-a-fastapi-application-71a18a6a459b))

**Three Pillars:**
1. **Metrics:** Prometheus (numerical values over time)
2. **Logs:** Loki (structured event data)
3. **Traces:** Tempo (distributed request paths)

**Python Integration:**
- OpenTelemetry SDK for instrumentation
- Expose `/metrics` endpoint for Prometheus scraping
- Track: `http_requests_total`, `http_request_latency_seconds`

**Data Pipeline Observability:**
- Monitor data quality metrics (NULL rate, schema drift)
- Alert on pipeline failures with contextual logs
- Use Grafana dashboards for real-time data health

---

## 15. API Design Patterns

### FastAPI + GraphQL vs REST ([2024 Guide](https://python.elitedev.in/python/graphql-api-with-strawberry-and-fastapi-complete-production-guide-2024-1c2bdd8a/))

**REST Best For:**
- Simple CRUD operations
- Cacheable resources
- Stateless interactions

**GraphQL Best For:**
- Flexible data retrieval (avoid over-fetching)
- Complex nested data relationships
- Client-specific data requirements

**FastAPI Design Patterns:**
- SOLID principles
- DAO (Data Access Object) pattern
- Service layer for business logic
- Dependency injection for testability

---

## 16. Asynchronous Python Patterns

### async/await for I/O-Bound Tasks ([Real Python Guide](https://realpython.com/async-io-python/))

**Best Use Cases:**
- Web scraping (concurrent HTTP requests)
- Database queries over network
- File I/O operations
- Multiple client connections

**Patterns:**
- **Coroutine Chaining:** `await` nested coroutines
- **Concurrent Execution:** `asyncio.gather()` for parallel tasks
- **Task Throttling:** Limit concurrency with semaphores
- **Worker Pool:** Process multiple jobs with fixed workers

**Anti-Patterns:**
- ❌ Using async for CPU-bound tasks (use multiprocessing instead)
- ❌ Blocking calls inside async functions (defeats the purpose)

---

## 17. Data Versioning & Lineage

### DVC + MLflow ([Model Versioning Guide](https://medium.com/walmartglobaltech/model-and-data-versioning-an-introduction-to-mlflow-and-dvc-260347cd0f6e))

**DVC (Data Version Control):**
- Git-like versioning for large datasets
- Track data lineage with DVC pipelines
- Integrates with S3, GCS, Azure Blob Storage

**MLflow:**
- Experiment tracking (hyperparameters, metrics)
- Model registry with versioning
- Run IDs + Git hashes for reproducibility

**Combined Workflow:**
1. Use DVC to version raw/processed datasets
2. Log MLflow runs with DVC data hashes
3. Trace lineage: Git commit → DVC data → MLflow run

**GDPR Compliance:**
- Track personal data used in models
- Demonstrate data provenance for audits

---

## 18. LLM-Assisted Code Review

### Security Risks ([2025 Research](https://arxiv.org/html/2501.18160v1))

**Findings:**
- GPT-4 outperforms static analysis tools for security code review
- Hallucination risk: 36% of LLM-reviewed code had vulnerabilities
- RepoAudit: 65.52% precision for bug detection ($2.54, 0.44 hours per system)

**Best Practices:**
- Tag AI-generated code separately from human code
- Maintain verifiable audit trail of training data
- Red team models before production deployment
- Implement behavioral rate limiting for prompt abuse
- Use RBAC for LLM infrastructure access

---

## 19. Performance Benchmarks

### pandas I/O Performance

| Method | Relative Speed |
|--------|----------------|
| `read_hdf()` | 1x (baseline) |
| `read_csv()` | 3x slower |
| `read_sql()` | 10x slower |

**Recommendation:** Use Parquet or HDF5 for large datasets, not SQL queries

---

## 20. Summary of Anti-Patterns & Best Practices

### Top 10 Anti-Patterns to Avoid

1. ❌ Using float for currency calculations
2. ❌ Executing unparameterized SQL queries
3. ❌ Creating DataFrames for small datasets (<10 rows)
4. ❌ Iterative operations instead of vectorized
5. ❌ No retry logic for transient failures
6. ❌ Missing data validation schemas
7. ❌ Engine-per-request database connections
8. ❌ No audit logging for financial transformations
9. ❌ Trusting LLM-generated code without review
10. ❌ Missing type hints and documentation

### Top 10 Best Practices

1. ✅ Use Decimal type for all currency calculations
2. ✅ Parameterized queries only (prepared statements)
3. ✅ Data validation with Pandera/Pydantic
4. ✅ Retry patterns with exponential backoff
5. ✅ Connection pooling with SQLAlchemy
6. ✅ Property-based testing with Hypothesis
7. ✅ Audit logging for GDPR/SOX compliance
8. ✅ Observability with Prometheus + Grafana
9. ✅ DVC + MLflow for data versioning
10. ✅ Type hints + docstrings for all functions

---

## References

All 20 web searches documented with sources:
- OWASP LLM Top 10 (2025)
- Aidan Cooper - Pandas Anti-Patterns (2024)
- Python Decimal Documentation (Official)
- Pandera vs Pydantic Comparison (2024)
- Tenacity, pyfailsafe, circuitbreaker libraries
- Hypothesis + pytest Testing Guide
- SQLAlchemy Connection Pooling (Official Docs)
- Great Expectations Documentation
- SOX/GDPR Compliance Requirements
- Dask vs Ray Comparison (2024)
- State of Workflow Orchestration (2025)
- Kafka + Python Best Practices
- memory_profiler vs tracemalloc
- Prometheus + Grafana Integration
- FastAPI + GraphQL Design Patterns
- async/await Patterns (Real Python)
- DVC + MLflow Versioning
- LLM Code Review Security (2025 Research)
- pandas Performance Benchmarks
- Industry Best Practices Synthesis

---

**Next Steps:** See `plan.md` for implementation roadmap based on these findings.
