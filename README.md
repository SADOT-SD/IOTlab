# Logtel IoT course 2026

Slides and lab files for the IoT course (Logtel, October 2026): Days 1 and 2 and the Day 4 hands-on lab. Day 3 (cellular IoT and security) is taught by another lecturer.

| File | What |
|---|---|
| [Day1_Foundations.pdf](Day1_Foundations.pdf) | Day 1 slides: networking basics and Wi-Fi, Wireshark, hardware interfaces, what IoT is, Bluetooth, NFC, RFID, UWB |
| [Day2_Technologies.pdf](Day2_Technologies.pdf) | Day 2 slides: architectures, connectivity, LoRaWAN, mesh, MQTT, Grafana, MakeCode |
| [Day4_Hands-on_Lab.pdf](Day4_Hands-on_Lab.pdf) | Day 4 slides: AWS IoT Core, certificates, the six lab parts, troubleshooting |
| [Day4_Lab_Guide.pdf](Day4_Lab_Guide.pdf) | Day 4 team lab guide: every step and every check |
| [team_app.py](team_app.py) | Part 3: the team app that runs in AWS CloudShell |
| [makecode/main.ts](makecode/main.ts) | Part 1: the micro:bit program (in class you get it as a MakeCode link) |

## Day 4, Part 3: the CloudShell blocks

Open CloudShell (the `>_` icon in the AWS console, Region N. Virginia) and paste one block at a time - the copy
button is at the top right of each block. In block 1, change `teamNN` to your team, for example `team03`.

**Block 1 - create the key pair and the certificate (AWS signs it and marks it ACTIVE)**

```bash
T=teamNN
ARN=$(aws iot create-keys-and-certificate --set-as-active \
  --certificate-pem-outfile $T.cert.pem --private-key-outfile $T.private.key \
  --query certificateArn --output text)
echo $ARN
```

**Block 2 - give the certificate the team policy, and tie it to your thing**

```bash
aws iot attach-policy --policy-name lab-team-policy --target $ARN
aws iot attach-thing-principal --thing-name $T --principal $ARN
```

**Block 3 - the CA that lets you trust AWS, and your account's endpoint**

```bash
curl -sO https://www.amazontrust.com/repository/AmazonRootCA1.pem
EP=$(aws iot describe-endpoint --endpoint-type iot:Data-ATS --output text)
echo $EP
ls
```

**Block 4 - download the team app, install the MQTT library once, then run**

```bash
R=https://raw.githubusercontent.com/samueldratwa-TG/logtel-iot-lab/main
curl -fsSLO $R/team_app.py
pip3 install --user paho-mqtt
python3 team_app.py $T $EP
```

Type `heart` and press Enter to send a command to your micro:bit. If port 8883 is blocked:
`python3 team_app.py $T $EP 443`.

Passwords, private keys and team cards are never put here.
