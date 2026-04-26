import {
  Activity,
  Bot,
  CalendarDays,
  ChartNoAxesCombined,
  CircleDot,
  Command,
  Download,
  FileText,
  Inbox,
  LayoutDashboard,
  Lock,
  Mail,
  Newspaper,
  NotebookPen,
  Pencil,
  Pin,
  PinOff,
  Plus,
  Search,
  Settings,
  Share2,
  Sparkles,
  Terminal,
  Trash2,
  Upload,
  WalletCards,
  X,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import type { FormEvent } from "react";

import "./styles.css";

type HealthStatus = "checking" | "online" | "offline";

type HealthResponse = {
  status: string;
  service: string;
  version: string;
  timestamp_utc: string;
};

type HealthState = {
  status: HealthStatus;
  summary: string;
  detail: string;
};

type NoteStatus = "checking" | "ready" | "offline" | "saving";

type NoteRecord = {
  id: string;
  title: string;
  body: string;
  tags: string[];
  pinned: boolean;
  created_at: string;
  updated_at: string;
};

type NotesState = {
  status: NoteStatus;
  summary: string;
  detail: string;
  items: NoteRecord[];
};

type NavItem = {
  label: string;
  icon: LucideIcon;
  active?: boolean;
};

type MetricCard = {
  label: string;
  value: string;
  detail: string;
  tone: "positive" | "neutral" | "warning" | "danger";
};

type ModuleCard = {
  title: string;
  status: string;
  detail: string;
  icon: LucideIcon;
  active?: boolean;
};

const navItems: NavItem[] = [
  { label: "Dashboard", icon: LayoutDashboard, active: true },
  { label: "Calendar", icon: CalendarDays },
  { label: "Email", icon: Mail },
  { label: "Markets", icon: ChartNoAxesCombined },
  { label: "Notes", icon: NotebookPen },
  { label: "AI Tools", icon: Bot },
  { label: "Terminal", icon: Terminal },
  { label: "Wallets", icon: WalletCards },
  { label: "Settings", icon: Settings },
];

const metrics: MetricCard[] = [
  {
    label: "Backend health",
    value: "Live",
    detail: "FastAPI status feed",
    tone: "positive",
  },
  {
    label: "Active modules",
    value: "8",
    detail: "Planned dashboard tiles",
    tone: "neutral",
  },
  {
    label: "Local mode",
    value: "On",
    detail: "No external secrets loaded",
    tone: "positive",
  },
  {
    label: "Security gate",
    value: "Strict",
    detail: "Send/sign/delete confirmations",
    tone: "warning",
  },
  {
    label: "Expansion slots",
    value: "3",
    detail: "Automation, calendar, analytics",
    tone: "neutral",
  },
];

const baseModules: ModuleCard[] = [
  {
    title: "Notes",
    status: "Local-first",
    detail: "SQLite-backed notes are ready.",
    icon: NotebookPen,
    active: true,
  },
  {
    title: "Gmail",
    status: "OAuth later",
    detail: "Unread count, search, drafts, replies.",
    icon: Inbox,
  },
  {
    title: "Weather",
    status: "Provider pending",
    detail: "Forecast, alerts, conditions.",
    icon: Activity,
  },
  {
    title: "News",
    status: "RSS planned",
    detail: "Sources, read state, saved links.",
    icon: Newspaper,
  },
  {
    title: "Terminal",
    status: "Warning-gated",
    detail: "PowerShell with command audit log.",
    icon: Terminal,
  },
  {
    title: "Wallets",
    status: "Read-only v1",
    detail: "MetaMask and Phantom balances.",
    icon: WalletCards,
  },
];

const progressItems = [
  { label: "Foundation", value: "100%", amount: "Repo, docs, scaffold", progress: 100 },
  { label: "Backend", value: "30%", amount: "Health endpoint online", progress: 30 },
  { label: "Frontend", value: "35%", amount: "Dashboard shell live", progress: 35 },
  { label: "Local data", value: "20%", amount: "Notes API online", progress: 20 },
];

const tickerItems = [
  { symbol: "BTC", price: "$--,--", change: "waiting" },
  { symbol: "ETH", price: "$-,---", change: "waiting" },
  { symbol: "SOL", price: "$---", change: "waiting" },
  { symbol: "BNB", price: "$---", change: "waiting" },
  { symbol: "BASE", price: "tracked later", change: "planned" },
];

const healthUrl =
  import.meta.env.VITE_BACKEND_HEALTH_URL ?? "http://127.0.0.1:8765/health";
const notesUrl = import.meta.env.VITE_BACKEND_NOTES_URL ?? "http://127.0.0.1:8765/notes";

function formatHealthTimestamp(timestampUtc: string) {
  const date = new Date(timestampUtc);

  if (Number.isNaN(date.getTime())) {
    return "time unknown";
  }

  return date.toLocaleTimeString([], {
    hour: "numeric",
    minute: "2-digit",
    second: "2-digit",
  });
}

function formatDashboardDate(date: Date) {
  return date.toLocaleDateString([], {
    weekday: "long",
    month: "long",
    day: "numeric",
    year: "numeric",
  });
}

function getGreeting(date: Date) {
  const hour = date.getHours();

  if (hour < 12) {
    return "Good morning";
  }

  if (hour < 18) {
    return "Good afternoon";
  }

  return "Good evening";
}

async function requestNotes(signal?: AbortSignal) {
  const response = await fetch(notesUrl, { signal });

  if (!response.ok) {
    throw new Error(`Notes request failed with HTTP ${response.status}`);
  }

  return (await response.json()) as NoteRecord[];
}

async function createDashboardNote(payload: { title: string; body: string }) {
  const response = await fetch(notesUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      title: payload.title,
      body: payload.body,
      tags: ["dashboard"],
      pinned: false,
    }),
  });

  if (!response.ok) {
    throw new Error(`Note save failed with HTTP ${response.status}`);
  }

  return (await response.json()) as NoteRecord;
}

async function updateDashboardNote(
  noteId: string,
  payload: Partial<Pick<NoteRecord, "title" | "body" | "tags" | "pinned">>,
) {
  const response = await fetch(`${notesUrl}/${noteId}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`Note update failed with HTTP ${response.status}`);
  }

  return (await response.json()) as NoteRecord;
}

async function deleteDashboardNote(noteId: string) {
  const response = await fetch(`${notesUrl}/${noteId}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    throw new Error(`Note delete failed with HTTP ${response.status}`);
  }
}

function App() {
  const [now, setNow] = useState(() => new Date());
  const [health, setHealth] = useState<HealthState>({
    status: "checking",
    summary: "Checking",
    detail: "Contacting local backend",
  });
  const [notes, setNotes] = useState<NotesState>({
    status: "checking",
    summary: "Checking",
    detail: "Loading local notes",
    items: [],
  });
  const [noteTitle, setNoteTitle] = useState("");
  const [noteBody, setNoteBody] = useState("");
  const [editingNoteId, setEditingNoteId] = useState<string | null>(null);

  useEffect(() => {
    const intervalId = window.setInterval(() => setNow(new Date()), 60000);
    return () => window.clearInterval(intervalId);
  }, []);

  useEffect(() => {
    let isMounted = true;

    async function checkHealth() {
      const controller = new AbortController();
      const timeoutId = window.setTimeout(() => controller.abort(), 4000);

      try {
        const response = await fetch(healthUrl, {
          signal: controller.signal,
        });

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        const payload = (await response.json()) as HealthResponse;

        if (!isMounted) {
          return;
        }

        setHealth({
          status: payload.status === "ok" ? "online" : "offline",
          summary: payload.status === "ok" ? "Online" : "Degraded",
          detail: `${payload.service} ${payload.version} at ${formatHealthTimestamp(
            payload.timestamp_utc,
          )}`,
        });
      } catch (error) {
        if (!isMounted) {
          return;
        }

        const detail =
          error instanceof Error && error.name === "AbortError"
            ? "Backend health check timed out"
            : "Start FastAPI on port 8765";

        setHealth({
          status: "offline",
          summary: "Offline",
          detail,
        });
      } finally {
        window.clearTimeout(timeoutId);
      }
    }

    void checkHealth();
    const intervalId = window.setInterval(checkHealth, 30000);

    return () => {
      isMounted = false;
      window.clearInterval(intervalId);
    };
  }, []);

  useEffect(() => {
    let isMounted = true;
    const controller = new AbortController();

    async function loadNotes() {
      try {
        const items = await requestNotes(controller.signal);

        if (!isMounted) {
          return;
        }

        setNotes({
          status: "ready",
          summary: `${items.length} saved`,
          detail: items.length > 0 ? "SQLite notes API connected" : "Ready for first note",
          items,
        });
      } catch {
        if (!isMounted) {
          return;
        }

        setNotes({
          status: "offline",
          summary: "Offline",
          detail: "Start backend to load notes",
          items: [],
        });
      }
    }

    void loadNotes();

    return () => {
      isMounted = false;
      controller.abort();
    };
  }, []);

  function setLoadedNotes(items: NoteRecord[], detail: string) {
    setNotes({
      status: "ready",
      summary: `${items.length} saved`,
      detail: items.length > 0 ? detail : "Ready for first note",
      items,
    });
  }

  async function handleNoteSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!noteBody.trim()) {
      return;
    }

    setNotes((current) => ({
      ...current,
      status: "saving",
      summary: "Saving",
      detail: "Writing note to SQLite",
    }));

    try {
      if (editingNoteId) {
        await updateDashboardNote(editingNoteId, {
          title: noteTitle.trim() || "Dashboard note",
          body: noteBody.trim(),
        });
      } else {
        await createDashboardNote({
          title: noteTitle.trim() || "Dashboard note",
          body: noteBody.trim(),
        });
      }

      const items = await requestNotes();

      setLoadedNotes(items, editingNoteId ? "Note updated locally" : "Latest note saved locally");
      setNoteTitle("");
      setNoteBody("");
      setEditingNoteId(null);
    } catch {
      setNotes((current) => ({
        ...current,
        status: "offline",
        summary: "Save failed",
        detail: "Check backend on port 8765",
      }));
    }
  }

  function startEditingNote(note: NoteRecord) {
    setEditingNoteId(note.id);
    setNoteTitle(note.title);
    setNoteBody(note.body);
  }

  function cancelEditingNote() {
    setEditingNoteId(null);
    setNoteTitle("");
    setNoteBody("");
  }

  async function handlePinToggle(note: NoteRecord) {
    setNotes((current) => ({
      ...current,
      status: "saving",
      summary: note.pinned ? "Unpinning" : "Pinning",
      detail: "Updating local note",
    }));

    try {
      await updateDashboardNote(note.id, {
        pinned: !note.pinned,
      });
      const items = await requestNotes();
      setLoadedNotes(items, note.pinned ? "Note unpinned" : "Note pinned");
    } catch {
      setNotes((current) => ({
        ...current,
        status: "offline",
        summary: "Update failed",
        detail: "Check backend on port 8765",
      }));
    }
  }

  async function handleDeleteNote(note: NoteRecord) {
    const confirmed = window.confirm(`Delete "${note.title}"?`);

    if (!confirmed) {
      return;
    }

    setNotes((current) => ({
      ...current,
      status: "saving",
      summary: "Deleting",
      detail: "Removing local note",
    }));

    try {
      await deleteDashboardNote(note.id);
      const items = await requestNotes();
      setLoadedNotes(items, "Note deleted locally");

      if (editingNoteId === note.id) {
        cancelEditingNote();
      }
    } catch {
      setNotes((current) => ({
        ...current,
        status: "offline",
        summary: "Delete failed",
        detail: "Check backend on port 8765",
      }));
    }
  }

  const liveHealthTone = useMemo(() => {
    if (health.status === "online") {
      return "positive";
    }

    if (health.status === "checking") {
      return "warning";
    }

    return "danger";
  }, [health.status]);

  const currentMetrics = useMemo(
    () =>
      metrics.map((metric) =>
        metric.label === "Backend health"
          ? {
              ...metric,
              value: health.summary,
              detail: health.detail,
              tone: liveHealthTone,
            }
          : metric,
      ),
    [health.detail, health.summary, liveHealthTone],
  );

  const currentModules = useMemo(
    () =>
      baseModules.map((module) =>
        module.title === "Notes"
          ? {
              ...module,
              status: notes.summary,
              detail:
                notes.status === "ready" && notes.items.length > 0
                  ? `Latest: ${notes.items[0].title}`
                  : notes.detail,
            }
          : module,
      ),
    [notes.detail, notes.items, notes.status, notes.summary],
  );

  return (
    <main className="dashboard-shell">
      <aside className="sidebar" aria-label="Dashboard sections">
        <div className="brand-lockup">
          <div className="brand-icon">
            <Command size={22} />
          </div>
          <div>
            <strong>C2</strong>
            <span>COMMAND CENTER</span>
          </div>
          <span className="beta-pill">BETA</span>
        </div>

        <div className="sidebar-rule" />

        <p className="sidebar-label">Operations</p>
        <nav className="side-nav">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <button
                className={item.active ? "side-nav-button active" : "side-nav-button"}
                key={item.label}
                type="button"
              >
                <Icon size={18} />
                <span>{item.label}</span>
                {item.active ? <CircleDot size={12} /> : null}
              </button>
            );
          })}
        </nav>
      </aside>

      <section className="page-shell" aria-label="Command center dashboard">
        <header className="page-header">
          <h1>Dashboard</h1>
          <div className="header-actions">
            <button className="toolbar-button" type="button">
              <Upload size={15} />
              <span>Import</span>
            </button>
            <button className="toolbar-button" type="button">
              <Download size={15} />
              <span>Export</span>
            </button>
            <button className="toolbar-button" type="button">
              <FileText size={15} />
              <span>Report</span>
            </button>
            <button className="icon-button" title="Privacy lock" type="button">
              <Lock size={17} />
            </button>
            <button className="primary-action" type="button">
              <Plus size={18} />
              <span>Add Tile</span>
            </button>
          </div>
        </header>

        <section className="content-surface">
          <section className="welcome-panel">
            <div>
              <div className="welcome-title-row">
                <h2>{getGreeting(now)}, Derek</h2>
                <span className="rank-badge">
                  <Sparkles size={14} />
                  LOCAL 1
                </span>
              </div>
              <p className="date-row">
                <CalendarDays size={15} />
                {formatDashboardDate(now)}
              </p>
              <p className="green-copy">Stay modular and keep every tile isolated.</p>
            </div>

            <div className="welcome-actions">
              <div className={`today-card health-${health.status}`}>
                <span>Backend</span>
                <strong>{health.summary}</strong>
              </div>
              <button className="share-button" type="button">
                <Share2 size={17} />
                <span>Share</span>
              </button>
            </div>
          </section>

          <section className="metric-grid" aria-label="System metrics">
            {currentMetrics.map((metric) => (
              <article className={`metric-card tone-${metric.tone}`} key={metric.label}>
                <span>{metric.label}</span>
                <strong>{metric.value}</strong>
                <p>{metric.detail}</p>
              </article>
            ))}
          </section>

          <section className="mini-grid" aria-label="Module summary">
            {currentModules.map((module) => {
              const Icon = module.icon;
              return (
                <article className={module.active ? "module-card active" : "module-card"} key={module.title}>
                  <Icon size={17} />
                  <div>
                    <span>{module.title}</span>
                    <strong>{module.status}</strong>
                    <p>{module.detail}</p>
                  </div>
                </article>
              );
            })}
          </section>

          <section className="lower-dashboard">
            <article className="progress-panel">
              <header className="panel-heading">
                <div>
                  <CircleDot size={15} />
                  <h2>Build Progress</h2>
                </div>
                <button className="ghost-action" type="button">
                  <Search size={15} />
                  <span>Inspect</span>
                </button>
              </header>

              <div className="progress-grid">
                {progressItems.map((item) => (
                  <div className="progress-card" key={item.label}>
                    <div className="progress-card-header">
                      <span>{item.label}</span>
                      <strong>{item.value}</strong>
                    </div>
                    <p>{item.amount}</p>
                    <div className="progress-track">
                      <span style={{ width: `${item.progress}%` }} />
                    </div>
                  </div>
                ))}
              </div>
            </article>

            <article className={`notes-panel notes-${notes.status}`}>
              <header className="panel-heading">
                <div>
                  <NotebookPen size={15} />
                  <h2>Quick Notes</h2>
                </div>
                <span className="notes-status">{notes.summary}</span>
              </header>

              <form className="note-form" onSubmit={handleNoteSubmit}>
                <input
                  aria-label="Note title"
                  onChange={(event) => setNoteTitle(event.target.value)}
                  placeholder="Title"
                  value={noteTitle}
                />
                <textarea
                  aria-label="Note body"
                  onChange={(event) => setNoteBody(event.target.value)}
                  placeholder="Capture a thought"
                  rows={4}
                  value={noteBody}
                />
                <div className="note-form-actions">
                  <button className="primary-action" disabled={!noteBody.trim()} type="submit">
                    <Plus size={17} />
                    <span>
                      {notes.status === "saving"
                        ? "Saving"
                        : editingNoteId
                          ? "Update Note"
                          : "Save Note"}
                    </span>
                  </button>
                  {editingNoteId ? (
                    <button className="ghost-action" onClick={cancelEditingNote} type="button">
                      <X size={16} />
                      <span>Cancel</span>
                    </button>
                  ) : null}
                </div>
              </form>

              <div className="notes-list" aria-label="Recent notes">
                {notes.items.slice(0, 3).map((note) => (
                  <article
                    className={note.pinned ? "note-preview pinned" : "note-preview"}
                    key={note.id}
                  >
                    <div className="note-preview-header">
                      <strong>{note.title}</strong>
                      <div className="note-actions">
                        <button
                          className="note-icon-button"
                          onClick={() => void handlePinToggle(note)}
                          title={note.pinned ? "Unpin note" : "Pin note"}
                          type="button"
                        >
                          {note.pinned ? <PinOff size={14} /> : <Pin size={14} />}
                        </button>
                        <button
                          className="note-icon-button"
                          onClick={() => startEditingNote(note)}
                          title="Edit note"
                          type="button"
                        >
                          <Pencil size={14} />
                        </button>
                        <button
                          className="note-icon-button danger"
                          onClick={() => void handleDeleteNote(note)}
                          title="Delete note"
                          type="button"
                        >
                          <Trash2 size={14} />
                        </button>
                      </div>
                    </div>
                    <p>{note.body}</p>
                  </article>
                ))}
                {notes.items.length === 0 ? (
                  <div className="empty-notes">
                    <span>{notes.detail}</span>
                  </div>
                ) : null}
              </div>
            </article>
          </section>
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
