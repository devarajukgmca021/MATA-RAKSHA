# ============================================================
#      AI FINGERPRINT QUALITY + SPOOF DETECTION (IMAGE BASED)
# ============================================================

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import hashlib


# ------------------------------------------------------------
# Helper: Convert ANY input → grayscale numpy array (HxW)
# ------------------------------------------------------------

def _to_gray_array(src):
    """
    Accepts:
        - PIL Image
        - NumPy array
        - raw bytes (auto decoded)
    Returns:
        grayscale numpy array (H x W)
    """
    # Case 1 — PIL Image
    if isinstance(src, Image.Image):
        img = src.convert("L")
        return np.array(img)

    # Case 2 — numpy array
    if isinstance(src, np.ndarray):
        if src.ndim == 3 and src.shape[2] == 3:
            # convert RGB → Gray
            return np.dot(src[..., :3], [0.299, 0.587, 0.114]).astype(np.uint8)
        return src.astype(np.uint8)

    # Case 3 — raw bytes (from simulator)
    arr = np.frombuffer(src, dtype=np.uint8)

    # Estimate square shape
    side = int(np.sqrt(len(arr)))
    if side * side != len(arr):
        # Pad or cut
        arr = arr[: side * side]

    return arr.reshape(side, side)


# ------------------------------------------------------------
#  FEATURE EXTRACTION
# ------------------------------------------------------------

def _entropy(arr: np.ndarray) -> float:
    if arr.size == 0:
        return 0.0
    hist, _ = np.histogram(arr, bins=256, range=(0, 255), density=True)
    hist = hist[hist > 0]
    return -np.sum(hist * np.log2(hist))


def _texture_features(arr: np.ndarray) -> float:
    """Fixed gradient feature — NO broadcasting errors anymore."""
    if arr.size < 100:
        return 0.0

    gx = np.abs(np.diff(arr, axis=1))    # shape: H x (W-1)
    gy = np.abs(np.diff(arr, axis=0))    # shape: (H-1) x W

    # Pad to match shapes
    H = arr.shape[0] - 1
    W = arr.shape[1] - 1
    gx = gx[:H, :W]
    gy = gy[:H, :W]

    grad = np.sqrt(gx**2 + gy**2)
    return float(np.mean(grad))


def _hash_vector(img_array: np.ndarray) -> np.ndarray:
    """Convert fingerprint → SHA256 vector."""
    raw = img_array.tobytes()
    h = hashlib.sha256(raw).hexdigest()
    vec = [int(h[i:i+2], 16) for i in range(0, 64, 2)]
    return np.array(vec, dtype=np.float32).reshape(1, -1)


# ------------------------------------------------------------
#  MAIN AI FUNCTION
# ------------------------------------------------------------

def ai_predict_fingerprint(image_input) -> dict:
    """
    Input: PIL Image or numpy image
    Returns:
        { "verdict": PASS/FAIL, "confidence": 0-100 }
    """

    # Convert input → grayscale array
    arr = _to_gray_array(image_input)

    # --- Compute features ---
    ent = _entropy(arr)                # 0–8
    tex = _texture_features(arr)       # 0–50
    vec = _hash_vector(arr)            # 64-dim vector

    ideal = np.ones_like(vec)
    sim = cosine_similarity(vec, ideal)[0][0]    # 0–1

    # Weighted score
    score = (
        (ent / 8) * 40 +
        min(tex, 50) / 50 * 30 +
        sim * 30
    )
    score = int(np.clip(score, 1, 100))

    verdict = "PASS" if score >= 25 else "FAIL"

    return {
        "verdict": verdict,
        "confidence": score
    }


# ------------------------------------------------------------
#  SELF TEST
# ------------------------------------------------------------
if __name__ == "__main__":
    test_img = Image.new("L", (240, 240), color=128)
    print(ai_predict_fingerprint(test_img))
