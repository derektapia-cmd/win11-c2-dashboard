# Command Center Dashboard Application Roadmap

## Status

Planning only. No code changes, no files generated, and no implementation work starts until Derek gives a clear launch decision.

Launch phrase: **LAUNCH APPROVED**

## Project Question Protocol
All planning questions for this project should be asked in a multiple-choice format whenever possible.

Preferred format:
- When Derek uses the phrase **askmequestions**, automatically format questions as a Markdown-formatted list.
- Use clickable-style Markdown options whenever possible.
- Since true in-chat buttons may not be available, use clean option rows that are easy to click/copy/select.
- Ask one question at a time unless grouped questions are clearly better.
- Use short lettered choices such as A, B, C, D.
- Include an **Other / custom** option when needed.
- Allow Derek to reply with a single letter like `A`, or compact grouped answers like `1C, 2A, 3D`.
- Avoid open-ended written responses unless the detail is truly necessary.

No implementation starts from answers alone. Implementation still requires the launch phrase: **LAUNCH APPROVED**

## Project Mission

Build a Windows 11 desktop command-center dashboard with a premium futuristic dark-mode interface. It should open on sign-in, display real-time tiles, connect to daily tools and data sources, and leave room for future expansion without creating messy cross-module conflicts.

The app should feel like a personal operating cockpit: email, weather, news, X feed, crypto prices, notes, AI tools, terminal access, wallets, and future workflow tiles in one unified layout.

## Core Design Rules

1. Plan first, build second.
2. No module talks directly to another module unless it goes through the approved event/data layer.
3. Each tile must be independently replaceable.
4. API keys, OAuth tokens, wallet secrets, email data, and notes stay protected.
5. Destructive actions require confirmation.
6. Wallet seed phrases/private keys are never stored by this app.
7. The dashboard should still load if one service fails.
8. Every tile must have a loading state, offline state, error state, and reconnect path.
9. Expansion slots are first-class citizens, not afterthought blank boxes.
10. The app must be packageable for normal Windows 11 devices.

## Recommended Build Stack

### Desktop Shell

Use **Electron** as the Windows 11 desktop shell.

Reason: it gives strong JavaScript/TypeScript UI support, Windows tray/startup behavior, local process control, and easier embedding of web-style dashboard components.

### Frontend

Use **React + TypeScript**.

Primary responsibilities:

- Dashboard layout
- Tiles
- Animations
- WebSocket client
- User settings screens
- Wallet connection UI
- Notes editor
- Terminal panel UI
- Bottom crypto ticker

### Backend

Use **Python FastAPI** running as a local backend service.

Primary responsibilities:

- Gmail API integration
- Weather API integration
- News/RSS aggregation
- CoinGecko API integration
- Binance WebSocket integration
- X API integration
- Notes storage
- Local search/indexing
- Scheduler jobs
- API token refresh handling
- Audit logging
- AI provider proxying where needed

### Local Database

Use **SQLite** for the first version.

Tables:

- user\_settings
- tile\_layouts
- oauth\_accounts
- api\_credentials\_metadata
- gmail\_cache
- weather\_cache
- news\_sources
- news\_items
- x\_feed\_cache
- crypto\_assets
- crypto\_prices
- notes
- command\_sessions
- wallet\_accounts
- app\_events
- audit\_log

### Optional Later Database Upgrade

Move to PostgreSQL only if the app grows into multi-device sync or very large historical market storage.

## High-Level Architecture

```
Windows 11
  └── Electron Desktop App
        ├── React Dashboard UI
        ├── Tile System
        ├── Secure IPC Bridge
        ├── Embedded Terminal Shell
        └── Local WebSocket Client

  └── Python Local Service
        ├── FastAPI REST API
        ├── WebSocket Hub
        ├── OAuth Manager
        ├── Scheduler
        ├── Gmail Connector
        ├── Weather Connector
        ├── News Connector
        ├── X Connector
        ├── CoinGecko Connector
        ├── Binance Connector
        ├── AI Provider Connector
        ├── Notes Service
        ├── Wallet Metadata Service
        └── SQLite Storage
```

## Main Dashboard Layout

### Global Layout

- Full-screen or resizable desktop window
- Dark futuristic interface
- Neon accent system
- Glass panels, soft glow, depth layering
- Smooth tile refresh animations
- No cheap default Bootstrap look
- Responsive grid with saved layout state

### Suggested Screen Areas

1. **Top command bar**

   - App title
   - Current time/date
   - Global search
   - Connection health indicator
   - Settings button
   - Lock/privacy mode

2. **Primary dashboard grid**

   - Gmail tile
   - Weather tile
   - News tile
   - X feed tile
   - Notes tile
   - ChatGPT tile
   - Claude Code tile
   - Terminal tile
   - MetaMask wallet tile
   - Phantom wallet tile
   - Expansion slot 1
   - Expansion slot 2
   - Expansion slot 3

3. **Bottom crypto ticker**

   - Fixed strip above Windows taskbar area
   - Appears from right side and scrolls left continuously
   - Displays selected crypto symbols, prices, 24h change, and source
   - Supports pausing on hover
   - Uses CoinGecko normalized pricing and Binance exchange pricing

4. **Side utility rail**

   - Dashboard
   - Email
   - Markets
   - Notes
   - AI
   - Wallets
   - Settings
   - Logs

## Tile System

Every tile should share one base contract:

- tile\_id
- tile\_type
- title
- size
- refresh\_strategy
- permissions\_required
- data\_source
- loading\_state
- error\_state
- offline\_state
- last\_updated\_at
- actions
- settings

Tile refresh types:

- Real-time WebSocket
- Polling interval
- Manual refresh
- Event-triggered refresh
- Startup-only refresh

## Required Tiles

### 1. Gmail Tile

Purpose: display and interact with Gmail from the dashboard.

Planned abilities:

- Unread count
- Priority inbox preview
- Search mail
- Read messages
- Create drafts
- Send email
- Reply
- Forward
- Archive
- Trash
- Label management
- Attachment awareness
- Optional mail rules/filters tile later

Safety requirements:

- No password storage
- OAuth only
- Sending email requires visible confirmation unless user later enables trusted mode
- Permanent deletion should be disabled by default
- Full mailbox access must be treated as high-risk permission
- Store only minimum cached email data needed for the dashboard

Suggested v1 scope approach:

- Start with read/search/send/modify-level capability
- Avoid permanent-delete-level access unless Derek explicitly approves it

### 2. Weather Tile

Purpose: current and forecasted weather for home.

Planned abilities:

- Current temperature
- Feels-like temperature
- Conditions
- Wind
- Humidity
- Hourly forecast
- 7-day forecast
- Weather alerts if supported by provider

Needed from Derek:

- Home city or ZIP code
- Preferred units: Fahrenheit or Celsius

### 3. News Feeds Tile

Purpose: favorite news sources in one tile.

Planned abilities:

- RSS feeds
- Manual feed URLs
- Categories
- Read/unread state
- Open article externally
- Save article to notes
- Optional AI summary later

Needed from Derek:

- Favorite news sources/feed URLs
- Whether political, crypto, tech, local, world, finance, or all

### 4. X Account Tile

Purpose: connect to X and display feed/activity.

Planned abilities:

- OAuth login
- Timeline/feed display if API access permits
- Selected account/list monitoring
- Keyword monitoring
- Post preview
- Open in browser

Constraints:

- X API permissions, pricing, and rate limits must be handled carefully
- The tile needs a quota manager so it does not burn credits unnecessarily

Needed from Derek:

- Display home feed, specific lists, specific accounts, or keyword feeds?
- Read-only or allow posting/replying later?

### 5. Crypto Ticker + Market Tile

Purpose: real-time crypto market display using CoinGecko and Binance.

Planned abilities:

- Top selected prices
- 24h change
- Source comparison: CoinGecko global average vs Binance exchange price
- Bottom continuous scrolling ticker
- Market tile with larger cards/charts later
- Favorite asset list
- Refresh health indicator

Data source model:

- Binance WebSocket for exchange-level fast updates
- CoinGecko REST/WebSocket for normalized global data
- Local price normalizer to prevent UI conflicts

Needed from Derek:

- Top coins/symbols to show
- Spot only, futures too, or both?
- Alert thresholds?

### 6. Notes Tile

Purpose: fast notes and dictated thoughts.

Planned abilities:

- Type notes
- Pin notes
- Tag notes
- Search notes
- Dictation input
- Attach a note to a dashboard event
- Export notes later

Needed from Derek:

- Local-only notes or cloud sync later?
- Voice dictation provider preference?

### 7. Command Line Tile

Purpose: command-line access inside the dashboard.

Planned abilities:

- PowerShell session
- Command Prompt session
- WSL/Linux shell if installed
- Project directory selector
- Command history
- Copy output
- Claude Code command integration

Safety requirements:

- Show working directory clearly
- Dangerous command warning mode
- Optional restricted/sandboxed mode
- Command audit log

### 8. Claude Code Tile

Purpose: access Claude Code from the dashboard.

Planned abilities:

- Launch Claude Code CLI session
- Show active project path
- Display current terminal output
- Run Claude Code in selected workspace
- Capture session logs locally

Needed from Derek:

- Which project folder should Claude Code open by default?
- Native Windows, WSL, or both?

### 9. ChatGPT Tile

Purpose: access ChatGPT or OpenAI-powered assistant functions inside the dashboard.

Two possible designs:

Option A: Official app launcher tile

- Opens ChatGPT Windows app or browser
- Most compliant and simple
- Limited embedding/control

Option B: Custom ChatGPT-style tile using OpenAI API

- Built-in chat panel inside dashboard
- Supports local context and dashboard actions
- Requires OpenAI API key
- More flexible and better integrated

Recommended: support both.

Needed from Derek:

- Do you want this tile to open the official ChatGPT app, run an embedded API assistant, or both?

### 10. MetaMask Wallet Tile

Purpose: connect and display MetaMask wallet info.

Planned abilities:

- Connect wallet through MetaMask-approved flow
- Display connected address
- Display selected network
- Display balances using public RPC/indexing APIs
- Watch account/network changes
- Open wallet externally if needed

Safety requirements:

- Never store seed phrase
- Never store private key
- Never auto-sign transactions
- Transaction signing must happen in wallet confirmation UI

### 11. Phantom Wallet Tile

Purpose: connect and display Phantom wallet info.

Planned abilities:

- Connect Phantom via supported web SDK flow
- Display Solana address
- Display EVM address if enabled
- Display balances
- Detect installed wallet where supported
- Open wallet externally if needed

Safety requirements:

- Never store seed phrase
- Never store private key
- Never auto-sign transactions
- Transaction signing must happen in wallet confirmation UI

### 12. Expansion Slots

Purpose: reserve future dashboard room.

Initial slots:

- Expansion Slot A: automation/control tile
- Expansion Slot B: calendar/tasks tile
- Expansion Slot C: trading/watchlist analytics tile

Each slot should be a real tile placeholder with settings and metadata, not just empty UI.

## Permissions Center

A dedicated settings page should show:

- Gmail status
- X status
- CoinGecko key status
- Binance key status if needed
- OpenAI key status
- Anthropic/Claude status
- MetaMask connection status
- Phantom connection status
- Weather provider status
- News source status

Each service should have:

- Connect
- Disconnect
- Reconnect
- Test connection
- Last successful sync
- Last error
- Permission explanation

## Security Model

### Secrets Storage

Use OS-protected secure storage where possible.

Store:

- OAuth refresh tokens
- API keys
- Provider metadata

Never store:

- Gmail password
- X password
- Wallet seed phrases
- Wallet private keys
- Raw long-term terminal secrets in logs

### Local Data Encryption

Recommended:

- Encrypt sensitive token storage
- Encrypt notes if Derek wants privacy mode
- Provide app lock PIN/password option later

### Audit Log

Track:

- Email sent
- Email deleted/trashed
- Wallet connected/disconnected
- API keys added/removed
- Terminal command executed
- Claude Code launched
- Notes exported
- Settings changed

## Data Flow Rules

Frontend never calls external APIs directly except wallet-provider browser flows when required.

Preferred flow:

```
React Tile -> Local API Client -> Python FastAPI -> Connector -> External API
React Tile <- WebSocket Event Hub <- Python FastAPI <- Connector <- External API
```

Wallet exception:

```
React Wallet Tile -> Wallet SDK/provider -> User wallet confirmation
React Wallet Tile -> Backend public RPC/indexing lookup for balances
```

## Refresh Strategy

### Real-Time

- Binance WebSocket streams
- CoinGecko WebSocket if paid plan is available
- Local dashboard WebSocket hub

### Fast Polling

- Crypto fallback: 10–30 seconds depending on API plan

### Medium Polling

- Gmail: push notifications or periodic sync
- X: interval based on access/rate limits
- News: 5–15 minutes

### Slow Polling

- Weather forecast: 15–60 minutes
- App update checks: daily

## Error Isolation

If one tile fails:

- The app remains open
- Failed tile shows error state
- Other tiles continue updating
- Error is logged
- User can retry tile manually

## Proposed Folder Structure

```
command-center-dashboard/
  apps/
    desktop/
      electron/
      renderer/
      preload/
    backend/
      app/
        api/
        core/
        connectors/
        services/
        models/
        storage/
        scheduler/
        websocket/
        security/
        tests/
  packages/
    shared-types/
    ui-kit/
    tile-contracts/
  docs/
    roadmap.md
    architecture.md
    api-integrations.md
    security-model.md
    tile-specs.md
    launch-checklist.md
  scripts/
  installer/
  .env.example
```

## Beginner Build Mode

Derek is a complete beginner for this build, so every phase should include:

- Plain-English explanation of what the step does.
- A small number of actions at a time.
- Multiple-choice selections instead of open-ended questions whenever possible.
- A quick checkpoint before moving to the next phase.
- No assumptions hidden in the build process.

Beginner rule: each build phase should answer these four things:

1. What are we doing?
2. Why are we doing it?
3. What can break?
4. How do we verify it worked?

## Development Milestones

### Milestone 0: Requirements Lock

Output:

- Approved feature list
- Approved tile list
- Approved API providers
- Approved permissions model
- Approved UI direction

No code yet.

### Milestone 1: Architecture Freeze

Output:

- Final architecture diagram
- Folder structure
- Tile contract
- Data flow rules
- Database schema draft
- Security model

No production code yet.

### Milestone 2: UI Prototype

Output:

- Static futuristic dashboard mockup
- Tile sizing and layout
- Bottom crypto ticker design
- Dark theme system
- Expansion slot visuals

### Milestone 3: Backend Skeleton

Output:

- Python FastAPI service shell
- Health endpoint
- WebSocket hub
- SQLite database setup
- Connector interfaces

### Milestone 4: Frontend Shell

Output:

- Electron shell
- React dashboard grid
- Tile registry
- Settings pages
- Secure IPC bridge

### Milestone 5: Integrations Round 1

Output:

- Weather
- News/RSS
- CoinGecko
- Binance
- Notes

### Milestone 6: Integrations Round 2

Output:

- Gmail OAuth
- X OAuth/API
- ChatGPT/OpenAI tile
- Claude Code terminal launch

### Milestone 7: Wallet Integrations

Output:

- MetaMask connect/display
- Phantom connect/display
- Balance reads
- Account/network event handling

### Milestone 8: Polish + Reliability

Output:

- Error states
- Reconnect logic
- Audit logs
- Settings backup/export
- Performance pass
- Animation polish

### Milestone 9: Windows Packaging

Output:

- Windows installer
- Start-on-login option
- Desktop shortcut
- App icon
- Local service startup strategy
- Update strategy decision

### Milestone 10: Launch Candidate

Output:

- Full QA checklist
- Integration tests
- Permission review
- Security review
- Manual install test
- Final go/no-go

## Test Plan

### Functional Tests

- App launches on Windows 11
- Dashboard loads without internet
- Each tile loads independently
- Each tile handles API failure
- Settings persist after restart
- Crypto ticker scrolls correctly
- Notes save/reload correctly
- Terminal opens in selected shell
- Wallet connect/disconnect works
- Gmail read/send flow works after OAuth

### Security Tests

- No API keys visible in logs
- OAuth tokens not exposed to frontend
- Wallet private keys never requested
- Email deletion requires confirmation
- Terminal dangerous-command warning works

### Reliability Tests

- Binance reconnect after disconnect
- CoinGecko fallback from WebSocket to REST
- X rate-limit handling
- Gmail token refresh
- Weather provider timeout
- App restart recovery

### UI Tests

- 1080p display
- 1440p display
- 4K display
- Windowed mode
- Fullscreen mode
- Tile drag/reorder
- Dark theme contrast

## Decisions Needed From Derek

### Identity and Access

1. Is this app for personal use only, or do you eventually want to distribute it?
2. Should Gmail have full access, or should permanent deletion stay disabled?
3. Should email sending always require confirmation?
4. Do you want app lock/privacy mode at startup?

### Layout and Look

5. Should the dashboard be always fullscreen, windowed, or both?
6. Should it auto-start when Windows signs in?
7. Preferred futuristic style: cyberpunk neon, glassmorphism, military HUD, luxury finance terminal, or hybrid?
8. Preferred accent color: blue, cyan, green, purple, red, gold, or custom?

### Weather

9. What ZIP code/city should be used as home weather?
10. Fahrenheit or Celsius?

### News

11. Which news sources/feeds do you want first?
12. Do you want article summaries, or just headlines and links for v1?

### X

13. Should the X tile show your home timeline, a list, specific accounts, or keyword searches?
14. Read-only for v1, or allow posting/replies?
15. Are you okay with X API pay-per-use/credit management?

### Crypto

16. Which coins should appear in the bottom ticker first?
17. Spot prices only, or futures/perps too?
18. Should Binance be used only for public market data, or will account/trading features come later?
19. Do you want alerts for price moves?

### Notes

20. Should notes be local-only?
21. Do you want voice dictation using Windows built-in speech, OpenAI transcription, or another provider?

### AI/Terminal

22. Should ChatGPT tile use the official app launcher, OpenAI API embedded chat, or both?
23. Should Claude Code run in PowerShell, CMD, WSL, or selectable?
24. What default project folder should the terminal and Claude Code open in?
25. Should terminal commands be unrestricted or warning-gated?

### Wallets

26. Should wallet tiles be read-only balance/portfolio views for v1?
27. Should transaction signing be blocked entirely in v1?
28. Which chains matter first: Ethereum, Base, Polygon, Solana, Bitcoin, Sui, BNB Chain, Arbitrum, Optimism?

### Expansion

29. What future tiles do you already know you want?
30. Should there be a calendar/tasks tile in v1 or saved for v2?

## Approval Gate

Implementation begins only after:

1. Derek answers the decision questions or approves default assumptions.
2. The architecture is frozen.
3. Derek says: **LAUNCH APPROVED**

## Derek's Phase 0A Selections

Locked planning choices:

1. Walkthrough speed: **Ultra beginner** — explain every command, folder, and tool.
2. Project location: **GitHub-backed project** — create/use a GitHub repository and work from a local cloned folder.
3. First build target: **Basic working skeleton first**, then make it beautiful.
4. Visual style: **Hybrid** — dark glass + HUD + finance terminal.
5. First integration group: **Local-only first** — notes, layout, settings before external APIs.
6. Command style: **One command at a time**.

GitHub setup selection so far:
- Repository: **Create a brand-new GitHub repo**
- Repo visibility: **Public**
- Repo name: **win11-c2-dashboard**
- Local folder: **C:\Users\Derek\Documents\GitHub\win11-c2-dashboard**
- First setup target: **Install/check tools first: Git, Node.js, Python, VS Code**
- Tool check: **Git installed and working**
- Tool check: **Node.js installed and working**
- Tool check: **Python installed and working**

Remaining GitHub setup details still need to be selected before setup begins.

## Default Assumptions Until Derek Answers

- Personal-use Windows 11 desktop app
- Electron + React/TypeScript frontend
- Python FastAPI local backend
- SQLite local database
- Dark futuristic glass/HUD hybrid UI
- Gmail read/modify/send, but no permanent-delete scope by default
- Wallets are read-only display/connect in v1
- Crypto uses public market data only in v1
- X is read-only in v1
- Terminal has dangerous-command warning enabled
- Notes are local-only in v1
- ChatGPT tile supports both official app launch and OpenAI API mode
- Claude Code opens in selected local project folder

Back in the main window. We’ll continue here and keep the roadmap as the master plan.

We are at **Phase 0: Beginner Setup + Build Path**.

No coding yet. First we choose the safest foundation so we do not build a messy app that breaks later.

## Phase 0A — Choose the Starting Setup

Reply like this:

`1A, 2C, 3A, 4E, 5B, 6A`

My recommended beginner choices are:

`1A, 2C, 3A, 4E, 5B, 6A`

### 1. How slow should I walk you through each step?

A. **Ultra beginner** — explain every command, every folder, every tool\
B. **Normal beginner** — explain the important stuff, keep moving\
C. **Fast mode** — mostly commands and quick notes

### 2. Where should we build the project on your PC?

A. Desktop\
B. Documents\
C. `C:\Projects\`\
D. Another location

### 3. What should we build first?

A. **Basic working skeleton first**, then make it beautiful\
B. Premium futuristic UI first\
C. Backend brain first\
D. Folder structure and documentation only

### 4. What visual style should we aim for?

A. Cyberpunk neon\
B. Glass HUD\
C. Military command center\
D. Luxury finance terminal\
E. Hybrid: dark glass + HUD + finance terminal

### 5. Which integrations should come first?

A. Local-only app first: notes, layout, settings\
B. Weather, news, crypto, and notes first\
C. Gmail and wallet integrations first\
D. Everything from the beginning

### 6. How should I give you commands later?

A. One command at a time\
B. Small batches\
C. Full script-style chunks\
D. Explain only, no copy/paste commands

After you answer, I’ll give you **Phase 0B: exact install checklist for Windows 11** with beginner explanations and no app code yet.\
