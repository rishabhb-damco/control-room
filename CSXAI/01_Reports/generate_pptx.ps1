# CSXAI Strategy Report - PowerPoint Generator
# Rishabh B | Damco Digital | 27 May 2026

$ErrorActionPreference = "Stop"

# -- COLOR HELPER (PowerPoint: R + G*256 + B*65536) --------------------------
function Col([int]$r,[int]$g,[int]$b){ return [int]($r + $g*256 + $b*65536) }

$cNavy  = Col 13 27 42        # #0D1B2A
$cBlue  = Col 26 107 181      # #1A6BB5
$cGold  = Col 201 168 64      # #C9A840
$cTeal  = Col 26 138 138      # #1A8A8A
$cWhite = Col 255 255 255     # #FFFFFF
$cLight = Col 248 249 252     # #F8F9FC
$cCard  = Col 241 245 249     # #F1F5F9
$cRed   = Col 220 38 38       # #DC2626
$cGreen = Col 22 163 74       # #16A34A
$cAmber = Col 217 119 6       # #D97706
$cMid   = Col 100 116 139     # #64748B
$cBdr   = Col 226 232 240     # #E2E8F0
$cPurp  = Col 124 58 237      # #7C3AED
$cGoldL = Col 251 245 230     # #FBF5E6
$cBlueL = Col 235 244 255     # #EBF4FF
$cRedL  = Col 254 226 226     # #FEE2E2
$cGrnL  = Col 220 252 231     # #DCFCE7

# -- SHAPE HELPERS ------------------------------------------------------------
function Rect($sl,$l,$t,$w,$h,$col,$noLine=$true){
    $s = $sl.Shapes.AddShape(1,$l,$t,$w,$h)
    $s.Fill.Solid(); $s.Fill.ForeColor.RGB = $col
    if($noLine){ $s.Line.Visible = 0 } else { $s.Line.ForeColor.RGB = $cBdr; $s.Line.Weight = 0.5 }
    return $s
}

function TBox($sl,$l,$t,$w,$h,$txt,$sz,$col,$bold=$false,$align=1,$va=1,$italic=$false,$wrap=$true){
    $s = $sl.Shapes.AddTextbox(1,$l,$t,$w,$h)
    $tf = $s.TextFrame
    $tf.TextRange.Text = $txt
    $tf.TextRange.Font.Size = $sz
    $tf.TextRange.Font.Color.RGB = $col
    $tf.TextRange.Font.Bold = $bold
    $tf.TextRange.Font.Italic = $italic
    $tf.TextRange.ParagraphFormat.Alignment = $align  # 1=L 2=C 3=R
    $tf.VerticalAnchor = $va   # 1=Top 3=Middle
    $tf.WordWrap = $wrap
    $s.Line.Visible = 0; $s.Fill.Visible = 0
    return $s
}

function NavHdr($sl,$title,$sub=""){
    Rect $sl 0 0 960 46 $cNavy | Out-Null
    Rect $sl 0 46 960 2 $cGold | Out-Null
    TBox $sl 20 10 680 28 $title 14 $cWhite $true 1 3 | Out-Null
    if($sub -ne ""){TBox $sl 700 14 240 20 $sub 8 (Col 160 180 210) $false 3 3 | Out-Null}
}

function NewSlide($prs){
    $sl = $prs.Slides.Add($prs.Slides.Count+1, 12)  # 12 = ppLayoutBlank
    try{ while($sl.Shapes.Count -gt 0){$sl.Shapes.Item(1).Delete()} }catch{}
    $sl.Background.Fill.Solid()
    $sl.Background.Fill.ForeColor.RGB = $cWhite
    return $sl
}

function DivLine($sl,$top){ Rect $sl 20 $top 920 1 $cBdr | Out-Null }

# -- INIT POWERPOINT ----------------------------------------------------------
Write-Host "Starting PowerPoint..."
$ppt = New-Object -ComObject PowerPoint.Application
$ppt.Visible = 1
$prs = $ppt.Presentations.Add(1)
$prs.PageSetup.SlideWidth  = 960  # 13.33 inches x 72pt = widescreen 16:9
$prs.PageSetup.SlideHeight = 540

# ============================================================================
# SLIDE 1 - COVER
# ============================================================================
Write-Host "Slide 1: Cover..."
$sl = NewSlide $prs
$sl.Background.Fill.ForeColor.RGB = $cNavy

Rect $sl 0 0 960 5 $cGold | Out-Null              # Gold top strip

# Brand block
$br = Rect $sl 0 150 960 240 (Col 18 33 58) $true  # Slightly lighter navy band
$br.Line.Visible = 0

TBox $sl 80 165 800 80 "CSX Intelligence" 52 $cWhite $true 2 3 | Out-Null
TBox $sl 80 248 800 26 "AI Voice Agent / Financial Services & Real Estate" 13 $cGold $false 2 3 | Out-Null

Rect $sl 340 282 280 2 (Col 80 100 130) | Out-Null  # Separator line

TBox $sl 80 292 800 40 "Market Intelligence & Paid Media Strategy" 20 (Col 210 220 235) $false 2 3 | Out-Null
TBox $sl 80 338 800 24 "Go-To-Market Executive Briefing" 12 (Col 150 165 185) $false 2 3 | Out-Null

# Bottom info
TBox $sl 80 460 500 30 "27 May 2026  |  Prepared by Rishabh B  |  Damco Digital" 10 (Col 120 140 165) $false 1 3 | Out-Null
TBox $sl 700 460 240 30 "For: Shaivi Tyagi -> Nitya & Proneeta" 9 (Col 100 120 150) $false 3 3 | Out-Null

# Confidential badge
$cbg = Rect $sl 400 500 160 26 (Col 30 50 80)
$cbg.Line.ForeColor.RGB = $cGold; $cbg.Line.Weight = 0.75; $cbg.Line.Visible = 1
TBox $sl 400 504 160 18 "CONFIDENTIAL" 8 $cGold $true 2 3 | Out-Null

# ============================================================================
# SLIDE 2 - AGENDA
# ============================================================================
Write-Host "Slide 2: Agenda..."
$sl = NewSlide $prs
NavHdr $sl "Agenda" "CSXAI Strategy Report - 27 May 2026"

$items = @(
    @("01", "Competitor Overview", "Scale, platform presence, messaging strategy, paid media approach and creative patterns"),
    @("02", "Market & Opportunity Insights", "Audience demand signals, search intent, paid media gaps, competitor inefficiencies"),
    @("03", "Recommended Paid Media Strategy", "3 budget scenarios (`$200 / `$800 / `$2,000), platform priority, lean campaign structure"),
    @("04", "Performance Estimates & Forecasting", "3-month projections per budget - leads, CPL, reach, impressions, clicks"),
    @("05", "Final Recommendations", "Priority performance marketing actions, mandatory optimizations, key testing opportunities")
)

$y = 68
foreach($item in $items){
    $nb = Rect $sl 20 $y 36 36 $cNavy
    TBox $sl 20 ($y+2) 36 32 $item[0] 11 $cGold $true 2 3 | Out-Null
    TBox $sl 64 $y 280 18 $item[1] 12 $cNavy $true 1 1 | Out-Null
    TBox $sl 64 ($y+18) 860 20 $item[2] 10 $cMid $false 1 1 | Out-Null
    DivLine $sl ($y+44)
    $y += 50
}

# ============================================================================
# SLIDE 3 - COMPETITOR OVERVIEW: THE LANDSCAPE
# ============================================================================
Write-Host "Slide 3: Competitor Overview..."
$sl = NewSlide $prs
NavHdr $sl "Competitor Overview - The Landscape" "4 key players analyzed"

$cards = @(
    @(18, 58, "ELTROPY", "Direct Competitor", $cRedL, $cRed,
      "Target: Community banks & credit unions (US)",
      "Scale: `$12M to `$33M ARR in 24 months",
      "Brand searches: 1,900/mo (+26% YoY)",
      "Google Ads: ZERO - not running any paid search",
      "Channels: SDR outbound + ABM + 50+ partner integrations + LinkedIn"),
    @(492, 58, "GLIA", "Direct Competitor", $cRedL, $cRed,
      "Target: Banks & credit unions - 700+ clients",
      "Scale: Market leader / AIFinTech100 2025",
      "Lead magnet: Gated industry benchmarks report (400 FIs data)",
      "Key CTA: Request an Impact Study - personalised ROI forecast",
      "Channels: LinkedIn Ads + Events (Glia Interact) + FIS partnership"),
    @(18, 290, "KASISTO", "Direct / Declining", $cGoldL, $cAmber,
      "Target: Enterprise banking - KAI conversational AI platform",
      "Brand searches: 390/mo - DOWN -19% (3 months) / -46% YoY",
      "Insight: People actively search kasisto competitors = exit intent",
      "Trend: Losing mindshare - an interception opportunity for CSXAI",
      "Channels: LinkedIn + blog; paid media unclear"),
    @(492, 290, "RETELL AI / SYNTHFLOW", "Adjacent - Not Direct", $cBlueL, $cBlue,
      "Retell AI: Developer infrastructure / `$0.07/min / API-first",
      "Synthflow: No-code builder / individual real estate agents / SMBs",
      "Not competing at CSXAI institutional / enterprise level",
      "Retell uses Google + LinkedIn Ads targeting developers",
      "Parloa (EU) most aggressive paid spend (~49% paid traffic) - best benchmark")
)

foreach($c in $cards){
    $l=$c[0]; $t=$c[1]; $name=$c[2]; $tag=$c[3]; $bgc=$c[4]; $acc=$c[5]
    $body = $c[6..10]
    $crd = Rect $sl $l $t 450 226 $bgc $false
    $crd.Line.ForeColor.RGB = $acc; $crd.Line.Weight = 1.5; $crd.Line.Visible = 1
    Rect $sl $l $t 450 4 $acc | Out-Null
    TBox $sl ($l+10) ($t+10) 280 20 $name 12 $cNavy $true 1 1 | Out-Null
    $tagbg = Rect $sl ($l+295) ($t+8) 145 18 $acc
    TBox $sl ($l+295) ($t+8) 145 18 $tag 8 $cWhite $true 2 3 | Out-Null
    Rect $sl ($l+10) ($t+32) 430 1 $cBdr | Out-Null
    $by = $t + 40
    foreach($line in $body){
        TBox $sl ($l+10) $by 430 22 "* $line" 9 (Col 40 55 75) $false 1 1 | Out-Null
        $by += 22
    }
}

# ============================================================================
# SLIDE 4 - COMPETITOR MESSAGING & PAID MEDIA
# ============================================================================
Write-Host "Slide 4: Competitor Messaging..."
$sl = NewSlide $prs
NavHdr $sl "Competitor Messaging & Paid Media - How They Communicate & Convert"

$cols = @(130, 190, 140, 130, 160, 190)
$colX = @(18, 148, 338, 478, 608, 768)
$hdrs = @("Competitor", "Headline / Hook", "Key Metric Used", "Primary CTA", "Paid Media Activity", "Positioning Angle")

Rect $sl 18 56 940 26 $cNavy | Out-Null
for($i=0;$i-lt 6;$i++){
    TBox $sl ($colX[$i]+2) 58 ($cols[$i]-4) 22 $hdrs[$i] 8 $cWhite $true 1 3 | Out-Null
}

$rows = @(
    @("Eltropy", '"The AI Platform Community FIs Trust"', "83% call containment / 1,200 digital leads/client/mo", "Schedule a Demo", "ZERO Google Ads paid search / LinkedIn Organic + SDR", "Efficiency + scale for community banks"),
    @("Glia", '"End Efficiency vs. Experience Tradeoff"', '"Handle 2x more calls without hiring"', "See a Demo + Request Impact Study (ROI calculator)", "LinkedIn Ads active / Minimal Google (~9% paid traffic)", "Efficiency + experience / no-hallucination guarantee"),
    @("Kasisto", '"1,000+ Banking Tasks Out of the Box"', "Task breadth + banking-specific capabilities", "Get a Demo", "Paid media evidence unclear / LinkedIn present", "Technical depth / enterprise banking AI"),
    @("Retell AI", '"Build voice AI at $0.07/min"', "Cost per minute / speed to deploy", "Start for Free / API Docs", "Google Ads + LinkedIn targeting developers", "Infrastructure price + speed / developer audience")
)

$rowColors = @($cWhite, $cCard, $cWhite, $cCard)
$ry = 82
for($r=0;$r-lt 4;$r++){
    Rect $sl 18 $ry 940 48 $rowColors[$r] | Out-Null
    Rect $sl 18 ($ry+47) 940 1 $cBdr | Out-Null
    for($ci=0;$ci-lt 6;$ci++){
        TBox $sl ($colX[$ci]+2) ($ry+2) ($cols[$ci]-4) 44 $rows[$r][$ci] 8 (Col 25 40 60) $false 1 1 | Out-Null
    }
    $ry += 48
}

Rect $sl 18 286 940 36 (Col 30 40 60) | Out-Null
TBox $sl 24 290 930 28 "Key Insight: All competitors lead with efficiency metrics - deflection rates, call volumes, task counts. None lead with empathy, experience quality, or compliance-first positioning." 9 (Col 220 235 255) $false 1 3 | Out-Null

# ============================================================================
# SLIDE 5 - THE UNOCCUPIED POSITION
# ============================================================================
Write-Host "Slide 5: The Open Position..."
$sl = NewSlide $prs
$sl.Background.Fill.ForeColor.RGB = $cNavy
Rect $sl 0 0 960 5 $cGold | Out-Null

TBox $sl 40 18 880 32 "The Unoccupied Position - CSXAI's Competitive Advantage" 18 $cWhite $true 1 3 | Out-Null

Rect $sl 30 58 440 310 (Col 22 38 60) | Out-Null
Rect $sl 30 58 440 4 $cRed | Out-Null
TBox $sl 40 66 420 22 "WHAT EVERY COMPETITOR LEADS WITH" 9 (Col 200 80 80) $true 1 3 | Out-Null
$left = @(
    '"83% call containment"',
    '"Handle 2x more calls without hiring"',
    '"1,000+ banking tasks out of the box"',
    '"Zero hallucinations - contractual guarantee"',
    "Automation volume / deflection rates / cost reduction",
    "Operational efficiency metrics dominate all messaging"
)
$ly = 94
foreach($line in $left){
    TBox $sl 40 $ly 420 26 "* $line" 10 (Col 210 220 235) $false 1 1 | Out-Null
    $ly += 30
}

Rect $sl 490 58 440 310 (Col 35 50 25) | Out-Null
Rect $sl 490 58 440 4 $cGold | Out-Null
TBox $sl 500 66 420 22 "WHAT NOBODY IS SAYING" 9 $cGold $true 1 3 | Out-Null
$right = @(
    "Empathy detection as a measured outcome",
    "Customer / member experience quality - not just deflection",
    "Compliance-native architecture (not a bolt-on)",
    "Digital twin trained on your own brand voice",
    '"How well calls went - not just how many"',
    "Emotional + regulatory intelligence as lead positioning"
)
$ry2 = 94
foreach($line in $right){
    TBox $sl 500 $ry2 420 26 "* $line" 10 (Col 235 245 210) $false 1 1 | Out-Null
    $ry2 += 30
}

Rect $sl 30 380 900 100 (Col 40 35 10) | Out-Null
Rect $sl 30 380 900 3 $cGold | Out-Null
TBox $sl 40 386 880 20 "CSXAI's Market Position" 9 $cGold $true 1 3 | Out-Null
TBox $sl 40 410 880 64 '"Every other platform tells you how many calls they can deflect. We tell you how well those calls went." - Lead every channel with empathy + compliance. This territory is completely unoccupied.' 11 (Col 245 235 200) $false 1 1 | Out-Null

# ============================================================================
# SLIDE 6 - TARGET MARKET EXPLAINED
# ============================================================================
Write-Host "Slide 6: Target Market..."
$sl = NewSlide $prs
NavHdr $sl "Target Market - The 9,500+ Explained" "Source: FDIC 2025 + NCUA 2025"

$panels = @(
    @(18, 56, "~4,600", "FDIC Community Banks", $cBlueL, $cBlue,
      "Source: FDIC 2025 - US community banks with `$100M-`$5B in assets",
      "Profile: Regional and community banks with real call volume",
      "Gap: Too large for DIY SMB tools; below Glia/Eltropy enterprise tier",
      "Decision-makers: VP Operations, Director Customer Service, CTO"),
    @(338, 56, "~4,900", "NCUA Credit Unions", $cGoldL, $cAmber,
      "Source: NCUA 2025 - federally insured CUs with `$10M-`$2B in assets",
      "Member-first mandate aligns directly with CSXAI empathy positioning",
      "Decision structure: Smaller C-suite = faster buying decisions vs banks",
      "C-suite is reachable directly via LinkedIn - no long procurement cycle"),
    @(658, 56, "~9,500", "Combined ICP", $cGrnL, $cGreen,
      "9,500 financial institutions in CSXAI's exact product-market fit range",
      "All share the same core problem: high call volume, limited staff, compliance risk",
      "None are currently served by a platform leading with empathy + compliance",
      "Real estate institutional segment adds additional upside (Phase 2)")
)

foreach($p in $panels){
    $l=$p[0]; $t=$p[1]; $num=$p[2]; $lbl=$p[3]; $bgc=$p[4]; $acc=$p[5]
    $b1=$p[6]; $b2=$p[7]; $b3=$p[8]; $b4=$p[9]
    $crd2 = Rect $sl $l $t 300 460 $bgc
    $crd2.Line.ForeColor.RGB = $acc; $crd2.Line.Weight = 1; $crd2.Line.Visible = 1
    Rect $sl $l $t 300 4 $acc | Out-Null
    TBox $sl ($l+10) ($t+12) 280 60 $num 42 $acc $true 2 3 | Out-Null
    TBox $sl ($l+10) ($t+70) 280 22 $lbl 10 $cNavy $true 2 3 | Out-Null
    Rect $sl ($l+20) ($t+96) 260 1 $acc | Out-Null
    $by3 = $t + 106
    foreach($line in @($b1,$b2,$b3,$b4)){
        TBox $sl ($l+12) $by3 276 46 "* $line" 9 (Col 40 55 75) $false 1 1 | Out-Null
        $by3 += 48
    }
}

Rect $sl 18 522 924 12 $cCard | Out-Null
TBox $sl 22 523 920 10 "Note: 9,500+ figure = FDIC community banks ~4,600 + NCUA credit unions ~4,900 in ICP asset size range (excludes mega-banks with 18-month procurement cycles and micro-institutions below CSXAI deployment threshold)." 7 $cMid $false 1 3 | Out-Null

# ============================================================================
# SLIDE 7 - DIGITAL MARKETING OPPORTUNITY
# ============================================================================
Write-Host "Slide 7: Digital Opportunity..."
$sl = NewSlide $prs
NavHdr $sl "Digital Marketing Opportunity - Where the Gaps Are" "Performance marketing perspective"

$insights = @(
    @(18, 58, "ELTROPY RUNS ZERO PAID ADS", $cRedL, $cRed,
      "1,900 people research Eltropy on Google every month.",
      "No competitor is bidding against this traffic.",
      "CSXAI can intercept every Eltropy research session from Day 1 of Google launch.",
      'CPC range: $5-$35 / Low competition index / Highest ROI keyword in universe.'),
    @(490, 58, "KEYWORD DEMAND IS GROWING FAST", $cGoldL, $cAmber,
      '"Conversational AI in banking" +400% search growth in 3 months.',
      '"Conversational AI banking" +300% in 3 months.',
      "Near-zero CPCs right now because advertisers have not noticed.",
      "First-mover window is open - it closes as category matures."),
    @(18, 295, "LINKEDIN AUDIENCE IS PRECISE", $cBlueL, $cBlue,
      "Can target VP Operations / CTO / COO at community banks by:",
      "Job function / Seniority / Industry / Company size / Geography",
      "Estimated 25,000+ decision-makers in CSXAI's ICP on LinkedIn.",
      "InMail reaches them directly in inbox - not a feed ad."),
    @(490, 295, "REAL ESTATE KEYWORD TRAP", $cGrnL, (Col 5 90 50),
      '"Real estate virtual assistant" = 1,900 searches/month.',
      "These are realtors looking to hire offshore human VAs (MyOutDesk etc.).",
      "Wrong audience entirely - VA staffing companies dominate this space.",
      'Use only AI-specific RE terms: "real estate ai assistant", "realtor virtual receptionist".')
)

foreach($ins in $insights){
    $l=$ins[0]; $t=$ins[1]; $title=$ins[2]; $bgc=$ins[3]; $acc=$ins[4]
    $b1=$ins[5]; $b2=$ins[6]; $b3=$ins[7]; $b4=$ins[8]
    $crd3 = Rect $sl $l $t 452 218 $bgc
    $crd3.Line.ForeColor.RGB = $acc; $crd3.Line.Weight = 1; $crd3.Line.Visible = 1
    Rect $sl $l $t 452 4 $acc | Out-Null
    TBox $sl ($l+10) ($t+10) 432 20 $title 9 $cNavy $true 1 3 | Out-Null
    Rect $sl ($l+10) ($t+33) 432 1 $cBdr | Out-Null
    $by4 = $t + 40
    foreach($line in @($b1,$b2,$b3,$b4)){
        TBox $sl ($l+10) $by4 432 42 "* $line" 9 (Col 35 50 70) $false 1 1 | Out-Null
        $by4 += 42
    }
}

# ============================================================================
# SLIDE 8 - STRATEGY OVERVIEW: 3 BUDGET OPTIONS
# ============================================================================
Write-Host "Slide 8: Strategy Overview..."
$sl = NewSlide $prs
NavHdr $sl "Recommended Paid Media Strategy - 3 Budget Scenarios" "Platform priority: LinkedIn InMail first, Google Ads second"

$rationale = Rect $sl 18 56 924 90 $cCard
$rationale.Line.ForeColor.RGB = $cNavy; $rationale.Line.Weight = 1; $rationale.Line.Visible = 1
Rect $sl 18 56 4 90 $cNavy | Out-Null
TBox $sl 28 62 900 18 "WHY LINKEDIN INMAIL TAKES PRIORITY OVER GOOGLE ADS AT ALL BUDGET LEVELS" 9 $cNavy $true 1 3 | Out-Null
TBox $sl 28 84 900 56 "(1) New brand = no Quality Score on Google; CPL is 3-4x higher in Month 1 vs. InMail  /  (2) LinkedIn InMail reaches named decision-makers directly in their inbox, not keyword guesses  /  (3) Credit unions: smaller governance = faster yes/no, C-suite directly reachable  /  (4) Google Ads added at `$2,000/month when budget allows running both channels with enough data volume" 9 $cMid $false 1 1 | Out-Null

$budgets = @(
    @(18, 158, '$200 / Month', "Phase: Minimum Viable Test", $cTeal, (Col 230 248 248),
      "Platform: LinkedIn InMail only",
      "Segment: Credit Union C-Suite (1 segment)",
      "Sends: ~500/month  /  Opens: ~260",
      'Est. Leads: 3-5/month  /  CPL: $40-67',
      "Purpose: Validate message + audience fit"),
    @(340, 158, '$800 / Month', "Phase: Primary Growth Plan", $cBlue, $cBlueL,
      "Platform: LinkedIn InMail only",
      "Segment: Both - Banking Ops + Credit Union (2 segments)",
      "Sends: ~2,400/month  /  Opens: ~1,248",
      'Est. Leads: 15-22/month  /  CPL: $36-53',
      "Purpose: Build pipeline, refine targeting"),
    @(662, 158, '$2,000 / Month', "Phase: Full-Funnel Launch", $cGold, $cGoldL,
      "Platform: LinkedIn InMail + Google Ads (2 campaigns)",
      "Google: Competitor Conquesting + Banking AI Category",
      "Sends: ~2,400 InMail  +  8,000+ Google impressions",
      'Est. Leads: 22-34/month  /  CPL: $59-91',
      "Purpose: Scale reach, capture search intent")
)

foreach($b in $budgets){
    $l=$b[0]; $t=$b[1]; $title=$b[2]; $sub=$b[3]; $acc=$b[4]; $bgc=$b[5]
    $b1=$b[6]; $b2=$b[7]; $b3=$b[8]; $b4=$b[9]; $b5=$b[10]
    $brd = Rect $sl $l $t 302 350 $bgc
    $brd.Line.ForeColor.RGB = $acc; $brd.Line.Weight = 1.5; $brd.Line.Visible = 1
    Rect $sl $l $t 302 4 $acc | Out-Null
    TBox $sl ($l+10) ($t+10) 282 32 $title 22 $cNavy $true 2 3 | Out-Null
    TBox $sl ($l+10) ($t+44) 282 18 $sub 8 $acc $true 2 3 | Out-Null
    Rect $sl ($l+20) ($t+66) 262 1 $cBdr | Out-Null
    $by5 = $t + 76
    foreach($line in @($b1,$b2,$b3,$b4,$b5)){
        TBox $sl ($l+10) $by5 282 50 $line 9 (Col 35 50 70) $false 1 1 | Out-Null
        $by5 += 50
    }
}

TBox $sl 18 516 924 18 'Recommendation: Start with $800/month (both InMail segments). Validate in 30 days. Move to $2,000 when first demo conversions are confirmed.' 9 $cMid $false 2 3 | Out-Null

# ============================================================================
# SLIDE 9 - $200/MONTH PLAN
# ============================================================================
Write-Host "Slide 9: $200 plan..."
$sl = NewSlide $prs
NavHdr $sl '$200/Month - Minimum Viable Campaign / LinkedIn InMail' "1 segment / Credit Union C-Suite"

$wc = Rect $sl 18 56 460 130 $cGoldL
$wc.Line.ForeColor.RGB = $cAmber; $wc.Line.Visible = 1
Rect $sl 18 56 4 130 $cAmber | Out-Null
TBox $sl 28 62 440 20 "WHY CREDIT UNIONS AT THIS BUDGET" 9 $cAmber $true 1 3 | Out-Null
TBox $sl 28 86 440 92 "* Smallest governance structure = fastest buying decisions`n* Mission-first mandate aligns with CSXAI empathy positioning`n* C-suite is reachable directly on LinkedIn with small send volumes`n* Lowest CPL in the entire channel mix - right audience for limited budget" 9 (Col 80 60 20) $false 1 1 | Out-Null

$tp = Rect $sl 490 56 450 130 $cBlueL
$tp.Line.ForeColor.RGB = $cBlue; $tp.Line.Visible = 1
Rect $sl 490 56 4 130 $cBlue | Out-Null
TBox $sl 500 62 430 20 "TARGETING PARAMETERS" 9 $cBlue $true 1 3 | Out-Null
TBox $sl 500 86 430 92 "Titles: CEO / COO / CTO / Chief Digital Officer / VP Technology / VP Member Experience`nIndustry: Financial Services (credit union companies filter)`nCompany size: 50-500 employees / Geography: United States`nSeniority: CXO / VP / Director / Owner" 9 (Col 20 50 100) $false 1 1 | Out-Null

TBox $sl 18 196 920 22 "3-MONTH PROJECTION" 10 $cNavy $true 1 3 | Out-Null
Rect $sl 18 218 924 28 $cNavy | Out-Null
$pHdrs = @("Metric", "Month 1", "Month 2", "Month 3")
$pColX = @(18, 318, 518, 718)
$pColW = @(300, 200, 200, 224)
for($i=0;$i-lt 4;$i++){TBox $sl ($pColX[$i]+6) 220 ($pColW[$i]-8) 24 $pHdrs[$i] 9 $cWhite $true 1 3 | Out-Null}
$pRows = @(
    @("Budget", '$200', '$200', '$200'),
    @("InMail Sends / Month", "500", "500", "500"),
    @("Estimated Opens (52%)", "260", "260", "260"),
    @("Engaged Prospects (5-8%)", "13-20", "13-20", "13-20"),
    @("Demo Leads Estimated", "3-5", "4-6", "5-8"),
    @("Blended CPL", '$40-67', '$33-50', '$25-40')
)
$pRowColors = @($cWhite,$cCard,$cWhite,$cCard,$cWhite,$cCard)
$pry = 246
for($r=0;$r-lt 6;$r++){
    Rect $sl 18 $pry 924 38 $pRowColors[$r] | Out-Null
    Rect $sl 18 ($pry+37) 924 1 $cBdr | Out-Null
    for($ci=0;$ci-lt 4;$ci++){
        $fcol = if($r -eq 4 -and $ci -gt 0){$cGreen}elseif($r -eq 5 -and $ci -gt 0){$cBlue}else{$cNavy}
        $fb = if($r -ge 4 -and $ci -gt 0){$true}else{$false}
        TBox $sl ($pColX[$ci]+6) ($pry+3) ($pColW[$ci]-8) 32 $pRows[$r][$ci] 10 $fcol $fb 1 3 | Out-Null
    }
    $pry += 38
}

TBox $sl 18 482 924 20 "Note: CPL improves as message is refined based on Month 1 open-to-reply data. Subject line and opening sentence are the highest-leverage variables in InMail performance." 8 $cMid $false 1 3 | Out-Null

# ============================================================================
# SLIDE 10 - $800/MONTH PLAN
# ============================================================================
Write-Host "Slide 10: $800 plan..."
$sl = NewSlide $prs
NavHdr $sl '$800/Month - Primary Growth Plan / LinkedIn InMail' "2 segments / Community Banking Ops + Credit Union C-Suite"

$splits = @(
    @(18, 56, "SEGMENT 1 - COMMUNITY BANKING OPS", '$500/month', $cBlueL, $cBlue,
      "Titles: VP Operations / Director Operations / Head of Customer Service / COO / VP Customer Experience",
      "Industry: Banking + Financial Services  /  Company size: 200-2,000 employees",
      "Message angle: Operations pain - call volume, repeat queries, staff capacity",
      "Sends: ~1,500/month  /  Opens: ~780"),
    @(490, 56, "SEGMENT 2 - CREDIT UNION C-SUITE", '$300/month', $cGoldL, $cAmber,
      "Titles: CEO / COO / CTO / Chief Digital Officer / VP Technology / VP Member Experience",
      "Industry: Financial Services (credit union filter)  /  Company size: 50-500 employees",
      "Message angle: Empathy + member service quality - mission alignment",
      "Sends: ~900/month  /  Opens: ~468")
)

foreach($sp in $splits){
    $l=$sp[0]; $t=$sp[1]; $title=$sp[2]; $budget=$sp[3]; $bgc=$sp[4]; $acc=$sp[5]
    $b1=$sp[6]; $b2=$sp[7]; $b3=$sp[8]; $b4=$sp[9]
    $crd4 = Rect $sl $l $t 452 136 $bgc
    $crd4.Line.ForeColor.RGB = $acc; $crd4.Line.Visible = 1
    Rect $sl $l $t 452 3 $acc | Out-Null
    TBox $sl ($l+10) ($t+8) 300 18 $title 8 $cNavy $true 1 3 | Out-Null
    Rect $sl ($l+316) ($t+6) 126 22 $acc | Out-Null
    TBox $sl ($l+316) ($t+6) 126 22 $budget 10 $cWhite $true 2 3 | Out-Null
    Rect $sl ($l+10) ($t+30) 432 1 $cBdr | Out-Null
    $by6 = $t + 38
    foreach($line in @($b1,$b2,$b3,$b4)){
        TBox $sl ($l+10) $by6 432 26 "* $line" 9 (Col 35 50 75) $false 1 1 | Out-Null
        $by6 += 25
    }
}

TBox $sl 18 200 920 22 '3-MONTH PROJECTION - $800/MONTH' 10 $cNavy $true 1 3 | Out-Null
Rect $sl 18 222 924 28 $cNavy | Out-Null
$h2 = @("Metric", "Month 1", "Month 2", "Month 3")
$cx2 = @(18, 318, 518, 718); $cw2 = @(300, 200, 200, 224)
for($i=0;$i-lt 4;$i++){TBox $sl ($cx2[$i]+6) 224 ($cw2[$i]-8) 24 $h2[$i] 9 $cWhite $true 1 3 | Out-Null}
$rows2 = @(
    @("Total Budget", '$800', '$800', '$800'),
    @("Total InMail Sends", "2,400", "2,400", "2,400"),
    @("Total Opens (52%)", "1,248", "1,248", "1,248"),
    @("Engaged Prospects (5-8%)", "62-100", "62-100", "62-100"),
    @("Demo Leads Estimated", "15-22", "18-26", "20-30"),
    @("Blended CPL", '$36-53', '$31-44', '$27-40')
)
$ry2b = 250
$rc2 = @($cWhite,$cCard,$cWhite,$cCard,$cWhite,$cCard)
for($r=0;$r-lt 6;$r++){
    Rect $sl 18 $ry2b 924 38 $rc2[$r] | Out-Null
    Rect $sl 18 ($ry2b+37) 924 1 $cBdr | Out-Null
    for($ci=0;$ci-lt 4;$ci++){
        $fc = if($r -eq 4 -and $ci -gt 0){$cGreen}elseif($r -eq 5 -and $ci -gt 0){$cBlue}else{$cNavy}
        $fb = if($r -ge 4 -and $ci -gt 0){$true}else{$false}
        TBox $sl ($cx2[$ci]+6) ($ry2b+3) ($cw2[$ci]-8) 32 $rows2[$r][$ci] 10 $fc $fb 1 3 | Out-Null
    }
    $ry2b += 38
}
TBox $sl 18 484 924 20 "Both segments run simultaneously. Month 2 adjustment: review open-to-reply rate per segment. If Segment 1 reply rate exceeds Segment 2, reallocate `$100 from Segment 2 to Segment 1." 8 $cMid $false 1 3 | Out-Null

# ============================================================================
# SLIDE 11 - $2,000/MONTH PLAN
# ============================================================================
Write-Host "Slide 11: $2000 plan..."
$sl = NewSlide $prs
NavHdr $sl '$2,000/Month - Full-Funnel Approach / InMail + Google Ads' 'LinkedIn InMail $800 + Google Ads $1,200'

$bs = @(
    @(18, 56, "LinkedIn InMail", "Both Segments", '$800', $cBlue, $cBlueL),
    @(248, 56, "Google - Competitor Conquesting", "Eltropy + Kasisto keywords", '$800', $cRed, $cRedL),
    @(478, 56, "Google - Banking AI Category", "Conversational AI banking", '$400', $cTeal, (Col 230 248 248)),
    @(708, 56, "Total Monthly Budget", "All channels combined", '$2,000', $cNavy, $cCard)
)
foreach($b in $bs){
    $l=$b[0]; $t=$b[1]; $nm=$b[2]; $sub=$b[3]; $bud=$b[4]; $acc=$b[5]; $bgc=$b[6]
    $cb = Rect $sl $l $t 220 100 $bgc
    $cb.Line.ForeColor.RGB = $acc; $cb.Line.Visible = 1
    Rect $sl $l $t 220 3 $acc | Out-Null
    TBox $sl ($l+8) ($t+8) 204 30 $nm 9 $cNavy $true 1 1 | Out-Null
    TBox $sl ($l+8) ($t+40) 204 16 $sub 8 $cMid $false 1 1 | Out-Null
    TBox $sl ($l+8) ($t+58) 204 36 $bud 24 $acc $true 2 3 | Out-Null
}

TBox $sl 18 164 920 18 "GOOGLE ADS - CAMPAIGN KEYWORDS (Phrase + Exact match only / No broad match)" 9 $cNavy $true 1 3 | Out-Null
$kg = @(
    @(18, 182, 'Competitor Conquesting ($800/mo)', @('"eltropy"', '"kasisto"', '"kasisto ai"', '"kasisto competitors"', '"glia banking"'), $cRedL, $cRed),
    @(490, 182, 'Banking AI Category ($400/mo)', @('"conversational ai for banking"', '"conversational ai in banking"', '"banking virtual assistant"', '"conversational banking"', '"conversational ai banking"'), (Col 230 248 248), $cTeal)
)
foreach($k in $kg){
    $l=$k[0]; $t=$k[1]; $nm=$k[2]; $kws=$k[3]; $bgc=$k[4]; $acc=$k[5]
    $ck = Rect $sl $l $t 452 96 $bgc
    $ck.Line.ForeColor.RGB = $acc; $ck.Line.Visible = 1
    Rect $sl $l $t 452 3 $acc | Out-Null
    TBox $sl ($l+8) ($t+6) 436 16 $nm 8 $cNavy $true 1 3 | Out-Null
    $kwText = $kws -join "  /  "
    TBox $sl ($l+8) ($t+26) 436 66 $kwText 8 (Col 35 50 80) $false 1 1 | Out-Null
}

TBox $sl 18 286 920 18 '3-MONTH PROJECTION - $2,000/MONTH' 10 $cNavy $true 1 3 | Out-Null
Rect $sl 18 304 924 28 $cNavy | Out-Null
$h3c = @("Channel", "Monthly Budget", "Est. Leads / Month", "Blended CPL")
$cx3 = @(18, 318, 568, 768); $cw3 = @(300, 250, 200, 156)
for($i=0;$i-lt 4;$i++){TBox $sl ($cx3[$i]+6) 306 ($cw3[$i]-8) 24 $h3c[$i] 9 $cWhite $true 1 3 | Out-Null}
$rows3 = @(
    @("LinkedIn InMail (both segments)", '$800', "15-22", '$36-53'),
    @("Google - Competitor Conquesting", '$800', "5-8", '$100-160'),
    @("Google - Banking AI Category", '$400', "2-4", '$100-200'),
    @("TOTAL", '$2,000', "22-34", '$59-91')
)
$ry3 = 332; $rc3 = @($cWhite,$cCard,$cWhite,$cNavy)
for($r=0;$r-lt 4;$r++){
    Rect $sl 18 $ry3 924 38 $rc3[$r] | Out-Null
    Rect $sl 18 ($ry3+37) 924 1 $cBdr | Out-Null
    $isTotal = $r -eq 3
    for($ci=0;$ci-lt 4;$ci++){
        $fc = if($isTotal){$cWhite}elseif($ci -eq 2){$cGreen}elseif($ci -eq 3){$cBlue}else{$cNavy}
        TBox $sl ($cx3[$ci]+6) ($ry3+3) ($cw3[$ci]-8) 32 $rows3[$r][$ci] 10 $fc $isTotal 1 3 | Out-Null
    }
    $ry3 += 38
}

TBox $sl 18 492 924 18 'CPL trajectory: Month 1 ~$91 blended  ->  Month 2 ~$74 (QS builds, negatives mature)  ->  Month 3 ~$60 (optimised). Google CPL improves fastest once Quality Score is established.' 8 $cMid $false 1 3 | Out-Null
TBox $sl 18 512 924 18 'Note: Only launch Google Ads at $2,000 after InMail has produced at least one demo conversion. Use that proof to write higher-converting Google ad copy.' 8 $cAmber $true 1 3 | Out-Null

# ============================================================================
# SLIDE 12 - 3-BUDGET COMPARISON
# ============================================================================
Write-Host "Slide 12: Comparison..."
$sl = NewSlide $prs
NavHdr $sl "3-Month Performance Comparison - All Budget Options" "Select the right entry point for CSXAI's stage"

Rect $sl 18 56 924 28 $cNavy | Out-Null
$chHdr = @("Metric", '$200/Month', '$800/Month', '$2,000/Month')
$chX = @(18, 268, 518, 768); $chW = @(250, 250, 250, 176)
for($i=0;$i-lt 4;$i++){TBox $sl ($chX[$i]+6) 58 ($chW[$i]-8) 24 $chHdr[$i] 9 $cWhite $true 1 3 | Out-Null}

$cRows = @(
    @("Platform", "LinkedIn InMail only", "LinkedIn InMail only", "InMail + Google Ads"),
    @("Active Segments / Campaigns", "1 (Credit Union C-Suite)", "2 (Banking Ops + Credit Union)", "2 InMail + 2 Google campaigns"),
    @("Monthly Sends / Impressions", "~500 sends", "~2,400 sends", "~2,400 sends + 8,000+ impressions"),
    @("Leads - Month 1", "3-5", "15-22", "22-34"),
    @("Leads - Month 3", "5-8", "20-30", "30-40"),
    @("CPL - Month 1", '$40-67', '$36-53', '$59-91'),
    @("CPL - Month 3 (optimised)", '$25-40', '$27-40', '$50-67'),
    @("Best For", "Proof of concept / first demos", "Pipeline building / message validation", "Scale / when InMail conversions proven")
)
$cRClr = @($cWhite,$cCard,$cWhite,$cCard,$cWhite,$cCard,$cWhite,$cBlueL)
$cry = 84
for($r=0;$r-lt 8;$r++){
    Rect $sl 18 $cry 924 42 $cRClr[$r] | Out-Null
    Rect $sl 18 ($cry+41) 924 1 $cBdr | Out-Null
    for($ci=0;$ci-lt 4;$ci++){
        $isLbl = $ci -eq 0
        $fc = if($r -ge 3 -and $r -le 4 -and $ci -gt 0){$cGreen}elseif($r -ge 5 -and $r -le 6 -and $ci -gt 0){$cBlue}else{$cNavy}
        $fb = if(($r -eq 3 -or $r -eq 4) -and $ci -gt 0){$true}else{$isLbl}
        TBox $sl ($chX[$ci]+6) ($cry+4) ($chW[$ci]-8) 34 $cRows[$r][$ci] 9 $fc $fb 1 1 | Out-Null
    }
    $cry += 42
}

Rect $sl 18 422 924 36 $cCard | Out-Null
Rect $sl 18 422 4 36 $cGold | Out-Null
TBox $sl 28 428 910 24 'Recommendation: Start with $800/month (both InMail segments) to build pipeline and validate messaging. Scale to $2,000 only once demo conversion is confirmed from at least one segment. Do not start with $200 if growth is the goal - it produces too few data points for optimization.' 8 (Col 80 70 20) $false 1 3 | Out-Null

# ============================================================================
# SLIDE 13 - FINAL RECOMMENDATIONS
# ============================================================================
Write-Host "Slide 13: Recommendations..."
$sl = NewSlide $prs
NavHdr $sl "Final Recommendations" "Priority performance marketing actions - implementation timing is flexible"

$recs = @(
    @("01", "PRIORITIZE CREDIT UNION OUTREACH FIRST", $cTeal, (Col 225 248 248),
      "Start InMail with the credit union C-suite segment. Fastest decision cycles, strongest mission alignment with CSXAI empathy angle, and lowest CPL in the full channel mix. This is the highest-probability path to a first qualified demo."),
    @("02", "INTERCEPT ELTROPY ON GOOGLE WHEN BUDGET ALLOWS", $cRed, $cRedL,
      '1,900 people research Eltropy monthly and nobody is bidding against them. At $2,000/month, this competitor conquesting campaign delivers the highest expected ROI per dollar in the keyword universe. Low competition index, $5-$35 CPC.'),
    @("03", "LEAD ALL MESSAGING WITH EMPATHY - NOT EFFICIENCY", $cGold, $cGoldL,
      "Every competitor leads with deflection rates and automation volume. CSXAI's differentiation is empathy + compliance. Every InMail subject line, ad headline, and landing page should lead with this. It is genuinely unoccupied territory."),
    @("04", "BUILD THE LEAD MAGNET BEFORE SCALING GOOGLE ADS", $cBlue, $cBlueL,
      "A downloadable lead magnet (finance or real estate white paper) significantly improves Google Ads conversion rates by offering value at the click stage. Prepare both lead magnets before Google campaigns go live."),
    @("05", 'DO NOT BID ON "REAL ESTATE VIRTUAL ASSISTANT" TERMS', $cAmber, $cGoldL,
      '1,900/mo of misleading search volume dominated by VA staffing companies. These searches are from individual realtors hiring offshore human VAs - not institutions evaluating AI platforms. Use only AI-specific RE terms.'),
    @("06", "REVIEW INMAIL COPY AT DAY 15 - NOT DAY 30", $cPurp, (Col 240 237 255),
      "Check open-to-reply conversion rate. If reply rate is below 4%, test a different subject line or opening sentence. InMail performance is highly sensitive to the first 2 lines. Iterate fast - 30 days is too long to wait.")
)

$leftY = 56; $rightY = 56

for($i=0;$i-lt 6;$i++){
    $rec = $recs[$i]; $num=$rec[0]; $title=$rec[1]; $acc=$rec[2]; $bgc=$rec[3]; $desc=$rec[4]
    $isRight = $i -ge 3
    $x = if($isRight){490}else{18}
    $y = if($isRight){$rightY}else{$leftY}

    $rc5 = Rect $sl $x $y 452 156 $bgc
    $rc5.Line.ForeColor.RGB = $acc; $rc5.Line.Visible = 1
    Rect $sl $x $y 452 3 $acc | Out-Null

    $nbg = Rect $sl ($x+10) ($y+8) 30 22 $acc
    TBox $sl ($x+10) ($y+8) 30 22 $num 9 $cWhite $true 2 3 | Out-Null
    TBox $sl ($x+46) ($y+8) 396 22 $title 9 $cNavy $true 1 3 | Out-Null
    Rect $sl ($x+10) ($y+32) 432 1 $cBdr | Out-Null
    TBox $sl ($x+10) ($y+38) 432 108 $desc 9 (Col 35 50 75) $false 1 1 | Out-Null

    if($isRight){$rightY += 162}else{$leftY += 162}
}

# ============================================================================
# SLIDE 14 - THANK YOU
# ============================================================================
Write-Host "Slide 14: Thank you..."
$sl = NewSlide $prs
$sl.Background.Fill.ForeColor.RGB = $cNavy
Rect $sl 0 0 960 4 $cGold | Out-Null

TBox $sl 100 140 760 80 "Thank You" 52 $cWhite $true 2 3 | Out-Null
TBox $sl 100 230 760 30 "Questions, feedback, and next steps" 16 $cGold $false 2 3 | Out-Null
Rect $sl 350 270 260 2 (Col 60 80 110) | Out-Null

TBox $sl 100 286 760 30 "Rishabh B  |  rishabhb@damcogroup.com" 12 (Col 200 215 235) $false 2 3 | Out-Null
TBox $sl 100 316 760 24 "Damco Digital  -  Paid Ads & Account Management" 10 (Col 150 170 200) $false 2 3 | Out-Null

$dn = Rect $sl 200 360 560 90 (Col 18 34 58)
$dn.Line.ForeColor.RGB = (Col 50 75 110); $dn.Line.Visible = 1
TBox $sl 210 368 540 16 "DATA SOURCES" 8 (Col 100 130 170) $true 2 3 | Out-Null
TBox $sl 210 388 540 56 "Google Keyword Planner (May 2026) / SimilarWeb traffic analysis / FDIC 2025 / NCUA 2025 / LinkedIn targeting documentation / Competitor website, LinkedIn & ad channel analysis / B2B SaaS platform benchmarks 2026" 8 (Col 160 180 210) $false 2 1 | Out-Null

TBox $sl 100 462 760 24 "27 May 2026  |  Confidential  |  Prepared for CSX Intelligence" 9 (Col 80 100 130) $false 2 3 | Out-Null

# ============================================================================
# SAVE PRESENTATION
# ============================================================================
Write-Host "Saving..."
$savePath = "C:\Users\Rishabhb\Downloads\control room\CSXAI\01_Reports\CSXAI_Strategy_Report_27May2026.pptx"
$prs.SaveAs($savePath)
Write-Host "Saved: $savePath"
$prs.Close()
$ppt.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($ppt) | Out-Null
Write-Host "Done."
