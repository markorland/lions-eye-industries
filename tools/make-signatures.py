"""Write assets/signatures.html — one email signature per mailbox.

Run from the repo root: python3 tools/make-signatures.py

The three signatures share a layout and differ only in the desk name and the
two fine-print lines, so they are generated rather than hand-kept. The markup
is deliberately plain — tables, inline styles, Arial — because Outlook renders
mail through Word's engine.
"""

LOGO = "https://lionseyeindustries.com/assets/img/logo-email.png"
SANS = "Arial, Helvetica, sans-serif"

DESKS = [
    dict(key="secretary", desk="Office of the Secretary",
         addr="enquiries@lionseyeindustries.com",
         fine=["Lions Eye Industries S.A. &middot; Registered office 46&deg;12&prime;14.84&Prime;&nbsp;N, 6&deg;09&prime;08.73&Prime;&nbsp;E",
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

def signature(d):
    fine = "\n".join(
        f'            <div style="font-family:{SANS};font-size:11px;line-height:17px;color:#6a6862;">{line}</div>'
        for line in d["fine"])
    return f'''<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">
  <tr>
    <td style="padding:0 16px 0 0;vertical-align:top;">
      <img src="{LOGO}" width="57" height="38" alt="Lions Eye Industries"
           style="display:block;width:57px;height:38px;border:0;outline:none;text-decoration:none;">
    </td>
    <td style="padding:0 0 0 16px;vertical-align:top;border-left:1px solid #e2ded5;">
      <div style="font-family:{SANS};font-size:13px;line-height:18px;letter-spacing:2px;color:#14161a;font-weight:bold;">LIONS EYE INDUSTRIES</div>
      <div style="font-family:{SANS};font-size:13px;line-height:20px;color:#8a6a22;">{d["desk"]}</div>
      <div style="font-family:{SANS};font-size:13px;line-height:20px;color:#14161a;">
        <a href="https://lionseyeindustries.com" style="color:#14161a;text-decoration:none;">lionseyeindustries.com</a>
      </div>
      <div style="height:1px;line-height:1px;font-size:0;background:#e2ded5;margin:10px 0 8px;">&nbsp;</div>
{fine}
    </td>
  </tr>
</table>'''

sigs = {d["key"]: signature(d) for d in DESKS}

# --- the copy-from page -----------------------------------------------------
blocks = "\n\n".join(f'''  <section>
    <h2>{d["desk"]} <span>{d["addr"]}</span></h2>
    <div class="sig">
{signature(d)}
    </div>
  </section>''' for d in DESKS)

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Email signatures — Lions Eye Industries</title>
<style>
  body {{ margin:0; background:#fff; color:#14161a; font:14px/1.6 {SANS}; }}
  .wrap {{ max-width:720px; margin:0 auto; padding:48px 24px 80px; }}
  h1 {{ font-size:20px; letter-spacing:.04em; margin:0 0 8px; }}
  .lede {{ color:#55534e; margin:0 0 40px; max-width:58ch; }}
  section {{ margin:0 0 44px; }}
  h2 {{ font-size:12px; text-transform:uppercase; letter-spacing:.14em; color:#8a6a22;
       margin:0 0 12px; font-weight:normal; }}
  h2 span {{ color:#9b998f; text-transform:none; letter-spacing:0; margin-left:8px; }}
  .sig {{ border:1px dashed #d8d4cb; padding:20px; }}
  footer {{ margin-top:56px; padding-top:20px; border-top:1px solid #e6e2d9;
            color:#6a6862; font-size:13px; }}
  code {{ background:#f4f2ed; padding:1px 5px; border-radius:3px; font-size:12px; }}
</style>
</head>
<body>
<div class="wrap">
  <h1>Email signatures</h1>
  <p class="lede">Select a signature inside its dashed box, copy, and paste into the signature
  settings of the mailbox named above it. Paste the rendered block — Gmail has no HTML view.</p>

{blocks}

  <footer>
    The logo loads from <code>lionseyeindustries.com/assets/img/logo-email.png</code>, so images
    only appear once the custom domain resolves. This page is not linked from the site and is
    marked <code>noindex</code>; delete it once the signatures are installed.
  </footer>
</div>
</body>
</html>
'''

open("assets/signatures.html", "w").write(page)
for k, v in sigs.items():
    open(f"/tmp/claude-1000/-mnt-f-mark-wd-Documents-Claude-lions-eye-industries/3dced30e-759e-4cfe-81d5-0ff508f4e27d/scratchpad/sig-{k}.html", "w").write(v)
print("wrote signatures.html and three snippets")
