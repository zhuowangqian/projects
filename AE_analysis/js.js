// var e = '__zp_stoken__', t, n = 3840, s = ".zhipin.com", a = '/'
window = {'gtk': '320305.131321201'};
var r = null;

function n(t, e) {
    for (var n = 0; n < e.length - 2; n += 3) {
        var r = e.charAt(n + 2);
        r = "a" <= r ? r.charCodeAt(0) - 87 : Number(r),
            r = "+" === e.charAt(n + 1) ? t >>> r : t << r,
            t = "+" === e.charAt(n) ? t + r & 4294967295 : t ^ r
    }
    return t
}


function b(t) {
    var o, i = t.match(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g);
    if (null === i) {
        var a = t.length;
        a > 30 && (t = "".concat(t.substr(0, 10)).concat(t.substr(Math.floor(a / 2) - 5, 10)).concat(t.substr(-10, 10)))
    } else {
        for (var s = t.split(/[\uD800-\uDBFF][\uDC00-\uDFFF]/), c = 0, u = s.length, l = []; c < u; c++)
            "" !== s[c] && l.push.apply(l, function (t) {
                if (Array.isArray(t))
                    return e(t)
            }(o = s[c].split("")) || function (t) {
                if ("undefined" != typeof Symbol && null != t[Symbol.iterator] || null != t["@@iterator"])
                    return Array.from(t)
            }(o) || function (t, n) {
                if (t) {
                    if ("string" == typeof t)
                        return e(t, n);
                    var r = Object.prototype.toString.call(t).slice(8, -1);
                    return "Object" === r && t.constructor && (r = t.constructor.name),
                        "Map" === r || "Set" === r ? Array.from(t) : "Arguments" === r || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r) ? e(t, n) : void 0
                }
            }(o) || function () {
                throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")
            }()),
            c !== u - 1 && l.push(i[c]);
        var p = l.length;
        p > 30 && (t = l.slice(0, 10).join("") + l.slice(Math.floor(p / 2) - 5, Math.floor(p / 2) + 5).join("") + l.slice(-10).join(""))
    }
    for (var d = "".concat(String.fromCharCode(103)).concat(String.fromCharCode(116)).concat(String.fromCharCode(107)), h = (null !== r ? r : (r = window[d] || "") || "").split("."), f = Number(h[0]) || 0, m = Number(h[1]) || 0, g = [], y = 0, v = 0; v < t.length; v++) {
        var _ = t.charCodeAt(v);
        _ < 128 ? g[y++] = _ : (_ < 2048 ? g[y++] = _ >> 6 | 192 : (55296 == (64512 & _) && v + 1 < t.length && 56320 == (64512 & t.charCodeAt(v + 1)) ? (_ = 65536 + ((1023 & _) << 10) + (1023 & t.charCodeAt(++v)),
            g[y++] = _ >> 18 | 240,
            g[y++] = _ >> 12 & 63 | 128) : g[y++] = _ >> 12 | 224,
            g[y++] = _ >> 6 & 63 | 128),
            g[y++] = 63 & _ | 128)
    }
    for (var b = f, w = "".concat(String.fromCharCode(43)).concat(String.fromCharCode(45)).concat(String.fromCharCode(97)) + "".concat(String.fromCharCode(94)).concat(String.fromCharCode(43)).concat(String.fromCharCode(54)), k = "".concat(String.fromCharCode(43)).concat(String.fromCharCode(45)).concat(String.fromCharCode(51)) + "".concat(String.fromCharCode(94)).concat(String.fromCharCode(43)).concat(String.fromCharCode(98)) + "".concat(String.fromCharCode(43)).concat(String.fromCharCode(45)).concat(String.fromCharCode(102)), x = 0; x < g.length; x++)
        b = n(b += g[x], w);
    return b = n(b, k),
    (b ^= m) < 0 && (b = 2147483648 + (2147483647 & b)),
        "".concat((b %= 1e6).toString(), ".").concat(b ^ f)
}

function e() {
    var r3Z = 22;
    while (!![]) {
        switch (r3Z) {
            case 1:
                if (r + s > 0) {
                    x = r + x;
                    s = r - x
                }
                r3Z += 24;
                break;
            case 2:
                i = i.p(h);
                r3Z += 12;
                break;
            case 3:
                L = L.p(I);
                r3Z += 6;
                break;
            case 4:
                i = i + 1;
                r3Z += 35;
                break;
            case 5:
                if (s + x < 0) {
                    r = p << s * x >> p
                }
                r3Z -= 2;
                break;
            case 6:
                if (p + r + p > 0) {
                    r = p >> s + x >> p;
                    x = r + x
                }
                r3Z += 7;
                break;
            case 7:
                for (var a8 = 0; a8 < V; a8++) {
                    a2 = a5[W];
                    a3 = a5[W + 1];
                    W = W + 2;
                    a2 = a2 - 46;
                    a3 = a3 - 46;
                    a1 = a3 * 19 + a2;
                    a0 = a1 ^ 11;
                    a7[a8] = a0
                }
                r3Z += 19;
                break;
            case 8:
                L = I;
                r3Z -= 7;
                break;
            case 9:
                if (r + s > 0) {
                    s = s << 2;
                    r = s >> x + x >> p;
                    x = r / x
                }
                r3Z += 25;
                break;
            case 10:
                i = [190, 72, 98];
                r3Z += 1;
                break;
            case 11:
                if (p && !r) {
                    x = s % 3;
                    x = r + x
                }
                r3Z += 1;
                break;
            case 12:
                for (var F = 0; F < i.length; F++) {
                    y = y + $(i[F] >> 1)
                }
                r3Z -= 10;
                break;
            case 13:
                var I = "oPIcuJUL0jTbdyr24ws7Hz3S=61e"
                    , L = 1;
                r3Z -= 5;
                break;
            case 14:
                r = -5;
                r3Z += 23;
                break;
            case 15:
                if (p + x < r) {
                    x = p >> s + x >> p - r >> x
                }
                r3Z += 20;
                break;
            case 16:
                h = i;
                r3Z -= 6;
                break;
            case 17:
                T = a4.length;
                r3Z += 23;
                break;
            case 18:
                h = 1;
                r3Z += 6;
                break;
            case 19:
                if (r + x > 0) {
                    x = s >> 4 + r >> 3 * r + s << 2
                }
                r3Z += 24;
                break;
            case 20:
                var a7 = [];
                r3Z += 22;
                break;
            case 21:
                if (s < 0) {
                    s = r >> p / x >> p
                }
                r3Z += 7;
                break;
            case 22:
                var h = "ydE"
                    , i = 1;
                r3Z -= 18;
                break;
            case 23:
                V = a5.length;
                r3Z -= 4;
                break;
            case 24:
                var y = "";
                r3Z += 17;
                break;
            case 25:
                I = 1;
                r3Z += 7;
                break;
            case 26:
                var a9 = "", a_, a$, aa, ab;
                r3Z += 10;
                break;
            case 27:
                if (!p) {
                    p = 5 + s >> 3
                }
                r3Z += 3;
                break;
            case 28:
                L = [5, 18, 19, 11, 6, 20, 14, 21, 4, 9, 17, 22, 23, 2, 3, 24, 7, 15, 25, 26, 8, 1, 0, 27, 12, 16, 10, 13];
                r3Z += 10;
                break;
            case 29:
                this[a9] = M.j("");
                return;
            case 30:
                for (var a6 = 0; a6 < T; a6++) {
                    U = a4.d(a6);
                    if (U >= 65536 && U <= 1114111) {
                        a5.p(U >> 18 & 7 | 240);
                        a5.p(U >> 12 & 63 | 128);
                        a5.p(U >> 6 & 63 | 128);
                        a5.p(U & 63 | 128)
                    } else if (U >= 2048 && U <= 65535) {
                        a5.p(U >> 12 & 15 | 224);
                        a5.p(U >> 6 & 63 | 128);
                        a5.p(U & 63 | 128)
                    } else if (U >= 128 && U <= 2047) {
                        a5.p(U >> 6 & 31 | 192);
                        a5.p(U & 63 | 128)
                    } else {
                        a5.p(U & 255)
                    }
                }
                r3Z -= 7;
                break;
            case 31:
                if (!r) {
                    s = s << 2 + r - p
                }
                r3Z -= 14;
                break;
            case 32:
                I = I * 5;
                r3Z -= 17;
                break;
            case 33:
                I = L;
                r3Z -= 12;
                break;
            case 34:
                var T, U, V, W, a0, a1, a2, a3, a4 = "627001";
                r3Z -= 3;
                break;
            case 35:
                var M = [];
                r3Z -= 2;
                break;
            case 36:
                for (var ac = 0; ac < a7.length; ac++) {
                    a_ = a7[ac].toString(2);
                    a$ = a_.match(/^1+?(?=0)/);
                    if (a$ && a_.length === 8) {
                        aa = a$[0].length;
                        ab = a7[ac].toString(2).slice(7 - aa);
                        for (var ad = 0; ad < aa; ad++) {
                            ab += a7[ad + ac].toString(2).slice(2)
                        }
                        a9 += $(parseInt(ab, 2));
                        ac += aa - 1
                    } else {
                        a9 += $(a7[ac])
                    }
                }
                r3Z -= 7;
                break;
            case 37:
                this[y] = [[1, 1, 0, 1, 0], [1, 1, 1, 0, 0], [1, 0, 0, 1, 1], [0, 1, 0, 1, 1]];
                r3Z -= 31;
                break;
            case 38:
                for (var P = 0; P < I.length; P++) {
                    M.p(I.c(L[P]))
                }
                r3Z -= 33;
                break;
            case 39:
                var p = 1
                    , r = -1
                    , s = 2
                    , x = 0;
                r3Z -= 21;
                break;
            case 40:
                var a5 = [];
                r3Z -= 13;
                break;
            case 41:
                if (p + r > 0) {
                    x = s >> 3;
                    x = r + x;
                    r = p >> s * x >> p;
                    x = r / x
                }
                r3Z -= 25;
                break;
            case 42:
                W = 0;
                r3Z -= 35;
                break;
            case 43:
                V = V / 2;
                r3Z -= 23;
                break;
        }
    }
}

function set(e, t, n, i, a) {
    var o = e + "=" + encodeURIComponent(t);
    if (n) {
        var s = new Date;
        s.setTime(s.getTime() + 60 * n * 1e3),
            o += ";expires=" + s.toGMTString()
    }
    if (o = i ? o + ";domain=" + i : o,
        o = a ? o + ";path=" + a : o,
        document.cookie = o,
    void 0 !== window.wst && "function" == typeof window.wst.postMessage) {
        var u = {
            name: "setWKCookie",
            params: {
                url: i || r,
                name: e,
                value: encodeURIComponent(t),
                expiredate: s.getTime(),
                path: a || "/"
            }
        };
        window.wst.postMessage(JSON.stringify(u))
    }
}

function clearcookie(e, t, n) {
    i.get(e) && (document.cookie = e + "=" + (t ? ";path=" + t : "") + (n ? ";domain=" + n : "") + ";expires=Thu,01-Jan-1970 00:00:01 GMT")
}


function cookie_get(t, n) {
    (new Date).getTime();
    var r = "";
    try {
        r = (new e).z(t, parseInt(n) + 60 * (480 + (new Date).getTimezoneOffset()) * 1e3)
    } catch (e) {
    }
    r && a.default.set("__zp_stoken__", r, 3840, s, "/")
    a.default.clearcookie("__zp_sseed__", "/", s),
        a.default.clearcookie("__zp_sname__", "/", s),
        a.default.clearcookie("__zp_sts__", "/", s)
}


function time() {
    // return (new Date).getTimezoneOffset();
    return new Date()['getTime']();
}


function Wqj() {
    var Bbf = 0
        , l9Q = [20, 11, 27, 1, 14, 17, 21, 19, 7, 25, 22, 10, 2, 26, 12, 6, 16];
    while (!![]) {
        switch (l9Q[Bbf++]) {
            case 1:
                i = i + 1;
                break;
            case 2:
                r = r / p[4];
                break;
            case 3:
                r = r / p[8];
                break;
            case 4:
                for (var F = 0; F < i.length; F++) {
                    x = x + $(i[F] >> 4)
                }
                break;
            case 5:
                r = r - p[2];
                break;
            case 6:
                h = i;
                break;
            case 7:
                p[8] = r / p[4];
                Lv1.apply(l9Q, myw);
                break;
            case 8:
                return x;
            case 9:
                r = r - p[2];
                break;
            case 10:
                var x = "";
                break;
            case 11:
                for (var s = 0; s < 10; s++) {
                    p.p(s + 6)
                }
                break;
            case 12:
                r = r - p[2];
                break;
            case 13:
                i = [1648, 1616, 1856, 1344, 1680, 1744, 1616];
                break;
            case 14:
                r = r + p[6];
                break;
            case 15:
                if (p[8] - p[5] > 0) {
                    r = r + p[4];
                    r = r + p[6] - p[5]
                } else {
                    r = r * p[0];
                    r = r - p[2]
                }
                break;
            case 16:
                r = r * p[6];
                break;
            case 17:
                r = r * p[7];
                break;
            case 18:
                i = i.p(h);
                break;
            case 19:
                h = 1;
                break;
            case 20:
                var h = "mvk", i = 1, p = [], r;
                var myw = [23, 15, 13, 24, 9, 3, 4, 5, 18, 8];
                break;
            case 21:
                if (p[6] - p[5] > 0) {
                    r = r + p[3];
                    r = r + p[2] - p[5]
                } else {
                    r = r * p[6];
                    r = r - p[2]
                }
                break;
            case 22:
                r = r + p[8];
                break;
            case 23:
                var y = p[0];
                break;
            case 24:
                p[4] = r - p[5];
                break;
            case 25:
                r = r - p[6];
                break;
            case 26:
                if (r - p[6]) {
                    r = r + p[3]
                }
                break;
            case 27:
                r = p[4] + p[6];
                var Lv1 = l9Q.p;
                break;
        }
    }
}


function z(a, b) {
    var X6w = 0
        , Cv9 = [6, 10, 8, 1, 25, 12, 28, 23, 2, 3, 20];
    while (!![]) {
        switch (Cv9[X6w++]) {
            case 1:
                p = i[4] + i[6];
                break;
            case 2:
                oH();
                break;
            case 3:
                i[8] = p / i[4];
                break;
            case 4:
                p = p - i[2];
                break;
            case 5:
                x = Opv(s, y);
                break;
            case 6:
                var h = new Date()[Wqj()](), i = [], p;
                break;
            case 7:
                s = FV(y, b, h);
                break;
            case 8:
                var s, x, y;
                var Aap = Cv9.p;
                break;
            case 9:
                p = p / i[4];
                break;
            case 10:
                for (var r = 0; r < 10; r++) {
                    i.p(r + 6)
                }
                break;
            case 11:
                p = p * i[6];
                break;
            case 12:
                y = a;
                var jA1 = [18, 19, 9, 7, 30, 22, 24, 11, 29, 16];
                break;
            case 13:
                if (i[8] - i[5] > 0) {
                    p = p + i[4];
                    p = p + i[6] - i[5]
                } else {
                    p = p * i[0];
                    p = p - i[2]
                }
                break;
            case 14:
                return Evn(914 - 539, t1);
            case 15:
                p = p - i[2];
                break;
            case 16:
                vOP(this[kPx()]);
                break;
            case 17:
                B[Evn(1875 - 1403)][Evn(1613 - 1334)]["t"] = new Date()[Evn(1398 - 857)]() - h;
                break;
            case 18:
                B[iND()][Sg()][hG8()] = h;
                var yVv = [13, 21, 31, 4, 26, 5, 15, 27, 17, 14];
                break;
            case 19:
                p = p + i[8];
                break;
            case 20:
                p = p - i[6];
                break;
            case 21:
                i[4] = p - i[5];
                break;
            case 22:
                p = p - i[2];
                break;
            case 23:
                if (i[6] - i[5] > 0) {
                    p = p + i[3];
                    p = p + i[2] - i[5]
                } else {
                    p = p * i[6];
                    p = p - i[2]
                }
                break;
            case 24:
                DmP(y, b);
                Aap.apply(Cv9, yVv);
                break;
            case 25:
                p = p + i[6];
                break;
            case 26:
                p = p / i[8];
                break;
            case 27:
                Evn(1365 - 1191, x, y, this[Evn(919 - 568)], h);
                break;
            case 28:
                p = p * i[7];
                Aap.apply(Cv9, jA1);
                break;
            case 29:
                var F = i[0];
                break;
            case 30:
                if (p - i[6]) {
                    p = p + i[3]
                }
                break;
            case 31:
                Nc2();
                break;
        }
    }
}