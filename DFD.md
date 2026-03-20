# 📊 Diagrama de Fluxo de Dados (DFD) - Salão V2.2

## 🗺️ DFD Nível 0 - Diagrama de Contexto

Diagrama de contexto mostrando o sistema como um processo único interagindo com entidades externas.

```mermaid
flowchart TD
    A[Recepcionista] -->|Solicita Agendamento<br/>Consulta Agenda| SYS[Sistema Salão V2.2]
    B[Admin] -->|Gerencia Usuários<br/>Relatórios| SYS
    C[Cliente] -->|Dados Pessoais| SYS
    
    SYS -->|Confirmação Agendamento<br/>Relatórios PDF| A
    SYS -->|Acesso Portal?| C
    SYS -->|Relatórios Gerenciais| B
    
    style SYS fill:#e1f5fe
```

## 🔍 DFD Nível 1 - Decomposição Principal

Decomposição em processos principais com fluxos de dados e repositórios.

```mermaid
flowchart TD
    %% Entidades Externas
    RE[Recepcionista] 
    AD[Admin]
    CL[Cliente]
    
    %% Processos (círculos)
    P1[1.0<br/>Gerenciar Agendamentos]
    P2[2.0<br/>Gerenciar Clientes]
    P3[3.0<br/>Gerenciar Profissionais]
    P4[4.0<br/>Gerenciar Serviços]
    P5[5.0<br/>Controle de Estoque]
    P6[6.0<br/>Gerar Relatórios]
    
    %% Data Stores (aberto retângulo)
    D1[(D1<br/>Clientes)]
    D2[(D2<br/>Agendamentos)]
    D3[(D3<br/>Profissionais)]
    D4[(D4<br/>Serviços)]
    D5[(D5<br/>Estoque)]
    
    %% Fluxos
    RE -->|Solicita Agendamento| P1
    RE -->|Consulta Agenda| P1
    CL -->|Dados Cliente| P2
    
    P1 -->|Cria/Atualiza Agendamento| D2
    P1 -->|Vincula Cliente/Profissional/Serviço| D2
    P1 -.->|Lista Disponibilidade| P3
    
    P2 <-->|CRUD Clientes| D1
    P2 -->|Cliente para Agendamento| P1
    
    P3 <-->|CRUD Profissionais| D3
    P3 -->|Agenda Profissional| P1
    
    P4 <-->|CRUD Serviços| D4
    P4 -->|Serviço para Agendamento| P1
    
    P5 <-->|Entradas/Saídas Estoque| D5
    P5 -.->|Produtos Usados| P1
    
    P6 -->|Relatórios PDF| AD
    P6 -.->|Dados Agendamentos/Clientes| D2
    P6 -.->|Dados Clientes| D1
    
    AD -->|Configura Sistema| P6
    AD -.->|Gerencia Usuários| P2
    
    %% Estilos
    classDef entity fill:#fff3e0,stroke:#ff9800
    classDef process fill:#e8f5e8,stroke:#4caf50,stroke-width:3px
    classDef datastore fill:#f3e5f5,stroke:#9c27b0
    
    class RE,AD,CL entity
    class P1,P2,P3,P4,P5,P6 process
    class D1,D2,D3,D4,D5 datastore
```

## 📋 Legenda
| Símbolo | Descrição |
|---------|-----------|
| `Retângulo` | **Entidade Externa** (Usuários reais) |
| `Círculo/Elipse` | **Processo** (Função do sistema) |
| `Retângulo aberto` | **Repositório de Dados** (Banco SQLite) |
| `Seta` | **Fluxo de Dados** |
| `Linha tracejada` | **Fluxo de Controle** |

## 🔗 Fluxos Principais Detalhados

### 1. Fluxo de Agendamento (Core)
```
Recepcionista → [1.0 Gerenciar Agendamentos] ← Clientes
                      ↓
             [Consulta Profissionais/Serviços]
                      ↓
                 Salva em D2 (Agendamentos)
                      ↓
              Atualiza Estoque (se produtos)
```

### 2. Geração de Relatórios
```
Admin → [6.0 Relatórios] → Consulta D1,D2,D3 → PDF → Admin
```

## 📈 Observações
- **Banco Centralizado**: SQLite `db.sqlite3` contém todos repositórios (D1-D5).
- **Segurança**: Recepcionista tem acesso restrito (sem relatórios).
- **Integrações**: Calendário visual, PDFs via ReportLab.

**Visualize no VSCode**: Instale extensão "Mermaid Preview" ou abra no GitHub!


