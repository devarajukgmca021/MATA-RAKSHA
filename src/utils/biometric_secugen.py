"""import os
import clr

DLL_DIR = os.path.join(os.path.dirname(__file__), "dll")
DLL_PATH = os.path.join(DLL_DIR, "SecuGen.FDxSDKPro.Windows.dll")

# Add DLL folder to PATH so native DLLs load correctly
os.environ["PATH"] = DLL_DIR + os.pathsep + os.environ.get("PATH", "")

# Load .NET FDx SDK DLL
try:
    clr.AddReference(DLL_PATH)
    print("[SecuGen] .NET SDK Loaded Successfully")
except Exception as e:
    raise RuntimeError(f"[SecuGen ERROR] Cannot load SDK.\n{e}")

# Import .NET classes
from SecuGen.FDxSDKPro.Windows import (
    SGFingerPrintManager,
    SGFPMDeviceName,
    SGFPMError,
    SGFPMFingerPosition,
    SGFPMSecurityLevel
)


class SecuGenScanner:
    def __init__(self):
        print("[SecuGen] Initializing reader...")
        self.fp = SGFingerPrintManager()

        # ✔ NEW ENUM NAME (v4.3.1)
        err = self.fp.Init(SGFPMDeviceName.DEV_AUTO)
        print("Init() →", err)

        if err != SGFPMError.ERROR_NONE:
            raise RuntimeError(f"Init failed → {err}")

        # Open device
        err = self.fp.OpenDevice(0)
        print("OpenDevice() →", err)

        if err != SGFPMError.NONE:
            raise RuntimeError(f"OpenDevice failed → {err}")

        # Read device info
        info = self.fp.GetDeviceInfo()
        self.width = info.ImageWidth
        self.height = info.ImageHeight

        print(f"[SecuGen] Device Ready: {self.width} x {self.height}")

    def capture_fingerprint(self):
        print("[SecuGen] Capturing image...")
        buf = bytearray(self.width * self.height)

        err = self.fp.GetImage(buf)
        print("GetImage() →", err)

        if err != SGFPMError.NONE:
            return None

        return bytes(buf)

    def create_template(self, img_bytes):
        print("[SecuGen] Creating template...")

        img = bytearray(img_bytes)
        template = bytearray(400)

        # SGFingerInfo is optional; None = auto-detect
        err = self.fp.CreateTemplate(
            None,       # ✔ NEW API FORMAT (v4.3.1)
            img,
            template
        )

        print("CreateTemplate() →", err)

        if err != SGFPMError.NONE:
            return None

        return bytes(template)

    def match_templates(self, tpl1, tpl2):
        print("[SecuGen] Matching templates...")

        matched = False
        score = 0

        # ✔ NEW API FORMAT (v4.3.1)
        err, matched, score = self.fp.MatchTemplate(
            bytearray(tpl1),
            bytearray(tpl2),
            SGFPMSecurityLevel.NORMAL
        )

        print(f"Match() → err={err}, matched={matched}, score={score}")

        return matched

import os
import clr

print(">>> LOADED biometric_secugen.py FROM:", __file__)

# ---------------------------------------------------------------
# Load SDK
# ---------------------------------------------------------------
DLL_DIR = os.path.join(os.path.dirname(__file__), "dll")
DLL_PATH = os.path.join(DLL_DIR, "SecuGen.FDxSDKPro.Windows.dll")

os.environ["PATH"] = DLL_DIR + os.pathsep + os.environ.get("PATH", "")

try:
    clr.AddReference(DLL_PATH)
    print("[SecuGen] .NET SDK Loaded Successfully")
except Exception as e:
    raise RuntimeError(f"[SecuGen ERROR] Cannot load SDK: {e}")

from SecuGen.FDxSDKPro.Windows import (
    SGFingerPrintManager,
    SGFPMDeviceName,
    SGFPMError,
    SGFPMSecurityLevel
)
import clr
import System

# Load the assembly explicitly
asm = System.Reflection.Assembly.LoadFrom(DLL_PATH)

# Get the SGFingerPrintManager type
fp_type = asm.GetType("SecuGen.FDxSDKPro.Windows.SGFingerPrintManager")

print("\n=== AVAILABLE TEMPLATE METHODS ===")
for m in fp_type.GetMethods():
    if "Template" in m.Name:
        print(m)


print("SGFPMError.ERROR_NONE =", SGFPMError.ERROR_NONE)
from SecuGen.FDxSDKPro.Windows import SGFPMFingerInfo


# ======================================================================
# WORKING SCANNER IMPLEMENTATION FOR YOUR SDK VERSION
# ======================================================================
class SecuGenScanner:

    def __init__(self):
        print("[SecuGen] Initializing reader...")
        self.fp = SGFingerPrintManager()

        # --- Init ---
        err = self.fp.Init(SGFPMDeviceName.DEV_AUTO)
        print("Init() →", err)
        if err != 0:
            raise RuntimeError(f"Init failed → {err}")

        # --- Open device ---
        err = self.fp.OpenDevice(0)
        print("OpenDevice() →", err)
        if err != 0:
            raise RuntimeError(f"OpenDevice failed → {err}")

        # --- Read device info ---
        from SecuGen.FDxSDKPro.Windows import SGFPMDeviceInfoParam
        info = SGFPMDeviceInfoParam()

        err = self.fp.GetDeviceInfo(info)
        print("GetDeviceInfo() →", err)
        if err != 0:
            raise RuntimeError(f"GetDeviceInfo failed → {err}")

        self.width = info.ImageWidth
        self.height = info.ImageHeight

        print(f"[SecuGen] Device Ready: {self.width} x {self.height}")


    # ==================================================================
    # Capture Image
    # ==================================================================
    def capture_fingerprint(self):
        print("[SecuGen] Capturing image...")

        # Create buffer
        buf = bytearray(self.width * self.height)

        # Capture fingerprint
        err = self.fp.GetImage(buf)
        print("GetImage() →", err)

        # If failure
        if err != 0:
            print("[ERROR] Unable to capture image.")
            return err, None
        print(bytes(buf), buf)
        # Success
        return 0, bytes(buf)



    # ==================================================================
    # Create Template
    # ==================================================================
    def create_template(self, img_bytes):
        print("[SecuGen] Creating template...")

        from SecuGen.FDxSDKPro.Windows import SGFPMFingerInfo, SGFPMFingerPosition

        img = bytearray(img_bytes)
        template = bytearray(400)

        # Create finger info struct
        finger_info = SGFPMFingerInfo()
        finger_info.FingerNumber = SGFPMFingerPosition.FINGPOS_UK
        finger_info.ImageQuality = 0    # let SDK calculate

        # Correct CreateTemplate signature:
        # CreateTemplate(SGFPMFingerInfo, Byte[], Byte[])
        err = self.fp.CreateTemplate(finger_info, img, template)

        print("CreateTemplate() →", err)

        if err != 0:
            print("[ERROR] Failed to create template.")
            return None

        return bytes(template)
    def create_template(self, img_bytes):
        print("[SecuGen] Creating template...")
        
        # Convert input to bytearray if it's not already
        img = bytearray(img_bytes)
        template = bytearray(400)  # Standard template size
        
        # Create a finger info object (required by some SDK versions)
        finger_info = SGFPMFingerInfo()
        from System import Int32
        finger_info.FingerNumber = Int32(0)  # Explicitly convert to Int32
        
        # Call CreateTemplate with the correct parameters
        err = self.fp.CreateTemplate(finger_info, img, template)
        print("CreateTemplate() →", err)
        
        if err != SGFPMError.ERROR_NONE:
            print(f"[ERROR] Failed to create template. Error code: {err}")
            return err, None
        
        return SGFPMError.ERROR_NONE, bytes(template)




    # ==================================================================
    # Match Templates
    # ==================================================================
    def match_templates(self, tpl1, tpl2):
        print("[SecuGen] Matching templates...")

        t1 = bytearray(tpl1)
        t2 = bytearray(tpl2)

        matched = False
        score = 0

        err, matched, score = self.fp.MatchTemplate(
            t1,
            t2,
            SGFPMSecurityLevel.NORMAL
        )

        print(f"Match() → err={err}, matched={matched}, score={score}")
        return matched"""

import os
import clr

print(">>> LOADED biometric_secugen.py FROM:", __file__)

# ---------------------------------------------------------------
# Load SDK
# ---------------------------------------------------------------
DLL_DIR = os.path.join(os.path.dirname(__file__), "dll")
DLL_PATH = os.path.join(DLL_DIR, "SecuGen.FDxSDKPro.Windows.dll")

os.environ["PATH"] = DLL_DIR + os.pathsep + os.environ.get("PATH", "")

try:
    clr.AddReference(DLL_PATH)
    print("[SecuGen] .NET SDK Loaded Successfully")
except Exception as e:
    raise RuntimeError(f"[SecuGen ERROR] Cannot load SDK: {e}")

from SecuGen.FDxSDKPro.Windows import (
    SGFingerPrintManager,
    SGFPMDeviceName,
    SGFPMError,
    SGFPMSecurityLevel,
    SGFPMFingerInfo
)
import System

from System import Array, Byte

# ======================================================================
# FINAL WORKING SCANNER CLASS
# ======================================================================
class SecuGenScanner:

    def __init__(self):
        print("[SecuGen] Initializing reader...")
        self.fp = SGFingerPrintManager()
        # ---- Init ----
        err = self.fp.Init(SGFPMDeviceName.DEV_AUTO)
        print("Init() ->", err)
        if err != 0:
            raise RuntimeError("Init failed")

        # ---- Open Device ----
        err = self.fp.OpenDevice(0)
        print("OpenDevice() ->", err)
        if err != 0:
            raise RuntimeError("OpenDevice failed")

        # ---- Get Image Size ----
        from SecuGen.FDxSDKPro.Windows import SGFPMDeviceInfoParam

        info = SGFPMDeviceInfoParam()
        err = self.fp.GetDeviceInfo(info)
        print("GetDeviceInfo() ->", err)

        self.width = info.ImageWidth
        self.height = info.ImageHeight

        print(f"[SecuGen] Device Ready: {self.width} x {self.height}")



    # ==================================================================
    # CAPTURE IMAGE
    # ==================================================================
    from System import Array, Byte


    def capture_fingerprint(self):
        print("[SecuGen] Capturing image...")

        # Must use .NET Byte array, not Python bytearray
        buf = Array.CreateInstance(Byte, self.width * self.height)

        err = self.fp.GetImage(buf)
        print("GetImage() →", err)

        if err != 0:
            return err, None

        # Convert .NET byte[] → Python bytes
        py_bytes = bytes(buf)
        return 0, py_bytes



    # ==================================================================
    # CREATE TEMPLATE
    # ==================================================================
    def create_template(self, img_bytes):
        from System import Array, Byte
        from SecuGen.FDxSDKPro.Windows import SGFPMFingerInfo, SGFPMFingerPosition

        # Convert Python bytes -> .NET Byte[]
        img = Array[Byte](img_bytes)

        # Allocate .NET Byte[] for template
        template = Array.CreateInstance(Byte, 400)

        finger_info = SGFPMFingerInfo()
        finger_info.FingerNumber = SGFPMFingerPosition.FINGPOS_UK

        # Correct create template
        err = self.fp.CreateTemplate(finger_info, img, template)
        print("CreateTemplate() ->", err)

        if err != 0:
            return err, None

        # Convert .NET Byte[] to Python bytes
        return 0, bytes(template)




    # ==================================================================
    # MATCH TEMPLATES
    # ==================================================================
    def match_templates(self, tpl1, tpl2):
        from System import Array, Byte, Boolean
        from SecuGen.FDxSDKPro.Windows import SGFPMSecurityLevel

        t1 = Array[Byte](tpl1)
        t2 = Array[Byte](tpl2)

        matched = Boolean(False)

        err = self.fp.MatchTemplate(t1, t2, SGFPMSecurityLevel.LOW, matched)
        if err[0] != 0:
            return False
        return bool(err[1])





 







