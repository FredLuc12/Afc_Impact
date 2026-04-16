const { init_MQTT } = require("./mqtt/client");
const { handle_temperature } = require("./handler/temperature");

function router(topic, message) {
  let data;

  try {
    data = JSON.parse(message);
  } catch (e) {
    console.error("JSON invalide");
    return;
  }

  switch (topic) {
    case "capteurs/temp":
      handle_temperature(data);
      break;

    default:
      console.log("Topic non géré:", topic);
  }
}

init_MQTT(router);
