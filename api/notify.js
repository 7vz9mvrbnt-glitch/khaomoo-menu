export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed" });

  const LINE_TOKEN = process.env.LINE_CHANNEL_ACCESS_TOKEN;
  const { message } = req.body;

  if (!message) return res.status(400).json({ error: "No message" });

  try {
    const r = await fetch("https://api.line.me/v2/bot/message/broadcast", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${LINE_TOKEN}`,
      },
      body: JSON.stringify({
        messages: [{ type: "text", text: message }]
      }),
    });
    const data = await r.json();
    res.status(200).json({ ok: true, data });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
}
