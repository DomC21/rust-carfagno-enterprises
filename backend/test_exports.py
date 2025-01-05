import json
import requests

def get_latest_analysis_id():
    # Use a known analysis ID from the server logs
    return '9f4e2d9d-8863-4a7e-9447-8b0a4a33ce4b'

def main():
    analysis_id = get_latest_analysis_id()
    print(f"Testing exports for analysis ID: {analysis_id}")
    
    # Test PDF export
    pdf_response = requests.get(f'http://localhost:8000/api/report/{analysis_id}?format=pdf')
    with open('test_export.pdf', 'wb') as f:
        f.write(pdf_response.content)
    print("PDF export saved to test_export.pdf")
    
    # Test CSV export
    csv_response = requests.get(f'http://localhost:8000/api/report/{analysis_id}?format=csv')
    with open('test_export.csv', 'wb') as f:
        f.write(csv_response.content)
    print("CSV export saved to test_export.csv")

if __name__ == '__main__':
    main()
