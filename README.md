# 🗃️ Product Management CRUD

![Category](https://img.shields.io/badge/MMEIA-01_CRUD-6f42c1)
![Python](https://img.shields.io/badge/Python-FastAPI-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791)
![Status](https://img.shields.io/badge/status-M1--M3%20complete-success)

A real, runnable product-management CRUD built as the **first MMEIA Reference Project**. It applies database design, API design, testing, deployment and Spec-Driven Development to a deliberately small domain.

## 📍 Portfolio Position

| Field | Value |
|---|---|
| **Collection** | MMEIA Reference Projects |
| **Reference** | `01_CRUD` |
| **Category** | CRUD / backend API |
| **Domain** | Products, categories and stock |
| **Engineering focus** | End-to-end delivery from specification to verified deployment |

## 🎯 What This Project Demonstrates

- Product and category management
- Stock management
- Explicit product lifecycle: `borrador → activo → descatalogado`
- Relational constraints enforced in PostgreSQL
- REST API contracts designed before implementation
- Automated tests against a real disposable PostgreSQL instance
- Docker-based deployment
- CI pipeline structure
- Technical decisions documented as project ADRs

## 🛠 Tech Stack

| Area | Technology |
|---|---|
| API | FastAPI |
| Database | PostgreSQL 16 |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Tests | Pytest |
| Deployment | Docker + Docker Compose |
| CI | GitHub Actions |

The stack is intentionally mainstream. The purpose of the project is to demonstrate **engineering decisions and verification**, not unusual framework choices.

## 🧭 Engineering Approach

This repository follows **Spec-Driven Development (SDD)**:

```text
spec.md
   ↓
requirements.md
   ↓
tasks.md
   ↓
design + contracts
   ↓
implementation
   ↓
verification evidence
```

The specification, requirements and implementation plan exist before the code they govern.

## ✅ Current Status

| Milestone | State | Evidence |
|---|---|---|
| M1 — Database | ✅ Complete | Real PostgreSQL constraint verification |
| M2 — API | ✅ Complete | 28 Pytest tests + real-server smoke test |
| M3 — Deployment | ✅ Complete | Docker Compose deployment and 5-point verification |
| M4 — Formal freeze | ⏳ Pending | Final review, CI confirmation and `v1.0.0` |

Current tagged delivery line: `v0.1.0` → `v0.2.0` → `v0.3.0`.

## 📂 Repository Structure

```text
.
├── spec.md
├── requirements.md
├── tasks.md
├── disenio.md
├── despliegue.md
├── api/
│   ├── contrato.md
│   └── VERIFICATION.md
├── db/
│   ├── schema.sql
│   └── VERIFICATION.md
├── docs/
│   ├── architecture.md
│   ├── decisions.md
│   └── deployment.md
├── src/
├── tests/
├── docker/
├── .env.example
└── .github/workflows/
```

## 📚 Key Documentation

| Document | Purpose |
|---|---|
| [`spec.md`](spec.md) | Exact product behaviour and scope |
| [`requirements.md`](requirements.md) | Functional and non-functional requirements |
| [`tasks.md`](tasks.md) | Milestones and implementation progress |
| [`disenio.md`](disenio.md) | Data-model design |
| [`api/contrato.md`](api/contrato.md) | API contracts |
| [`docs/architecture.md`](docs/architecture.md) | Architecture and rationale |
| [`docs/decisions.md`](docs/decisions.md) | Project engineering decisions |
| [`docs/deployment.md`](docs/deployment.md) | Deployment verification evidence |

## 💡 How to Use This Repository

This is a **reference implementation**, not a project to copy blindly. Its value is in comparing its requirements, decisions, contracts, implementation and verification evidence against another solution to the same problem.

## 🧭 MMEIA Reference Projects

| # | Category | Repository |
|---|---|---|
| 01 | 🗃️ CRUD | **mmeia-crud-product-management** |
| 02 | 🔐 Secure API | [mmeia-secure-task-api](https://github.com/JyanesDev/mmeia-secure-task-api) |
| 03 | 🏢 SaaS | [mmeia-multitenant-workspaces](https://github.com/JyanesDev/mmeia-multitenant-workspaces) |
| 04 | 🔌 MCP | [mmeia-notes-mcp-server](https://github.com/JyanesDev/mmeia-notes-mcp-server) |
| 05 | 🤖 RAG | [mmeia-support-rag](https://github.com/JyanesDev/mmeia-support-rag) |

## 👨‍💻 Author

**Jonay Yanes** — [GitHub profile](https://github.com/JyanesDev)
