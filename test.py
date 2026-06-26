"""
SecuGen Fingerprint Capture Diagnostic Test
-------------------------------------------
This script is intended for SecuGen Customer Care.

It demonstrates that:
1. The .NET SDK loads correctly.
2. The device initializes successfully.
3. GetImage() returns SGFDX_ERROR_NONE (0).
4. BUT the image buffer returned by GetImage() is entirely zero,
   meaning no real fingerprint data is being sent by the driver layer.

This helps confirm whether the root cause is:
- A missing native driver (sgfplib.dll / sgdxdrv.dll)
- A USB interface issue
- A 32-bit / 64-bit mismatch
- A malfunction in the native capture layer


from src.utils.biometric_secugen import SecuGenScanner

print("\n=== SecuGen Fingerprint Capture Diagnostic ===\n")

# Initialize the device
scanner = SecuGenScanner()

input("\nPlace your finger firmly on the scanner, THEN press ENTER...")

# Create capture buffer
raw = bytearray(scanner.width * scanner.height)

print("\nCapturing image...")
err = scanner.fp.GetImage(raw)
print("GetImage() returned →", err)

if err != 0:
    print("[ERROR] GetImage() failed. This is an SDK/device error.")
    exit()

# Check if the buffer contains real image data
nonzero_pixels = sum(1 for b in raw if b != 0)

print(f"Image size          : {len(raw)} bytes")
print(f"Non-zero pixels     : {nonzero_pixels}")

if nonzero_pixels == 0:
    print("\n[CRITICAL] Image buffer is COMPLETELY BLACK.")
    print("[Meaning] The device initializes but NO image data is delivered.")
    print("[Possible Causes]")
    print(" - Native drivers (sgfplib.dll / sgdxdrv.dll) missing or not loaded")
    print(" - USB interface active for GUI tool but NOT for SDK")
    print(" - Python running in wrong architecture (32-bit vs 64-bit)")
    print(" - Missing SecuGen WBF drivers")
    print(" - Device not bound to FDxSDKPro capture layer\n")
else:
    print("\n[OK] Device is sending valid pixel data.")

# Check image quality using SDK
q = 0
err, q = scanner.fp.GetImageQuality(scanner.width, scanner.height, raw, 0)
print("Image Quality →", q)

if q == 0:
    print("\n[NOTE] SDK reports image quality 0 because captured buffer is black.\n")

print("\n=== Diagnostic Complete ===\n")

from src.utils.biometric_secugen import SecuGenScanner

print("\n=== SecuGen Test ===\n")

scanner = SecuGenScanner()

input("Place finger and press ENTER...")

img = scanner.capture_image()
if img is None:
    print("[ERROR] Failed to capture image")
    exit()

print(f"Captured {len(img)} bytes")

# Compute quality
q = 0
err, q = scanner.fp.GetImageQuality(scanner.width, scanner.height, img, 0)
print("Image Quality =", q)

tpl = scanner.create_template(img)
if tpl is None:
    print("[ERROR] Template failed")
else:
    print("[SUCCESS] Template size =", len(tpl))"""

from src.utils.biometric_secugen import SecuGenScanner

print("=== SecuGen Python Test ===")

scanner = SecuGenScanner()

input("Place finger on sensor & press ENTER...")

err, img = scanner.capture_fingerprint()
if err != 0:
    print("Capture failed")
    exit()
else:("capture succes")
err, tpl = scanner.create_template(img)
if err == 0:
    print("[OK] Template created successfully")
else:
    print("[ERROR] Template creation failed, code =", err)


print("Place finger for TEMPLATE 1 and press ENTER...")
input()

err, img1 = scanner.capture_fingerprint()
if err != 0:
    print("[ERROR] Failed to capture first fingerprint.")
    exit()

err, tpl1 = scanner.create_template(img1)
if err != 0:
    print("[ERROR] Failed to create first template.")
    exit()

print("[OK] Template 1 created.")
print("----------------------------------------")

print("Place same finger OR different finger for TEMPLATE 2 and press ENTER...")
input()

err, img2 = scanner.capture_fingerprint()
if err != 0:
    print("[ERROR] Failed to capture second fingerprint.")
    exit()

err, tpl2 = scanner.create_template(img2)
if err != 0:
    print("[ERROR] Failed to create second template.")
    exit()

print("[OK] Template 2 created.")
print("----------------------------------------")

print("Matching templates...")
matched = scanner.match_templates(tpl1, tpl2)

if matched:
    print("MATCH SUCCESS! Both templates belong to the same finger.")
else:
    print("MATCH FAILED! Fingerprints do not match.")










