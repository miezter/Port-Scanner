import streamlit as st
import socket
import threading

# Scan result storage
open_ports = []

# Port scanning function
def scan_port(target, port):
    try:
        s = socket.socket()
        s.settimeout(0.5)
        result = s.connect_ex((target, port))
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "Unknown"
            open_ports.append((port, service))
        s.close()
    except:
        pass

# UI layout
st.title(" Web-Based Port Scanner")
st.markdown("Simple web port scanner built using Python & Streamlit")

target = st.text_input("Enter target IP address or hostname")
start_port = st.number_input("Start Port", value=1, min_value=1, max_value=65534)
end_port = st.number_input("End Port", value=1024, min_value=1, max_value=65535)

if st.button("Start Scan"):
    if not target:
        st.warning(" Please enter a valid target.")
    else:
        open_ports.clear()
        st.info(f"Scanning {target} from port {start_port} to {end_port}...")
        
        threads = []
        for port in range(start_port, end_port + 1):
            t = threading.Thread(target=scan_port, args=(target, port))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        if open_ports:
            st.success("Scan Complete. Open Ports:")
            for port, service in sorted(open_ports):
                st.write(f" Port {port} - {service}")
        else:
            st.info("No open ports found in the selected range.")

