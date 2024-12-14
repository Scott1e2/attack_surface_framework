import pandas as pd
import json
import os
import requests
from fpdf import FPDF


def save_to_csv(data, filename="report.csv"):
    """
    Saves data to a CSV file.
    """
    try:
        df = pd.DataFrame(data)
        output_dir = "reports/output/"
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)
        df.to_csv(file_path, index=False)
        print(f"CSV report saved to {file_path}")
    except Exception as e:
        print(f"Error saving CSV report: {e}")


def save_to_json(data, filename="report.json"):
    """
    Saves data to a JSON file.
    """
    try:
        output_dir = "reports/output/"
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"JSON report saved to {file_path}")
    except Exception as e:
        print(f"Error saving JSON report: {e}")


def send_to_splunk(data, splunk_url, splunk_token):
    """
    Sends data to Splunk using HTTP Event Collector (HEC).
    """
    try:
        headers = {"Authorization": f"Splunk {splunk_token}"}
        response = requests.post(splunk_url, headers=headers, json={"event": data})
        if response.status_code == 200:
            print("Data successfully sent to Splunk.")
        else:
            print(f"Failed to send data to Splunk. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending data to Splunk: {e}")


def send_to_elasticsearch(data, elastic_url, index_name):
    """
    Sends data to Elasticsearch.
    """
    try:
        headers = {"Content-Type": "application/json"}
        response = requests.post(f"{elastic_url}/{index_name}/_doc", headers=headers, json=data)
        if response.status_code in (200, 201):
            print("Data successfully sent to Elasticsearch.")
        else:
            print(f"Failed to send data to Elasticsearch. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending data to Elasticsearch: {e}")


def generate_pdf_report(data, filename="report.pdf"):
    """
    Generates a PDF report from the given data.
    """
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Attack Surface Report", ln=True, align="C")
        pdf.ln(10)

        for item in data:
            pdf.multi_cell(0, 10, txt=json.dumps(item, indent=4))
            pdf.ln(5)

        output_dir = "reports/output/"
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)
        pdf.output(file_path)
        print(f"PDF report saved to {file_path}")
    except Exception as e:
        print(f"Error generating PDF report: {e}")


def summarize_results(results):
    """
    Generates a summary of plug-in execution results.
    """
    summary = []
    for result in results:
        summary.append({
            "Plugin": result.get("plugin"),
            "Issues Found": len(result.get("result", [])),
        })
    return summary
