import numpy as np
import pandas as pd

def compute_snr(ad, top_percentile=20, bottom_percentile=10, sample_col="ImageID"):
    """
    Compute the ratio of top percentile to bottom percentile for each protein in each sample.

    Parameters:
        ad (AnnData): Anndata object containing single-cell data.
        top_percentile (int): Top X% of values used for signal.
        bottom_percentile (int): Bottom X% of values used for noise.
        sample_col (str): Name of the column in ad.obs indicating sample ID (default: 'ImageID').

    Returns:
        pd.DataFrame: Dataframe with columns: sample ID, Protein, SNR ratio.
    """
    try:
        results = []

        if sample_col not in ad.obs.columns:
            print(f"'{sample_col}' not found in ad.obs. Proceeding as single-sample.")

            for protein in ad.var_names:
                values = ad[:, protein].X.flatten()
                if len(values) < 20:
                    continue
                sorted_vals = np.sort(values)
                top_vals = sorted_vals[-int(len(sorted_vals) * top_percentile / 100):]
                bottom_vals = sorted_vals[:int(len(sorted_vals) * bottom_percentile / 100)]

                top_mean = np.mean(top_vals)
                bottom_mean = np.mean(bottom_vals)
                snr = np.nan if bottom_mean == 0 else top_mean / bottom_mean

                results.append({'Sample': 'SingleSample', 'Protein': protein, 'SNR': snr})
        else:
            for sample_id in ad.obs[sample_col].unique():
                sub_ad = ad[ad.obs[sample_col] == sample_id]
                for protein in sub_ad.var_names:
                    values = sub_ad[:, protein].X.flatten()
                    if len(values) < 20:
                        continue
                    sorted_vals = np.sort(values)
                    top_vals = sorted_vals[-int(len(sorted_vals) * top_percentile / 100):]
                    bottom_vals = sorted_vals[:int(len(sorted_vals) * bottom_percentile / 100)]

                    top_mean = np.mean(top_vals)
                    bottom_mean = np.mean(bottom_vals)
                    snr = np.nan if bottom_mean == 0 else top_mean / bottom_mean

                    results.append({'Sample': sample_id, 'Protein': protein, 'SNR': snr})

        return pd.DataFrame(results)

    except Exception as e:
        print(f"Error calculating SNR: {e}")
        return pd.DataFrame()
