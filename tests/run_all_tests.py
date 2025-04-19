#!/usr/bin/env python
"""
Comprehensive test runner for Green Academy API.
This script runs all test types from the dedicated test folder and generates coverage reports.
"""
import os
import sys
import subprocess
import time
import argparse
from datetime import datetime


def run_command(command):
    """Run a shell command and return the output."""
    print(f"Running: {' '.join(command)}")
    start_time = time.time()
    result = subprocess.run(command, capture_output=True, text=True)
    duration = time.time() - start_time
    
    print(f"Command completed in {duration:.2f} seconds")
    return result


def run_tests(test_type=None, generate_coverage=False):
    """Run the specified tests."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "green_academy.settings")
    
    # Determine which tests to run
    if test_type == 'unit':
        test_modules = ['tests.unit']
    elif test_type == 'security':
        test_modules = ['tests.security']
    elif test_type == 'integration':
        test_modules = ['tests.integration']
    elif test_type == 'performance':
        test_modules = ['tests.performance']
    else:
        # Run all tests
        test_modules = ['tests']
    
    # Build the command
    if generate_coverage:
        command = ['coverage', 'run', '--source=api,tests', 'manage.py', 'test'] + test_modules
    else:
        command = [sys.executable, 'manage.py', 'test'] + test_modules
    
    # Run the tests
    result = run_command(command)
    
    # Print the output
    print("\nTest Output:")
    print(result.stdout)
    
    if result.stderr:
        print("\nErrors:")
        print(result.stderr)
    
    # Generate coverage report if requested
    if generate_coverage and result.returncode == 0:
        print("\nGenerating coverage report...")
        
        # Generate console report
        run_command(['coverage', 'report'])
        
        # Generate HTML report
        html_result = run_command(['coverage', 'html'])
        
        if html_result.returncode == 0:
            print("\nHTML coverage report generated in 'htmlcov' directory")
            print("Open 'htmlcov/index.html' in a browser to view the report")
        
        # Generate XML report for CI tools
        xml_result = run_command(['coverage', 'xml'])
        
        if xml_result.returncode == 0:
            print("XML coverage report generated in 'coverage.xml'")
    
    return result.returncode


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Run Green Academy API tests')
    parser.add_argument('--type', choices=['unit', 'security', 'integration', 'performance', 'all'],
                        default='all', help='Type of tests to run')
    parser.add_argument('--coverage', action='store_true', help='Generate coverage report')
    parser.add_argument('--verbose', '-v', action='store_true', help='Increase verbosity')
    
    args = parser.parse_args()
    
    print(f"=== Green Academy API Test Runner ===")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Test type: {args.type}")
    print(f"Coverage report: {'Yes' if args.coverage else 'No'}")
    print(f"Verbose mode: {'Yes' if args.verbose else 'No'}")
    print("=" * 40)
    
    # Set Django test verbosity
    if args.verbose:
        os.environ['DJANGO_TEST_VERBOSITY'] = '2'
    else:
        os.environ['DJANGO_TEST_VERBOSITY'] = '1'
    
    test_type = None if args.type == 'all' else args.type
    exit_code = run_tests(test_type, args.coverage)
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
