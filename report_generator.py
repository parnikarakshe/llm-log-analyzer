import json
from datetime import datetime

def generate_report(all_results, output_name):
    # Same as before — build the report dictionary
    report = {
        "analyzed_at": datetime.now().isoformat(),
        "total_issues": 0,
        "critical": [],
        "errors": [],
        "warnings": [],
        "summaries": []
    }

    for result in all_results:
        for issue in result.get("issues", []):
            report["total_issues"] += 1
            severity = issue["severity"].upper()
            if severity == "CRITICAL":
                report["critical"].append(issue)
            elif severity == "ERROR":
                report["errors"].append(issue)
            else:
                report["warnings"].append(issue)
        report["summaries"].append(result.get("summary", ""))

    # Save JSON report
    json_path = f"{output_name}.json"
    with open(json_path, 'w') as f:
        json.dump(report, f, indent=2)

    # Save HTML report
    html_path = f"{output_name}.html"
    html_content = generate_html(report)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # Print summary
    print("=" * 40)
    print("ANALYSIS COMPLETE")
    print("=" * 40)
    print(f"Total issues : {report['total_issues']}")
    print(f"Critical     : {len(report['critical'])}")
    print(f"Errors       : {len(report['errors'])}")
    print(f"Warnings     : {len(report['warnings'])}")
    print(f"JSON saved   : {json_path}")
    print(f"HTML saved   : {html_path}")
    print("=" * 40)


def generate_html(report):
    # Build issue rows for the table
    def make_rows(issues, color):
        rows = ""
        for issue in issues:
            rows += f"""
            <tr>
                <td><span class="badge" style="background:{color}">{issue['severity']}</span></td>
                <td>{issue['timestamp']}</td>
                <td><strong>{issue['bug_title']}</strong><br>
                    <small>{issue['description']}</small></td>
                <td>{issue['root_cause']}</td>
                <td>{issue['suggested_fix']}</td>
            </tr>
            """
        return rows

    critical_rows = make_rows(report['critical'], '#e74c3c')
    error_rows = make_rows(report['errors'], '#e67e22')
    warning_rows = make_rows(report['warnings'], '#f1c40f')
    all_rows = critical_rows + error_rows + warning_rows

    # Build summaries
    summary_items = ""
    for i, s in enumerate(report['summaries']):
        summary_items += f"<li><strong>Chunk {i+1}:</strong> {s}</li>"

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Log Analysis Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', sans-serif;
            background: #0f0f0f;
            color: #e0e0e0;
            padding: 30px;
        }}
        .header {{
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            border-left: 5px solid #76b900;
            padding: 25px 30px;
            border-radius: 8px;
            margin-bottom: 25px;
        }}
        .header h1 {{
            color: #76b900;
            font-size: 26px;
            letter-spacing: 1px;
        }}
        .header p {{
            color: #888;
            margin-top: 5px;
            font-size: 13px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 25px;
        }}
        .stat-card {{
            background: #1a1a2e;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
        }}
        .stat-card .number {{
            font-size: 36px;
            font-weight: bold;
        }}
        .stat-card .label {{
            font-size: 12px;
            color: #888;
            margin-top: 5px;
            text-transform: uppercase;
        }}
        .section {{
            background: #1a1a2e;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        .section h2 {{
            font-size: 16px;
            margin-bottom: 15px;
            color: #76b900;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}
        th {{
            background: #0f0f0f;
            padding: 10px;
            text-align: left;
            color: #76b900;
            font-size: 11px;
            text-transform: uppercase;
        }}
        td {{
            padding: 12px 10px;
            border-bottom: 1px solid #2a2a3e;
            vertical-align: top;
        }}
        tr:hover {{ background: #16213e; }}
        .badge {{
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: bold;
            color: white;
        }}
        small {{ color: #888; }}
        ul {{ padding-left: 20px; }}
        li {{ margin-bottom: 8px; font-size: 13px; color: #ccc; }}
    </style>
</head>
<body>

    <div class="header">
        <h1>🔍 AI Log Analysis Report</h1>
        <p>Generated at {report['analyzed_at']} &nbsp;|&nbsp; Powered by Gemini</p>
    </div>

    <div class="stats">
        <div class="stat-card">
            <div class="number" style="color:#e0e0e0">{report['total_issues']}</div>
            <div class="label">Total Issues</div>
        </div>
        <div class="stat-card">
            <div class="number" style="color:#e74c3c">{len(report['critical'])}</div>
            <div class="label">Critical</div>
        </div>
        <div class="stat-card">
            <div class="number" style="color:#e67e22">{len(report['errors'])}</div>
            <div class="label">Errors</div>
        </div>
        <div class="stat-card">
            <div class="number" style="color:#f1c40f">{len(report['warnings'])}</div>
            <div class="label">Warnings</div>
        </div>
    </div>

    <div class="section">
        <h2>All Issues</h2>
        <table>
            <thead>
                <tr>
                    <th>Severity</th>
                    <th>Timestamp</th>
                    <th>Issue</th>
                    <th>Root Cause</th>
                    <th>Suggested Fix</th>
                </tr>
            </thead>
            <tbody>
                {all_rows}
            </tbody>
        </table>
    </div>

    <div class="section">
        <h2>Chunk Summaries</h2>
        <ul>
            {summary_items}
        </ul>
    </div>

</body>
</html>
"""
    return html