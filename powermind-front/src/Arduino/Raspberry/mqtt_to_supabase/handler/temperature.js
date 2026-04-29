const { send_to_supabase, send_measure } = require("../service/supabase_service");

// 🔥 cache multi-capteurs
const cache = {};

async function handle_temperature(data) {
  const key = `${data.id_installation}_${data.name}`;

  if (!cache[key]) {
    cache[key] = {
      lastSent: 0,
      lastValue: null,
      capteur: null
    };
  }

  const now = Date.now();
  const c = cache[key];

  const timeOk = now - c.lastSent > 10000;
  const valueChanged =
    c.lastValue === null || Math.abs(data.value - c.lastValue) >= 0.5;

  if (!timeOk && !valueChanged) return;

  console.log("Temp handler:", data);

  // 🔥 UPSERT capteur (toujours récupéré)
  const capteur = await send_to_supabase({
    installation_id: data.id_installation,
    name: data.name,
    type: "temperature"
  });

  if (!capteur) {
    console.log("capteur null ❌");
    return;
  }

  cache[key] = {
    lastSent: now,
    lastValue: data.value,
    capteur
  };

  await send_measure(capteur.id, 1, data.value);
}

module.exports = { handle_temperature };