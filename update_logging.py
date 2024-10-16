import os
import re

def update_logging_level(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Use regex to replace logger.info with logger.debug
                updated_content = re.sub(r'(logger|logging)\.info\(', r'\1.debug(', content)
                
                if content != updated_content:
                    with open(file_path, 'w') as f:
                        f.write(updated_content)
                    print(f"Updated {file_path}")

if __name__ == "__main__":
    src_directory = os.path.join(os.getcwd(), 'src')
    update_logging_level(src_directory)
    print("Logging level update completed.")
