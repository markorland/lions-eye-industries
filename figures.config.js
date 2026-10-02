/* ──────────────────────────────────────────────────────────────────────────
   Lions Eye Industries — group figures
   ──────────────────────────────────────────────────────────────────────────
   This is the only file you need to edit to move the numbers in the
   "footprint" band. Bump them whenever you like; nothing else has to change.

   figures one entry per tile, rendered left to right, after "Year established"
   asAt    optional. The reporting date above the figures is normally derived
           from the current quarter, in step with the group bulletin numeral
           (third quarter 2026 → "as at 30 September 2026"). Set asAt only to
           pin it to some other date.

   Each figure takes:
     label  the small caps line above the number
     value  a string shown verbatim ('68,400'), or a plain number (68400),
            which gets thousands separators automatically
     unit   optional, set in gold at a smaller size beside the number
     key    optional. The figure tagged key: 'jurisdictions' also fills in the
            "Operating in N jurisdictions" line at the top of the page.

   Add or remove entries freely — the grid reflows. Four or five reads best.
   ────────────────────────────────────────────────────────────────────────── */

window.LEI_FIGURES = {

  // asAt: '30 June 2026',   // uncomment to pin the reporting date

  figures: [
    { label: 'Jurisdictions of operation', value: 41, key: 'jurisdictions' },
    { label: 'Personnel under direction',  value: 68400 },
    { label: 'Facilities & installations',  value: 212 },
    { label: 'Assets under direction',     value: '94.6', unit: 'B USD' }
  ]

};
