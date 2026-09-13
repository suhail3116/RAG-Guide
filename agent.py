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
import json
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
from services.curated_docs import get_curated_documents

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

last_sources = []
show_sources_by_default = False

def print_sources(sources_list=None):
    """Print sources in an organized, readable view."""
    global last_sources
    target = sources_list if sources_list is not None else last_sources
    if not target:
        console.print("[yellow]No source citations available for the last query.[/yellow]\n")
        return

    console.print(f"\n[bold cyan]📚 Wikipedia Sources ({len(target)} citations):[/bold cyan]")
    for idx, s in enumerate(target, 1):
        src_name = s.get("source", "Wikipedia")
        url = s.get("url", "")
        url_str = f" ([link={url}]{url}[/link])" if url else ""
        console.print(f"  [bold cyan][{idx}][/bold cyan] [bold]{src_name}[/bold]{url_str}")
        preview = s.get("chunk_preview", "").replace("\n", " ").strip()
        console.print(f"      [dim]\"{preview[:140]}...\"[/dim]")
    console.print()

def show_help():
    """Display interactive commands."""
    table = Table(title="Available Commands", border_style="dim")
    table.add_column("Command", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")
    table.add_row("/sources", "View sources for the last answer (or '/sources on|off' to toggle)")
    table.add_row("/topics", "List all currently indexed Wikipedia articles")
    table.add_row("/add <topic>", "Fetch and index a Wikipedia article (e.g. /add Machine learning)")
    table.add_row("/search <query>", "Search Wikipedia for article titles")
    table.add_row("/build", "Index all 37 technical & engineering topics into ChromaDB")
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
    table.add_row("Active Engine LLM", getattr(qa_engine, "active_model", config.LLM_MODEL))
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

def build_default_topics(interactive: bool = True):
    """Cleanly build vector database from the 32 Wikipedia topics + 5 curated engineering workflows."""
    curated_docs = get_curated_documents()
    total_count = len(config.DEFAULT_TOPICS) + len(curated_docs)
    console.print(f"[yellow]This will cleanly rebuild the knowledge base with {total_count} topics ({len(config.DEFAULT_TOPICS)} Wikipedia + {len(curated_docs)} Curated Guides).[/yellow]")

    if interactive:
        confirm = Prompt.ask("Proceed with clean build?", choices=["y", "n"], default="y")
        if confirm != "y":
            console.print("[dim]Build cancelled.[/dim]\n")
            return

    docs = []
    cache_file = Path("./data/articles_cache.json")
    cache_file.parent.mkdir(exist_ok=True)
    cached_data = {}
    if cache_file.exists():
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                cached_data = json.load(f)
        except Exception:
            cached_data = {}

    # 1. Fetch Wikipedia articles (using local cache when available)
    with console.status("[cyan]Retrieving Wikipedia articles...[/cyan]", spinner="dots") as status:
        for idx, t in enumerate(config.DEFAULT_TOPICS, 1):
            status.update(f"[cyan][{idx}/{len(config.DEFAULT_TOPICS)}] Processing '{t}'...[/cyan]")
            if t in cached_data and cached_data[t]:
                d = cached_data[t]
                docs.append(d)
                console.print(f"  [green]✓[/green] [{idx}/{len(config.DEFAULT_TOPICS)}] {t} [dim](cached)[/dim]")
            else:
                d = fetcher.fetch(t)
                if d:
                    cached_data[t] = d
                    docs.append(d)
                    console.print(f"  [green]✓[/green] [{idx}/{len(config.DEFAULT_TOPICS)}] {t} [dim]({d['length']} chars)[/dim]")
                else:
                    console.print(f"  [yellow]✗[/yellow] [{idx}/{len(config.DEFAULT_TOPICS)}] {t} (not found)")

    # Save cache
    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(cached_data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

    # 2. Append curated technical documents
    for c in curated_docs:
        docs.append({
            "title": c["title"],
            "page_content": c["full_text"],
            "summary": c["full_text"][:400],
            "full_text": c["full_text"],
            "url": c["url"],
            "categories": c.get("categories", []),
            "length": len(c["full_text"])
        })
        console.print(f"  [green]✓[/green] [bold cyan]{c['title']}[/bold cyan] [dim]({len(c['full_text'])} chars)[/dim]")

    console.print(f"\n[cyan]Generating embeddings for {len(docs)} articles with {config.EMBED_MODEL}...[/cyan]")
    with console.status("[cyan]Embedding chunks into ChromaDB (this may take 1-2 minutes)...[/cyan]", spinner="dots"):
        embedder.build_index(docs)
        qa_engine._build_chain()

    stats = embedder.get_stats()
    console.print(f"[bold green]✓ Clean build complete! Total topics indexed: {stats['topics_count']} | Total chunks: {stats['total_chunks']}[/bold green]\n")

def ask_question(question: str):
    """Execute QA query with real-time streaming answer and sources."""
    stats = embedder.get_stats()
    if stats["total_chunks"] == 0:
        console.print("[bold red]No articles indexed in vector database![/bold red]")
        console.print("Please index at least one topic first. Examples:")
        console.print("  • [cyan]/add Python (programming language)[/cyan]")
        console.print("  • [cyan]/add Artificial intelligence[/cyan]")
        console.print("  • [cyan]/build[/cyan] (indexes all default topics)\n")
        return

    with console.status(f"[cyan]Searching knowledge base & connecting to {config.LLM_MODEL}...[/cyan]", spinner="dots"):
        stream_gen = qa_engine.stream_query(question, top_k=config.TOP_K_RESULTS)

    console.print("\n" + "-" * 60)
    sources = []
    has_tokens = False

    try:
        for token, src_list in stream_gen:
            if token:
                console.print(token, end="")
                has_tokens = True
            if src_list is not None:
                sources = src_list
    except Exception as e:
        console.print(f"\n[bold red]Error during query:[/] {e}")
        return

    if not has_tokens and not sources:
        console.print("[dim italic]No response generated.[/dim italic]")

    console.print("\n" + "-" * 60)

    # Handle sources (hidden by default to keep terminal clean)
    global last_sources, show_sources_by_default
    last_sources = sources
    if sources:
        if show_sources_by_default:
            print_sources(sources)
        else:
            console.print(
                f"[dim]📚 [bold]{len(sources)} sources hidden[/bold]. "
                f"Type [bold cyan]/sources[/bold cyan] to view, or [bold cyan]/sources on[/bold cyan] to auto-show.[/dim]\n"
            )

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
        elif sys.argv[1] == "--build":
            build_default_topics(interactive=False)
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
        elif cmd in ("/engineering", "/build engineering"):
            build_engineering_topics()
        elif cmd in ("/sources", "/source"):
            print_sources()
        elif cmd in ("/sources on", "/sources enable", "/sources show"):
            show_sources_by_default = True
            console.print("[green]✓ Sources will now be displayed automatically after each answer.[/green]\n")
        elif cmd in ("/sources off", "/sources disable", "/sources hide"):
            show_sources_by_default = False
            console.print("[yellow]✓ Sources will be hidden by default. Type /sources to inspect them anytime.[/yellow]\n")
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
