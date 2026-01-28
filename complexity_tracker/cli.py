"""Command-line interface for complexity tracker."""
import argparse
import sys
from pathlib import Path

from complexity_tracker.config import Config
from complexity_tracker.tracker import ComplexityTracker
from complexity_tracker.reporters.json_reporter import JsonReporter
from complexity_tracker.reporters.html_reporter import HtmlReporter
from complexity_tracker.reporters.chart_generator import ChartGenerator


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Complexity Tracker - Analyze code complexity across repositories',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with a configuration file
  complexity-tracker --config config.yaml

  # Run with specific repositories
  complexity-tracker --repos owner/repo1 owner/repo2

  # Run for an entire organization
  complexity-tracker --organization myorg --max-repos 10

  # Run with custom output directory
  complexity-tracker --config config.yaml --output my_reports
        """
    )
    
    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration file (YAML or JSON)'
    )
    
    parser.add_argument(
        '--repos',
        nargs='+',
        help='List of repositories to analyze (format: owner/repo)'
    )
    
    parser.add_argument(
        '--organization',
        type=str,
        help='GitHub organization to analyze all repositories from'
    )
    
    parser.add_argument(
        '--max-repos',
        type=int,
        help='Maximum number of repositories to analyze (when using --organization)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='complexity_reports',
        help='Output directory for reports (default: complexity_reports)'
    )
    
    parser.add_argument(
        '--no-charts',
        action='store_true',
        help='Disable chart generation'
    )
    
    parser.add_argument(
        '--format',
        choices=['html', 'json', 'both'],
        default='both',
        help='Report format (default: both)'
    )
    
    parser.add_argument(
        '--github-token',
        type=str,
        help='GitHub personal access token for API access'
    )
    
    args = parser.parse_args()
    
    # Load or create configuration
    if args.config:
        try:
            config = Config(args.config)
            print(f"Loaded configuration from: {args.config}")
        except Exception as e:
            print(f"Error loading configuration: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        config = Config()
        print("Using default configuration")
    
    # Override configuration with command-line arguments
    if args.repos:
        config.set('repositories.type', 'list')
        config.set('repositories.repos', args.repos)
    
    if args.organization:
        config.set('repositories.type', 'organization')
        config.set('repositories.organization', args.organization)
        if args.max_repos:
            config.set('repositories.max_repos', args.max_repos)
    
    if args.github_token:
        config.set('github.token', args.github_token)
    
    config.set('output.directory', args.output)
    config.set('output.charts', not args.no_charts)
    
    # Validate configuration
    if config.get('repositories.type') == 'list' and not config.get('repositories.repos'):
        print("Error: No repositories specified. Use --config, --repos, or --organization", file=sys.stderr)
        parser.print_help()
        sys.exit(1)
    
    # Run complexity tracker
    try:
        tracker = ComplexityTracker(config)
        results, summary = tracker.run()
        
        # Generate reports
        output_dir = Path(config.get('output.directory'))
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print("\n" + "=" * 60)
        print("Generating Reports")
        print("=" * 60)
        
        # Generate JSON report
        if args.format in ['json', 'both']:
            json_reporter = JsonReporter()
            json_reporter.generate(results, summary, output_dir)
        
        # Generate charts
        if config.get('output.charts'):
            chart_gen = ChartGenerator(output_dir)
            chart_gen.generate_all_charts(results)
        
        # Generate HTML report
        if args.format in ['html', 'both']:
            html_reporter = HtmlReporter()
            html_reporter.generate(results, summary, output_dir)
        
        print("\n" + "=" * 60)
        print("✅ Complexity Tracking Complete!")
        print("=" * 60)
        print(f"Reports saved to: {output_dir.absolute()}")
        
        return 0
    
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
