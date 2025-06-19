"""
Command-line interface for PROJECT SOVEREIGN.

Provides interactive execution, file processing, and debugging
capabilities for the assembly language.
"""

import sys
from pathlib import Path

import click
from rich.console import Console
from rich.prompt import Prompt
from rich.syntax import Syntax
from rich.table import Table

from ..core.interpreter import SovereignInterpreter
from ..core.parser import ParseError, SovereignParser
from ..vm.virtual_machine import SovereignVM

console = Console()


@click.group()
@click.version_option()
def cli():
    """PROJECT SOVEREIGN - Assembly-Like Agentic Programming Language"""
    pass


@cli.command()
@click.argument("source_file", type=click.Path(exists=True, path_type=Path))
@click.option("--debug", "-d", is_flag=True, help="Enable debug mode")
@click.option("--evolution", "-e", is_flag=True, help="Enable error-driven evolution")
def run(source_file: Path, debug: bool, evolution: bool):
    """Execute a PROJECT SOVEREIGN program."""
    try:
        # Read source file
        source_code = source_file.read_text()

        # Display source if debug mode
        if debug:
            syntax = Syntax(source_code, "assembly", theme="monokai", line_numbers=True)
            console.print("\n[bold blue]Source Code:[/bold blue]")
            console.print(syntax)
            console.print()

        # Create interpreter
        interpreter = SovereignInterpreter()

        if evolution:
            console.print(
                "[yellow]Warning: Evolution mode not yet implemented[/yellow]"
            )

        # Execute program
        console.print("[bold green]Executing program...[/bold green]")
        interpreter.run(source_code)

        # Display results
        if debug:
            display_vm_state(interpreter.vm)

        console.print("[bold green]Execution completed successfully[/bold green]")

    except ParseError as e:
        console.print(f"[bold red]Parse Error:[/bold red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Runtime Error:[/bold red] {e}")
        if evolution:
            console.print(
                "[yellow]Evolution would trigger here (not yet implemented)[/yellow]"
            )
        sys.exit(1)


@cli.command()
def repl():
    """Start interactive REPL mode."""
    console.print("[bold blue]PROJECT SOVEREIGN Interactive REPL[/bold blue]")
    console.print("Enter instructions or 'help' for commands, 'exit' to quit\n")

    interpreter = SovereignInterpreter()

    while True:
        try:
            # Get input
            line = Prompt.ask("[bold green]sovereign>[/bold green]").strip()

            if line.lower() in ("exit", "quit"):
                break
            if line.lower() == "help":
                show_repl_help()
            elif line.lower() == "state":
                display_vm_state(interpreter.vm)
            elif line.lower() == "reset":
                interpreter.reset()
                console.print("[yellow]VM state reset[/yellow]")
            elif line:
                # Execute instruction
                interpreter.execute_single(line)

        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")

    console.print("\n[blue]Goodbye![/blue]")


@cli.command()
@click.argument("source_file", type=click.Path(exists=True, path_type=Path))
def validate(source_file: Path):
    """Validate syntax of a PROJECT SOVEREIGN program."""
    try:
        source_code = source_file.read_text()
        parser = SovereignParser()

        if parser.validate_syntax(source_code):
            console.print(f"[green]✓[/green] {source_file} - Syntax valid")
        else:
            console.print(f"[red]✗[/red] {source_file} - Syntax invalid")
            sys.exit(1)

    except Exception as e:
        console.print(f"[red]Error validating {source_file}:[/red] {e}")
        sys.exit(1)


@cli.command()
def opcodes():
    """List all available op-codes."""
    from ..core.opcodes import OpCodeCategory, OpCodeRegistry

    registry = OpCodeRegistry()

    for category in OpCodeCategory:
        table = Table(title=f"{category.value.title()} Operations")
        table.add_column("Op-Code", style="cyan")
        table.add_column("Description", style="white")

        opcodes = registry.list_opcodes(category)
        for opcode in opcodes:
            table.add_row(opcode.name, opcode.description)

        console.print(table)
        console.print()


def display_vm_state(vm: SovereignVM):
    """Display current VM state."""
    state = vm.dump_state()

    table = Table(title="VM State")
    table.add_column("Component", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("Data Stack", str(state["data_stack"]))
    table.add_row("Control Stack", str(state["control_stack"]))
    table.add_row("Program Counter", str(state["program_counter"]))
    table.add_row("Running", str(state["running"]))
    table.add_row("Memory Items", str(len(state["memory"])))

    if state["error_state"]:
        table.add_row("Error", f"[red]{state['error_state']}[/red]")

    console.print(table)


def show_repl_help():
    """Show REPL help information."""
    help_text = """
[bold blue]REPL Commands:[/bold blue]
  help    - Show this help
  state   - Display VM state
  reset   - Reset VM state
  exit    - Exit REPL

[bold blue]Instructions:[/bold blue]
  Enter any PROJECT SOVEREIGN instruction to execute immediately
  Examples: PUSH #42, ADD, POP, HALT

[bold blue]Op-codes:[/bold blue]
  Run 'sovereign opcodes' for complete list
"""
    console.print(help_text)


def main():
    """Main entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
