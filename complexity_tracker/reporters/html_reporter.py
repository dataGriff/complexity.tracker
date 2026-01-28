"""HTML reporter for generating web-based reports."""
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
from complexity_tracker.reporters import BaseReporter


class HtmlReporter(BaseReporter):
    """Reporter for generating HTML reports."""
    
    def generate(self, results: List[Dict[str, Any]], summary: Dict[str, Any], output_dir: Path):
        """Generate HTML report.
        
        Args:
            results: List of repository analysis results
            summary: Summary statistics
            output_dir: Output directory for reports
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        
        html_content = self._generate_html(results, summary, output_dir)
        
        output_file = output_dir / 'complexity_report.html'
        with open(output_file, 'w') as f:
            f.write(html_content)
        
        print(f"HTML report saved to: {output_file}")
    
    def _generate_html(self, results: List[Dict[str, Any]], summary: Dict[str, Any], output_dir: Path) -> str:
        """Generate HTML content.
        
        Args:
            results: List of repository analysis results
            summary: Summary statistics
            output_dir: Output directory
            
        Returns:
            HTML content as string
        """
        # Start HTML document
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Complexity Tracker Report</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #34495e;
            margin-top: 30px;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 8px;
        }
        h3 {
            color: #7f8c8d;
            margin-top: 20px;
        }
        .summary-box {
            background-color: #ecf0f1;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .metric {
            display: inline-block;
            margin: 10px 20px 10px 0;
        }
        .metric-label {
            font-weight: bold;
            color: #7f8c8d;
        }
        .metric-value {
            font-size: 1.5em;
            color: #2c3e50;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #3498db;
            color: white;
            font-weight: bold;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .repo-section {
            margin: 30px 0;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        .chart-container {
            margin: 20px 0;
        }
        .chart-container img {
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        .complexity-high {
            color: #e74c3c;
            font-weight: bold;
        }
        .complexity-medium {
            color: #f39c12;
        }
        .complexity-low {
            color: #27ae60;
        }
        .timestamp {
            color: #95a5a6;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Complexity Tracker Report</h1>
"""
        
        html += f"        <p class=\"timestamp\">Generated: {summary.get('timestamp', datetime.now().isoformat())}</p>\n"
        
        # Summary section
        html += """
        <h2>Summary</h2>
        <div class="summary-box">
"""
        
        html += f"""
            <div class="metric">
                <div class="metric-label">Total Repositories</div>
                <div class="metric-value">{summary.get('total_repositories', 0)}</div>
            </div>
"""
        
        # Add aggregated metrics
        agg_metrics = summary.get('aggregated_metrics', {})
        
        if 'code_complexity' in agg_metrics:
            cc = agg_metrics['code_complexity']
            html += f"""
            <div class="metric">
                <div class="metric-label">Total Functions</div>
                <div class="metric-value">{cc.get('total_functions', 0):,}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Avg Complexity</div>
                <div class="metric-value">{cc.get('average_complexity', 0):.2f}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Max Complexity</div>
                <div class="metric-value">{cc.get('max_complexity', 0)}</div>
            </div>
"""
        
        if 'dependency_complexity' in agg_metrics:
            dc = agg_metrics['dependency_complexity']
            html += f"""
            <div class="metric">
                <div class="metric-label">Total Dependencies</div>
                <div class="metric-value">{dc.get('total_dependencies', 0):,}</div>
            </div>
"""
        
        if 'documentation_tokens' in agg_metrics:
            dt = agg_metrics['documentation_tokens']
            html += f"""
            <div class="metric">
                <div class="metric-label">Documentation Tokens</div>
                <div class="metric-value">{dt.get('total_tokens', 0):,}</div>
            </div>
"""
        
        html += """
        </div>
"""
        
        # Charts section
        chart_files = ['complexity_by_repo.png', 'dependencies_by_repo.png', 
                      'documentation_by_repo.png', 'complexity_distribution.png',
                      'top_complex_functions.png']
        
        html += """
        <h2>Visualizations</h2>
"""
        
        for chart_file in chart_files:
            chart_path = output_dir / chart_file
            if chart_path.exists():
                html += f"""
        <div class="chart-container">
            <img src="{chart_file}" alt="{chart_file}">
        </div>
"""
        
        # Repository details
        html += """
        <h2>Repository Details</h2>
"""
        
        for result in results:
            repo_name = result.get('repository', 'Unknown')
            html += f"""
        <div class="repo-section">
            <h3>🔍 {repo_name}</h3>
"""
            
            # Code complexity
            if 'code_complexity' in result['analyses']:
                cc = result['analyses']['code_complexity']
                if 'error' not in cc:
                    avg_complexity = cc.get('average_complexity', 0)
                    complexity_class = 'complexity-high' if avg_complexity > 10 else 'complexity-medium' if avg_complexity > 5 else 'complexity-low'
                    
                    html += f"""
            <h4>Code Complexity</h4>
            <p>
                <strong>Files:</strong> {cc.get('total_files', 0)} | 
                <strong>Functions:</strong> {cc.get('total_functions', 0)} | 
                <strong>Avg Complexity:</strong> <span class="{complexity_class}">{avg_complexity:.2f}</span> | 
                <strong>Max Complexity:</strong> {cc.get('max_complexity', 0)} | 
                <strong>Lines of Code:</strong> {cc.get('total_lines_of_code', 0):,}
            </p>
"""
                    
                    # High complexity functions
                    high_complex = cc.get('high_complexity_functions', [])
                    if high_complex:
                        html += """
            <p><strong>High Complexity Functions:</strong></p>
            <table>
                <tr>
                    <th>File</th>
                    <th>Function</th>
                    <th>Complexity</th>
                </tr>
"""
                        for func in high_complex[:5]:  # Top 5
                            html += f"""
                <tr>
                    <td>{func['file']}</td>
                    <td>{func['function']}</td>
                    <td class="complexity-high">{func['complexity']}</td>
                </tr>
"""
                        html += """
            </table>
"""
            
            # Dependency complexity
            if 'dependency_complexity' in result['analyses']:
                dc = result['analyses']['dependency_complexity']
                if 'error' not in dc:
                    html += f"""
            <h4>Dependencies</h4>
            <p>
                <strong>Total Dependencies:</strong> {dc.get('total_dependencies', 0)} | 
                <strong>Dependency Files:</strong> {dc.get('total_dependency_files', 0)}
            </p>
"""
            
            # Documentation
            if 'documentation_tokens' in result['analyses']:
                dt = result['analyses']['documentation_tokens']
                if 'error' not in dt:
                    html += f"""
            <h4>Documentation</h4>
            <p>
                <strong>Doc Files:</strong> {dt.get('total_doc_files', 0)} | 
                <strong>Tokens:</strong> {dt.get('total_tokens', 0):,} | 
                <strong>Avg Tokens/File:</strong> {dt.get('average_tokens_per_file', 0):.0f}
            </p>
"""
            
            html += """
        </div>
"""
        
        # Close HTML
        html += """
    </div>
</body>
</html>
"""
        
        return html
