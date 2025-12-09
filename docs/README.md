> [!WARNING]
> This project is not production-ready since it's currently in beta phase and has no proper documentation yet

# ax
Portable and lightweight TCP chatting server with straightforward configuration and deployment

## Features
- Containerized with Docker
- Dependency-free
- Simple and hackable source code

## Server-side payloads
- SLOW_DOWN
- PING
- MISSING_NICK
- UNAUTHORIZED
- NICK_ALREADY_SET
- INVALID_NICK
- NICK_TAKEN
- SET_NICK|<desired_nickname>
- NEW_USER_MESSAGE|<author>|<content>