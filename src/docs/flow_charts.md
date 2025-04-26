# WhatsApp Auto Sender - Flow Charts

## 1. Application Initialization
```mermaid
flowchart TD
    A[Start Application] --> B[Load Configuration]
    B --> C[Initialize WhatsApp Desktop]
    C --> D[Setup File Watcher]
    D --> E[Create GUI Interface]
    E --> F[Ready for Monitoring]
    
    C -->|Failed| G[Show Error Message]
    G --> H[Exit Application]
```

## 2. File Monitoring Process
```mermaid
flowchart TD
    A[Start Monitoring] --> B[Watch Folder]
    B --> C{New File Detected?}
    C -->|No| B
    C -->|Yes| D[Check File Readiness]
    D -->|Not Ready| B
    D -->|Ready| E[Extract Contact Name]
    E --> F[Open WhatsApp Chat]
    F -->|Failed| G[Log Error]
    G --> B
    F -->|Success| H[Attach File]
    H -->|Failed| G
    H -->|Success| I[Send Message]
    I -->|Failed| G
    I -->|Success| J[Log Success]
    J --> B
```

## 3. WhatsApp Automation Flow
```mermaid
flowchart TD
    A[Start WhatsApp Operation] --> B[Connect to WhatsApp]
    B -->|Failed| C[Retry Connection]
    C -->|Max Retries| D[Log Error]
    C -->|Success| E[Open Chat]
    B -->|Success| E
    E -->|Failed| F[Retry Open Chat]
    F -->|Max Retries| D
    F -->|Success| G[Attach File]
    E -->|Success| G
    G -->|Failed| H[Retry Attach]
    H -->|Max Retries| D
    H -->|Success| I[Send Message]
    G -->|Success| I
    I -->|Failed| J[Retry Send]
    J -->|Max Retries| D
    J -->|Success| K[Operation Complete]
    I -->|Success| K
```

## 4. Error Handling Flow
```mermaid
flowchart TD
    A[Error Occurs] --> B{Error Type?}
    B -->|Connection Error| C[Retry Connection]
    B -->|File Error| D[Skip File]
    B -->|WhatsApp Error| E[Retry Operation]
    
    C -->|Success| F[Continue]
    C -->|Failed| G[Show Critical Error]
    
    D --> H[Log Error]
    H --> I[Continue Monitoring]
    
    E -->|Success| F
    E -->|Failed| G
    
    G --> J[Stop Monitoring]
    F --> K[Continue Operation]
```

## 5. File Processing Decision Tree
```mermaid
flowchart TD
    A[New File Detected] --> B{Valid Extension?}
    B -->|No| C[Skip File]
    B -->|Yes| D{File Locked?}
    D -->|Yes| E[Wait & Retry]
    D -->|No| F{File Age > 5s?}
    F -->|No| E
    F -->|Yes| G{Already Processed?}
    G -->|Yes| C
    G -->|No| H[Process File]
    
    E -->|Max Retries| C
    E -->|Not Max| D
```

## 6. Configuration Management
```mermaid
flowchart TD
    A[Load Configuration] --> B{Config File Exists?}
    B -->|No| C[Create Default Config]
    B -->|Yes| D[Load Config File]
    C --> E[Validate Settings]
    D --> E
    E -->|Invalid| F[Use Defaults]
    E -->|Valid| G[Apply Settings]
    F --> G
```

## 7. GUI State Management
```mermaid
flowchart TD
    A[GUI Initialized] --> B{Monitoring State}
    B -->|Not Monitoring| C[Enable Start Button]
    B -->|Monitoring| D[Enable Stop Button]
    
    C --> E[Show Ready Status]
    D --> F[Show Monitoring Status]
    
    E --> G[Update Activity Log]
    F --> G
    
    G --> H[Handle User Input]
    H -->|Start Clicked| I[Start Monitoring]
    H -->|Stop Clicked| J[Stop Monitoring]
    
    I --> B
    J --> B
``` 