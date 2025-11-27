from cli_interface import CLIInterface

def main():
    """CLI Application Entry Point"""
    try:
        cli = CLIInterface()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Application interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")

if __name__ == "__main__":
    main()