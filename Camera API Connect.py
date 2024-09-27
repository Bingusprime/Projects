Python
from cffi import FFI

ffi = FFI()

# Define the C function signatures you need
ffi.cdef("""
    int EdsInitializeSDK();
    // Add other function signatures as needed
""")

# Load the library
edsdk_lib = ffi.dlopen("C:\Users\mattb\AppData\Local\Temp\8087785f-da7f-413d-abf9-7b6e048f8823_EDSDK-2.9.zip.823\EDSDK 2.9 Windows\EDSDK\Library\EDSDK.lib")

# Call the function
result = edsdk_lib.EdsInitializeSDK()

if result != 0:
    print("Error initializing EDSDK")

# ... other EDSDK function calls

