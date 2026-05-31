# safeweb_ai_machine
# 🛡️ SafeWeb AI Blocker — Enterprise Child Safety Filter

**SafeWeb AI Blocker** is an intelligent, real-time content filtering system designed to create a safe browsing environment for children. Powered by Machine Learning, the application analyzes website URLs and text inputs instantly to detect and block inappropriate, explicit, or harmful web content.

Developed as a core utility under the R&D suite of **Easy Business Technology**, this tool moves beyond rigid keyword-blocking to leverage semantic text analysis for high-accuracy child protection guidelines.

---

## 🚀 Key Features

- **AI-Driven Deep Scan:** Uses custom-trained natural language intelligence to classify URLs and text payloads instantly.
- **Dynamic Risk Scoring:** Generates an AI analyst risk matrix percentage (%) for every analyzed endpoint.
- **Premium Glassmorphic UI:** Features a high-end, responsive dark-mode dashboard built with Streamlit and custom CSS.
- **Session Audit Logs:** Keeps a temporary historic log of all content analyzed within the current active session.
- **Export Data Metrics:** Allows administrators or parents to download full session audit history as a clean CSV/Excel spreadsheet.
- **Robust Failure Resilience:** Built-in cryptographic safety nets to prevent system crashes during engine loads.

---

## 🛠️ Tech Stack & Architecture

- **Core Language:** Python 3
- **Framework:** Streamlit (Custom Embedded Web Components)
- **Machine Learning Architecture:** Linear Support Vector Classification (`LinearSVC`)
- **Natural Language Processing:** Term Frequency-Inverse Document Frequency (`TF-IDF Vectorizer`)
- **Model Storage:** Joblib Serialized Pipelines

---

## 📦 Installation & Setup

To run this application locally on your workstation, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/mrupdatepython/safeweb-ai-blocker.git](https://github.com/mrupdatepython/safeweb-ai-blocker.git)
   cd safeweb-ai-blocker
