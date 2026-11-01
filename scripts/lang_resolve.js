/* Language resolution for every page without a language prefix (inlined into each by build_site.py; tests run this file in node).
   Order: ?lang=xx in the URL > the language the visitor chose before (localStorage) > navigator.languages (first supported) > English.
   Plain ES5, no module syntax: the file is pasted into the page as-is. */
function ltNorm(code, supported) {
  var c = String(code == null ? '' : code).toLowerCase().replace(/_/g, '-').split('-')[0];
  return supported.indexOf(c) >= 0 ? c : null;
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
