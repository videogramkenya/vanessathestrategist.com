/* Recorded webinar: sign-up form and watch progress. Draft 3 Nov 2026 (ticket #046). */
(function () {
  var C = window.WEBINAR_CONFIG || {};
  var KEY = "webinar_session", SENT = "webinar_sent";
  var page = document.body.getAttribute("data-page");

  function store(k, v) { try { sessionStorage.setItem(k, JSON.stringify(v)); return true; } catch (e) { return false; } }
  function fetchStore(k) { try { return JSON.parse(sessionStorage.getItem(k)); } catch (e) { return null; } }
  function send(payload, timeoutMs) {
    var ctl = window.AbortController ? new AbortController() : null;
    var timer = ctl ? setTimeout(function () { ctl.abort(); }, timeoutMs || 15000) : null;
    return fetch(C.webhookUrl, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload), keepalive: true, signal: ctl ? ctl.signal : undefined
    }).then(function (r) {
      if (timer) clearTimeout(timer);
      return r.json().catch(function () { return {}; }).then(function (j) { return { status: r.status, body: j }; });
    });
  }
  function track(name, params) { try { if (window.analyticsEnabled) gtag("event", name, params || {}); } catch (e) {} }

  /* ---------- sign-up page ---------- */
  if (page === "signup") {
    var form = document.getElementById("signup-form");
    var msg = document.getElementById("form-msg");
    var btn = document.getElementById("signup-btn");
    var loaded = Date.now();
    track("webinar_signup_view");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      msg.textContent = "";
      if (!form.checkValidity()) { form.reportValidity(); return; }
      btn.disabled = true;
      var d = new FormData(form);
      send({
        type: "signup",
        first_name: d.get("first_name"), last_name: d.get("last_name"), email: d.get("email"),
        company_website: d.get("company_website"),
        elapsed_ms: Date.now() - loaded
      }).then(function (res) {
        if (res.status === 200 && res.body && res.body.ok) {
          store(KEY, { lead_id: res.body.lead_id || null, sig: res.body.sig || null });
          track("webinar_signup");
          location.assign("/webinar/watch");
        } else {
          btn.disabled = false;
          msg.textContent = "Something went wrong on our side. Please try again in a moment.";
        }
      }).catch(function () {
        btn.disabled = false;
        msg.textContent = "We could not reach the sign-up. Check your connection and try again.";
      });
    });
  }

  /* ---------- watch page ---------- */
  if (page === "watch") {
    var sess = fetchStore(KEY);
    if (!sess) { location.replace("/webinar"); return; }
    var box = document.getElementById("player");
    var next = document.getElementById("next");
    var sent = fetchStore(SENT) || {};
    var watched = 0, last = null, duration = 0, tries = {}, inflight = {};

    function report(ev) {
      if (!sess.lead_id || !sess.sig) { sent[ev] = true; return; }
      if (sent[ev] || inflight[ev]) return;
      tries[ev] = (tries[ev] || 0) + 1;
      if (tries[ev] > 3) return;
      inflight[ev] = true;
      send({ type: "progress", lead_id: sess.lead_id, sig: sess.sig, event: ev }, 10000).then(function (res) {
        inflight[ev] = false;
        if (res.status === 200) { sent[ev] = true; store(SENT, sent); }
      }).catch(function () { inflight[ev] = false; });
      track("webinar_" + ev);
    }
    function showNext() { next.classList.add("ready"); }
    function onPlay() { report("started"); }
    function onTime(t, dur) {
      if (dur > 0) duration = dur;
      if (last !== null) { var d = t - last; if (d > 0 && d <= 2) watched += d; }
      last = t;
      if (!duration) return;
      if (watched >= 0.45 * duration) report("halfway");
      if (watched >= 0.9 * duration) { report("finished"); showNext(); }
    }
    function onEnded() {
      if (duration && watched >= 0.8 * duration) report("finished");
      showNext();
    }

    if (C.html5Url) {
      var v = document.createElement("video");
      v.controls = true; v.setAttribute("playsinline", ""); v.preload = "metadata"; v.src = C.html5Url;
      box.appendChild(v);
      v.addEventListener("play", onPlay);
      v.addEventListener("timeupdate", function () { onTime(v.currentTime, v.duration); });
      v.addEventListener("seeking", function () { last = null; });
      v.addEventListener("ended", onEnded);
    } else {
      var f = document.createElement("iframe");
      f.src = "https://iframe.mediadelivery.net/embed/" + encodeURIComponent(C.bunny.libraryId) + "/" + encodeURIComponent(C.bunny.videoId) + "?preload=true";
      f.allow = "accelerometer;gyroscope;autoplay;encrypted-media;picture-in-picture;fullscreen";
      f.setAttribute("allowfullscreen", "");
      f.title = "Why More Leads Aren’t Turning Into More Sales";
      box.appendChild(f);
      var s = document.createElement("script");
      s.src = "https://assets.mediadelivery.net/playerjs/player-0.1.0.min.js";
      s.onload = function () {
        var p = new playerjs.Player(f);
        p.on("ready", function () {
          p.on("play", onPlay);
          p.on("timeupdate", function (d) { onTime(d.seconds, d.duration); });
          p.on("seeked", function () { last = null; });
          p.on("ended", onEnded);
        });
      };
      document.head.appendChild(s);
    }
  }
})();
