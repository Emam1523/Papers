# Stage 2 of the Markdown -> Word pipeline (see md2docx.py).
# Opens the .docx in Word, turns each equation bookmark (eq1, eq2, ...) into a
# real Word equation (UnicodeMath build-up), inserts the table of contents, and
# saves the .docx plus a PDF copy.
param(
    [Parameter(Mandatory = $true)][string]$Docx,
    [string]$Pdf = ""
)

$Docx = (Resolve-Path $Docx).Path
$eqs = Get-Content -Raw -Encoding UTF8 "$Docx.eq.json" | ConvertFrom-Json

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open($Docx)
    $failed = 0
    foreach ($prop in $eqs.PSObject.Properties) {
        $key = $prop.Name
        if (-not $doc.Bookmarks.Exists($key)) {
            Write-Output "missing bookmark $key"
            $failed++
            continue
        }
        $bookmark = $doc.Bookmarks.Item($key)
        $rng = $bookmark.Range
        $bookmark.Delete()
        $math = $rng.OMaths.Add($rng)
        try {
            $om = $math.OMaths(1)
            $paragraphsBefore = $doc.Paragraphs.Count
            $om.BuildUp()
            if ($doc.Paragraphs.Count -ne $paragraphsBefore) {
                Write-Output "build-up merged paragraphs at $key : $($prop.Value.latex)"
                $failed++
            }
            # an equation alone in a paragraph (e.g. a table cell) would
            # otherwise default to centred display mode
            if (-not $prop.Value.display) { $om.Type = 1 }
            # BuildUp does not throw on bad input; leftover linear-format
            # operators mean the equation stayed as plain text
            if ($om.Range.Text -match '[_^\u2592\u25A0\u00A6]') {
                Write-Output "not built up $key : $($prop.Value.latex)"
                $failed++
            }
        } catch {
            Write-Output "build-up failed for $key : $($prop.Value.latex)"
            $failed++
        }
    }

    $rng = $doc.Content
    if ($rng.Find.Execute("@@TOC@@")) {
        $rng.Text = ""
        $toc = $doc.TablesOfContents.Add($rng, $true, 1, 2)
        foreach ($styleId in -20, -21) {  # wdStyleTOC1, wdStyleTOC2
            $pf = $doc.Styles.Item($styleId).ParagraphFormat
            $pf.SpaceBefore = 0
            $pf.SpaceAfter = 1
            $pf.LineSpacingRule = 0  # single
        }
        $toc.Update()
    }
    $doc.Fields.Update() | Out-Null

    $doc.Save()
    if ($Pdf -ne "") {
        $doc.ExportAsFixedFormat($Pdf, 17)
    }
    $doc.Close()
    Write-Output ("equations: {0} total, {1} problems" -f @($eqs.PSObject.Properties).Count, $failed)
} finally {
    $word.Quit()
}
Remove-Item "$Docx.eq.json"
