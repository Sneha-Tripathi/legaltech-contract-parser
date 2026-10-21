from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from django.core.paginator import Paginator

from reportlab.pdfgen import canvas

import re
import json

from .models import Contract, ExtractedClause, RiskFlag, AIAnalysis
from .utils import extract_text_from_pdf
from .analyzer import detect_clauses, detect_risks
from .queries import get_contract_with_details
from contracts.services.pdf_processor import PDFProcessor
from contracts.services.clause_detector import ClauseDetector
from contracts.services.risk_scorer import RiskScorer
from contracts.services.ai_analyzer import analyze_contract

import threading

# ======================================================
# Home Page
# ======================================================

def home(request):
    return render(request, "home.html")


# ======================================================
# Features Page
# ======================================================

def features_view(request):
    return render(request, "contracts/features.html")


# ======================================================
# FAQ Page
# ======================================================

def faq_view(request):
    return render(request, "contracts/faq.html")


# ======================================================
# Upload Contract
# ======================================================

@login_required
def upload_contract(request):

    if request.method == "POST":

        title = request.POST.get("title")
        uploaded_file = request.FILES.get("file")

        if not title or not uploaded_file:
            return render(
                request,
                "contracts/upload.html",
                {
                    "error": "Please provide title and PDF file."
                }
            )

        # Save Contract
        contract = Contract.objects.create(
            user=request.user,
            title=title,
            uploaded_file=uploaded_file
        )

        # Extract PDF Text
        processor = PDFProcessor(contract.uploaded_file.path)
        text = processor.extract_text()
        processor.close()

        # Save extracted text
        contract.extracted_text = text

        # Summary
        if text:
            contract.summary = text[:300]
        else:
            contract.summary = "No Summary Generated"

        # Keywords
        if text:
            words = text.split()
            unique_words = []
            for word in words:
                word = word.strip(",.!?()[]{}").lower()
                if len(word) > 4 and word not in unique_words:
                    unique_words.append(word)
            contract.keywords = ", ".join(unique_words[:15])

        contract.save()

        # Detect Clauses
        detector = ClauseDetector(text)
        clauses = detector.detect()

        for clause in clauses:
            ExtractedClause.objects.create(
                contract=contract,
                clause_name=clause
            )

        # Risk Analysis
        scorer = RiskScorer(clauses)
        risk_report = scorer.calculate()

        for level, items in risk_report.items():
            for item in items:
                RiskFlag.objects.create(
                    contract=contract,
                    risk_type=level,
                    description=item
                )

        # ============================================
        # AI-POWERED ANALYSIS (Async via Threading)
        # ============================================
        # Run AI analysis in background thread so upload is never blocked.
        # The AIAnalysis will be saved to database when ready.

        def run_ai_analysis():
            """Run AI analysis in background thread."""
            try:
                import django
                django.db.close_old_connections()

                ai_result = analyze_contract(text)

                if not ai_result.get("error"):
                    AIAnalysis.objects.create(
                        contract=contract,
                        summary=ai_result.get("summary", ""),
                        risk_analysis=ai_result.get("risk_analysis", []),
                        missing_clauses=ai_result.get("missing_clauses", []),
                        recommendations=ai_result.get("recommendations", []),
                        confidence=ai_result.get("confidence", ""),
                        tags=ai_result.get("tags", []),
                        raw_response=ai_result,
                    )
            except Exception:
                pass  # AI failure never crashes upload

        thread = threading.Thread(target=run_ai_analysis, daemon=True)
        thread.start()

        messages.success(
            request,
            "Contract uploaded and analyzed successfully."
        )

        return redirect("result", contract.id)

    return render(
        request,
        "contracts/upload.html"
    )
# ======================================================
# Result Page
# ======================================================

@login_required
def result_view(request, contract_id):

    contract = get_contract_with_details(contract_id)

    clauses = contract.extractedclause_set.all()

    risks = contract.riskflag_set.all()

    # AI ANALYSIS RESULTS
    ai_analysis = AIAnalysis.objects.filter(
        contract=contract
    ).first()

    # DEADLINE EXTRACTION (Anjali Feature)
    deadlines = []
    if contract.extracted_text:
        pattern = r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}\s+[A-Za-z]+\s+\d{4}"
        deadlines = re.findall(pattern, contract.extracted_text)

    return render(
        request,
        "contracts/result.html",
        {
            "contract": contract,
            "clauses": clauses,
            "risks": risks,
            "deadlines": deadlines,
            "ai_analysis": ai_analysis,
        }
    )


# ======================================================
# Dashboard — Analytics Hub
# ======================================================

@login_required
def dashboard(request):

    contracts = Contract.objects.filter(user=request.user)

    # ---- Stat Counts ----
    total_contracts = contracts.count()
    
    # High Risk = contracts with High Risk flags
    high_risk_ids = RiskFlag.objects.filter(
        contract__user=request.user,
        risk_type__icontains="High"
    ).values_list('contract_id', flat=True).distinct()
    high_risk_count = len(set(high_risk_ids))
    
    total_clauses = ExtractedClause.objects.filter(
        contract__user=request.user
    ).count()
    
    total_risks = RiskFlag.objects.filter(
        contract__user=request.user
    ).count()

    # ---- Monthly Upload Trend (last 6 months) ----
    monthly_qs = contracts.annotate(
        month=TruncMonth('uploaded_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')[:6]

    monthly_labels = []
    monthly_values = []
    for entry in monthly_qs:
        monthly_labels.append(entry['month'].strftime('%b %Y'))
        monthly_values.append(entry['count'])

    # ---- Risk Distribution ----
    risk_dist = RiskFlag.objects.filter(
        contract__user=request.user
    ).values('risk_type').annotate(
        count=Count('id')
    ).order_by('-count')

    # Map to High / Medium / Low
    risk_dist_map = {"High Risk": 0, "Medium Risk": 0, "Low Risk": 0}
    for entry in risk_dist:
        rt = entry['risk_type']
        if 'High' in rt:
            risk_dist_map["High Risk"] += entry['count']
        elif 'Medium' in rt:
            risk_dist_map["Medium Risk"] += entry['count']
        else:
            risk_dist_map["Low Risk"] += entry['count']

    # ---- Clause Distribution ----
    clause_dist = ExtractedClause.objects.filter(
        contract__user=request.user
    ).values('clause_name').annotate(
        count=Count('id')
    ).order_by('-count')

    clause_labels = [c['clause_name'] for c in clause_dist]
    clause_values = [c['count'] for c in clause_dist]
    clause_data_count = len(clause_labels)

    # ---- Activity: Recent Contracts ----
    recent_contracts = contracts.select_related('user').order_by('-uploaded_at')[:5]

    # ---- Activity: Recent Risk Detections ----
    recent_risks = RiskFlag.objects.filter(
        contract__user=request.user
    ).select_related('contract').order_by('-created_at', '-id')[:5]

    # ---- Contract summaries & keywords counts ----
    summaries_count = contracts.exclude(summary__isnull=True).exclude(summary="").count()
    keywords_count = contracts.exclude(keywords__isnull=True).exclude(keywords="").count()

    return render(
        request,
        "contracts/dashboard.html",
        {
            "total_contracts": total_contracts,
            "high_risk_count": high_risk_count,
            "total_clauses": total_clauses,
            "total_risks": total_risks,
            "summaries_count": summaries_count,
            "keywords_count": keywords_count,
            "monthly_labels_json": json.dumps(monthly_labels),
            "monthly_values_json": json.dumps(monthly_values),
            "risk_labels_json": json.dumps(list(risk_dist_map.keys())),
            "risk_values_json": json.dumps(list(risk_dist_map.values())),
            "clause_labels_json": json.dumps(clause_labels),
            "clause_values_json": json.dumps(clause_values),
            "clause_data_count": clause_data_count,
            "recent_contracts": recent_contracts,
            "recent_risks": recent_risks,
        }
    )


# ======================================================
# Contracts List — with Search, Pagination, Sorting
# ======================================================

@login_required
def contracts_list(request):

    search = request.GET.get("search", "")
    sort_by = request.GET.get("sort", "-uploaded_at")
    page = request.GET.get("page", 1)

    allowed_sorts = [
        "id", "-id",
        "title", "-title",
        "uploaded_at", "-uploaded_at",
    ]
    if sort_by not in allowed_sorts:
        sort_by = "-uploaded_at"

    contracts = Contract.objects.filter(
        user=request.user
    ).prefetch_related(
        'extractedclause_set',
        'riskflag_set'
    ).order_by(sort_by)

    if search:
        contracts = contracts.filter(title__icontains=search)

    # Annotate each contract with risk info
    contract_list = []
    for c in contracts:
        risks = c.riskflag_set.all()
        has_high = any('High' in r.risk_type for r in risks)
        has_medium = any('Medium' in r.risk_type for r in risks)
        has_low = any('Low' in r.risk_type for r in risks)
        
        if has_high:
            risk_label = "High Risk"
            risk_badge = "danger"
        elif has_medium:
            risk_label = "Medium Risk"
            risk_badge = "warning"
        elif has_low:
            risk_label = "Low Risk"
            risk_badge = "success"
        else:
            risk_label = "No Risk"
            risk_badge = "secondary"
        
        clause_count = c.extractedclause_set.count()
        
        contract_list.append({
            'id': c.id,
            'title': c.title,
            'uploaded_at': c.uploaded_at,
            'risk_label': risk_label,
            'risk_badge': risk_badge,
            'clause_count': clause_count,
        })

    # Pagination
    paginator = Paginator(contract_list, 10)
    page_obj = paginator.get_page(page)

    return render(
        request,
        "contracts/contracts_list.html",
        {
            "page_obj": page_obj,
            "contracts": page_obj.object_list,
            "search": search,
            "sort_by": sort_by,
            "total": paginator.count,
        }
    )


# ======================================================
# Database Statistics
# ======================================================

@login_required
def database_stats(request):

    contracts = Contract.objects.filter(user=request.user)

    return render(
        request,
        "contracts/stats.html",
        {
            "total_contracts": contracts.count(),
            "total_clauses": ExtractedClause.objects.filter(
                contract__user=request.user
            ).count(),
            "total_risks": RiskFlag.objects.filter(
                contract__user=request.user
            ).count(),
            "total_summaries": contracts.exclude(summary="").count(),
            "total_keywords": contracts.exclude(keywords="").count(),
        }
    )


# ======================================================
# Risk Explorer — View contracts by risk level
# ======================================================

@login_required
def risk_explorer(request):

    level = request.GET.get("level", "High")

    # Optimized: find contract IDs with matching risk flags at DB level
    risk_contract_ids = RiskFlag.objects.filter(
        contract__user=request.user,
        risk_type__icontains=level
    ).values_list('contract_id', flat=True).distinct()

    contracts = Contract.objects.filter(
        id__in=risk_contract_ids,
        user=request.user
    ).prefetch_related(
        'extractedclause_set',
        'riskflag_set'
    ).order_by('-uploaded_at')

    return render(
        request,
        "contracts/risk_explorer.html",
        {
            "contracts": contracts,
            "level": level,
            "levels": ["High", "Medium", "Low"],
        }
    )


# ======================================================
# Clause Explorer — View all clauses grouped
# ======================================================

@login_required
def clause_explorer(request):

    # Group clauses by name with count
    clause_groups = ExtractedClause.objects.filter(
        contract__user=request.user
    ).values('clause_name').annotate(
        count=Count('id')
    ).order_by('-count')

    # Optimized: bulk-fetch contracts for all clause types in one pass
    clause_names = [c['clause_name'] for c in clause_groups]

    # Build a dict of clause_name -> list of contracts
    clause_contracts_map = {name: [] for name in clause_names}
    all_matching = ExtractedClause.objects.filter(
        contract__user=request.user,
        clause_name__in=clause_names
    ).select_related('contract').order_by('-contract__uploaded_at')

    for ec in all_matching:
        name = ec.clause_name
        if len(clause_contracts_map[name]) < 5:
            if ec.contract not in clause_contracts_map[name]:
                clause_contracts_map[name].append(ec.contract)

    clause_data = []
    for cg in clause_groups:
        name = cg['clause_name']
        clause_data.append({
            'name': name,
            'count': cg['count'],
            'contracts': clause_contracts_map.get(name, []),
        })

    total_clauses = sum(cg['count'] for cg in clause_groups)

    return render(
        request,
        "contracts/clause_explorer.html",
        {
            "clause_data": clause_data,
            "total_clauses": total_clauses,
            "unique_clauses": len(clause_groups),
        }
    )
# ======================================================
# Settings Page
# ======================================================

@login_required
def settings_view(request):
    """Render the Settings page."""
    return render(
        request,
        "contracts/settings.html",
        {
            "user": request.user,
        }
    )


# ======================================================
# Profile Page
# ======================================================

@login_required
def profile_view(request):
    """Render the Profile page with user stats."""
    contracts = Contract.objects.filter(user=request.user)
    total_contracts = contracts.count()
    total_clauses = ExtractedClause.objects.filter(
        contract__user=request.user
    ).count()
    total_risks = RiskFlag.objects.filter(
        contract__user=request.user
    ).count()
    recent_contracts = contracts.order_by('-uploaded_at')[:5]

    return render(
        request,
        "contracts/profile.html",
        {
            "user": request.user,
            "total_contracts": total_contracts,
            "total_clauses": total_clauses,
            "total_risks": total_risks,
            "recent_contracts": recent_contracts,
        }
    )


# ======================================================
# Download PDF Report
# ======================================================

@login_required
def download_report(request, contract_id):

    contract = get_object_or_404(
        Contract,
        id=contract_id,
        user=request.user
    )

    clauses = ExtractedClause.objects.filter(
        contract=contract
    )

    risks = RiskFlag.objects.filter(
        contract=contract
    )

    response = HttpResponse(
        content_type="application/pdf"
    )

    response[
        "Content-Disposition"
    ] = f'attachment; filename="{contract.title}_Report.pdf"'

    pdf = canvas.Canvas(response)

    width, height = 595, 842

    y = height - 50

    # =====================================================
    # Heading
    # =====================================================

    pdf.setFont("Helvetica-Bold", 18)

    pdf.drawString(
        130,
        y,
        "LEGALTECH CONTRACT REPORT"
    )

    y -= 40

    pdf.setFont("Helvetica", 12)

    pdf.drawString(
        50,
        y,
        f"Contract Title : {contract.title}"
    )

    y -= 20

    pdf.drawString(
        50,
        y,
        f"Uploaded : {contract.uploaded_at}"
    )

    y -= 30

    # =====================================================
    # Summary (Anjali Feature)
    # =====================================================

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawString(
        50,
        y,
        "Summary"
    )

    y -= 20

    pdf.setFont(
        "Helvetica",
        11
    )

    summary = getattr(
        contract,
        "summary",
        ""
    )

    if summary:

        pdf.drawString(
            60,
            y,
            summary[:120]
        )

    else:

        pdf.drawString(
            60,
            y,
            "No Summary Available"
        )

    y -= 40

    # =====================================================
    # Keywords (Anjali Feature)
    # =====================================================

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawString(
        50,
        y,
        "Keywords"
    )

    y -= 20

    pdf.setFont(
        "Helvetica",
        11
    )

    keywords = getattr(
        contract,
        "keywords",
        ""
    )

    if keywords:

        pdf.drawString(
            60,
            y,
            keywords[:120]
        )

    else:

        pdf.drawString(
            60,
            y,
            "No Keywords Available"
        )

    y -= 40

    # =====================================================
    # Clauses
    # =====================================================

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawString(
        50,
        y,
        "Detected Clauses"
    )

    y -= 20

    pdf.setFont(
        "Helvetica",
        11
    )

    if clauses.exists():

        for clause in clauses:

            pdf.drawString(
                60,
                y,
                f"• {clause.clause_name}"
            )

            y -= 18

            if y < 70:

                pdf.showPage()

                y = 800

                pdf.setFont(
                    "Helvetica",
                    11
                )

    else:

        pdf.drawString(
            60,
            y,
            "No Clauses Found"
        )

        y -= 20

    # =====================================================
    # Risks
    # =====================================================

    y -= 15

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawString(
        50,
        y,
        "Risk Analysis"
    )

    y -= 20

    pdf.setFont(
        "Helvetica",
        11
    )

    if risks.exists():

        for risk in risks:

            pdf.drawString(
                60,
                y,
                f"{risk.risk_type}"
            )

            y -= 18

            pdf.drawString(
                80,
                y,
                risk.description
            )

            y -= 25

            if y < 70:

                pdf.showPage()

                y = 800

                pdf.setFont(
                    "Helvetica",
                    11
                )

    else:

        pdf.drawString(
            60,
            y,
            "No Risks Found"
        )

    # =====================================================
    # Footer
    # =====================================================

    pdf.setFont(
        "Helvetica-Oblique",
        10
    )

    pdf.drawString(
        50,
        30,
        "Generated by LegalTech Contract Parsing Engine"
    )

    pdf.save()

    return response


# ======================================================
# Delete Contract
# ======================================================

@login_required
def delete_contract(request, contract_id):

    contract = get_object_or_404(
        Contract,
        id=contract_id,
        user=request.user
    )

    contract.delete()

    messages.success(
        request,
        "Contract deleted successfully."
    )

    return redirect(
        "contracts_list"
    )