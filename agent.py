import sys
import os
import warnings

# Ensure UTF-8 encoding on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Suppress library deprecation warnings for clean terminal display
warnings.filterwarnings("ignore")
warnings.simplefilter("ignore")
from pathlib import Path
import httpx
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.prompt import Prompt
from rich.text import Text

from config import config
from services.fetcher import fetcher
from services.embedder import embedder
from services.qa_engine import qa_engine

console = Console()

def check_ollama():
    """Verify Ollama server is reachable and inspect available models."""
    try:
        resp = httpx.get(f"{config.OLLAMA_BASE_URL}/api/tags", timeout=3.0)
        if resp.status_code == 200:
            models = [m.get("name") for m in resp.json().get("models", [])]
            return True, models
    except Exception:
        pass
    return False, []

def print_banner():
    """Display welcome banner with current system state."""
    banner_text = (
        "[bold cyan]Wikipedia Chatbot Terminal Agent[/bold cyan]\n"
        "[dim]Local Retrieval-Augmented Generation powered by Ollama, ChromaDB, & Wikipedia[/dim]\n\n"
        f"• LLM Model: [bold green]{config.LLM_MODEL}[/bold green]\n"
        f"• Embeddings: [bold green]{config.EMBED_MODEL}[/bold green]\n"
        "• Type your question or use [bold yellow]/help[/bold yellow] for commands. Type [bold red]exit[/bold red] to quit."
    )
    console.print(Panel(banner_text, border_style="cyan", title=" WikiAgent CLI "))

def show_help():
    """Display interactive commands."""
    table = Table(title="Available Commands", border_style="dim")
    table.add_column("Command", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")
    table.add_row("/topics", "List all currently indexed Wikipedia articles")
    table.add_row("/add <topic>", "Fetch and index a Wikipedia article (e.g. /add Machine learning)")
    table.add_row("/search <query>", "Search Wikipedia for article titles")
    table.add_row("/build", "Index all default Wikipedia topics")
    table.add_row("/stats", "Show database statistics and model info")
    table.add_row("/clear", "Clear the terminal screen")
    table.add_row("/help", "Show this help table")
    table.add_row("exit / quit", "Exit the chatbot agent")
    console.print(table)

def show_stats():
    """Display vector database and Ollama stats."""
    stats = embedder.get_stats()
    ollama_ok, models = check_ollama()

    table = Table(title="System Status", border_style="dim")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green" if ollama_ok else "red")

    table.add_row("Ollama Server", "Connected" if ollama_ok else "Disconnected (check 'ollama serve')")
    table.add_row("Configured LLM", config.LLM_MODEL)
    table.add_row("Configured Embedder", config.EMBED_MODEL)
    table.add_row("Available Models", ", ".join(models) if models else "None")
    table.add_row("Total Chunks in DB", str(stats.get("total_chunks", 0)))
    table.add_row("Indexed Topics Count", str(stats.get("topics_count", 0)))
    console.print(table)

def show_topics():
    """List all indexed Wikipedia topics."""
    stats = embedder.get_stats()
    topics = stats.get("topics", [])
    if not topics:
        console.print("[yellow]No topics are currently indexed in the vector database.[/yellow]")
        console.print("Use [bold cyan]/add <topic>[/] to add an article or [bold cyan]/build[/] to index default topics.\n")
        return

    table = Table(title=f"Indexed Wikipedia Topics ({len(topics)} total)", border_style="dim")
    table.add_column("#", style="dim", width=4)
    table.add_column("Topic Title", style="cyan")
    for idx, topic in enumerate(sorted(topics), 1):
        table.add_row(str(idx), topic)
    console.print(table)
    console.print(f"[dim]Total indexed chunks: {stats.get('total_chunks', 0)}[/dim]\n")

def search_wikipedia(query: str):
    """Search for topic titles on Wikipedia."""
    if not query.strip():
        console.print("[yellow]Please specify a query: /search <topic>[/yellow]")
        return

    with console.status(f"[cyan]Searching Wikipedia for '{query}'...[/cyan]", spinner="dots"):
        results = fetcher.search(query, limit=5)

    if not results:
        console.print(f"[yellow]No exact match found for '{query}'.[/yellow]")
    else:
        console.print(f"[green]Found match:[/] [bold cyan]{results[0]}[/bold cyan]")
        console.print(f"To index this topic, run: [bold yellow]/add {results[0]}[/bold yellow]\n")

def add_topic(topic: str):
    """Fetch, chunk, and index a single Wikipedia article."""
    if not topic.strip():
        console.print("[yellow]Please specify a topic name: /add <topic>[/yellow]")
        return

    with console.status(f"[cyan]Fetching article '{topic}' from Wikipedia...[/cyan]", spinner="dots"):
        doc = fetcher.fetch(topic)

    if not doc:
        console.print(f"[red]Error:[/] Could not find Wikipedia article '{topic}'. Check title spelling.")
        return

    console.print(f"[green]✓[/green] Downloaded [bold]{doc['title']}[/bold] ({doc['length']} characters)")

    with console.status(f"[cyan]Chunking and generating embeddings with {config.EMBED_MODEL}...[/cyan]", spinner="dots"):
        embedder.add_documents([doc])
        qa_engine._build_chain()

    console.print(f"[bold green]✓ Successfully indexed '{doc['title']}' into the knowledge base![/bold green]\n")

def build_default_topics():
    """Index all default Wikipedia topics."""
    console.print(f"[yellow]This will fetch and index {len(config.DEFAULT_TOPICS)} default topics.[/yellow]")
    console.print("[dim]Articles: " + ", ".join(config.DEFAULT_TOPICS) + "[/dim]")
    confirm = Prompt.ask("Proceed with indexing?", choices=["y", "n"], default="y")
    if confirm != "y":
        console.print("[dim]Build cancelled.[/dim]\n")
        return

    docs = []
    with console.status("[cyan]Fetching default articles from Wikipedia...[/cyan]", spinner="dots") as status:
        for t in config.DEFAULT_TOPICS:
            status.update(f"[cyan]Fetching '{t}'...[/cyan]")
            d = fetcher.fetch(t)
            if d:
                docs.append(d)
                console.print(f"  [green]✓[/green] {t}")
            else:
                console.print(f"  [yellow]✗[/yellow] {t} (not found)")

    console.print(f"[cyan]Generating embeddings for {len(docs)} articles with {config.EMBED_MODEL}...[/cyan]")
    with console.status("[cyan]Embedding chunks into ChromaDB (this may take 1-2 minutes)...[/cyan]", spinner="dots"):
        embedder.build_index(docs)
        qa_engine._build_chain()

    stats = embedder.get_stats()
    console.print(f"[bold green]✓ Build complete! Total chunks indexed: {stats['total_chunks']}[/bold green]\n")

def ask_question(question: str):
    """Execute QA query and print formatted answer with sources."""
    stats = embedder.get_stats()
    if stats["total_chunks"] == 0:
        console.print("[bold red]No articles indexed in vector database![/bold red]")
        console.print("Please index at least one topic first. Examples:")
        console.print("  • [cyan]/add Python (programming language)[/cyan]")
        console.print("  • [cyan]/add Artificial intelligence[/cyan]")
        console.print("  • [cyan]/build[/cyan] (indexes all default topics)\n")
        return

    with console.status(f"[cyan]Searching knowledge base & generating answer with {config.LLM_MODEL}...[/cyan]", spinner="dots"):
        try:
            result = qa_engine.query(question, top_k=config.TOP_K_RESULTS)
        except Exception as e:
            console.print(f"[bold red]Error during query:[/] {e}")
            return

    # Print answer
    console.print("\n" + "-" * 60)
    console.print(Markdown(result["answer"]))
    console.print("-" * 60)

    # Print sources
    sources = result.get("sources", [])
    if sources:
        console.print("[dim bold]Sources:[/dim bold]")
        for idx, s in enumerate(sources, 1):
            src_name = s.get("source", "Wikipedia")
            url = s.get("url", "")
            url_str = f" ([link={url}]{url}[/link])" if url else ""
            console.print(f" [cyan]{idx}.[/cyan] [bold]{src_name}[/bold]{url_str}")
            preview = s.get("chunk_preview", "").replace("\n", " ").strip()
            console.print(f"    [dim]\"{preview[:140]}...\"[/dim]")
    console.print()

def main():
    # Support non-interactive test flag
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test-query":
            q = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "What is Python?"
            ask_question(q)
            return
        elif sys.argv[1] == "--status":
            show_stats()
            return
        elif sys.argv[1] == "--topics":
            show_topics()
            return

    print_banner()

    # Pre-flight check
    ollama_ok, models = check_ollama()
    if not ollama_ok:
        console.print("[bold red]Warning:[/] Ollama is not detected at http://localhost:11434.")
        console.print("Make sure you run [bold cyan]ollama serve[/bold cyan] in another terminal window.\n")
    elif config.LLM_MODEL not in [m.split(":")[0] for m in models] and config.LLM_MODEL not in models:
        console.print(f"[bold yellow]Note:[/] Model '{config.LLM_MODEL}' was not found in Ollama.")
        console.print(f"Run [bold cyan]ollama pull {config.LLM_MODEL}[/bold cyan] in your terminal.\n")

    # Main REPL Loop
    while True:
        try:
            user_input = Prompt.ask("[bold cyan]WikiAgent[/bold cyan]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Goodbye![/dim]")
            break

        if not user_input:
            continue

        cmd = user_input.lower()

        if cmd in ("exit", "quit", ":q"):
            console.print("[dim]Goodbye![/dim]")
            break
        elif cmd == "/help":
            show_help()
        elif cmd in ("/stats", "/status"):
            show_stats()
        elif cmd in ("/topics", "/list"):
            show_topics()
        elif cmd == "/clear":
            os.system("cls" if os.name == "nt" else "clear")
            print_banner()
        elif cmd == "/build":
            build_default_topics()
        elif cmd.startswith("/add "):
            topic = user_input[5:].strip()
            add_topic(topic)
        elif cmd.startswith("/search "):
            query = user_input[8:].strip()
            search_wikipedia(query)
        elif cmd.startswith("/"):
            console.print(f"[yellow]Unknown command '{user_input}'. Type [bold]/help[/bold] for available commands.[/yellow]")
        else:
            ask_question(user_input)

if __name__ == "__main__":
    main()
