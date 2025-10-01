#!/usr/bin/env python3
"""
Install Python dependencies for the Python scripts (English version)
"""
import subprocess
import sys

def install_package(package, mirror_url=None):
    """Install a Python package via pip"""
    cmd = [sys.executable, "-m", "pip", "install", package]
    if mirror_url:
        cmd.extend(["-i", mirror_url])
    
    try:
        print(f"📦 Installing {package}...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {package} installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    print("🐱 Bongo Cat Monitor - Dependency Installer")
    print("=" * 50)
    # Optional: Use a mirror to speed up downloads
    mirror_url = "https://pypi.tuna.tsinghua.edu.cn/simple"
    
    # Packages to install
    packages = [
        "pyserial",      # Serial communication
        "psutil",        # System monitoring
    ]
    
    print("📋 Installing required packages:")
    print(f"   Mirror: {mirror_url}")
    print()
    
    success_count = 0
    for package in packages:
        if install_package(package, mirror_url):
            success_count += 1
        print()
    
    print("=" * 50)
    if success_count == len(packages):
        print("✅ All packages installed successfully!")
        print("\n💡 You can now run:")
        print("   python3 find_ports.py      # List ports")
        print("   python3 direct_test.py     # Test ESP32")
    else:
        print(f"⚠️  {success_count}/{len(packages)} packages installed successfully")
        print("💡 Some packages failed to install. Please check the errors above.")
    
    print("\n🔧 If you encounter permission issues:")
    print("   pip3 install --user pyserial psutil")

if __name__ == "__main__":
    main()
