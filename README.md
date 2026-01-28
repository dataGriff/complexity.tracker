# Complexity Tracker

A comprehensive tool for analyzing and tracking code complexity across multiple repositories. The Complexity Tracker helps identify where complexity is highest in your codebase by analyzing:

- **Code Complexity**: Cyclomatic complexity and other code metrics (language-agnostic)
- **Dependency Complexity**: Number and distribution of dependencies across different package managers
- **Documentation Tokens**: Amount of documentation in repositories

## Features

- 🔍 **Multi-Repository Analysis**: Analyze specific repositories, entire organizations, or custom lists
- 🌐 **Language Agnostic**: Works with any programming language
- 📊 **Visual Reports**: Generate beautiful HTML reports with charts and graphs
- 📈 **Multiple Metrics**: Track code complexity, dependencies, and documentation
- 🎯 **Identify Hotspots**: Quickly find the most complex areas of your codebase
- 💾 **Export Data**: JSON export for further analysis and integration

## Installation

```bash
# Clone the repository
git clone https://github.com/dataGriff/complexity.tracker.git
cd complexity.tracker

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Quick Start

### Using Command Line Arguments

```bash
# Analyze specific repositories
complexity-tracker --repos owner/repo1 owner/repo2

# Analyze an entire organization
complexity-tracker --organization myorg --max-repos 10

# Analyze with a GitHub token (for private repos and higher rate limits)
complexity-tracker --organization myorg --github-token YOUR_TOKEN
```

### Using Configuration File

1. Create a configuration file (see `config.example.yaml`):

```yaml
repositories:
  type: list
  repos:
    - owner/repo1
    - owner/repo2

analysis:
  code_complexity: true
  dependency_complexity: true
  documentation_tokens: true

output:
  directory: complexity_reports
  format:
    - html
    - json
  charts: true
```

2. Run the tracker:

```bash
complexity-tracker --config config.yaml
```

## Configuration Options

### Repository Sources

**Specific Repositories:**
```yaml
repositories:
  type: list
  repos:
    - octocat/Hello-World
    - github/gitignore
```

**Organization:**
```yaml
repositories:
  type: organization
  organization: myorg
  max_repos: 20  # Optional limit
```

### Analysis Options

```yaml
analysis:
  code_complexity: true        # Cyclomatic complexity analysis
  dependency_complexity: true   # Dependency counting
  documentation_tokens: true    # Documentation analysis
  
  exclude_patterns:
    - "*/test/*"
    - "*/node_modules/*"
```

### Output Options

```yaml
output:
  directory: complexity_reports
  format:
    - html  # Interactive HTML report
    - json  # Raw data export
  charts: true  # Generate visualizations
```

## Understanding the Metrics

### Code Complexity
- **Cyclomatic Complexity**: Measures the number of independent paths through code
- **High Complexity Functions**: Functions with complexity > 10 are flagged
- **Average Complexity**: Mean complexity across all functions
- Works with: Python, JavaScript, Java, C++, Go, Ruby, PHP, and more

### Dependency Complexity
- Counts dependencies from various package managers:
  - npm (package.json)
  - pip (requirements.txt, Pipfile)
  - Maven (pom.xml)
  - Gradle (build.gradle)
  - Cargo (Cargo.toml)
  - Go modules (go.mod)
  - And many more...

### Documentation Tokens
- Counts words/tokens in documentation files
- Includes: README, markdown files, docs directories
- Helps assess documentation coverage

## Generated Reports

The tool generates comprehensive reports including:

1. **HTML Report** (`complexity_report.html`):
   - Summary dashboard with key metrics
   - Visual charts and graphs
   - Detailed per-repository breakdown
   - List of high-complexity functions

2. **Charts**:
   - Complexity by repository
   - Dependencies by repository
   - Documentation tokens by repository
   - Complexity distribution histogram
   - Top complex functions

3. **JSON Data** (`complexity_results.json`, `complexity_summary.json`):
   - Raw data for custom analysis
   - Integration with other tools

## Example Output

After running the tracker, you'll see:

```
============================================================
Complexity Tracker
============================================================
Cloning/updating repositories...
Cloning repository: Hello-World
Cloning repository: gitignore

Analyzing repositories...

Analyzing: Hello-World
  Running code_complexity analyzer...
  Running dependency_complexity analyzer...
  Running documentation_tokens analyzer...

============================================================
Analysis Complete
============================================================
Total repositories analyzed: 2

============================================================
Generating Reports
============================================================
Detailed results saved to: complexity_reports/complexity_results.json
Summary saved to: complexity_reports/complexity_summary.json

Generating charts...
Chart saved: complexity_reports/complexity_by_repo.png
Chart saved: complexity_reports/dependencies_by_repo.png
...

HTML report saved to: complexity_reports/complexity_report.html

============================================================
✅ Complexity Tracking Complete!
============================================================
Reports saved to: /path/to/complexity_reports
```

## CLI Reference

```bash
usage: complexity-tracker [-h] [--config CONFIG] [--repos REPOS [REPOS ...]]
                          [--organization ORGANIZATION] [--max-repos MAX_REPOS]
                          [--output OUTPUT] [--no-charts]
                          [--format {html,json,both}] [--github-token GITHUB_TOKEN]

Options:
  --config CONFIG               Path to configuration file (YAML or JSON)
  --repos REPOS [REPOS ...]    List of repositories to analyze
  --organization ORGANIZATION   GitHub organization to analyze
  --max-repos MAX_REPOS        Maximum number of repositories to analyze
  --output OUTPUT              Output directory (default: complexity_reports)
  --no-charts                  Disable chart generation
  --format {html,json,both}    Report format (default: both)
  --github-token GITHUB_TOKEN  GitHub personal access token
```

## Use Cases

- **Technical Debt Assessment**: Identify areas with highest complexity for refactoring
- **Team Metrics**: Track complexity across organization repositories
- **Code Quality Monitoring**: Regular tracking of complexity trends
- **Dependency Management**: Identify repositories with excessive dependencies
- **Documentation Coverage**: Assess documentation across projects

## Requirements

- Python 3.8+
- Git
- Internet connection (for cloning repositories)
- Optional: GitHub Personal Access Token (for private repos and higher API limits)

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.