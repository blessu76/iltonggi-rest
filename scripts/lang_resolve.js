/* Language resolution for every page without a language prefix (inlined into each by build_site.py; tests run this file in node).
   Order: ?lang=xx in the URL > the language the visitor chose before (localStorage) > navigator.languages (first supported) > English.
   Plain ES5, no module syntax: the file is pasted into the page as-is. */
function ltNorm(code, supported) {
  /* code (en, ko-KR, zh_TW, pt, in ...) -> the supported tag it means (zh-Hant, pt-BR ...) or null. Same rules as ipe_web_kit.languages.resolve:
     zh -> zh-Hant only for Hant/TW/HK/MO (Simplified is not supported), pt* -> pt-BR, in -> id. */
  var p = String(code == null ? '' : code).toLowerCase().replace(/_/g, '-').split('-').filter(Boolean), c = p[0];
  if (!c) return null;
  if (c === 'in') c = 'id'; /* legacy Indonesian code (old Android / Java): in -> id */
  if (c === 'zh') {
    var rest = p.slice(1), script = null, region = null;
    for (var j = 0; j < rest.length; j++) {
      if (rest[j].length === 4 && !script) script = rest[j]; else if (rest[j].length === 2 && !region) region = rest[j];
    }
    c = (script ? script === 'hant' : (region === 'tw' || region === 'hk' || region === 'mo')) ? 'zh-hant' : '';
  }
  if (c === 'pt') c = 'pt-br';
  for (var i = 0; i < supported.length; i++) if (supported[i].toLowerCase() === c) return supported[i];
  return null;
}
function ltParam(search) {
  var m = /[?&]lang=([^&#]*)/.exec(search || '');
  if (!m) return null;
  try { return decodeURIComponent(m[1]); } catch (e) { return null; }
}
function ltStrip(search) {
  var parts = String(search || '').replace(/^\?/, '').split('&').filter(function (p) { return p && !/^lang=/.test(p); });
  return parts.length ? '?' + parts.join('&') : '';
}
/* o = { search, stored, languages, supported } -> { lang, from: 'url' | 'stored' | 'browser' | 'default' } */
function ltResolve(o) {
  var s = o.supported, v = ltNorm(ltParam(o.search), s);
  if (v) return { lang: v, from: 'url' };
  v = ltNorm(o.stored, s);
  if (v) return { lang: v, from: 'stored' };
  var list = o.languages || [];
  for (var i = 0; i < list.length; i++) { v = ltNorm(list[i], s); if (v) return { lang: v, from: 'browser' }; }
  return { lang: 'en', from: 'default' };
}
