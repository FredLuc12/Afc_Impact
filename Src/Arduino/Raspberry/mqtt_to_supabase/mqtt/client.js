const mqtt = require("mqtt");

const client = mqtt.connect("mqtt://localhost");

function init_MQTT(onMessage) {
  client.on("connect", () => {
    console.log("MQTT connecté");

    client.subscribe("capteurs/#"); // wildcard
  });

  client.on("message", (topic, message) => {
    onMessage(topic, message.toString());
  });
}

module.exports = { init_MQTT };
