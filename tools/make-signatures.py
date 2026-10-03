"""Write assets/signatures.html — one email signature per mailbox.

Run from the repo root: python3 tools/make-signatures.py

The three signatures share a layout and differ only in the desk name and the
two fine-print lines, so they are generated rather than hand-kept.

Nothing in the layout depends on CSS. Clients strip padding when the markup is
pasted into a signature box, so gaps are transparent 1x1 images stretched by
their width and height attributes — dimensions survive where styles do not —
and the horizontal rule is an <hr>, which carries its own margins and is kept
by sanitisers because it is semantic HTML. The <hr> also takes size, noshade
and color attributes, so a fully stripped fallback is still a hairline rather
than the default 3D line. Styles remain on the text for colour and face; if
they are dropped, the signature degrades to plain text in the right order.
"""

LOGO = "https://lionseyeindustries.com/assets/img/logo-email.png"
SPACER = "https://lionseyeindustries.com/assets/img/spacer.png"
SANS = "Arial, Helvetica, sans-serif"
RULE = "#dcd8cf"
GUTTER = 18

DESKS = [
    dict(key="secretary", desk="Office of the Secretary",
         addr="enquiries@lionseyeindustries.com",
         fine=["Lions Eye Industries S.A. &middot; Registered office "
               "46&deg;12&prime;14.84&Prime;&nbsp;N, 6&deg;09&prime;08.73&Prime;&nbsp;E",
               "Correspondence is read and retained indefinitely."]),
    dict(key="disclosure", desk="Group Disclosure",
         addr="disclosure@lionseyeindustries.com",
         fine=["The group does not comment on operational matters.",
               "Nothing in this message constitutes an admission."]),
    dict(key="engagements", desk="Engagements Desk",
         addr="engagements@lionseyeindustries.com",
         fine=["Credentials are required before a substantive reply.",
               "This message is not an offer and creates no obligation."]),
]

SPACER_IMG = ('<img src="%s" width="%%d" height="%%d" alt="" '
              'style="display:block;border:0;">' % SPACER)

FINE = ('      <div style="font-family:%s;font-size:11px;line-height:17px;'
        'color:#6a6862;">%s</div>')

SIG = '''<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">
  <tr>
    <td valign="middle">
      <img src="%(logo)s" width="57" height="38" alt="Lions Eye Industries"
           style="display:block;width:57px;height:38px;border:0;outline:none;text-decoration:none;">
    </td>
    <td valign="middle">%(gutter)s</td>
    <td bgcolor="%(rule)s" valign="middle" style="background-color:%(rule)s;">%(hair)s</td>
    <td valign="middle">%(gutter)s</td>
    <td valign="middle">
      <div style="font-family:%(sans)s;font-size:13px;line-height:18px;letter-spacing:2px;color:#14161a;font-weight:bold;">LIONS EYE INDUSTRIES</div>
      <div style="font-family:%(sans)s;font-size:13px;line-height:20px;color:#8a6a22;">%(desk)s</div>
      <hr size="1" noshade color="%(rule)s" style="border:0;border-top:1px solid %(rule)s;height:1px;margin:10px 0 9px;">
%(fine)s
    </td>
  </tr>
</table>'''


def signature(d):
    fine = "\n".join(FINE % (SANS, line) for line in d["fine"])
    return SIG % dict(logo=LOGO, sans=SANS, rule=RULE, desk=d["desk"], fine=fine,
                      gutter=SPACER_IMG % (GUTTER, 1), hair=SPACER_IMG % (1, 1))


SECTION = '''  <section>
    <h2>%s <span>%s</span></h2>
    <div class="sig">
%s
    </div>
  </section>'''

PAGE = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Email signatures &mdash; Lions Eye Industries</title>
<style>
  body { margin:0; background:#fff; color:#14161a; font:14px/1.6 SANS_STACK; }
  .wrap { max-width:720px; margin:0 auto; padding:48px 24px 80px; }
  h1 { font-size:20px; letter-spacing:.04em; margin:0 0 8px; }
  .lede { color:#55534e; margin:0 0 40px; max-width:58ch; }
  section { margin:0 0 44px; }
  h2 { font-size:12px; text-transform:uppercase; letter-spacing:.14em; color:#8a6a22;
       margin:0 0 12px; font-weight:normal; }
  h2 span { color:#9b998f; text-transform:none; letter-spacing:0; margin-left:8px; }
  .sig { border:1px dashed #d8d4cb; padding:20px; }
  footer { margin-top:56px; padding-top:20px; border-top:1px solid #e6e2d9;
           color:#6a6862; font-size:13px; }
  code { background:#f4f2ed; padding:1px 5px; border-radius:3px; font-size:12px; }
</style>
</head>
<body>
<div class="wrap">
  <h1>Email signatures</h1>
  <p class="lede">Select a signature inside its dashed box, copy, and paste into the signature
  settings of the mailbox named above it. Paste the rendered block &mdash; Gmail has no HTML view.</p>

%s

  <footer>
    Images load from <code>lionseyeindustries.com/assets/img/</code>, so the logo and the spacers
    that hold the gaps open only appear once the custom domain resolves. This page is not linked
    from the site and is marked <code>noindex</code>; delete it once the signatures are installed.
  </footer>
</div>
</body>
</html>
'''.replace("SANS_STACK", SANS)

blocks = "\n\n".join(SECTION % (d["desk"], d["addr"], signature(d)) for d in DESKS)
open("assets/signatures.html", "w").write(PAGE % blocks)

for d in DESKS:
    open("/tmp/claude-1000/-mnt-f-mark-wd-Documents-Claude-lions-eye-industries/"
         "3dced30e-759e-4cfe-81d5-0ff508f4e27d/scratchpad/sig-%s.html" % d["key"],
         "w").write(signature(d))

print("wrote assets/signatures.html and three snippets")
