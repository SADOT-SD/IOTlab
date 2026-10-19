// Logtel IoT lab (2026) - Day 4, Part 1: micro:bit V2 + ELECFREAKS IoT:bit V1.6 -> class gateway (MQTT).
// Extension: ESP8266_IoT v2.3.2 (github:elecfreaks/pxt-esp8266iot#v2.3.2). Same blocks as slides "Part 1a-1c".
// The LECTURER fills <Logtel Wi-Fi> (if known) and <gateway> before sharing - never put a password in a shared project.
// The TEAM changes teamNN (4 places), the Wi-Fi <password> (on the whiteboard) and the gateway password <on your card>.
// Rules from research/R5: text goes raw into AT commands (no quote, comma or backslash in names and passwords);
// the JSON text needs \" and \, ; reconnect false = the module reconnects by itself; retain must stay false.
ESP8266_IoT.MqttEvent("lab/teamNN/cmd", ESP8266_IoT.QosList.Qos1, function (message) {
    if (message.includes("heart")) {
        basic.showIcon(IconNames.Heart)
    } else if (message.includes("smile")) {
        basic.showIcon(IconNames.Happy)
    } else {
        basic.showString(message)
    }
})
let msg = ""
ESP8266_IoT.initWIFI(SerialPin.P8, SerialPin.P12, BaudRate.BaudRate115200)
ESP8266_IoT.connectWifi("<Logtel Wi-Fi>", "<password>")
ESP8266_IoT.setMQTT(
ESP8266_IoT.SchemeList.TCP,
"teamNN",
"teamNN",
"<on your card>",
""
)
ESP8266_IoT.connectMQTT("<gateway>", 1883, false)
if (ESP8266_IoT.isMqttBrokerConnected()) {
    basic.showIcon(IconNames.Yes)
} else {
    basic.showIcon(IconNames.Sad)
}
loops.everyInterval(5000, function () {
    msg = "{\\\"temp\\\":" + input.temperature() + "\\,\\\"light\\\":" + input.lightLevel() + "}"
    ESP8266_IoT.publishMqttMessage(msg, "lab/teamNN/telemetry", ESP8266_IoT.QosList.Qos0, false)
})
