# Network Event Monitoring System (UDP-based)

## 📌 Overview

This project implements a **distributed network monitoring system** where multiple client nodes send network events (such as latency, packet loss, CPU usage) to a central server using **UDP sockets**.

The system supports:

- Multiple clients connecting to a single server
- Secure communication using **HMAC authentication**
- Event classification
- Network-wide anomaly detection (aggregation)
- Real-time dashboard display
- Performance evaluation (latency and throughput)

---

## 🏗️ System Architecture

```
Clients (Multiple Nodes)
        ↓
   UDP Packets
        ↓
     Server
  ┌────────────────────┐
  │ HMAC Verification  │
  │ Classification     │
  │ Aggregation        │
  │ Dashboard          │
  └────────────────────┘
```

---

## 📂 Project Structure

```
network-monitor/

server.py       # Main server (processing, aggregation, dashboard)
client.py       # Simulates network nodes (event generator)
security.py     # HMAC authentication logic
classifier.py   # Event classification rules
config.py       # Configuration (IP, port)
```

---

## ⚙️ Features

### ✅ Multi-Client Support

- Multiple clients can send data concurrently
- Can run on different devices on the same network

---

### 🔐 Security (HMAC Authentication)

- Uses **HMAC with SHA-256**
- Ensures:
  - Message integrity
  - Authentication
  - Tamper detection

---

### 📊 Event Classification

| Event Type  | Classification             |
| ----------- | -------------------------- |
| latency     | NORMAL / CONGESTION        |
| packet_loss | NORMAL / WARNING / FAILURE |
| cpu_usage   | NORMAL / HIGH / OVERLOAD   |
| node_down   | NORMAL / NODE_FAILURE      |

---

### 🚨 Aggregation (Anomaly Detection)

Detects network-wide issues:

- High latency across multiple nodes → **Network Congestion**
- Multiple node failures → **System Failure**

---

### 📈 Performance Metrics

The server computes:

- **Latency** → time difference between event generation and reception
- **Throughput** → events processed per second
- **Total events processed**

---

### 🖥️ Dashboard

Displays:

- Number of active nodes
- Latest event per node
- Classification of each node

---

## 🚀 How to Run

### 1️⃣ Start the Server

```bash
python server.py
```

---

### 2️⃣ Run Client(s)

```bash
python client.py
```

Run multiple clients in separate terminals or devices.

---

### 3️⃣ Running on Different Devices

- Ensure both devices are on the same WiFi
- Set server IP in `config.py`

Example:

```python
SERVER_IP = "192.168.x.x"
```

---

## 📌 Example Output

```
NODE1 -> latency (210) -> CONGESTION | Latency: 0.0023s | Throughput: 4.12/s

===== NETWORK DASHBOARD =====
Active Nodes: 3

Node   | Event        | Value | Class
--------------------------------------
NODE1  | latency      | 210   | CONGESTION
NODE2  | cpu_usage    | 95    | NODE_OVERLOAD
NODE3  | packet_loss  | 12    | NETWORK_FAILURE
=============================
```

---

## 🧪 Performance Evaluation

The system was tested under:

- Multiple concurrent clients
- Continuous event generation
- UDP-based communication

### Observations:

- Low latency due to lightweight UDP protocol
- High throughput as number of clients increases
- System scales well with additional nodes

---

## 🛠️ Optimization & Error Handling

Implemented:

- Malformed packet detection
- Invalid signature rejection
- Exception handling using try/except
- Safe parsing of values
- Memory control (event log capped at 50 entries)

---

## ⚖️ Design Decisions

### Why UDP?

- Fast and lightweight
- No connection overhead
- Suitable for real-time monitoring systems

### Why HMAC instead of SSL?

- UDP does not support SSL directly
- HMAC provides authentication + integrity efficiently

---

## 🎯 Conclusion

This project demonstrates a **secure, scalable, and efficient distributed monitoring system** with real-time analytics and performance evaluation.

---

## 👨‍💻 Authors

- Arvind Ajay Bharadwaj
- Bhoomika Patil
- Aditya Kalloli

---

## 🚀 Future Improvements

- Web-based dashboard
- Persistent storage (database)
- RSA-based authentication
- Alert notifications (email/Slack)
