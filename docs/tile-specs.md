# Tile Specs

Every dashboard tile should follow the same basic contract so tiles can be replaced or upgraded independently.

## Base Tile Contract

- `tile_id`
- `tile_type`
- `title`
- `size`
- `refresh_strategy`
- `permissions_required`
- `data_source`
- `loading_state`
- `error_state`
- `offline_state`
- `last_updated_at`
- `actions`
- `settings`

## Refresh Strategies

- Real-time WebSocket
- Polling interval
- Manual refresh
- Event-triggered refresh
- Startup-only refresh

## Required States

- Loading
- Ready
- Offline
- Error
- Reconnecting

## First Local Tiles

- Notes tile
- Settings/status tile
- Expansion slot tiles
- Placeholder tiles for future integrations

