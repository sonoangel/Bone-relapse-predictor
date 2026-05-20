# 🧬 Bone Relapse Risk Predictor

Web application that predicts bone relapse risk in breast cancer patients
using gene expression profiles from primary tumors.

**Live app:** [Open in Streamlit](https://bone-relapse-predictor-cjk5kzekxeqt2dccmbzpuq.streamlit.app/)

---

## Features

- 📊 Upload any CSV with Affymetrix HG-U133A gene expression data
- 🎯 Predicts bone relapse probability per patient
- 🔴 Risk classification with clinically optimized threshold (0.30)
- 📈 Interactive probability chart
- 🔍 SHAP explainability — see which genes drove each prediction
- ⬇️ Download results as CSV

## How it works

1. Upload a CSV file with gene expression data
2. App extracts 35 differentially expressed genes (DEGs)
3. Logistic Regression predicts bone relapse probability
4. SHAP explains the contribution of each gene per patient
5. Results shown with risk classification and interactive charts

## Model performance

| Metric | Value |
|--------|-------|
| AUC-ROC (test set) | 0.669 |
| AUC-ROC (5-fold CV) | 0.697 ± 0.047 |
| Recall (bone relapse) | 0.43 |
| Classification threshold | 0.30 (optimized for recall) |
| Training set | 228 patients |
| Test set | 58 patients |

## Dataset

**GSE2034** — Wang et al. 2005, *The Lancet*
286 node-negative breast cancer patients
Primary tumor RNA extracted at surgery
Follow-up: up to 10 years for bone relapse events

## Analysis pipeline

This app is the final product of a complete bioinformatics pipeline:

1. **Quality Control** — log2 normalization, outlier detection, gene filtering
2. **Differential Expression** — t-test across 16,712 genes + FDR correction
3. **Unsupervised Analysis** — PCA + K-means clustering (3 molecular subgroups)
4. **ML Classification** — Logistic Regression with threshold optimization
5. **Explainability** — SHAP values per gene per patient

Full analysis notebooks: [breast-cancer-bioinformatics](https://github.com/sonoangel/breast-cancer-bioinformatics)

## Files

| File | Description |
|------|-------------|
| `app.py` | Streamlit application |
| `mejor_modelo.pkl` | Trained Logistic Regression model |
| `scaler.pkl` | StandardScaler fitted on training data |
| `features_list.pkl` | List of 35 DEG features |
| `umbral_optimo.pkl` | Classification threshold (0.30) |
| `shap_explainer.pkl` | Pre-fitted SHAP LinearExplainer |
| `muestra_test.csv` | Sample file for testing |
| `requirements.txt` | Python dependencies |

## How to run locally

```bash
git clone https://github.com/sonoangel/bone-relapse-predictor.git
cd bone-relapse-predictor
pip install -r requirements.txt
streamlit run app.py
```
## 📝 Technical Article

**From Raw Data to Clinical Predictions: A Bioinformatics Pipeline
for Breast Cancer Bone Relapse Using Python and Machine Learning**

Published on Medium — [Read the article](https://medium.com/@lcarmonav10/from-raw-data-to-clinical-predictions-a-bioinformatics-pipeline-for-breast-cancer-bone-relapse-e1d99c5abc79)

Covers the complete pipeline: QC → DEG → PCA → ML → SHAP → Deployment

---

⚠️ *For research purposes only. Not validated for clinical use.*

*Biological Engineer | Bioinformatics + AI | Colombia*
