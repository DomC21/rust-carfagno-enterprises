import sys
import os

def check_environment():
    print("Python Path:")
    for path in sys.path:
        print(f"- {path}")
    
    print("\nCurrent Directory Structure:")
    for root, dirs, files in os.walk('app'):
        level = root.replace('app', '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{subindent}{f}")

    print("\nChecking __init__.py files:")
    required_dirs = ['app', 'app/services']
    for dir_path in required_dirs:
        init_path = os.path.join(dir_path, '__init__.py')
        if os.path.exists(init_path):
            print(f"✓ {init_path} exists")
        else:
            print(f"✗ Missing {init_path}")
            with open(init_path, 'w') as f:
                f.write('')
            print(f"  Created {init_path}")

if __name__ == "__main__":
    check_environment()
