import {
  Activity,
  Bot,
  CloudSun,
  Command,
  Cpu,
  Gauge,
  Inbox,
  LayoutDashboard,
  Lock,
  Mail,
  Newspaper,
  NotebookPen,
  PlugZap,
  Search,
  Settings,
  ShieldCheck,
  Terminal,
  WalletCards,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";

import "./styles.css";

type TileStatus = "ready" | "local" | "planned" | "offline";

type DashboardTile = {
  id: string;
  title: string;
  eyebrow: string;
  status: TileStatus;
  metric: string;
  detail: string;
  accent: "cyan" | "green" | "amber" | "rose" | "violet" | "blue";
  icon: LucideIcon;
};

const navItems = [
  { label: "Dashboard", icon: LayoutDashboard },
  { label: "Email", icon: Mail },
  { label: "Markets", icon: Activity },
  { label: "Notes", icon: NotebookPen },
  { label: "AI", icon: Bot },
  { label: "Wallets", icon: WalletCards },
  { label: "Settings", icon: Settings },
];

const tiles: DashboardTile[] = [
  {
    id: "gmail",
    title: "Gmail",
    eyebrow: "Integration planned",
    status: "planned",
    metric: "OAuth later",
    detail: "Unread count, priority inbox, search, drafts, and send confirmation.",
    accent: "blue",
    icon: Inbox,
  },
  {
    id: "weather",
    title: "Weather",
    eyebrow: "Provider pending",
    status: "planned",
    metric: "Home forecast",
    detail: "Current conditions, alerts, hourly view, and seven-day outlook.",
    accent: "cyan",
    icon: CloudSun,
  },
  {
    id: "news",
    title: "News Feeds",
    eyebrow: "RSS ready next",
    status: "planned",
    metric: "Sources",
    detail: "Headlines, read state, article links, and save-to-notes flow.",
    accent: "amber",
    icon: Newspaper,
  },
  {
    id: "notes",
    title: "Notes",
    eyebrow: "Local-first",
    status: "local",
    metric: "Draft space",
    detail: "Pinned notes, tags, local search, and future dictation support.",
    accent: "green",
    icon: NotebookPen,
  },
  {
    id: "terminal",
    title: "Terminal",
    eyebrow: "Safety gated",
    status: "planned",
    metric: "PowerShell",
    detail: "Command history, clear working directory, and warning gates.",
    accent: "violet",
    icon: Terminal,
  },
  {
    id: "ai",
    title: "AI Tools",
    eyebrow: "Launcher mode",
    status: "planned",
    metric: "Chat + Code",
    detail: "ChatGPT launcher/API mode and Claude Code workspace sessions.",
    accent: "rose",
    icon: Bot,
  },
  {
    id: "wallets",
    title: "Wallets",
    eyebrow: "Read-only v1",
    status: "planned",
    metric: "No signing",
    detail: "MetaMask and Phantom balances through approved wallet flows.",
    accent: "amber",
    icon: WalletCards,
  },
  {
    id: "expansion",
    title: "Expansion Slots",
    eyebrow: "Reserved",
    status: "ready",
    metric: "3 slots",
    detail: "Automation, calendar/tasks, and market analytics placeholders.",
    accent: "cyan",
    icon: PlugZap,
  },
];

const tickerItems = [
  { symbol: "BTC", price: "$--,--", change: "waiting", tone: "neutral" },
  { symbol: "ETH", price: "$-,---", change: "waiting", tone: "neutral" },
  { symbol: "SOL", price: "$---", change: "waiting", tone: "neutral" },
  { symbol: "BNB", price: "$---", change: "waiting", tone: "neutral" },
  { symbol: "BASE", price: "tracked later", change: "planned", tone: "neutral" },
];

function App() {
  return (
    <main className="dashboard-shell">
      <aside className="utility-rail" aria-label="Dashboard sections">
        <div className="brand-mark" aria-label="Win11 C2 Dashboard">
          <Command size={22} />
        </div>
        <nav className="rail-nav">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <button
                className="rail-button"
                key={item.label}
                title={item.label}
                type="button"
              >
                <Icon size={20} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </aside>

      <section className="workspace" aria-label="Command center dashboard">
        <header className="top-command-bar">
          <div>
            <p className="kicker">Local command center</p>
            <h1>Win11 C2 Dashboard</h1>
          </div>

          <label className="global-search">
            <Search size={18} />
            <input aria-label="Global search" placeholder="Search notes, tiles, commands" />
          </label>

          <div className="status-cluster" aria-label="System status">
            <span className="status-pill online">
              <ShieldCheck size={16} />
              Local safe
            </span>
            <button className="icon-button" title="Privacy lock" type="button">
              <Lock size={18} />
            </button>
            <button className="icon-button" title="Settings" type="button">
              <Settings size={18} />
            </button>
          </div>
        </header>

        <section className="overview-strip" aria-label="System overview">
          <div className="overview-item">
            <Gauge size={18} />
            <span>Backend health</span>
            <strong>Ready</strong>
          </div>
          <div className="overview-item">
            <Cpu size={18} />
            <span>Mode</span>
            <strong>Local-first</strong>
          </div>
          <div className="overview-item">
            <Activity size={18} />
            <span>Tiles</span>
            <strong>8 planned</strong>
          </div>
        </section>

        <section className="tile-grid" aria-label="Dashboard tiles">
          {tiles.map((tile) => {
            const Icon = tile.icon;
            return (
              <article className={`dashboard-tile accent-${tile.accent}`} key={tile.id}>
                <header className="tile-header">
                  <div className="tile-icon">
                    <Icon size={20} />
                  </div>
                  <div>
                    <p>{tile.eyebrow}</p>
                    <h2>{tile.title}</h2>
                  </div>
                  <span className={`tile-status status-${tile.status}`}>{tile.status}</span>
                </header>
                <div className="tile-metric">{tile.metric}</div>
                <p className="tile-detail">{tile.detail}</p>
              </article>
            );
          })}
        </section>
      </section>

      <footer className="market-ticker" aria-label="Crypto ticker placeholder">
        <div className="ticker-track">
          {[...tickerItems, ...tickerItems].map((item, index) => (
            <span className="ticker-item" key={`${item.symbol}-${index}`}>
              <strong>{item.symbol}</strong>
              <span>{item.price}</span>
              <em>{item.change}</em>
            </span>
          ))}
        </div>
      </footer>
    </main>
  );
}

export default App;
