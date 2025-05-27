import streamlit as st
import pandas as pd
import anndata as ad
import compute_snr  # Importing the SNR calculation function
from PIL import Image


#st.set_option('server.maxUploadSize', 10240)

# Load and display the logo
logo = Image.open("assets/Scilife_NBIS.jpg")
st.image(logo, width=200)


st.title("Signal-to-Noise Ratio (SNR) Calculator")
st.markdown("""
Welcome to **SNRApp** - an interactive web app to calculate and visualize the Signal-to-Noise Ratio (SNR) from spatial omics data.
""")

# Uploading the data file
st.header("Upload Your Data")
uploaded_file = st.file_uploader("Upload an Anndata (.h5ad) file", type=["h5ad"])


if uploaded_file is not None:
    # Load the Anndata file
    try:
        adata = ad.read_h5ad(uploaded_file)
        st.success("File loaded successfully!")

        # Configuration options
        top_percentile = st.slider("Top Percentile (%)", min_value=1, max_value=50, value=20, step=1)
        bottom_percentile = st.slider("Bottom Percentile (%)", min_value=1, max_value=50, value=10, step=1)

        # Choose sampleID column
        sample_col = st.selectbox("Select Sample ID Column; if it is a single sample adata object please select 'Single Sample'", options=['Single Sample'] + adata.obs.columns.tolist(), index=0)

        # Compute SNR using the function from compute_snr.py
        st.header("Calculating SNR")
        snr_df = compute_snr.compute_snr(adata, top_percentile, bottom_percentile, sample_col=sample_col)

        if not snr_df.empty:
            st.success("SNR calculation complete!")
            st.dataframe(snr_df)

            # Display a download button for the results
            csv = snr_df.to_csv(index=False)
            st.download_button(
                label="Download SNR Results as CSV",
                data=csv,
                file_name="snr_results.csv",
                mime="text/csv"
            )
        else:
            st.warning("SNR calculation did not return any results. Check your data and settings.")

    except Exception as e:
        st.error(f"Error: {e}")

else:
    st.info("Upload an `h5ad` file to begin.")
