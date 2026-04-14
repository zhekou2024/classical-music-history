/**
 * Single source of truth for per-work Spotify links.
 * Works must carry canonicalSpotifyUrl and/or canonicalSpotifyTrackId from data/*.json
 * (merged from data/spotify_canonical_map.json at build time).
 */
(function (global) {
  var TRACK_URL = /^https:\/\/open\.spotify\.com\/track\/[0-9A-Za-z]{22}\/?$/;

  function getCanonicalSpotifyTrackUrl(work) {
    if (!work || typeof work === "string") return null;
    var u = work.canonicalSpotifyUrl;
    if (typeof u === "string" && TRACK_URL.test(u.trim())) return u.trim().replace(/\/$/, "");
    var id = work.canonicalSpotifyTrackId;
    if (typeof id === "string") {
      id = id.trim();
      if (/^[0-9A-Za-z]{22}$/.test(id)) return "https://open.spotify.com/track/" + id;
    }
    return null;
  }

  global.getCanonicalSpotifyTrackUrl = getCanonicalSpotifyTrackUrl;
})(typeof window !== "undefined" ? window : globalThis);
