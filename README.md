# Google-FlowX

Google-FlowX is an automated AI orchestration pipeline for generating movie-length cinematic videos using Gemini Pro Thinking, multi-agent LLM screenwriting, and parallel NNL/ML rendering[span_0](start_span)[span_0](end_span). It features a 1,000-run matrix testing suite and an integrated mathematical alpha unblending engine to remove visible Google Flow and Veo watermarks seamlessly[span_1](start_span)[span_1](end_span).

---

## 🚀 Architecture & Tech Stack

*   **AI Orchestration:** Vertex AI (Gemini Pro Thinking, Veo) for core script generation, diffusion rendering, and multi-agent coordination.
*   **Pipeline Modules:** 50 specialized Python modules spanning screenwriting, diffusion rendering, ML post-processing, and QA matrix testing.
*   **Backend & State:** Python, FastAPI, TensorFlow, PyTorch, OpenCV, and Redis for low-latency state management and scene memory.
*   **Infrastructure & CI/CD:** Docker, Docker Compose, GitHub Actions, and Google Kubernetes Engine (GKE).

---

## 📁 Project Structure

```text
Google-FlowX/
├── .github/
│   └── workflows/
│       └── google-flowx-ci.yml   # Automated CI/CD, linting, matrix testing & Docker publishing
├── orchestrator/
│   └── api_gateway.py            # Main FastAPI gateway & orchestration router
├── watermark_remover/
│   └── artifact_inpainter.py     # Alpha unblender & diffusion artifact cleaner
├── matrix_testing/
│   └── batch_predictor.py        # 1000-run QA validation matrix test suite
├── Dockerfile                    # Production container specification
├── docker-compose.yml            # Local development orchestration (Redis + API)
├── requirements.txt              # Python dependency manifest
└── README.md
