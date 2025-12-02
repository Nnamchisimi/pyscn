import sys
import os
from PyQt5 import QtWidgets, QtCore, QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
import json
import pandas as pd
import re


UPLOAD_DIRECTORY = 'uploaded_files'
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

class WebAppViewer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Code Scanner")
        self.setGeometry(100, 100, 1280, 720)

        # Set up QWebEngineView to load the local HTML file
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        self.load_html()

        self.uploaded_file_path = None  # Store the uploaded file path

    def load_html(self):
        # Load HTML file from the local file system
        html_file_path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.browser.setUrl(QtCore.QUrl.fromLocalFile(html_file_path))

    def delete_uploaded_file(self):
        if self.uploaded_file_path and os.path.exists(self.uploaded_file_path):
            os.remove(self.uploaded_file_path)
            self.uploaded_file_path = None  # Reset uploaded file path
            return {"message": "Uploaded file has been removed successfully!"}
        else:
            return {"message": "No uploaded file found to delete."}

    def save_to_excel(self, part_number, raf_number, quantity, num_pieces):
        # Use the uploaded file name to determine the path
        if self.uploaded_file_path:
            excel_file_path = os.path.join(UPLOAD_DIRECTORY, f"{os.path.splitext(os.path.basename(self.uploaded_file_path))[0]}.xlsx")

            # Read the existing Excel file or create a new DataFrame if it doesn't exist
            if os.path.exists(excel_file_path):
                df = pd.read_excel(excel_file_path)
            else:
                df = pd.DataFrame(columns=["Part number", "Raf Number", "Package Quantity", "No of pieces"])

            # Check if the entry already exists
            existing_row = df[(df['Part number'] == part_number) & (df['Raf Number'] == raf_number)]

            if not existing_row.empty:
                # If exists, increment the values
                index = existing_row.index[0]
                df.at[index, "Package Quantity"] += quantity  # Increment Package Quantity
                df.at[index, "No of pieces"] += num_pieces  # Increment No of pieces
            else:
                # If not, create a new row
                new_row = pd.DataFrame({
                    "Part number": [part_number],
                    "Raf Number": [raf_number],
                    "Package Quantity": [quantity],
                    "No of pieces": [num_pieces]
                })
                df = pd.concat([df, new_row], ignore_index=True)

            # Save the updated DataFrame to Excel
            df.to_excel(excel_file_path, index=False)
            return {"message": "Details have been input successfully!"}
        else:
            return {"message": "No uploaded file found to save data."}

    def handle_form_submission(self, data):
        qr_code = data.get('qr_code')
        part_number = data.get('part_number')
        raf_number = data.get('raf_number')
        num_pieces = data.get('num_pieces', 1)

        # Handle QR code input
        if qr_code.isdigit():
            extracted_value = int(qr_code)  # Use the number directly as quantity
        else:
            cleaned_qr_code = qr_code.replace("<GS>", " ").replace("\r", "").replace("\n", "")
            extracted_value = self.extract_value(cleaned_qr_code)  # Extract if it's a valid QR code

        if extracted_value != "Not Found":
            if part_number and raf_number:
                return self.save_to_excel(part_number, raf_number, extracted_value, num_pieces)
            else:
                return {"message": "Part number and RAF number are required."}
        else:
            return {"message": "QR code value not found."}

    def extract_value(self, qr_code):
        """Extract the value after 'Q' from the QR code string."""
        match = re.search(r'Q(\d+)', qr_code)
        if match:
            return int(match.group(1))  # Return as an integer
        return "Not Found"

    def handle_request(self, request):
        # Parse the request data
        data = {key: value for key, value in request.form.items()}

        if request.method == 'POST':
            if 'delete' in data:
                return self.delete_uploaded_file()
            else:
                return self.handle_form_submission(data)

# Main app execution
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = WebAppViewer()
    window.show()
    sys.exit(app.exec_())
