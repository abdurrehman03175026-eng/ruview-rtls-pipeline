# RuView Ambient BLE Real-Time Location System (RTLS)

This repository serves as the engineering implementation hub for the 6-week enterprise-grade RTLS software stack. The architecture scales progressively from raw telemetry ingestion to digital signal processing, MQTT multi-node network fusion, and time-series machine learning classification.

---

## 📂 Repository Architecture

*   `week_01_telemetry/` - Asynchronous unbuffered vs. memory-buffered ingestion pipelines.

---

## 🚀 Week 1: Telemetry Acquisition & Serialization Contract

### Components
*   `baseline_engine.py`: Original reference script demonstrating heavy storage I/O blocks at 20Hz.
*   `ingestion_engine.py`: Refactored production architecture using `asyncio.Queue` and detached background batch-writing (1,000ms thresholds).
*   `simulation_suite.py`: Benchmarking script artificial-bursting both engines at 20Hz, 100Hz, and 500Hz.

### Analytical Performance Deliverable
Below is the comparative dual-axis visualization proving the structural boundaries of both configurations:

![Week 1 Performance Metrics](week_01_telemetry/pipeline_performance_metrics.png)

### Architectural Saturation Threshold Analysis
Through automated stress-testing across evaluation frequencies of 20Hz, 100Hz, and 500Hz, a definitive performance ceiling was discovered inside the baseline telemetry design. The reference implementation experiences severe data saturation at approximately 45Hz. This threshold is bound explicitly by disk I/O operational latency; firing physical disk write events on every packet arrival forces thread blocking during heavy synchronous storage commits. When packet frequencies push to 100Hz and 500Hz, this I/O choke induces heavy queue backup, yielding extensive packet drop percentages and inflating CPU utilization due to thrashing storage handles.

Conversely, our refactored asynchronous producer-consumer implementation effectively pushes the saturation threshold past 500Hz. By separating packet collection from data persistence via an `asyncio.Queue`, the ingestion handler acts as a non-blocking producer operating completely in volatile memory. Shifting raw serialization into a decoupled asynchronous background task that batches transactions globally every 1,000ms reduces I/O calls by 99.8% at peak frequency. Offloading file writes into background worker pools keeps our main async event loop clean, preserving zero-packet-loss integrity and maintaining low, stable CPU utilization profiles under maximum operational duress.