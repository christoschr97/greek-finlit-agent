#!/usr/bin/env python3
"""
Model management utility for the Financial Literacy Agent.
"""

import sys
import os
import argparse

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from finlit_agent.config.settings import list_available_models, AVAILABLE_MODELS, get_model_info


def list_models():
    """List all available models."""
    list_available_models()


def show_model_info(model_id: str):
    """Show detailed information about a specific model."""
    if model_id not in AVAILABLE_MODELS:
        print(f"❌ Unknown model: {model_id}")
        print("\nAvailable models:")
        for available_model in AVAILABLE_MODELS.keys():
            print(f"  • {available_model}")
        return
    
    info = get_model_info(model_id)
    print(f"Model: {model_id}")
    print(f"Name: {info['name']}")
    print(f"Description: {info['description']}")
    print(f"Minimum RAM: {info['min_ram_gb']}GB")
    print(f"Recommended: {'Yes' if info['recommended'] else 'No'}")
    
    print(f"\nTo use this model:")
    print(f"  export OLLAMA_MODEL='{model_id}'")
    print(f"  python main.py")
    
    print(f"\nTo download this model:")
    print(f"  ollama pull {model_id}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Model management utility for Financial Literacy Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python models.py list                 # List all available models
  python models.py info gemma3:7b       # Show info about specific model
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all available models')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show information about a specific model')
    info_parser.add_argument('model', help='Model ID to show information for')
    
    args = parser.parse_args()
    
    if args.command == 'list':
        list_models()
    elif args.command == 'info':
        show_model_info(args.model)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
