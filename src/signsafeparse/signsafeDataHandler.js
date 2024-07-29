const p = "D23ABC@#56"
function w(t) {
    var {SIGN: t, str: n} = t
      , n = (n = decodeURI(n),
    u.a.HmacSHA1(u.a.enc.Utf8.parse(n), t));
    t = u.a.enc.Base64.stringify(n).toString();
    return s()(t)
}
O = w({
    SIGN: p,
    str: d.replace(/^\/|https?:\/\/\/?/, "")
})