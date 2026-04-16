const axios = require("axios");
const config = require("../config/supabase");

// 🔥 UPSERT capteur (pas d'erreur 23505)
async function send_to_supabase(data) {
  try {
    const res = await axios.post(
  `${config.url}/rest/v1/${config.table}?on_conflict=nom`,
  {
    installation_id: data.installation_id,
    nom: data.name,
    type: data.type
  },
  {
    headers: {
      apikey: config.apiKey,
      Authorization: `Bearer ${config.apiKey}`,
      "Content-Type": "application/json",

      // 🔥 garde ça
      Prefer: "resolution=merge-duplicates,return=representation"
    }
  }
);

    console.log("capteur upsert OK");

    return res.data[0];

  } catch (err) {
    console.error("erreur capteur :", err.response?.data || err.message);
    return null;
  }
}

// 🔥 insertion mesure
async function send_measure(capteur_id, type_mesure_id, value) {
  try {
    await axios.post(
      `${config.url}/rest/v1/mesures`,
      {
        capteur_id,
        type_mesure_id,
        value
      },
      {
        headers: {
          apikey: config.apiKey,
          Authorization: `Bearer ${config.apiKey}`,
          "Content-Type": "application/json"
        }
      }
    );

    console.log("mesure envoyée ✔");

  } catch (err) {
    console.error("erreur mesure :", err.response?.data || err.message);
  }
}

module.exports = { send_to_supabase, send_measure };