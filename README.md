# 🧬 Bone Relapse Risk Predictor

Web application that predicts bone relapse risk in breast cancer patients
using gene expression profiles from primary tumors.

**Live app:** [Open in Streamlit](https://bone-relapse-predictor-cjk5kzekxeqt2dccmbzpuq.streamlit.app/)

## How it works

1. Upload a CSV file with gene expression data (Affymetrix HG-U133A format)
2. The app extracts 35 differentially expressed genes (DEGs)
3. Logistic Regression model predicts bone relapse probability
4. Results shown with risk classification and interactive chart

## Model performance

| Metric | Value |
|--------|-------|
| AUC-ROC | 0.669 (test) / 0.697 (5-fold CV) |
| Recall (bone relapse) | 0.43 (threshold=0.30) |
| Classification threshold | 0.30 (optimized for recall) |
| Training set | 228 patients |
| Test set | 58 patients |

## Dataset

**GSE2034** — Wang et al. 2005, *The Lancet*  
286 node-negative breast cancer patients  
Primary tumor RNA extracted at surgery  
Follow-up: up to 10 years for bone relapse events  

## Features

35 differentially expressed genes identified via:
- t-test across 16,712 filtered genes
- Benjamini-Hochberg FDR correction (FDR < 0.05)
- |log2 Fold Change| > 1

## How to run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Files

- `app.py` — Streamlit application
- `mejor_modelo.pkl` — trained Logistic Regression model
- `scaler.pkl` — StandardScaler fitted on training data
- `features_list.pkl` — list of 35 DEG features
- `umbral_optimo.pkl` — classification threshold (0.30)
- `muestra_test.csv` — sample file for testing
- `requirements.txt` — Python dependencies

---

⚠️ *For research purposes only. Not validated for clinical use.*  
*Biological Engineer | Bioinformatics + AI*
