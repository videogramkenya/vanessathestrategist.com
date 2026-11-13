/* Webinar settings. Filled in at go-live. Nothing secret belongs here: the web address of the
   sign-up receiver is public by nature, and the video ids are public in the page anyway. */
window.WEBINAR_CONFIG = {
  webhookUrl: "https://n8n.loopsera.com/webhook/webinar-signup", /* the real receiver, live 13 Nov 2026 (was the DEMO one) */
  bunny: { libraryId: "REPLACE_AT_GO_LIVE", videoId: "REPLACE_AT_GO_LIVE" },
  html5Url: "/webinar-media/why-more-leads-arent-turning-into-more-sales.mp4", /* the recording, hosted on her own site (Alex, 4 Nov 2026) */
  posterUrl: "/webinar-media/why-more-leads-poster.jpg"
};
