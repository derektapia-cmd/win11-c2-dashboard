# API Integrations

This document tracks planned integrations and their first safe scope.

## V1 Local-Only Foundation

- Notes: local SQLite storage
- Layout: saved tile positions/settings
- Settings: local preferences
- Audit log: local event records

## V1 External Candidates

- Weather provider for current conditions and forecast
- RSS/news feeds
- CoinGecko public market prices
- Binance public market data

## Later Integrations

- Gmail OAuth
- X API/OAuth
- OpenAI API
- Claude Code launcher
- MetaMask wallet connection
- Phantom wallet connection

## Rules

- Frontend should not call external APIs directly except wallet-provider flows when required.
- Secrets and OAuth tokens stay out of the renderer process.
- Each integration must expose loading, offline, error, and reconnect states.

