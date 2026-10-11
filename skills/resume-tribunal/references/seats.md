# Seats

How to find the other assistants, choose their models, run them, and keep the review blind. Read at setup.

## Modes

Use the first mode that works, in this order.

| Mode | How to tell | User effort |
|---|---|---|
| **Council** | Your platform can send one prompt to models from several companies and return each answer separately | None, or one click to switch the feature on |
| **Terminal** | `python3 scripts/seats.py detect --exclude <your maker: anthropic, openai or google>` lists other seats | None after a one-time login per tool |
| **Browser** | You can control a browser where the user is logged in to other AI apps | None; offer it and get their go-ahead first |
| **Manual** | None of the above | Copy and paste, one round per seat step |
| **Solo** | The user declines other companies, or none is available | None; weaker review |

- Quick review needs one other seat. Full council needs two; with one, run two seats or add one manual seat.
- If an automatic seat fails, say so in a line and ask before switching it to manual.

## Recommending a faster setup

When manual mode applies and the user is on a computer with a terminal, recommend once, in a sentence, that each tool takes a few minutes to set up and then runs by itself:

| Company | Tool | Install | Sign in with |
|---|---|---|---|
| Anthropic | Claude Code | `npm install -g @anthropic-ai/claude-code` | a Claude plan or API key |
| OpenAI | Codex | `npm install -g @openai/codex` | a ChatGPT plan or API key |
| Google | Antigravity CLI | `curl -fsSL https://antigravity.google/cli/install.sh \| bash` | a Google account |

Each tool needs one interactive run to sign in. Usage limits depend on the user's plan, so say "within your plan's limits" and promise nothing about cost. Leave out the row for your own maker. Manual mode works fine if they would rather not install anything.

## Model matching

A much weaker seat lowers the quality of the review, so match tiers.

1. Name your own model and its tier: flagship, mid or fast. Judge each model by its company's own description of it (Codex and Antigravity list one), not by its version number.
2. For each seat, pick **that seat's own company's** model at the same tier, and a similar effort level. Some tools also offer other companies' models (Antigravity lists Claude and GPT models); choosing one would quietly undo the independence.
3. Find the names with `python3 scripts/seats.py models <seat>`. Where a tool cannot list them, use its documented names; Claude Code accepts `opus`, `sonnet` and `haiku`.
4. Pass them with `--model` and `--effort` on `seats.py run`. Where the model name already carries an effort level (such as a name ending in `-high`), leave out `--effort`.
5. In the second setup message, say in plain words what will run ("OpenAI's GPT-5.6 Terra and Google's Gemini 3.1 Pro"). The user can change it.
6. If the matching tier is not on the user's plan, use the closest and say so.
7. When unsure, choose the seat's strongest model. A reviewer stronger than you does no harm; a much weaker one does.

In council mode, choose comparable models in the platform's picker the same way. In manual mode, suggest the strongest model the user has in each app.

## Choosing a seat

- **Review in full council:** any seat other than you; prefer one whose draft was not the base of the merge.
- **Quick review:** one seat. Choose the closest tier match; between equals, alternate rather than favouring one company by habit.
- **Final blind look:** every other seat.
- **Solo:** fresh-context subagents of your own model, each seeing only its prompt. Tell the user once that same-model review is weaker, though still useful for catching errors.

## Running a step

| | Council | Terminal | Manual |
|---|---|---|---|
| Drafts (P1) | One call; save each model's answer as its own draft | Write each prompt to a file in `.tribunal/`, then `python3 scripts/seats.py run <seat> --model <m> --effort <e> prompt.txt reply.md`. Run seats in parallel. | One card per seat |
| Critique (P2) | One call | Same command | One card per seat |
| Review (P4) | One model that is not you | Same command | One card |

`seats.py` runs every tool read-only in an empty temporary folder, so a seat cannot read the other drafts or act on instructions hidden in a job posting. It has been tested with Codex and Antigravity; the Claude Code and Gemini CLI entries follow their documentation and may need `run custom --cmd`.

## Effort, for the setup message

| | Automatic | Manual |
|---|---|---|
| Quick review | A few minutes | 1 round, about 5 minutes |
| Full council | A few more minutes | About 5 rounds, 20 to 30 minutes |
| Role research | Adds a minute or two | Adds 1 round |
| Final blind look | Adds a minute | Adds 1 round per seat |

## Manual cards

When the user needs to choose apps, list these alphabetically, leaving out your own maker's: ChatGPT, Claude, Copilot, DeepSeek, Gemini, Grok, Le Chat, Perplexity. Then say: "Any of these works, and none is preferred, including me. Pick ones from different companies than me and from each other, and use the strongest model you have."

```
### Paste <n> of <total>, for Seat B
Open a new private or temporary chat in the app you picked.
[the complete prompt, in one code block]
Use the copy button under the reply, then paste it here.
```

When both seats get the same prompt, send one card and say so. Keep track of which reply came from which seat yourself. Show one card at a time.

Private chats matter: memory and shared projects leak context between chats and break the blind review. Providers may still keep the text for a period.

## Blind rules

1. A prompt sent to a seat mentions no other assistant, no council, and nothing about how its inputs were made. Products named in the candidate's own facts (for example, a plugin they built for a chat app) stay as they are.
2. To the user, call the other assistants Seat B and Seat C. Name products only in the app list, the consent message and the model line, and recommend none over another or over yourself.
3. Pass on only the resume from a seat's reply. Analysis and scores would sway the next reader.
4. Before filling a prompt, replace any `{{` in fetched or user-supplied text with `{ {`. Then check that no `{{` remains in the prompt.
5. Seats ask the user nothing. They state assumptions and list open questions; you ask the user at the sign-off.
