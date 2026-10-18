// Example run viewer. Reads the run from <script id="run-data"> (examples/<slug>/run.json, written by
// examples/tools/export.py) and the list of examples from <script id="examples-data">. Plays the run on the
// timeline; the chat shows what each AI was sent and said, and the resume shows the lines each message is about.
(function () {
  "use strict";
  var R = JSON.parse(document.getElementById("run-data").textContent);
  var EX = JSON.parse((document.getElementById("examples-data") || { textContent: "[]" }).textContent);
  var WHO = R.who, END = R.end, STEPS = R.steps, EV = R.events, LANES = R.lanes, CAND = R.candidate;

  var $ = function (s) { return document.querySelector(s); };
  var $$ = function (s) { return Array.prototype.slice.call(document.querySelectorAll(s)); };
  var esc = function (s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); };
  var pad = function (n) { return String(n).padStart(2, "0"); };
  var clock = function (s) { s = Math.floor(s); return pad(Math.floor(s / 60)) + ":" + pad(s % 60); };
  var dur = function (s) { return s >= 60 ? Math.floor(s / 60) + " min " + (s % 60) + " s" : s + " s"; };
  var long = function (s) { return s >= 5400 ? Math.round(s / 3600) + " hours" : Math.round(s / 60) + " minutes"; };
  var pct = function (s) { return (s / END * 100).toFixed(3) + "%"; };
  var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  var narrow = function () { return matchMedia("(max-width: 859px)").matches; };
  var stepEnd = function (k) { return k + 1 < STEPS.length ? STEPS[k + 1].t : END; };

  // ---------- text ----------
  function inline(s) {
    return esc(s).replace(/\*\*(.+?)\*\*/g, "<b>$1</b>").replace(/`([^`]+)`/g, "<code>$1</code>");
  }
  // Enough Markdown for the host's messages: paragraphs, lists, headings, code blocks and tables (shown as typed).
  function md(src) {
    var out = [], lines = String(src).split("\n"), i = 0, para = [];
    var flush = function () { if (para.length) { out.push("<p>" + inline(para.join(" ")) + "</p>"); para = []; } };
    while (i < lines.length) {
      var l = lines[i];
      if (/^\s*```/.test(l)) {
        flush(); var code = []; i++;
        while (i < lines.length && !/^\s*```/.test(lines[i])) code.push(lines[i++]);
        var pre = "<pre>" + esc(code.join("\n")) + "</pre>";  // a long block, such as a whole prompt on a paste card, starts folded
        out.push(code.length > 25 ? '<details class="longcode"><summary>Show the full text (' + code.length + " lines)</summary>" + pre + "</details>" : pre); i++; continue;
      }
      if (/^\s*\|/.test(l)) {
        flush(); var rows = [];
        while (i < lines.length && /^\s*\|/.test(lines[i])) rows.push(lines[i++]);
        out.push("<pre>" + esc(rows.join("\n")) + "</pre>"); continue;
      }
      var list = /^\s*([-*]|\d+[.)])\s+/.exec(l);
      if (list) {
        flush(); var ordered = /\d/.test(list[1]), items = [];
        while (i < lines.length && /^\s*([-*]|\d+[.)])\s+/.test(lines[i])) {
          var item = lines[i++].replace(/^\s*([-*]|\d+[.)])\s+/, "");
          while (i < lines.length && /^\s{2,}\S/.test(lines[i]) && !/^\s*([-*]|\d+[.)])\s+/.test(lines[i])) item += " " + lines[i++].trim();
          items.push("<li>" + inline(item) + "</li>");
        }
        out.push((ordered ? "<ol>" : "<ul>") + items.join("") + (ordered ? "</ol>" : "</ul>")); continue;
      }
      if (/^#{1,6}\s/.test(l)) { flush(); out.push("<h4>" + inline(l.replace(/^#+\s*/, "")) + "</h4>"); i++; continue; }
      if (!l.trim()) flush(); else para.push(l.trim());
      i++;
    }
    flush();
    return out.join("");
  }

  // ---------- tabs ----------
  var TABS = [{ id: "chat", who: "host", n: CAND + " and the host", about: "What " + CAND + " saw: every message from the host, and " + CAND + "'s answers." }];
  var PASTED = { chatgpt: 1, gemini: 1 }; // apps the candidate pasted prompts into, in manual mode
  Object.keys(WHO).forEach(function (k) {
    var w = WHO[k];
    if (k === "user" || k === "host" || k === "check") return;
    var about = w.fresh ? "A new session of the host's own model that sees only its prompt, nothing of the host's own draft."
      : PASTED[k] ? "The cards the host gave " + CAND + " to paste into " + w.n + ", and the replies " + CAND + " pasted back. " + w.n + " never sees " + CAND + "'s name or who wrote each draft."
      : "What the host sent " + w.n + " and what came back. " + w.n + " never sees " + CAND + "'s name or who wrote each draft.";
    TABS.push({ id: k, who: k, n: w.n, about: about });
  });
  if (WHO.check) TABS.push({ id: "check", who: "check", n: "Checks", about: "The script that flags numbers, names and titles it cannot find in " + CAND + "'s own material, for the host to settle." });
  TABS.push({ id: "all", who: "all", n: "Everything", about: "Every message, in the order it happened." });

  var tabOf = function (e) { return e.kind === "ask" ? e.to : e.kind === "reply" ? e.who : e.kind === "check" ? "check" : "chat"; };
  var inTab = function (e, t) { return t === "all" || tabOf(e) === t; };
  var laneTab = function (l, t) { return t === "all" || (t === "chat" ? (l[0] === "host" || l[0] === "user") : l[0] === t); };

  // ---------- resume ----------
  var FROM = { "own words": "from " + CAND + "'s own words", "sign-off": "confirmed at sign-off", "old resume": "from the old resume", "linked page": "from a linked page" };
  var ui = { v: "after", diff: true, zoom: "page" }, userV = null;  // userV: the version the visitor picked, which playback then leaves alone
  function renderResume() {
    var doc = ui.v === "before" ? R.before : R.after;
    $("#sheet").innerHTML = doc.map(function (l) {
      if (l.k === "name") return '<div class="s-name">' + inline(l.tx) + "</div>";
      if (l.k === "h2") return '<div class="s-h2">' + inline(l.tx) + "</div>";
      var cls = "s-" + (l.k === "contact" ? "contact" : l.k) + " ln" + (l.s ? " " + l.s : "");
      var why = l.why && l.s ? '<div class="why">' + esc(l.why) + "</div>" : "";
      var from = ui.v === "after" && l.s && l.from ? '<span class="from">' + esc(FROM[l.from] || l.from) + "</span>" : "";
      return '<div class="' + cls + '" data-id="' + esc(l.id || "") + '"><span class="tx">' + inline(l.tx) + "</span>" + from + why + "</div>";
    }).join("");
    $("#sheet").classList.toggle("diff", ui.diff);
    $(".rv-pane-resume").classList.toggle("diff-on", ui.diff);
    $("#key").innerHTML = (ui.v === "before"
      ? '<span><i class="sw strike"></i>Cut</span><span><i class="sw" style="--k:var(--p-rw)"></i>Reworded in the new resume</span>'
      : '<span><i class="sw" style="--k:var(--p-new)"></i>New line</span><span><i class="sw" style="--k:var(--p-rw)"></i>Reworded</span><span><i class="ex-from">' + esc(FROM["own words"]) + "</i>where the facts came from</span>")
      + '<span><i class="ex-why">Blue text</i>why the line changed</span>';
    fit();
  }
  function fit() {
    var paper = $("#paper"), box = $("#resume-scroll");
    if (ui.zoom === "page") {
      var cs = getComputedStyle(box), h = box.clientHeight - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom);
      paper.style.width = Math.max(240, Math.min(box.clientWidth - 2 * parseFloat(cs.paddingLeft), h * 8.5 / 11)) + "px";
    } else paper.style.width = "";
  }
  // Scroll inside one pane only, so the page itself never jumps.
  function scrollWithin(box, el, where) {
    if (!el) return;
    var top = el.getBoundingClientRect().top - box.getBoundingClientRect().top + box.scrollTop;
    var y = where === "center" ? top - box.clientHeight / 2 + el.offsetHeight / 2 : where === "bottom" ? box.scrollHeight : top - 12;
    box.scrollTo({ top: y, behavior: reduce ? "auto" : "smooth" });
  }
  function flash(ids, scroll) {
    $$("#sheet .flash").forEach(function (n) { n.classList.remove("flash"); });
    var doc = ui.v === "before" ? R.before : R.after, other = ui.v === "before" ? R.after : R.before;
    var has = function (d, id) { return d.some(function (l) { return l.id === id; }); };
    var nodes = ids.map(function (id) { return $('#sheet [data-id="' + id + '"]'); }).filter(Boolean);
    nodes.forEach(function (n) { n.classList.add("flash"); });
    if (scroll && nodes[0]) scrollWithin($("#resume-scroll"), nodes[0], "center");
    var missing = ids.filter(function (id) { return !has(doc, id) && has(other, id); });
    var bar = $("#cutbar");
    if (missing.length && !nodes.length) {
      var toBefore = ui.v === "after";
      bar.innerHTML = "<span>" + (toBefore ? "That line was cut, so it's only in the old resume." : "That line is new, so it's only in the new resume.") +
        '</span><button type="button" class="rv-ghost" data-jump="' + (toBefore ? "before" : "after") + '">Show ' + (toBefore ? "Before" : "After") + "</button>";
      bar.hidden = false;
    } else bar.hidden = true;
  }

  // ---------- timeline ----------
  function buildLanes() {
    var h = '<div></div><div class="stepband">' + STEPS.map(function (s, k) {
      return '<button type="button" data-step="' + k + '" style="left:' + pct(s.t) + ";width:" + pct(stepEnd(k) - s.t) + '">' + s.n + " " + esc(s.name) + "</button>";
    }).join("") + "</div>";
    var rows = ["user", "host"].concat(Object.keys(WHO).filter(function (k) { return k !== "user" && k !== "host"; }));
    rows.forEach(function (k) {
      h += '<div class="lane-label who-' + k + '"><i></i>' + esc(WHO[k].n) + '</div><div class="track who-' + k + '">';
      LANES.forEach(function (l, j) {
        if (l[0] !== k) return;
        var tick = l[1] === l[2];
        h += '<button type="button" class="blk who-' + k + (l[4] ? " wait" : "") + (tick ? " tick" : "") + '" style="left:' + pct(l[1]) + ";width:" + pct(l[2] - l[1]) +
          '" data-j="' + j + '" aria-pressed="false" title="' + esc(WHO[k].n + ", " + clock(l[1]) + (tick ? "" : " to " + clock(l[2])) + (l[3] ? ": " + l[3] : "")) + '">' + esc(l[3]) + "</button>";
      });
      h += "</div>";
    });
    $("#lanes").innerHTML = h + '<div class="playhead" id="playhead"></div>';
  }
  // The message a bar stands for: a seat's reply at its end, otherwise the first message inside the bar.
  function laneEvent(l) {
    var i = -1;
    EV.some(function (e, k) { if (e.who === l[0] && e.t === l[2] && e.kind === "reply") { i = k; return true; } return false; });
    if (i < 0) EV.some(function (e, k) { if (e.who === l[0] && e.t >= l[1] && e.t <= l[2] && e.kind !== "step") { i = k; return true; } return false; });
    return i;
  }

  // ---------- chat ----------
  var tab = "chat", selected = -1, shownKey = "", seen = {}, now = END;
  var visible = function (t, n) { return EV.filter(function (e) { return e.t <= n && inTab(e, t) && e.kind !== "step"; }).length; };
  var busyLanes = function (n) { return LANES.filter(function (l) { return l[5] && l[1] <= n && n < l[2]; }); };
  function renderTabs() {
    var busy = busyLanes(now);
    $("#ctabs").innerHTML = TABS.map(function (t) {
      var working = t.id !== "all" && busy.some(function (l) { return laneTab(l, t.id); });
      var unread = t.id === tab || t.id === "all" ? 0 : Math.max(0, visible(t.id, now) - (seen[t.id] || 0));
      return '<button type="button" role="tab" class="ctab who-' + t.who + '" data-tab="' + t.id + '" aria-selected="' + (t.id === tab) + '" tabindex="' + (t.id === tab ? 0 : -1) + '">' +
        (working ? '<i class="spin" role="img" aria-label="working"></i>' : '<i class="dot"></i>') + esc(t.n) +
        (unread ? '<span class="cbadge" aria-label="' + unread + ' new">' + unread + "</span>" : "") + "</button>";
    }).join("");
  }
  function msgHTML(e, i, arrive) {
    var w = WHO[e.who], cls = " who-" + e.who + (i === selected ? " sel" : "") + (arrive ? " arrive" : "");
    if (e.kind === "step") return '<div class="step-div">Step ' + e.step + ": " + esc(e.text) + "</div>";
    if (e.kind === "note") return '<div class="act' + cls + '" data-i="' + i + '" tabindex="0"><b>' + esc(w.n) + "</b><span>" + esc(e.text) + '</span><span class="tl">' + clock(e.t) + "</span></div>";
    var name = e.to ? w.n + " to " + WHO[e.to].n : w.n;
    var pills = (e.stop ? '<span class="mpill stop">' + esc(e.stop) + ": " + esc(CAND) + "'s turn</span>" : "") + (e.d ? '<span class="mpill">' + (PASTED[e.who] ? "pasted back after " : "took ") + dur(e.d) + "</span>" : "")
      + (e.waited ? '<span class="mpill" title="The timeline shows this wait as 5 minutes">answered after ' + long(e.waited) + ", shortened on the timeline</span>" : "");
    var files = (e.files || []).map(function (f) {
      return '<a href="files/' + encodeURIComponent(f) + '" target="_blank" rel="noopener">' + (e.kind === "ask" ? "Read the full prompt" : e.kind === "reply" ? "Read the full reply" : esc(f)) + "</a>";
    }).join("");
    return '<div class="msg' + cls + (e.kind === "user" ? " user" : "") + (e.kind === "ask" ? " ask" : "") + '" data-i="' + i + '" tabindex="0"><div class="av" aria-hidden="true">' + esc(w.s) + "</div>" +
      '<div class="mbody"><div class="mmeta"><b>' + esc(name) + "</b><span>" + (e.to ? "" : esc(w.role)) + '</span><span class="tl" title="Time into the run">' + clock(e.t) + "</span>" + pills + "</div>" +
      '<div class="bubble">' + md(e.text) + "</div>" + (files ? '<div class="files">' + files + "</div>" : "") + "</div></div>";
  }
  function renderChat(follow) {
    var shown = [];
    EV.forEach(function (e, i) { if (e.t <= now && inTab(e, tab) && (e.kind !== "step" || tab === "chat" || tab === "all")) shown.push(i); });
    var busy = busyLanes(now).filter(function (l) { return laneTab(l, tab); });
    var key = tab + "|" + shown.length + "|" + busy.map(function (l) { return l[5]; }).join();
    if (key === shownKey) return;
    var grew = shownKey.indexOf(tab + "|") === 0 && shown.length > +shownKey.split("|")[1];
    shownKey = key;
    seen[tab] = visible(tab, now);
    var t = TABS.filter(function (x) { return x.id === tab; })[0];
    var h = '<p class="tab-about">' + esc(t.about) + "</p>";
    h += shown.length ? shown.map(function (i, k) { return msgHTML(EV[i], i, follow && grew && k === shown.length - 1); }).join("") : '<p class="rv-empty">Nothing here yet.</p>';
    h += busy.map(function (l) { return '<div class="typing who-' + l[0] + '"><i></i><i></i><i></i>' + esc(l[5]) + "…</div>"; }).join("");
    if (now >= END) h += '<p class="end-note">That\'s the whole run. Press play to watch it from the start, or click any bar or message to jump to it.</p>';
    $("#feed").innerHTML = h;
    if (follow) scrollWithin($("#chat-scroll"), $("#feed").lastElementChild, "bottom");
  }
  function openTab(t, keepScroll) {
    if (t === tab) return;
    tab = t; shownKey = ""; renderTabs(); renderChat(false);
    if (!keepScroll) scrollWithin($("#chat-scroll"), $("#feed").lastElementChild, "bottom");
  }

  // ---------- playback ----------
  var RATE = 20; // seconds of the run per real second at Normal speed
  var playing = false, last = 0, holdUntil = 0, raf = 0, tabsKey = "";
  function setNow(t, follow) {
    now = Math.max(0, Math.min(END, t));
    $("#scrub").value = Math.floor(now);
    $("#clock").textContent = clock(now);
    $("#playhead").style.left = "calc(104px + (100% - 104px) * " + (now / END) + ")";
    $$(".blk").forEach(function (b) { b.classList.toggle("future", LANES[b.dataset.j][1] > now); });
    var st = 0; STEPS.forEach(function (s, k) { if (s.t <= now) st = k; });
    $$(".stepband button").forEach(function (b) { b.classList.toggle("on", +b.dataset.step === st); });
    TABS.forEach(function (t) { var v = visible(t.id, now); if (seen[t.id] > v) seen[t.id] = v; });
    renderChat(follow);
    var k = busyLanes(now).map(function (l) { return l[5]; }).join() + TABS.map(function (t) { return visible(t.id, now) - (seen[t.id] || 0); }).join();
    if (k !== tabsKey) { tabsKey = k; renderTabs(); }
  }
  function select(i, scrollChat) {
    selected = i;
    var e = EV[i], j = -1;
    LANES.some(function (l, x) { if (laneEvent(l) === i) { j = x; return true; } return false; });
    $$(".blk").forEach(function (b) { b.setAttribute("aria-pressed", +b.dataset.j === j); });
    if (!inTab(e, tab)) openTab(tabOf(e), true);
    $$(".msg.sel, .act.sel").forEach(function (n) { n.classList.remove("sel"); });
    var m = $('[data-i="' + i + '"]');
    if (m) { m.classList.add("sel"); if (scrollChat !== false) scrollWithin($("#chat-scroll"), m, "center"); }
    flash(e.links || [], !!(e.links && e.links.length));
  }
  function holdFor(e) { var words = e.text.split(/\s+/).length; return Math.min(7000, Math.max(1600, 900 + words * 95)); }
  function frame(ts) {
    if (!playing) return;
    var dt = last ? (ts - last) / 1000 : 0; last = ts;
    var speed = +$("#speed").value;
    if (ts >= holdUntil) {
      var t = now + dt * RATE * speed, next = -1;
      EV.some(function (e, k) { if (e.t > now && e.t <= t) { next = k; return true; } return false; });
      if (next >= 0) {
        if ($("#follow").checked && !inTab(EV[next], tab) && EV[next].kind !== "step") openTab(tabOf(EV[next]), true);
        setNow(EV[next].t, true);
        select(next, false);
        holdUntil = ts + (EV[next].kind === "step" ? 600 : holdFor(EV[next])) / speed;
      } else setNow(t, true);
      if (now >= END) { pause(); return; }
    }
    raf = requestAnimationFrame(frame);
  }
  function setPlayButton(label, icon) { $("#play-label").textContent = label; $("#play-icon").innerHTML = icon; }
  var PLAY = '<path d="M3 1.5v13l11-6.5z"/>', PAUSE = '<path d="M3 1.5h3.5v13H3zM9.5 1.5H13v13H9.5z"/>';
  function play() {
    if (now >= END) {
      TABS.forEach(function (t) { seen[t.id] = 0; });
      if (!userV) setVersion("before");  // the run plays from the old resume and ends on the new one
      selected = -1; tab = ""; openTab("chat", true); setNow(0, false); select(0, false);
      holdUntil = performance.now() + holdFor(EV[0]);
    }
    playing = true; last = 0; setPlayButton("Pause", PAUSE);
    raf = requestAnimationFrame(frame);
  }
  function pause() {
    playing = false; cancelAnimationFrame(raf); setPlayButton(now >= END ? "Play again" : "Play", PLAY);
    if (now >= END && !userV && ui.v !== "after") setVersion("after");
  }
  // Picking a moment by hand pauses the run, so it stays on what was picked.
  function jumpTo(i) { if (i < 0) return; if (playing) pause(); holdUntil = 0; setNow(EV[i].t, false); select(i); }

  // ---------- settings (kept in this browser only) ----------
  var store = { get: function (k) { try { return localStorage.getItem("rv-" + k); } catch (e) { return null; } },
                set: function (k, v) { try { localStorage.setItem("rv-" + k, v); } catch (e) {} } };
  [["autoplay", "checked"], ["follow", "checked"], ["speed", "value"]].forEach(function (x) {
    var el = $("#" + x[0]), v = store.get(x[0]);
    if (v !== null) el[x[1]] = x[1] === "checked" ? v === "1" : v;
    el.addEventListener("change", function () { store.set(x[0], x[1] === "checked" ? (el.checked ? "1" : "0") : el.value); });
  });
  var pop = $("#settings"), gear = $("#settings-btn");
  function showSettings(open) { pop.hidden = !open; gear.setAttribute("aria-expanded", String(open)); }
  gear.onclick = function () { showSettings(pop.hidden); };
  document.addEventListener("click", function (e) { if (!pop.hidden && !e.target.closest(".rv-settings")) showSettings(false); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !pop.hidden) { showSettings(false); gear.focus(); } });

  // ---------- wiring ----------
  function showPane(p) { $("#panes").dataset.show = p; $$("button[data-show]").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.show === p); }); fit(); }
  function setVersion(v) {
    ui.v = v; $$("[data-v]").forEach(function (x) { x.setAttribute("aria-pressed", x.dataset.v === v); }); renderResume();
    if (selected >= 0) flash(EV[selected].links || [], true);
  }
  $("#play").onclick = function () { if (playing) pause(); else play(); };
  $("#scrub").max = END;
  $("#scrub").addEventListener("input", function (e) { holdUntil = 0; setNow(+e.target.value, false); scrollWithin($("#chat-scroll"), $("#feed").lastElementChild, "bottom"); });
  $("#lanes").addEventListener("click", function (ev) {
    var b = ev.target.closest(".blk"), s = ev.target.closest("[data-step]");
    if (b) { jumpTo(laneEvent(LANES[b.dataset.j])); if (narrow()) showPane("chat"); }
    if (s) { var st = STEPS[+s.dataset.step]; var i = -1; EV.some(function (e, k) { if (e.kind === "step" && e.t === st.t) { i = k; return true; } return false; }); jumpTo(i); }
  });
  $("#ctabs").addEventListener("click", function (ev) { var b = ev.target.closest("[data-tab]"); if (b) { $("#follow").checked = false; openTab(b.dataset.tab); } });
  $("#ctabs").addEventListener("keydown", function (ev) {
    if (ev.key !== "ArrowRight" && ev.key !== "ArrowLeft") return;
    var k = 0; TABS.forEach(function (t, x) { if (t.id === tab) k = x; });
    var n = TABS[(k + (ev.key === "ArrowRight" ? 1 : TABS.length - 1)) % TABS.length].id;
    $("#follow").checked = false; openTab(n); $('[data-tab="' + n + '"]').focus();
  });
  $("#feed").addEventListener("click", function (ev) {
    if (ev.target.closest("a")) return;
    var m = ev.target.closest("[data-i]");
    if (m) { if (playing) pause(); select(+m.dataset.i, false); if (narrow() && (EV[m.dataset.i].links || []).length) showPane("resume"); }
  });
  $("#feed").addEventListener("keydown", function (ev) { if (ev.key === "Enter" && ev.target.matches("[data-i]")) ev.target.click(); });
  $$("[data-v]").forEach(function (b) { b.onclick = function () { userV = b.dataset.v; store.set("version", userV); setVersion(userV); }; });
  $("#cutbar").addEventListener("click", function (ev) { var b = ev.target.closest("[data-jump]"); if (b) setVersion(b.dataset.jump); });
  $("#diff").onchange = function (e) { ui.diff = e.target.checked; store.set("diff", ui.diff ? "1" : "0"); renderResume(); };
  function setZoom(z) { ui.zoom = z; $$("[data-z]").forEach(function (x) { x.setAttribute("aria-pressed", x.dataset.z === z); }); fit(); }
  $$("[data-z]").forEach(function (b) { b.onclick = function () { store.set("zoom", b.dataset.z); setZoom(b.dataset.z); }; });
  $$("button[data-show]").forEach(function (b) { b.onclick = function () { showPane(b.dataset.show); }; });
  function setDetails(open) {
    $("#rv-bar").classList.toggle("closed", !open);
    var b = $("#details-toggle"); b.textContent = open ? "Hide details" : "Show details"; b.setAttribute("aria-expanded", String(open));
  }
  $("#details-toggle").onclick = function () {
    var open = $("#rv-bar").classList.contains("closed"); setDetails(open); store.set("details", open ? "open" : "closed"); sizeToHeader();
  };
  setDetails(store.get("details") === "open");  // details start folded until the visitor opens them
  function setLanes(open) {
    $("#timeline").classList.toggle("closed", !open);
    var b = $("#lanes-toggle"); b.textContent = open ? "Hide timeline" : "Show timeline"; b.setAttribute("aria-expanded", String(open)); fit();
  }
  $("#lanes-toggle").onclick = function () { var open = $("#timeline").classList.contains("closed"); store.set("timeline", open ? "open" : "closed"); setLanes(open); };
  var pick = $("#example");
  if (EX.length) {
    var modes = []; EX.forEach(function (x) { if (modes.indexOf(x.mode) < 0) modes.push(x.mode); });
    pick.innerHTML = modes.map(function (m) {
      return '<optgroup label="' + esc(m) + '">' + EX.filter(function (x) { return x.mode === m; }).map(function (x) {
        return '<option value="' + esc(x.slug) + '"' + (x.slug === R.slug ? " selected" : "") + ">" + esc(x.title) + "</option>";
      }).join("") + "</optgroup>";
    }).join("");
    pick.onchange = function () { location.href = "../" + pick.value + "/"; };
  }
  function sizeToHeader() { var h = $("header.site"); document.documentElement.style.setProperty("--hdr", (h ? h.offsetHeight : 0) + "px"); fit(); }
  addEventListener("resize", sizeToHeader);
  document.addEventListener("keydown", function (ev) {
    if (ev.target.closest("input, select, textarea, button, a, [data-i]")) return;
    if (ev.key === " ") { ev.preventDefault(); if (playing) pause(); else play(); }
    if (ev.key === "ArrowRight" || ev.key === "ArrowLeft") {
      var dir = ev.key === "ArrowRight" ? 1 : -1, i = selected < 0 ? EV.length : selected;
      do { i += dir; } while (i >= 0 && i < EV.length && EV[i].kind === "step");
      if (i >= 0 && i < EV.length) jumpTo(i);
    }
  });
  (function () { // drag the divider to resize the panes on wide screens
    var d = $("#divider"), panes = $("#panes");
    var set = function (p) { p = Math.max(25, Math.min(75, p)); panes.style.setProperty("--split", p + "%"); d.setAttribute("aria-valuenow", Math.round(p)); fit(); };
    d.addEventListener("pointerdown", function (e) {
      d.setPointerCapture(e.pointerId); d.classList.add("drag");
      var r = panes.getBoundingClientRect();
      var move = function (ev) { set((ev.clientX - r.left) / r.width * 100); };
      var up = function () { d.classList.remove("drag"); d.removeEventListener("pointermove", move); d.removeEventListener("pointerup", up); };
      d.addEventListener("pointermove", move); d.addEventListener("pointerup", up);
    });
    d.addEventListener("keydown", function (e) { var cur = +d.getAttribute("aria-valuenow"); if (e.key === "ArrowLeft") set(cur - 3); if (e.key === "ArrowRight") set(cur + 3); });
  })();

  // the visitor's own choices win; otherwise: changes shown, whole page, timeline open, the new resume at rest
  userV = store.get("version"); ui.v = userV || "after"; ui.diff = store.get("diff") !== "0"; $("#diff").checked = ui.diff;
  $$("[data-v]").forEach(function (x) { x.setAttribute("aria-pressed", x.dataset.v === ui.v); });
  setZoom(store.get("zoom") || "page");
  buildLanes(); renderResume(); sizeToHeader();
  TABS.forEach(function (t) { seen[t.id] = visible(t.id, END); }); // at rest the whole run is on show, so nothing counts as new
  showPane("chat");
  setLanes(store.get("timeline") !== "closed");
  // Autoplay starts from the beginning, so the whole run is drawn only when it stays at rest.
  if ($("#autoplay").checked && !reduce) play(); else { setNow(END, false); renderTabs(); }
})();
