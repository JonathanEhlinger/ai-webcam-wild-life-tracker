import cv2
import platform

def list_cameras(max_test=10):
    print("Testing camera indices 0 to", max_test-1)
    for i in range(max_test):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            print(f"Camera index {i}: AVAILABLE")
            cap.release()
        else:
            print(f"Camera index {i}: not available")

    if platform.system() == "Windows":
        print("\nAttempting to list USB camera device names (Windows only):")
        try:
            import subprocess
            result = subprocess.run(
                [
                    "powershell",
                    "-Command",
                    "Get-CimInstance Win32_PnPEntity | Where-Object {$_.Service -eq 'usbvideo'} | Select-Object -ExpandProperty Name"
                ],
                capture_output=True, text=True, timeout=5
            )
            print(result.stdout)
        except Exception as e:
            print("Could not get device names:", e)

if __name__ == "__main__":
    list_cameras()
