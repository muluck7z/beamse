module.exports = function handler(req, res) {
  res.setHeader(
    "Set-Cookie",
    "beamse_session=; Path=/; HttpOnly; SameSite=Lax; Max-Age=0"
  );
  res.json({ success: true });
};
