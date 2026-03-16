def classify_event(event_type, value):
    if event_type == "packet_loss":
        value = int(value)
        if value > 10:
            return "NETWORK_FAILURE"
        elif value > 5:
            return "NETWORK_WARNING"
        else:
            return "NORMAL"
        
    elif event_type == "latency":
        value = int(value)
        if value > 300:
            return "SEVERE_CONGESTION"
        elif value > 150:
            return "CONGESTION"
        else:
            return "NORMAL"
        
    elif event_type == "cpu_usage":
        value = int(value)
        if value > 90:
            return "NODE_OVERLOAD"
        elif value > 70:
            return "HIGH_USAGE"
        else:
            return "NORMAL"
        
    elif event_type == "node_down":
        value = int(value)
        if value == 1:
            return "NODE_FAILURE"
        else:
            return "NORMAL"
    
    return "UNKNOWN"