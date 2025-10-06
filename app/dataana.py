import os
import sys
import numpy as np
import math

def detect_delimiter(sample_line):
    for d in [",", "\t", ";", "|"]:
        if d in sample_line:
            return d
    return ","  # fallback

def read_csv_as_strings(path, max_preview=2000):
    """Read CSV into a list-of-lists of strings.
       Does not assume uniform row length; returns ragged rows trimmed/padded as needed.
    """
    with open(path, "r", errors="replace") as fh:
        lines = [ln.rstrip("\n\r") for ln in fh]
    if len(lines) == 0:
        return []
    delim = detect_delimiter(lines[0])
    rows = [line.split(delim) for line in lines]
    # trim whitespace and quotes
    rows = [[cell.strip().strip('"').strip("'") for cell in row] for row in rows]
    return rows

def transpose_pad(rows, pad_value=""):
    """Convert ragged rows to rectangular matrix by padding shorter rows with pad_value."""
    if not rows:
        return np.empty((0,0), dtype=object)
    maxc = max(len(r) for r in rows)
    mat = np.full((len(rows), maxc), pad_value, dtype=object)
    for i, r in enumerate(rows):
        for j, cell in enumerate(r):
            mat[i, j] = cell
    return mat

def is_float_string(s):
    if s is None:
        return False
    s = s.strip()
    if s == "":
        return False
    # allow scientific notation, leading +/-
    try:
        float(s)
        return True
    except:
        return False

def detect_numeric_columns(str_mat, min_numeric_fraction=0.6):
    """Return list of column indices which are sufficiently numeric."""
    if str_mat.size == 0:
        return []
    nrows, ncols = str_mat.shape
    numeric_cols = []
    for j in range(ncols):
        col = str_mat[:, j]
        numeric_count = 0
        tested = 0
        # sample up to first 500 rows to speed detection on large files
        for val in col[:min(nrows, 500)]:
            tested += 1
            if is_float_string(str(val)):
                numeric_count += 1
        frac = numeric_count / max(1, tested)
        if frac >= min_numeric_fraction:
            numeric_cols.append(j)
    return numeric_cols

def extract_numeric_array(str_mat, numeric_cols):
    """Return a float 2D numpy array with shape (nrows, len(numeric_cols)).
       Non-convertible cells are converted to np.nan.
    """
    nrows = str_mat.shape[0]
    out = np.full((nrows, len(numeric_cols)), np.nan, dtype=float)
    for idx, j in enumerate(numeric_cols):
        col = str_mat[:, j]
        for i, cell in enumerate(col):
            try:
                val = float(cell)
                out[i, idx] = val
            except:
                out[i, idx] = np.nan
    return out

def summarize_array(arr):
    """Return summary dict for 2D float array."""
    arr = np.asarray(arr, dtype=float)
    nrows, ncols = arr.shape
    total_nans = int(np.isnan(arr).sum())
    per_col = []
    for j in range(ncols):
        col = arr[:, j]
        nonan = col[~np.isnan(col)]
        if nonan.size == 0:
            per_col.append({"col": j, "count": 0, "mean": None, "std": None, "min": None, "max": None})
        else:
            per_col.append({
                "col": j,
                "count": int(nonan.size),
                "mean": float(np.mean(nonan)),
                "std": float(np.std(nonan, ddof=1)) if nonan.size > 1 else 0.0,
                "min": float(np.min(nonan)),
                "max": float(np.max(nonan))
            })
    return {"shape": (nrows, ncols), "total_nans": total_nans, "per_column": per_col}

def impute_with_col_mean(arr):
    arr = np.array(arr, dtype=float, copy=True)
    for j in range(arr.shape[1]):
        col = arr[:, j]
        if np.all(np.isnan(col)):
            arr[:, j] = 0.0
            continue
        mean = np.nanmean(col)
        col[np.isnan(col)] = mean
        arr[:, j] = col
    return arr

def normalize_zero_mean_unit_var(arr):
    arr = np.array(arr, dtype=float, copy=True)
    mean = np.mean(arr, axis=0)
    std = np.std(arr, axis=0, ddof=1)
    std_safe = np.where(std == 0, 1.0, std)
    normalized = (arr - mean) / std_safe
    return normalized, mean, std_safe

def pca_via_covariance(arr, n_components=None):
    """
    arr should be centered (or not; this function computes cov of arr).
    returns (components, eigenvalues, projected_data)
    components: columns are eigenvectors (shape = n_features x n_components)
    """
    arr = np.asarray(arr, dtype=float)
    cov = np.cov(arr, rowvar=False)
    eigvals, eigvecs = np.linalg.eigh(cov)  # symmetric
    idx = np.argsort(eigvals)[::-1]
    eigvals = eigvals[idx]
    eigvecs = eigvecs[:, idx]
    if n_components is not None:
        eigvals = eigvals[:n_components]
        eigvecs = eigvecs[:, :n_components]
    projected = np.dot(arr - np.mean(arr, axis=0), eigvecs)
    return eigvecs, eigvals, projected

def analyze_csv_file(path, outdir=None, min_numeric_fraction=0.6, save_npy=True, n_pca_components=None):
    rows = read_csv_as_strings(path)
    if len(rows) == 0:
        raise ValueError("Empty file: " + path)
    str_mat = transpose_pad(rows)
    numeric_cols = detect_numeric_columns(str_mat, min_numeric_fraction=min_numeric_fraction)
    if len(numeric_cols) == 0:
        raise ValueError("No numeric columns detected in file: " + path)
    numeric_arr = extract_numeric_array(str_mat, numeric_cols)
    summary = summarize_array(numeric_arr)
    imputed = impute_with_col_mean(numeric_arr)
    normalized, mean, std = normalize_zero_mean_unit_var(imputed)
    comps, vals, proj = pca_via_covariance(normalized, n_components=n_pca_components)

    base = os.path.splitext(os.path.basename(path))[0]
    out = {
        "summary": summary,
        "numeric_cols_indices": numeric_cols,
        "imputed": imputed,
        "normalized": normalized,
        "pca_components": comps,
        "pca_eigenvalues": vals,
        "projected": proj
    }

    if outdir and save_npy:
        os.makedirs(outdir, exist_ok=True)
        np.save(os.path.join(outdir, f"{base}__numeric_cols_indices.npy"), np.array(numeric_cols))
        np.save(os.path.join(outdir, f"{base}__imputed.npy"), imputed)
        np.save(os.path.join(outdir, f"{base}__normalized.npy"), normalized)
        np.save(os.path.join(outdir, f"{base}__pca_components.npy"), comps)
        np.save(os.path.join(outdir, f"{base}__pca_eigenvalues.npy"), vals)
        np.save(os.path.join(outdir, f"{base}__projected.npy"), proj)

    return out

def print_summary(out):
    s = out["summary"]
    print("Shape:", s["shape"])
    print("Total NaNs:", s["total_nans"])
    for c in s["per_column"]:
        print(" Col", c["col"], "count=", c["count"], "mean=", c["mean"], "std=", c["std"], "min=", c["min"], "max=", c["max"])

def main():
    import argparse
    p = argparse.ArgumentParser(description="Numpy CSV analyzer (numeric columns only).")
    p.add_argument("files", nargs="+", help="CSV file(s) to analyze")
    p.add_argument("--outdir", default="./numpy_analysis_out", help="Directory to save .npy outputs")
    p.add_argument("--min_numeric_fraction", type=float, default=0.6,
                   help="Fraction of sampled cells in a column that must parse as float to consider the column numeric.")
    p.add_argument("--no-save", dest="save", action="store_false", help="Do not save .npy outputs")
    p.add_argument("--pca-components", type=int, default=None, help="Number of PCA components to keep")
    args = p.parse_args()

    for f in args.files:
        try:
            print("\nAnalyzing:", f)
            out = analyze_csv_file(f, outdir=args.outdir, min_numeric_fraction=args.min_numeric_fraction,
                                   save_npy=args.save, n_pca_components=args.pca_components)
            print_summary(out)
            print("Detected numeric columns indices (0-based):", out["numeric_cols_indices"])
            if args.save:
                print("Saved numpy outputs to:", args.outdir)
        except Exception as e:
            print("Error analyzing", f, ":", str(e))

if _name_ == "_main_":
    main()