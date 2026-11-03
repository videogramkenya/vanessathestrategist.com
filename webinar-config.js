/* Webinar settings. Filled in at go-live. Nothing secret belongs here: the web address of the
   sign-up receiver is public by nature, and the video ids are public in the page anyway. */
window.WEBINAR_CONFIG = {
  webhookUrl: "https://n8n.loopsera.com/webhook/demo-webinar-signup", /* DEMO receiver, ticket #046 */
  bunny: { libraryId: "REPLACE_AT_GO_LIVE", videoId: "REPLACE_AT_GO_LIVE" },
  html5Url: "/proof/webinar-lead-follow-up.mp4" /* STAND-IN clip until the Bunny video exists */
};
