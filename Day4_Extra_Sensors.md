# Day 4 extra: send more sensor readings

Your board already sends `{"temp":24,"light":120}` every 5 seconds. The micro:bit V2 has more sensors. This page
shows how to add two of them, **sound** and **movement**, so that the message becomes:

```
{"temp":24,"light":120,"sound":38,"move":1040}
```

Nothing changes on the gateway or in AWS: the topic stays `lab/teamNN/telemetry`. Only the text of the message
grows.

## 1. Add the readings (Blocks)

1. Open your team's project, the one that shows the tick.
2. Find the **every 5000 ms** block and, inside it, **set msg to join ...**.
3. Click the **+** at the right end of the **join** block four times: four new empty slots appear.
4. Drag the final `}` text to the last slot, then fill the slots in this order:

| Slot | Put in | Where to find it |
|---|---|---|
| text | `\,\"sound\":` | Text > the empty text block, then type it |
| number | **sound level** | Input (V2 only; if you do not see it, click **more** under Input) |
| text | `\,\"move\":` | Text |
| number | **acceleration (mg) strength** | Input > **acceleration (mg) x**, then choose **strength** |
| text | `}` | (moved from before) |

5. **Download** and wait for the tick.

The same line in **JavaScript**, if you prefer to edit there:

```javascript
msg = "{\\\"temp\\\":" + input.temperature() + "\\,\\\"light\\\":" + input.lightLevel() + "\\,\\\"sound\\\":" + input.soundLevel() + "\\,\\\"move\\\":" + input.acceleration(Dimension.Strength) + "}"
```

## 2. The three rules for every new field

1. **A backslash before every quote and before every comma**: `\"name\":` and `\,`. The Wi-Fi module receives the
   message inside an AT command, where a bare `"` or `,` ends the text. The backslashes do not reach AWS: AWS
   receives clean JSON.
2. **Names in lowercase letters, no spaces**: `sound`, `move`, `tilt`.
3. **Numbers only, and keep the whole message short** (under about 100 characters).

## 3. Check it

- **AWS console > IoT Core > MQTT test client**: subscribe to `lab/teamNN/telemetry`. Every 5 seconds:
  `{"temp":24,"light":120,"sound":38,"move":1040}`.
- **CloudShell**: `team_app.py` prints every message in full, so the new fields show up there too.
- Make noise next to the board, then shake it: `sound` and `move` jump.

What the numbers mean:

| Field | Range | At rest | When it changes |
|---|---|---|---|
| `sound` | 0 - 255 | low in a quiet room | clap or talk close to the board |
| `move` | milli-g | about 1000 (gravity) | shaking gives 2000 and more |

Each reading is a snapshot taken at that moment, once every 5 seconds.

## 4. More ideas

- **Tilt**: `acceleration (mg) x` goes from about -1000 (tilted to one side) to about 1000 (the other side).
- **Shakes counter**: make a variable `shakes`. Add **on shake** > **change shakes by 1**. In **every 5000 ms**, send
  `\,\"shakes\":` + `shakes`, then **set shakes to 0**.
- **Button presses**: the same idea with **on button A pressed**.
- **Magnetic force**: Input > more > **magnetic force**. Hold a magnet near the board.

## 5. Where the new fields appear, and where they do not

| Place | New fields? | Why |
|---|---|---|
| MQTT test client | yes | it shows the whole message |
| `team_app.py` in CloudShell | yes | it prints the whole message |
| DynamoDB table `lab_telemetry` | **no** | the rule picks only `temp` and `light` |
| The class wall (Grafana) | **no** | each tile shows only `temp` and `light` |

### How the lecturer would store them in the table too

Team users cannot change rules. The lecturer would do this:

1. AWS console > **IoT Core > Message routing > Rules > `lab_telemetry_to_dynamodb` > Edit**.
2. In **SQL statement**, change the first line:
   - before: `SELECT temp, light, topic(2) AS team, timestamp() AS ts FROM 'lab/+/telemetry'`
   - after: `SELECT temp, light, sound, move, topic(2) AS team, timestamp() AS ts FROM 'lab/+/telemetry'`
   - or, to keep **any** field a team adds: `SELECT *, topic(2) AS team, timestamp() AS ts FROM 'lab/+/telemetry'`
3. **Update**. The next messages carry the new columns.

Nothing changes in the table itself. DynamoDB fixes only the two keys, `team` and `ts`; every other attribute can be
added at any time. Older items simply have no `sound` or `move`.

To see the table like a spreadsheet: **DynamoDB > Tables > `lab_telemetry` > Explore table items**. Choose **Scan**
for every team, or **Query** with `team` = `team03` for one team. Click a column title to sort. `ts` is the time in
milliseconds since 1970.
