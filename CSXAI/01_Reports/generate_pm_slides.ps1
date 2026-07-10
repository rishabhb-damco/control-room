# CSxAI Performance Marketing Slides v2
# Analytical / Data-driven / Performance-focused
# Indigo + Blue + White palette ONLY
# Rishabh B | Damco Digital | 28 May 2026
$ErrorActionPreference = "Stop"

function Col([int]$r,[int]$g,[int]$b){ return [int]($r + $g*256 + $b*65536) }

$cW   = Col 255 255 255   # white
$cN   = Col 11  16  32    # dark navy
$cB   = Col 15  76  129   # deep blue primary
$cI   = Col 79  70  229   # indigo accent
$cM   = Col 37  99  235   # medium blue
$cDB  = Col 30  64  175   # deep medium blue
$cLB  = Col 219 234 254   # light blue card bg
$cPB  = Col 239 246 255   # pale blue bg
$cIB  = Col 244 248 255   # icy blue near-white
$cHL  = Col 214 230 253   # highlight for Leads/CPL cols
$cTR  = Col 205 222 252   # total row bg
$cBd  = Col 196 215 245   # border
$cBT  = Col 20  40  90    # body text dark blue
$cMT  = Col 90  115 165   # muted text

# ============================================================
# SHAPE HELPERS
# ============================================================
function Rect($sl,$l,$t,$w,$h,$col,$noLine=$true){
    $s = $sl.Shapes.AddShape(1,$l,$t,$w,$h)
    $s.Fill.Solid(); $s.Fill.ForeColor.RGB = $col
    if($noLine){ $s.Line.Visible = 0 }
    else{ $s.Line.ForeColor.RGB = $cBd; $s.Line.Weight = 0.5 }
    return $s
}

function TBox($sl,$l,$t,$w,$h,$txt,$sz,$col,$bold=$false,$align=1,$fn="Aptos",$va=1){
    $s  = $sl.Shapes.AddTextbox(1,$l,$t,$w,$h)
    $tf = $s.TextFrame
    $tf.TextRange.Text = $txt
    $tf.TextRange.Font.Size  = [float]$sz
    $tf.TextRange.Font.Color.RGB = $col
    $tf.TextRange.Font.Bold  = $bold
    try{ $tf.TextRange.Font.Name = $fn }catch{}
    $tf.TextRange.ParagraphFormat.Alignment = $align
    $tf.VerticalAnchor = $va   # 1=top 3=mid
    $tf.WordWrap = $true
    $s.Line.Visible = 0; $s.Fill.Visible = 0
    return $s
}

function NewSlide($prs){
    $sl = $prs.Slides.Add($prs.Slides.Count+1, 12)
    try{ while($sl.Shapes.Count -gt 0){ $sl.Shapes.Item(1).Delete() } }catch{}
    $sl.Background.Fill.Solid()
    $sl.Background.Fill.ForeColor.RGB = $cW
    return $sl
}

function SlideHdr($sl,$title,$sub=""){
    Rect $sl 0 0 960 4 $cB | Out-Null
    TBox $sl 36 10 888 30 $title 18 $cB $true 1 "Poppins" | Out-Null
    if($sub -ne ""){
        TBox $sl 36 44 888 16 $sub 10 $cMT $false 1 "Aptos" | Out-Null
    }
    Rect $sl 36 64 888 1 $cBd | Out-Null
}

# ============================================================
# PROJECTION TABLE COLUMN LAYOUT  (total 888px starting x=36)
# ============================================================
# Widths:  130  55  94  52  68  72  44  68  45  48  52  52  52  56
# X:        36 166 221 315 367 435 507 551 619 664 712 764 816 868
$pX  = @(36,166,221,315,367,435,507,551,619,664,712,764,816,868)
$pW  = @(130, 55, 94, 52, 68, 72, 44, 68, 45, 48, 52, 52, 52, 56)
$pH  = @("Campaign","Platform","Focus / Target","Mo. Bud.","Audience","Sends / Impr.","Freq.","Opens / Clicks","CTR / Open%","Conv. Rate","Leads (Est.)","CPL","Daily Budget","Avg CPC")
$hlC = @(10, 11)   # highlight Leads and CPL columns

function DrawColHdrs($sl,$y){
    Rect $sl 36 $y 888 26 $cN | Out-Null
    for($i=0;$i-lt 14;$i++){
        TBox $sl ($pX[$i]+2) ($y+1) ($pW[$i]-4) 24 $pH[$i] 7.5 $cW $true 2 "Aptos" 3 | Out-Null
    }
}

function DrawRow($sl,$y,$rh,$vals,$bgc,$fc,$bold){
    Rect $sl 36 $y 888 $rh $bgc $false | Out-Null
    for($i=0;$i-lt $vals.Count;$i++){
        if($i -in $hlC -and $vals[$i] -ne ""){ Rect $sl ($pX[$i]) $y ($pW[$i]) $rh $cHL | Out-Null }
        $al = if($i -le 2){1}else{2}
        TBox $sl ($pX[$i]+2) ($y+2) ($pW[$i]-4) ($rh-4) $vals[$i] 7.5 $fc $bold $al "Aptos" 3 | Out-Null
    }
    Rect $sl 36 ($y+$rh) 888 1 $cBd | Out-Null
}

function DrawTotal($sl,$y,$vals){
    Rect $sl 36 $y 888 34 $cTR | Out-Null
    Rect $sl 36 $y 888 3 $cB  | Out-Null
    for($i=0;$i-lt $vals.Count;$i++){
        if($i -in $hlC -and $vals[$i] -ne ""){ Rect $sl ($pX[$i]) $y ($pW[$i]) 34 $cLB | Out-Null }
        $al = if($i -le 2){1}else{2}
        TBox $sl ($pX[$i]+2) ($y+4) ($pW[$i]-4) 26 $vals[$i] 8.5 $cB $true $al "Aptos" 3 | Out-Null
    }
}

function MonthBar($sl,$y,$lbl,$m1,$m2,$m3){
    Rect $sl 36 $y 888 30 $cIB $false | Out-Null
    TBox $sl 40 ($y+4) 200 22 $lbl 9 $cMT $true 1 "Aptos" | Out-Null
    TBox $sl 240 ($y+4) 200 22 "Month 1: $m1" 9 $cBT $false 1 "Aptos" | Out-Null
    TBox $sl 490 ($y+4) 200 22 "Month 2: $m2" 9 $cBT $false 1 "Aptos" | Out-Null
    TBox $sl 740 ($y+4) 184 22 "Month 3: $m3" 9 $cBT $false 1 "Aptos" | Out-Null
}

# ============================================================
Write-Host "Starting PowerPoint..."
$ppt = New-Object -ComObject PowerPoint.Application
$ppt.Visible = 1
$prs = $ppt.Presentations.Add(1)
$prs.PageSetup.SlideWidth  = 960
$prs.PageSetup.SlideHeight = 540

# ============================================================
# SLIDE 1 - COMPETITOR PAID MEDIA ANALYSIS
# ============================================================
Write-Host "Slide 1: Competitor Analysis..."
$sl = NewSlide $prs
SlideHdr $sl "Competitor Paid Media Analysis" "How direct competitors generate leads - platform presence, paid activity, and interception gaps"

# Table: 5 rows x 6 columns
$c6X = @(36, 136, 241, 381, 501, 681)
$c6W = @(100,105, 140, 120, 180, 243)
$c6H = @("Competitor","Google Ads","LinkedIn Activity","Other Channels","Lead Gen Method","CSXAI Paid Opportunity")

Rect $sl 36 74 888 24 $cN | Out-Null
for($i=0;$i-lt 6;$i++){
    TBox $sl ($c6X[$i]+3) 76 ($c6W[$i]-6) 20 $c6H[$i] 8 $cW $true 1 "Aptos" 3 | Out-Null
}

$cData = @(
    @("Eltropy",       "ZERO paid search",         "LinkedIn organic + SDR",   "ABM + 50+ partner integrations", "SDR outbound to community banks/CUs. Named-account ABM. Partner co-marketing.",      "1,900 branded searches/month with ZERO paid competition. High-intent buyers researching Eltropy have no CSXAI ad to click."),
    @("Glia",          "~9% paid traffic (est.)",   "LinkedIn Ads active",      "Events (Glia Interact) + FIS",   "Gated ROI benchmark report + 'Request Impact Study' CTA. High-value lead qualification.", "Glia's gated content playbook is the benchmark to match. CSXAI needs a comparable lead magnet before Google Ads launch."),
    @("Kasisto",       "Unclear - likely none",     "LinkedIn organic",         "Press + exec panels",            "Customer case studies + exec speaking presence. Bank-skewed (enterprise).",              "'Kasisto competitors' is actively searched. These buyers are in exit intent. An opportunity for Phase 2."),
    @("Interface.ai",  "Likely LinkedIn Ads",       "Founder-led (Srinivas Njay)", "Industry events + webinars", "Bold outcome claims + founder personal brand. 68% AI automation in hooks.",               "Strongest voice AI founder brand. If CSXAI founder is not posting, compensate with data-led content and ROI hooks."),
    @("Retell AI",     "Google Ads (developers)",   "LinkedIn Ads (devs)",      "API docs + GitHub",              "Developer acquisition: 'Start for Free' + API pricing. Targeting builders, not buyers.", "Not a direct threat at institutional level. Their Google Ads target developers, not VP Ops/CTO at banks.")
)

$rowBg = @($cW, $cIB, $cW, $cIB, $cW)
$ry = 98
for($r=0;$r-lt 5;$r++){
    $rh = 72
    Rect $sl 36 $ry 888 $rh $rowBg[$r] $false | Out-Null
    Rect $sl 36 ($ry+$rh) 888 1 $cBd | Out-Null
    for($ci=0;$ci-lt 6;$ci++){
        $fc = if($ci -eq 5){$cB}else{$cBT}
        $fb = if($ci -eq 0 -or $ci -eq 5){$true}else{$false}
        TBox $sl ($c6X[$ci]+3) ($ry+3) ($c6W[$ci]-6) ($rh-6) $cData[$r][$ci] 8 $fc $fb 1 "Aptos" 1 | Out-Null
    }
    $ry += $rh
}

Rect $sl 36 458 888 56 $cLB $false | Out-Null
Rect $sl 36 458 4 56 $cI | Out-Null
TBox $sl 46 462 874 12 "KEY PATTERN ACROSS ALL COMPETITORS" 8 $cI $true 1 "Aptos" | Out-Null
TBox $sl 46 476 874 34 "Every competitor leads with efficiency metrics: deflection rates, call containment numbers, automation volume. NONE lead with empathy, experience quality, or compliance-first architecture. This positioning space is completely unoccupied and is CSXAI's strongest paid media angle across all channels." 9 $cBT $false 1 "Aptos" 1 | Out-Null

# ============================================================
# SLIDE 2 - KEY TAKEAWAYS FROM COMPETITOR RESEARCH
# ============================================================
Write-Host "Slide 2: Key Takeaways..."
$sl = NewSlide $prs
SlideHdr $sl "Key Takeaways from Competitor Research" "Actionable learnings that directly shape the CSXAI paid media approach"

$tkX = @(36, 494)
$tkY = @(74, 74, 228, 228, 382)
$tkC = @($cLB, $cPB, $cLB, $cPB, $cLB)
$tkA = @($cB,  $cI,  $cDB, $cB,  $cI)

$tks = @(
    @("01", "Eltropy has the biggest paid media gap in the category",
      "1,900 people search Eltropy every month. Nobody intercepts them on Google. This is the single highest-ROI keyword opportunity in the category - low competition index, `$5-35 CPC, active vendor evaluation intent. Available as Phase 2 when budget reaches `$2,000+."),
    @("02", "Gated content converts better than cold demo CTAs",
      "Glia's 'Request Impact Study' and gated benchmark reports are their highest-converting assets. A cold 'Book a Demo' CTA performs significantly worse than value-first offers. CSXAI needs a lead magnet (ROI calculator or white paper) before scaling Google Ads."),
    @("03", "Empathy + compliance = completely unoccupied positioning",
      "Every competitor message is built around operational efficiency: deflection rates, automation volume, cost reduction. Not one competitor leads with empathy, call quality, or compliance-native architecture. CSXAI should own this lane in every paid ad and InMail subject line."),
    @("04", "LinkedIn InMail is the most underused channel by competitors",
      "Eltropy runs SDR outreach but no InMail ads. Glia runs LinkedIn feed ads (not InMail). None appear to run structured InMail campaigns to named decision-makers at community banks and credit unions. This is the least contested channel for reaching CSXAI's ICP."),
    @("05", "Founder-led content is a moat Interface.ai has built - CSXAI needs a content alternative",
      "Srinivas Njay (Interface.ai) has built a personal brand at industry events and LinkedIn. If CSXAI's leadership is not going to post personally, compensate with data-led LinkedIn content, ROI-focused hooks, and case study format posts once first clients are live.")
)

$placed = @(0,1,2,3,4)
for($i=0;$i-lt 5;$i++){
    $col = $i % 2
    $row = [Math]::Floor($i / 2)
    $x   = $tkX[$col]
    $y   = 74 + $row * 154
    if($i -eq 4){ $x=36; $y=382 }
    $w   = if($i -eq 4){888}else{448}
    $h   = if($i -eq 4){134}else{144}
    $acc = $tkA[$i]
    $bgc = $tkC[$i]

    Rect $sl $x $y $w $h $bgc $false | Out-Null
    Rect $sl $x $y 3 $h $acc | Out-Null
    TBox $sl ($x+12) ($y+8) 36 20 $tks[$i][0] 11 $acc $true 2 "Poppins" 3 | Out-Null
    TBox $sl ($x+54) ($y+8) ($w-66) 20 $tks[$i][1] 10 $cB $true 1 "Aptos" | Out-Null
    Rect $sl ($x+12) ($y+30) ($w-24) 1 $cBd | Out-Null
    TBox $sl ($x+12) ($y+36) ($w-24) ($h-44) $tks[$i][2] 9 $cBT $false 1 "Aptos" 1 | Out-Null
}

# ============================================================
# SLIDE 3 - RECOMMENDED STRATEGY OVERVIEW
# ============================================================
Write-Host "Slide 3: Strategy Overview..."
$sl = NewSlide $prs
SlideHdr $sl "Recommended Strategy Overview" "Strategic logic: why these channels, in this order, at these budgets"

# Why InMail first box
Rect $sl 36 74 888 56 $cN | Out-Null
TBox $sl 46 78 878 16 "WHY INMAIL LEADS THE STRATEGY" 9 $cLB $true 1 "Aptos" | Out-Null
TBox $sl 46 96 878 28 "New brand with no Quality Score = Google CPL is 3-4x higher in Month 1. LinkedIn InMail reaches named VP/CTO/COO directly in inbox - no Quality Score required, no feed algorithm, no display auction. Cost per send `$0.26-0.50. 52% open rate benchmark. Add Google only when InMail has confirmed at least one demo conversion." 8.5 $cLB $false 1 "Aptos" | Out-Null

# 4 strategic phases in 2x2
$phases = @(
    @(36,  138, "PHASE 1 - NOW",          "LinkedIn InMail: Both Segments",    $cLB, $cB,
      "Start both InMail segments simultaneously (`$500 Banking Ops + `$300 Credit Union). Review open-to-reply rate at Day 15. If rate is below 4%, test a new subject line before continuing. Run for 60 days before drawing CPL conclusions."),
    @(494, 138, "PHASE 2 - WHEN CONVERTING", "Add Google Ads: Financial Campaign", $cPB, $cI,
      "Once first demo conversion is confirmed from InMail, add Google Financial Campaign (`$400+). Use InMail reply language to write Google ad copy - the exact phrases that got replies are your highest-converting hooks for search ads."),
    @(36,  316, "EMAIL (PARALLEL - ANY TIME)", "MailChimp Nurture Sequences",   $cPB, $cDB,
      "Email nurture runs independently of paid. Activate both sequences (Financial + Real Estate) as soon as lead pipeline exists. Email reinforces InMail: prospects who received InMail and are on the fence often convert via email follow-up."),
    @(494, 316, "PHASE 3 - SCALE",        "Full Platform Mix at `$2,000+",     $cLB, $cM,
      "At `$2,000/month activate all 3 Google campaigns (Financial `$600 + Real Estate `$400 + General `$200) alongside InMail `$800. Google volume remains low at this stage - 3-6 high-intent leads/month. InMail remains the primary lead engine.")
)

foreach($phase in $phases){
    $x=$phase[0]; $y=$phase[1]; $label=$phase[2]; $title=$phase[3]; $bgc=$phase[4]; $acc=$phase[5]; $desc=$phase[6]
    Rect $sl $x $y 448 160 $bgc $false | Out-Null
    Rect $sl $x $y 448 3 $acc | Out-Null
    TBox $sl ($x+12) ($y+8) 424 16 $label 8 $acc $true 1 "Aptos" | Out-Null
    TBox $sl ($x+12) ($y+26) 424 18 $title 11 $cB $true 1 "Aptos" | Out-Null
    Rect $sl ($x+12) ($y+46) 424 1 $cBd | Out-Null
    TBox $sl ($x+12) ($y+52) 424 98 $desc 9 $cBT $false 1 "Aptos" 1 | Out-Null
}

TBox $sl 36 486 888 38 "Measurement triggers: Day 15 (open-to-reply rate per segment)  |  Month 1 end (CPL vs. benchmark)  |  Month 2 (first demo conversion)  |  Month 3 (CPL trend - is it declining?)  |  If CPL is NOT declining by Month 2, test new subject lines before increasing budget." 8.5 $cMT $false 1 "Aptos" | Out-Null

# ============================================================
# SLIDE 4 - LINKEDIN INMAIL: AUDIENCE & SEGMENT DESIGN
# ============================================================
Write-Host "Slide 4: LinkedIn InMail..."
$sl = NewSlide $prs
SlideHdr $sl "LinkedIn InMail Strategy" "Message Ads - named decision-maker targeting, direct inbox delivery at `$0.26-0.50/send"

# Funnel math banner
Rect $sl 36 74 888 32 $cN | Out-Null
TBox $sl 46 80 100 20 "FUNNEL MATH" 8 $cLB $true 1 "Aptos" 3 | Out-Null
$funnelSteps = @("2,400 sends/mo", "->", "1,248 opens (52%)", "->", "37-62 replies (3-5% of opens)", "->", "16-22 qualified leads (40-60% of replies)")
$fColW = @(105, 20, 140, 20, 195, 20, 358)
$fX = 148
foreach($step in $funnelSteps){
    $fw = $fColW[[array]::IndexOf($funnelSteps, $step)]
    $fc = if($step -eq "->"){$cMT}elseif($step -match "leads"){$cI}else{$cLB}
    $fb = if($step -match "leads"){$true}else{$false}
    TBox $sl $fX 80 $fw 20 $step 8 $fc $fb 1 "Aptos" 3 | Out-Null
    $fX += $fw
}

# Two segment cards
$segs = @(
    @(36, 114, "SEGMENT 1 - COMMUNITY BANKING OPS", '$500/month', $cLB, $cB,
      @("Job Titles:", "VP Operations / Director Operations / Head of Customer Service / COO / VP Customer Experience"),
      @("Industry:", "Banking + Financial Services"),
      @("Company Size:", "200 - 2,000 employees   |   Geography: United States"),
      @("Message Angle:", "Operational pain: call volume, after-hours coverage, repeat queries, staff capacity"),
      @("Sends / Opens:", "~1,500 sends/mo   |   ~780 opens (52%)   |   Est. 10-14 leads   |   CPL `$36-50")),
    @(490, 114, "SEGMENT 2 - CREDIT UNION C-SUITE", '$300/month', $cPB, $cI,
      @("Job Titles:", "CEO / COO / CTO / Chief Digital Officer / VP Technology / VP Member Experience"),
      @("Industry:", "Financial Services - credit union companies filter"),
      @("Company Size:", "50 - 500 employees   |   Geography: United States"),
      @("Message Angle:", "Member experience + empathy: mission-first language, 24/7 coverage, compliance"),
      @("Sends / Opens:", "~900 sends/mo   |   ~468 opens (52%)   |   Est. 6-8 leads   |   CPL `$38-50"))
)

foreach($seg in $segs){
    $sx=$seg[0]; $sy=$seg[1]; $st=$seg[2]; $sb=$seg[3]; $sbg=$seg[4]; $sa=$seg[5]
    Rect $sl $sx $sy 444 290 $sbg $false | Out-Null
    Rect $sl $sx $sy 444 3 $sa | Out-Null
    TBox $sl ($sx+12) ($sy+8) 290 18 $st 9 $cB $true 1 "Aptos" | Out-Null
    $bb = Rect $sl ($sx+308) ($sy+6) 126 22 $sa
    TBox $sl ($sx+308) ($sy+6) 126 22 $sb 10 $cW $true 2 "Poppins" 3 | Out-Null
    Rect $sl ($sx+12) ($sy+30) 420 1 $cBd | Out-Null
    $ly = $sy + 38
    foreach($line in $seg[6..10]){
        TBox $sl ($sx+12) $ly 60 18 $line[0] 8.5 $sa $true 1 "Aptos" | Out-Null
        TBox $sl ($sx+76) $ly 356 18 $line[1] 8.5 $cBT $false 1 "Aptos" | Out-Null
        $ly += 46
    }
}

# Copy guidance
Rect $sl 36 410 888 100 $cIB $false | Out-Null
Rect $sl 36 410 4 100 $cB | Out-Null
TBox $sl 46 416 868 14 "COPY DIRECTION + OPTIMIZATION RULE" 9 $cB $true 1 "Aptos" | Out-Null
TBox $sl 46 432 420 70 "Subject line formula: [Problem they recognise] + [Unexpected framing].`nExample: 'Your members are calling after hours. Here is what is happening.'`nOpen sentence: one specific operational truth, not a product pitch.`nMessage length: under 150 words. Single CTA: demo booking link." 9 $cBT $false 1 "Aptos" 1 | Out-Null
TBox $sl 490 432 420 70 "Day 15 review rule: If open-to-reply rate is below 4%, pause and test a new subject line before Day 30. Do not wait the full 30 days. InMail performance is driven almost entirely by the first 2 lines. Every 30-day cycle that runs on a weak subject line costs 450 sends and ~234 opens with no replies." 9 $cBT $false 1 "Aptos" 1 | Out-Null

# ============================================================
# SLIDE 5 - EMAIL MARKETING STRATEGY
# ============================================================
Write-Host "Slide 5: Email Strategy..."
$sl = NewSlide $prs
SlideHdr $sl "Email Marketing Strategy" "Parallel nurture channel / Tool: MailChimp / Two separate sequences"

# Strategy logic
Rect $sl 36 74 888 38 $cN | Out-Null
TBox $sl 46 80 878 26 "Email is a parallel nurture channel, not a cold acquisition channel. It reinforces InMail: prospects who received an InMail and are on the fence often convert via email follow-up. Activate both sequences as soon as first leads come in from paid channels. Segment strictly - financial institutions and real estate receive completely separate sequences." 9 $cLB $false 1 "Aptos" 3 | Out-Null

# Column headers
$eHdrs = @("Email No.", "Send Day", "Subject Focus", "Content Angle", "CTA")
$eX    = @(36, 106, 166, 416, 666)
$eW    = @(70,  60, 250, 250, 258)
Rect $sl 36 120 888 24 $cB | Out-Null
for($i=0;$i-lt 5;$i++){
    TBox $sl ($eX[$i]+3) 122 ($eW[$i]-6) 20 $eHdrs[$i] 8.5 $cW $true 1 "Aptos" 3 | Out-Null
}

# SEQUENCE 1 - Financial Institutions
TBox $sl 36 150 888 18 "SEQUENCE 1 - FINANCIAL INSTITUTIONS (Banks + Credit Unions)" 9 $cB $true 1 "Aptos" | Out-Null
$seq1 = @(
    @("Email 1", "Day 0",  "The real cost of manual call handling at a bank",         "Awareness: quantify the problem they already feel but have not measured",            "Read more - no CTA yet"),
    @("Email 2", "Day 3",  "What compliance-native AI sounds like vs. standard AI",   "Product depth: compliance + empathy positioning vs. generic deflection-first tools", "One link to product page"),
    @("Email 3", "Day 7",  "How [similar institution] handled 800 calls without adding staff", "Social proof framing (anonymised or category-level result if no client yet)",  "Request 15-min demo"),
    @("Email 4", "Day 14", "Still thinking? Here is the ROI breakdown for your size", "Lead magnet: ROI one-pager for institutions of their asset size",                    "Download ROI guide"),
    @("Email 5", "Day 30", "Final follow-up: one question",                           "Single question close: 'Is call volume a priority for your team this quarter?'",     "Reply to this email / Book demo")
)
$ry1 = 170; $ri1 = 0
foreach($row in $seq1){
    $rowBg1 = if($ri1 % 2 -eq 0){$cIB}else{$cW}
    Rect $sl 36 $ry1 888 38 $rowBg1 $false | Out-Null
    for($i=0;$i-lt 5;$i++){
        TBox $sl ($eX[$i]+3) ($ry1+3) ($eW[$i]-6) 32 $row[$i] 8.5 $cBT $false 1 "Aptos" 1 | Out-Null
    }
    Rect $sl 36 ($ry1+38) 888 1 $cBd | Out-Null
    $ry1 += 38; $ri1++
}

# SEQUENCE 2 - Real Estate
TBox $sl 36 362 888 18 "SEQUENCE 2 - REAL ESTATE INSTITUTIONS" 9 $cI $true 1 "Aptos" | Out-Null
$seq2 = @(
    @("Email 1", "Day 0",  "100 property inquiries a day. How many happen after hours?",   "Awareness: frame the after-hours coverage gap at institutional scale",            "Read more"),
    @("Email 2", "Day 4",  "How AI-native voice handles complex property queries",          "Product: feature depth for RE - multi-language, sentiment detection, escalation", "Product walkthrough link"),
    @("Email 3", "Day 10", "Demo: AI voice for a firm your size",                           "Size-specific CTA: show you understand their scale",                              "Book 15-min demo"),
    @("Email 4", "Day 21", "One question about your team's inquiry volume",                 "Final single-question close",                                                     "Reply / Book demo")
)
$ry2 = 382; $ri2 = 0
foreach($row in $seq2){
    $rowBg2 = if($ri2 % 2 -eq 0){$cIB}else{$cW}
    Rect $sl 36 $ry2 888 36 $rowBg2 $false | Out-Null
    for($i=0;$i-lt 5;$i++){
        TBox $sl ($eX[$i]+3) ($ry2+3) ($eW[$i]-6) 30 $row[$i] 8.5 $cBT $false 1 "Aptos" 1 | Out-Null
    }
    Rect $sl 36 ($ry2+36) 888 1 $cBd | Out-Null
    $ry2 += 36; $ri2++
}

TBox $sl 36 528 888 10 "Note: Avoid clinical jargon in subject lines. Financial email tone: expert-peer. Real estate email tone: operational, practical. Both sequences should feel like they come from a knowledgeable colleague, not a vendor." 7.5 $cMT $false 1 "Aptos" | Out-Null

# ============================================================
# SLIDE 6 - GOOGLE ADS: 3 CAMPAIGN STRUCTURE
# ============================================================
Write-Host "Slide 6: Google Ads..."
$sl = NewSlide $prs
SlideHdr $sl "Google Ads - 3 Campaign Structure" "Phrase + exact match only / No broad match / No competitor conquest / Activate at `$1,200+ budget"

# Context box
Rect $sl 36 74 888 34 $cIB $false | Out-Null
Rect $sl 36 74 4 34 $cMT | Out-Null
TBox $sl 46 80 876 22 "Total addressable search volume across all 3 campaigns: ~3,200-5,000 searches/month. Google is a high-intent supplement to LinkedIn outbound, not a volume channel. Expected contribution: 3-8 high-quality leads/month at `$1,200+ tier. CPL on Google starts high (Month 1 `$150-300) and improves as Quality Score builds." 8.5 $cMT $false 1 "Aptos" 3 | Out-Null

# 3 campaign cards - full width stack
$camps = @(
    @(36, 116, "FINANCIAL SERVICES CAMPAIGN", "Activate first. Highest commercial intent. Start at `$400/mo.", $cLB, $cB,
      "conversational ai for banking (+50% trend)  /  conversational ai in banking (+400% trend)  /  banking virtual assistant (+25%)  /  conversational banking (+50%)  /  conversational ai banking (+300%)",
      "~290 monthly searches. Phrase + exact match only. Budget: `$400-600/mo. Avg CPC `$11-25. Est. clicks: 16-36/mo. Conv rate 2%. Est. leads: 1-2/mo.",
      "Mid-to-bottom funnel. Vendors actively evaluating banking AI solutions. Highest lead quality of all 3 campaigns. CPC is high due to commercial intent."),
    @(36, 254, "REAL ESTATE CAMPAIGN", "AI-specific terms only. Strict negative keyword list required.", $cPB, $cI,
      "real estate ai assistant  /  realtor virtual receptionist  /  virtual receptionist real estate  /  voice ai for real estate  /  ai voice agent real estate",
      "~230 monthly searches. Budget: `$300-400/mo. Avg CPC `$10-18. Est. clicks: 17-40/mo. Conv rate 2%. Est. leads: 1-2/mo.",
      "CRITICAL: Add negatives - hire / hiring / salary / offshore / philippines / upwork / freelance / staffing. Without these, 1,900/mo of VA hiring traffic will consume budget immediately."),
    @(36, 392, "GENERAL AI VOICE CAMPAIGN", "Broader terms. Top-of-funnel awareness. Lower intent than Financial.", $cIB, $cDB,
      "ai voice agent (2,400/mo)  /  voice ai company (260/mo)  /  conversational ai voice assistant (140/mo)",
      "~2,800 monthly searches - dominated by 'ai voice agent'. Budget: `$200/mo. Avg CPC `$7-15. Est. clicks: 14-29/mo. Conv rate 1.5%. Est. leads: 0-1/mo.",
      "Top-of-funnel. Mix of researchers and buyers. Lower conversion rate than Financial campaign. Value: brand presence on the generic category term before competition intensifies.")
)

foreach($c in $camps){
    $cx=$c[0]; $cy=$c[1]; $ct=$c[2]; $cs=$c[3]; $cb=$c[4]; $ca=$c[5]
    $kws=$c[6]; $stats=$c[7]; $note=$c[8]
    Rect $sl $cx $cy 888 128 $cb $false | Out-Null
    Rect $sl $cx $cy 888 3 $ca | Out-Null
    TBox $sl ($cx+12) ($cy+8) 560 16 $ct 10 $ca $true 1 "Aptos" | Out-Null
    TBox $sl ($cx+12) ($cy+26) 860 16 "Keywords: $kws" 8.5 $cBT $false 1 "Aptos" | Out-Null
    Rect $sl ($cx+12) ($cy+44) 860 1 $cBd | Out-Null
    TBox $sl ($cx+12) ($cy+48) 420 72 "Stats: $stats" 8.5 $cBT $false 1 "Aptos" 1 | Out-Null
    TBox $sl ($cx+444) ($cy+48) 444 72 $note 8.5 $cB $false 1 "Aptos" 1 | Out-Null
}

# ============================================================
# SLIDE 7 - $800/MONTH MEDIA PLAN
# ============================================================
Write-Host "Slide 7: `$800 Plan..."
$sl = NewSlide $prs
SlideHdr $sl "Media Plan - Budget: `$800 / Month" "LinkedIn InMail only / 2 segments running simultaneously"

# Package header
Rect $sl 36 74 888 24 $cB | Out-Null
TBox $sl 40 76 880 20 "BUDGET: `$800 / MONTH   |   PLATFORM: LinkedIn InMail   |   SEGMENTS: 2   |   GOOGLE ADS: Not active at this tier" 9 $cW $true 1 "Aptos" 3 | Out-Null

DrawColHdrs $sl 98
$rh7 = 38
$r1 = @("InMail - Banking Ops","LinkedIn","VP Ops/Dir Ops/COO (Banks 200-2K emp)",'$500',"~12,000","1,500 sends","1x","780 opens","52%","1.5%","10-14",'$36-50','$16.67','$0.33')
$r2 = @("InMail - Credit Unions","LinkedIn","CEO/CTO/COO (CUs 50-500 emp)",'$300',"~8,000","900 sends","1x","468 opens","52%","1.5%","6-8",'$38-50','$10.00','$0.33')
DrawRow $sl 124 $rh7 $r1 $cW $cBT $false
DrawRow $sl 162 $rh7 $r2 $cIB $cBT $false
DrawTotal $sl 200 @("TOTAL","","","$800","~20,000","2,400 sends","","1,248 opens","","","16-22",'$36-50',"","")

# 3-month progression
Rect $sl 36 242 888 22 $cN | Out-Null
TBox $sl 40 244 880 18 "3-MONTH CPL IMPROVEMENT TRAJECTORY (InMail optimisation)" 9 $cW $true 1 "Aptos" 3 | Out-Null
MonthBar $sl 264 "Blended CPL:" '$36-50' '$31-44' '$27-40'
MonthBar $sl 294 "What drives change:" "Learning phase - subject line and audience being tested" "Refine subject line from Day 15/30 open data. Audience filters tightening." "Warm replies converting. Negative audiences excluded. Opening tested."
MonthBar $sl 324 "Est. Leads:" "10-14" "12-17" "14-20"

# Context note
Rect $sl 36 362 888 66 $cIB $false | Out-Null
Rect $sl 36 362 4 66 $cB | Out-Null
TBox $sl 46 368 868 54 "At `$800/month, LinkedIn InMail is the ONLY active paid channel. Total targetable ICP on LinkedIn across both segments: ~20,000 decision-makers. At 2,400 sends/month it takes ~8 months to cycle through the full audience once, meaning the same audience can be re-messaged at lower frequency without burn. Key optimization variable: subject line open rate. If Day 15 open rate is below 40%, the subject line is the problem - not the offer." 8.5 $cBT $false 1 "Aptos" 1 | Out-Null

# ============================================================
# SLIDE 8 - $1,200/MONTH MEDIA PLAN
# ============================================================
Write-Host "Slide 8: `$1,200 Plan..."
$sl = NewSlide $prs
SlideHdr $sl "Media Plan - Budget: `$1,200 / Month" "LinkedIn InMail `$800 + Google Ads Financial Campaign `$400"

Rect $sl 36 74 888 24 $cB | Out-Null
TBox $sl 40 76 880 20 "BUDGET: `$1,200 / MONTH   |   PLATFORMS: LinkedIn InMail + Google Ads   |   CAMPAIGNS: 3 total   |   GOOGLE: Financial Keywords only" 9 $cW $true 1 "Aptos" 3 | Out-Null

DrawColHdrs $sl 98
$rh8 = 36
$g1  = @("Financial Keywords","Google","Conversational AI banking intent",'$400',"~290 srch/mo","~4,500 impr","N/A","~27 clicks","~3%","2%","1-2",'$200-400','$13.33','$11-15')
DrawRow $sl 124 $rh8 $r1 $cW $cBT $false
DrawRow $sl 160 $rh8 $r2 $cIB $cBT $false
DrawRow $sl 196 $rh8 $g1 $cPB $cBT $false
DrawTotal $sl 232 @("TOTAL","","","$1,200","","","","","","","17-24",'$50-71',"","")

Rect $sl 36 274 888 20 $cN | Out-Null
TBox $sl 40 276 880 16 "3-MONTH CPL IMPROVEMENT TRAJECTORY" 9 $cW $true 1 "Aptos" 3 | Out-Null
MonthBar $sl 294 "Blended CPL:" '$50-71' '$44-62' '$38-54'
MonthBar $sl 324 "InMail CPL:" '$36-50' '$31-44' '$27-40'
MonthBar $sl 354 "Google CPL:" '$200-400 (no QS)' '$150-250 (QS building)' '$100-180 (QS established)'

Rect $sl 36 392 888 66 $cIB $false | Out-Null
Rect $sl 36 392 4 66 $cI | Out-Null
TBox $sl 46 398 868 54 "Google at `$400/month targets ~290 monthly searches across conversational AI banking keywords. This is a low-volume, high-intent segment. Expect 1-2 leads/month from Google at this tier. The primary value is not lead volume - it is Quality Score development and brand presence on high-intent terms before the category becomes competitive. Blended CPL is higher than InMail because Google's learning phase inflates early costs." 8.5 $cBT $false 1 "Aptos" 1 | Out-Null

Rect $sl 36 466 888 48 $cN | Out-Null
TBox $sl 40 470 868 40 "KEYWORD DIRECTION - FINANCIAL CAMPAIGN: conversational ai for banking (70/mo +50%)  /  conversational ai in banking (70/mo +400%)  /  banking virtual assistant (50/mo +25%)  /  conversational banking (70/mo +50%)  /  conversational ai banking (30/mo +300%)  |  Match types: Phrase + Exact only. No broad match." 8.5 $cLB $false 1 "Aptos" 1 | Out-Null

# ============================================================
# SLIDE 9 - $2,000/MONTH MEDIA PLAN
# ============================================================
Write-Host "Slide 9: `$2,000 Plan..."
$sl = NewSlide $prs
SlideHdr $sl "Media Plan - Budget: `$2,000 / Month" "LinkedIn InMail `$800 + Google Ads `$1,200 across 3 campaigns"

Rect $sl 36 74 888 24 $cB | Out-Null
TBox $sl 40 76 880 20 "BUDGET: `$2,000 / MONTH   |   PLATFORMS: LinkedIn InMail + Google Ads   |   CAMPAIGNS: 5 total   |   GOOGLE: Financial `$600 + Real Estate `$400 + General `$200" 9 $cW $true 1 "Aptos" 3 | Out-Null

DrawColHdrs $sl 98
$rh9 = 32
$g2  = @("Financial Keywords","Google","Conversational AI banking intent",'$600',"~290 srch/mo","~6,500 impr","N/A","~40 clicks","~3%","2%","1-2",'$300-600','$20.00','$11-17')
$g3  = @("Real Estate AI","Google","RE AI intent (AI-specific only)",'$400',"~230 srch/mo","~4,000 impr","N/A","~25 clicks","~2.5%","2%","1-2",'$200-400','$13.33','$10-18')
$g4  = @("General AI Voice","Google","AI voice agent, voice AI company",'$200',"~2,660 srch/mo","~800 impr","N/A","~20 clicks","~3%","1.5%","0-1",'$200+',' $6.67','$7-10')

DrawRow $sl 124 $rh9 $r1 $cW $cBT $false
DrawRow $sl 156 $rh9 $r2 $cIB $cBT $false
DrawRow $sl 188 $rh9 $g2 $cPB $cBT $false
DrawRow $sl 220 $rh9 $g3 $cW $cBT $false
DrawRow $sl 252 $rh9 $g4 $cIB $cBT $false
DrawTotal $sl 284 @("TOTAL","","","$2,000","","","","","","","18-27",'$74-111',"","")

Rect $sl 36 326 888 20 $cN | Out-Null
TBox $sl 40 328 880 16 "3-MONTH CPL IMPROVEMENT TRAJECTORY" 9 $cW $true 1 "Aptos" 3 | Out-Null
MonthBar $sl 346 "Blended CPL:" '$74-111' '$65-95' '$55-80'
MonthBar $sl 376 "InMail CPL:" '$36-50' '$31-44' '$27-40'
MonthBar $sl 406 "Google blended CPL:" '$150-300 (learning phase)' '$100-200 (QS building)' '$75-150 (approaching steady state)'

Rect $sl 36 444 888 70 $cIB $false | Out-Null
Rect $sl 36 444 4 70 $cI | Out-Null
TBox $sl 46 448 440 62 "Google volume reality check: Across all 3 campaigns, total search volume is ~3,200-5,600 searches/month. At `$1,200 Google budget, expect 3-5 leads/month from Google. These are high-quality, bottom-funnel leads - people actively searching for AI voice solutions - but volume is fundamentally limited by category size. InMail remains the primary pipeline engine at this budget." 8.5 $cBT $false 1 "Aptos" 1 | Out-Null
TBox $sl 500 448 378 62 "Activation rule: Only launch Real Estate campaign after Financial campaign has run for 30+ days and shown at least 1 lead. Only launch General campaign after both Financial and Real Estate are running profitably. Build Quality Score on the highest-intent terms first, then expand." 8.5 $cB $false 1 "Aptos" 1 | Out-Null

# ============================================================
Write-Host "Saving..."
$savePath = "C:\Users\Rishabhb\Downloads\control room\CSXAI\01_Reports\CSXAI_PM_Slides_LinkedInDeck.pptx"
if (Test-Path $savePath) { Remove-Item $savePath -Force }
$prs.SaveAs($savePath)
Write-Host "Saved: $savePath"
$prs.Close()
$ppt.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($ppt) | Out-Null
Write-Host "Done. 9 slides."
