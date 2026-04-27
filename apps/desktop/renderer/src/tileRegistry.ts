import {
  Activity,
  Bot,
  CalendarDays,
  ChartNoAxesCombined,
  Inbox,
  Newspaper,
  NotebookPen,
  PlugZap,
  Terminal,
  WalletCards,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";

export type TileStatus = "local" | "ready" | "planned" | "offline";
export type TileSize = "small" | "medium" | "wide";
export type RefreshStrategy =
  | "realtime"
  | "polling"
  | "manual"
  | "startup-only"
  | "event-triggered";

export type DashboardTileDefinition = {
  tileId: string;
  tileType: string;
  title: string;
  navLabel?: string;
  status: TileStatus;
  defaultSize: TileSize;
  refreshStrategy: RefreshStrategy;
  permissionsRequired: string[];
  dataSource: string;
  summary: string;
  detail: string;
  icon: LucideIcon;
  visibleByDefault: boolean;
  placeholder?: boolean;
};

export const tileRegistry: DashboardTileDefinition[] = [
  {
    tileId: "notes",
    tileType: "local.notes",
    title: "Notes",
    navLabel: "Notes",
    status: "local",
    defaultSize: "wide",
    refreshStrategy: "event-triggered",
    permissionsRequired: ["local-database"],
    dataSource: "SQLite notes API",
    summary: "Local-first",
    detail: "SQLite-backed notes are ready.",
    icon: NotebookPen,
    visibleByDefault: true,
  },
  {
    tileId: "gmail",
    tileType: "integration.gmail",
    title: "Gmail",
    navLabel: "Email",
    status: "planned",
    defaultSize: "medium",
    refreshStrategy: "manual",
    permissionsRequired: ["gmail-oauth"],
    dataSource: "Gmail connector",
    summary: "OAuth later",
    detail: "Unread count, search, drafts, replies.",
    icon: Inbox,
    visibleByDefault: true,
    placeholder: true,
  },
  {
    tileId: "weather",
    tileType: "integration.weather",
    title: "Weather",
    status: "planned",
    defaultSize: "medium",
    refreshStrategy: "polling",
    permissionsRequired: ["weather-provider-key"],
    dataSource: "Weather provider",
    summary: "Provider pending",
    detail: "Forecast, alerts, conditions.",
    icon: Activity,
    visibleByDefault: true,
    placeholder: true,
  },
  {
    tileId: "news",
    tileType: "integration.news",
    title: "News",
    status: "planned",
    defaultSize: "medium",
    refreshStrategy: "polling",
    permissionsRequired: [],
    dataSource: "RSS feeds",
    summary: "RSS planned",
    detail: "Sources, read state, saved links.",
    icon: Newspaper,
    visibleByDefault: true,
    placeholder: true,
  },
  {
    tileId: "terminal",
    tileType: "local.terminal",
    title: "Terminal",
    navLabel: "Terminal",
    status: "planned",
    defaultSize: "wide",
    refreshStrategy: "event-triggered",
    permissionsRequired: ["local-command-confirmation"],
    dataSource: "PowerShell session",
    summary: "Warning-gated",
    detail: "PowerShell with command audit log.",
    icon: Terminal,
    visibleByDefault: true,
    placeholder: true,
  },
  {
    tileId: "wallets",
    tileType: "integration.wallets",
    title: "Wallets",
    navLabel: "Wallets",
    status: "planned",
    defaultSize: "medium",
    refreshStrategy: "manual",
    permissionsRequired: ["wallet-readonly-connection"],
    dataSource: "MetaMask and Phantom",
    summary: "Read-only v1",
    detail: "MetaMask and Phantom balances.",
    icon: WalletCards,
    visibleByDefault: true,
    placeholder: true,
  },
  {
    tileId: "ai-tools",
    tileType: "integration.ai_tools",
    title: "AI Tools",
    navLabel: "AI Tools",
    status: "planned",
    defaultSize: "medium",
    refreshStrategy: "manual",
    permissionsRequired: ["provider-api-key"],
    dataSource: "Local tool launcher",
    summary: "Planned",
    detail: "Prompt pads, saved agents, and tool shortcuts.",
    icon: Bot,
    visibleByDefault: true,
    placeholder: true,
  },
  {
    tileId: "calendar",
    tileType: "integration.calendar",
    title: "Calendar",
    navLabel: "Calendar",
    status: "planned",
    defaultSize: "medium",
    refreshStrategy: "polling",
    permissionsRequired: ["calendar-oauth"],
    dataSource: "Calendar connector",
    summary: "Planned",
    detail: "Agenda, reminders, and schedule blocks.",
    icon: CalendarDays,
    visibleByDefault: true,
    placeholder: true,
  },
  {
    tileId: "markets",
    tileType: "integration.markets",
    title: "Markets",
    navLabel: "Markets",
    status: "planned",
    defaultSize: "wide",
    refreshStrategy: "realtime",
    permissionsRequired: [],
    dataSource: "Public market feeds",
    summary: "Planned",
    detail: "Crypto watchlists, alerts, and portfolio views.",
    icon: ChartNoAxesCombined,
    visibleByDefault: true,
    placeholder: true,
  },
  {
    tileId: "automation",
    tileType: "local.automation",
    title: "Automation",
    status: "planned",
    defaultSize: "medium",
    refreshStrategy: "event-triggered",
    permissionsRequired: ["local-command-confirmation"],
    dataSource: "Local workflow runner",
    summary: "Expansion slot",
    detail: "Manual-first workflows with audit trails.",
    icon: PlugZap,
    visibleByDefault: false,
    placeholder: true,
  },
];

export const visibleDashboardTiles = tileRegistry.filter((tile) => tile.visibleByDefault);
export const placeholderTileCount = tileRegistry.filter((tile) => tile.placeholder).length;
