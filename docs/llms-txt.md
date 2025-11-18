# LLMs.txt

Georouting provides LLMs.txt files to help AI assistants understand and work with our library more effectively.

## What is LLMs.txt?

LLMs.txt is a structured documentation format specifically designed for large language models (LLMs). It provides AI assistants with concise, well-organized information about georouting, enabling them to give you more accurate and helpful responses when working with the library.

Learn more about the standard at [llmstxt.org](https://llmstxt.org/).

## Available Files

| File | Description | Size |
|------|-------------|------|
| [llms.txt](https://wybert.github.io/georouting/llms.txt) | Concise overview with installation, quick start, features, and API links | ~2KB |
| [llms-full.txt](https://wybert.github.io/georouting/llms-full.txt) | Complete documentation compiled from all sources | ~55KB |

## Choosing the Right File

- **Use `llms.txt`** for most tasks - It fits within standard context windows and provides enough information for common questions about installation, basic usage, and API navigation.

- **Use `llms-full.txt`** when you need comprehensive reference - Use this for detailed API documentation, advanced usage patterns, or when working with AI tools that support large context windows (200K+ tokens).

## Usage with AI Tools

### Claude, ChatGPT, and other AI Assistants

Include the URL directly in your prompt:

```
Using georouting documentation from https://wybert.github.io/georouting/llms.txt,
help me calculate driving distances between multiple locations.
```

Or for comprehensive documentation:

```
Reference https://wybert.github.io/georouting/llms-full.txt to help me
implement a custom router for georouting.
```

### Cursor

Use `@Docs` to add the llms.txt URL to your workspace:

1. Open Cursor Settings > Features > Docs
2. Add a new doc with URL: `https://wybert.github.io/georouting/llms.txt`
3. Reference it in chat using `@Docs`

### Windsurf

Add the documentation to your cascade:

1. Use `@docs` in the chat
2. Add the URL: `https://wybert.github.io/georouting/llms.txt`

### Claude Code

When using Claude Code, you can reference the documentation:

```
Fetch https://wybert.github.io/georouting/llms.txt and help me
create a distance matrix using OSRM.
```

## Example Prompts

Here are some example prompts you can use with AI assistants:

**Basic usage:**
```
Using https://wybert.github.io/georouting/llms.txt, show me how to
get driving directions between Boston and New York using OSRM.
```

**API exploration:**
```
Reference https://wybert.github.io/georouting/llms-full.txt and explain
the difference between get_distance_matrix and get_distances_batch.
```

**Integration help:**
```
Using georouting docs from https://wybert.github.io/georouting/llms.txt,
help me integrate Google Maps routing into my Flask application.
```

## Regenerating LLMs.txt Files

If you're contributing to georouting and need to update the documentation:

```bash
# Regenerate llms-full.txt from all documentation
python generate_llms_full.py
```

The `llms.txt` file is manually maintained to keep it concise and focused.
