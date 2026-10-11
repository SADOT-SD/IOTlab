"""Logtel IoT lab - Part 3 team app (runs in AWS CloudShell).

    python3 team_app.py team03 <endpoint> [443]

Connects to AWS IoT Core with the team's own X.509 certificate (mutual TLS, port 8883 - or 443 with ALPN
x-amzn-mqtt-ca if a network blocks 8883), prints the team's telemetry and sends what you type as a command:
    heart            -> lab/team03/cmd   {"led": "heart"}
    team04 heart     -> lab/team04/cmd   (the policy does not allow it - watch what happens)
Needs <team>.cert.pem, <team>.private.key and AmazonRootCA1.pem in the current folder.
Only one copy per team at a time: AWS IoT drops the older connection when a client ID is reused.
"""
import json
import ssl
import sys

import paho.mqtt.client as mqtt     # paho-mqtt 2.x:  pip3 install --user paho-mqtt

QOS = 1                             # AWS IoT Core supports QoS 0 and 1 only


def main():
    if len(sys.argv) not in (3, 4):
        sys.exit(__doc__)
    team, endpoint = sys.argv[1], sys.argv[2]
    port = int(sys.argv[3]) if len(sys.argv) == 4 else 8883

    ctx = ssl.create_default_context(cafile="AmazonRootCA1.pem")             # checks AWS's certificate
    ctx.load_cert_chain(certfile=f"{team}.cert.pem", keyfile=f"{team}.private.key")   # proves who we are
    if port == 443:
        ctx.set_alpn_protocols(["x-amzn-mqtt-ca"])                          # MQTT + X.509 on 443 needs ALPN

    def on_connect(client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            print(f"connect refused: {reason_code}")
            return
        print(f"connected to {endpoint}:{port} as {team}")
        client.subscribe(f"lab/{team}/telemetry", qos=QOS)

    def on_subscribe(client, userdata, mid, reason_codes, properties):
        for rc in reason_codes:
            if rc.is_failure:
                print(f"subscribe refused: {rc}")

    def on_message(client, userdata, msg):
        print(f"{msg.topic}  {msg.payload.decode(errors='replace')}")

    def on_disconnect(client, userdata, flags, reason_code, properties):
        print(f"disconnected: {reason_code} - reconnecting")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=team)   # client ID = thing name
    client.tls_set_context(ctx)
    client.on_connect, client.on_subscribe = on_connect, on_subscribe
    client.on_message, client.on_disconnect = on_message, on_disconnect
    client.connect(endpoint, port, keepalive=60)
    client.loop_start()
    print("type a command (heart, smile, ...) or 'team04 heart'; Ctrl+C to stop")
    try:
        for line in sys.stdin:
            words = line.split()
            if not words:
                continue
            target, value = (words[0], words[1]) if len(words) > 1 else (team, words[0])
            topic = f"lab/{target}/cmd"
            client.publish(topic, json.dumps({"led": value}), qos=QOS)
            print(f"sent to {topic}: {value}")
    except KeyboardInterrupt:
        pass
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
