import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title='Bone Relapse Predictor',
    page_icon='🧬',
    layout='centered'
)

@st.cache_resource
def cargar_modelo():
    # Nota: Asegúrate de que estos archivos existan en tu directorio
    modelo   = joblib.load('mejor_modelo.pkl')
    scaler   = joblib.load('scaler.pkl')
    features = joblib.load('features_list.pkl')
    umbral   = joblib.load('umbral_optimo.pkl')
    return modelo, scaler, features, umbral

try:
    modelo, scaler, features, umbral = cargar_modelo()
except Exception as e:
    st.error(f"Error al cargar archivos del modelo: {e}")
    st.stop()

st.title('🧬 Bone Relapse Risk Predictor')
st.markdown("""
Predicts **bone relapse** risk in breast cancer patients 
using gene expression profiles from primary tumors.

**Model:** Logistic Regression — GSE2034 (286 patients)  
**Features:** 35 DEGs | **AUC:** 0.697 | **Threshold:** 0.30
""")

st.divider()

with st.sidebar:
    st.header('About this tool')
    st.markdown("""
    **Dataset:** GSE2034  
    Wang et al. 2005, *The Lancet*
    
    **Pipeline:**  
    1. QC + log2 normalization  
    2. DEG analysis (t-test + FDR)  
    3. PCA + K-means clustering  
    4. Logistic Regression  
    
    **Threshold:** 0.30 (max recall)
    
    ⚠️ Research purposes only.
    """)
    st.divider()
    st.markdown('**Genes used:**')
    for g in features[:10]:
        st.markdown(f'- `{g}`')
    st.markdown(f'... and {len(features)-10} more')

# --- SECCIÓN DE CARGA ---
col1, col2 = st.columns([2, 1])
with col1:
    archivo = st.file_uploader(
        'Upload CSV (patients as rows, genes as columns)',
        type=['csv']
    )
with col2:
    st.markdown('**Expected format:**')
    st.markdown('- Rows: patients')
    st.markdown('- Columns: gene IDs (Affymetrix)')
    st.markdown('- Values: log2 expression')

if archivo is not None:
    try:
        df = pd.read_csv(archivo, index_col=0)
        st.success(f'Loaded: {df.shape[0]} patients, {df.shape[1]} genes')
        
        # Validación de genes
        genes_ok  = [g for g in features if g in df.columns]
        genes_out = [g for g in features if g not in df.columns]
        
        if len(genes_ok) < 1: # Cambiado de 10 a 1 para evitar bloqueos si solo falta alguno, ajusta a tu gusto
            st.error('No matching genes found in the CSV.')
            st.stop()
        
        if genes_out:
            st.warning(f'{len(genes_out)} genes missing — filling with mean of existing genes.')
            for g in genes_out:
                df[g] = df[genes_ok].mean(axis=1)
        
        # Preparar datos y predecir
        X_pred    = df[features].values
        X_pred_sc = scaler.transform(X_pred)
        probs     = modelo.predict_proba(X_pred_sc)[:, 1]
        preds     = (probs >= umbral).astype(int)
        
        # Resultados
        st.divider()
        st.header('Prediction Results')
        
        df_res = pd.DataFrame({
            'Patient':     df.index,
            'Probability': probs.round(3),
            'Risk':        ['HIGH' if p >= umbral else 'LOW' for p in probs],
            'Prediction':  ['Bone relapse risk' if p == 1 else 'Low risk' for p in preds]
        })
        
        c1, c2, c3 = st.columns(3)
        c1.metric('Patients', len(df_res))
        c2.metric('High risk', int(preds.sum()))
        c3.metric('Low risk', int((preds == 0).sum()))
        
        st.dataframe(df_res, use_container_width=True)

        # --- GRÁFICO (Movido aquí adentro) ---
        st.divider()
        st.subheader('Risk Probability Distribution')
        
        fig = go.Figure()
        colores_bar = ['#E84C4C' if p >= umbral else '#4C9BE8' for p in probs]
        
        fig.add_trace(go.Bar(
            x=df_res['Patient'].tolist(),
            y=probs.tolist(),
            marker_color=colores_bar,
            text=[f'{p:.2f}' for p in probs],
            textposition='outside'
        ))
        
        fig.add_hline(
            y=umbral, line_dash='dash',
            line_color='black',
            annotation_text=f'Threshold ({umbral})'
        )
        
        fig.update_layout(
            title='Bone Relapse Probability per Patient',
            yaxis=dict(title='Probability', range=[0, 1.1]),
            xaxis=dict(title='Patient ID'),
            height=450
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.download_button(
            label='⬇️ Download results CSV',
            data=df_res.to_csv(index=False),
            file_name='predictions.csv',
            mime='text/csv'
        )
        
    except Exception as e:
        st.error(f'Error durante el procesamiento: {str(e)}')

else:
    st.info('👆 Upload a CSV file to get predictions')
    # Botón de muestra
    ruta_muestra = Path('muestra_test.csv')
    if ruta_muestra.exists():
        with open(ruta_muestra, 'rb') as f:
            st.download_button(
                label='⬇️ Download sample file',
                data=f,
                file_name='muestra_test.csv',
                mime='text/csv'
            )