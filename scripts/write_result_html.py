import os

content = r"""{% extends "base_dashboard.html" %}
{% load static %}

{% block page_title_text %}Contract Analysis Report{% endblock %}
{% block page_subtitle_text %}{{ contract.title }} &bull; AI Generated Legal Contract Summary{% endblock %}

{% block dashboard_content %}

<!-- ========== CONTRACT DETAILS & RISK ========== -->
<div class="row g-4 mb-4">
  <div class="col-12 col-md-6">
    <div class="card" style="background:var(--bg-card);backdrop-filter:blur(16px);border:1px solid var(--border-color);border-radius:var(--radius-2xl);height:100%;width:100%;padding:24px;">
      <h5 style="color:var(--accent);font-weight:700;margin-bottom:12px;">&#x1f4cb; Contract Details</h5>
      <hr style="border-color:var(--border-color);margin:12px 0;">
      <p style="color:var(--text-primary);font-size:15px;line-height:1.6;"><strong style="color:var(--text-secondary);">Title:</strong> {{ contract.title }}</p>
      <p style="color:var(--text-primary);font-size:15px;line-height:1.6;"><strong style="color:var(--text-secondary);">Uploaded:</strong> {{ contract.uploaded_at }}</p>
    </div>
  </div>
  <div class="col-12 col-md-6">
    <div class="card text-center" style="background:var(--bg-card);backdrop-filter:blur(16px);border:1px solid var(--border-color);border-radius:var(--radius-2xl);height:100%;width:100%;padding:24px;">
      <h5 style="color:var(--danger);font-weight:700;margin-bottom:12px;">&#x26a0; Risk Score</h5>
      <hr style="border-color:var(--border-color);margin:12px 0;">
      {% if risks %}
      <span class="badge fs-5" style="background:var(--danger-bg);color:var(--danger);padding:8px 24px;border-radius:var(--radius-full);font-size:18px;">HIGH RISK</span>
      {% else %}
      <span class="badge fs-5" style="background:var(--success-bg);color:var(--success);padding:8px 24px;border-radius:var(--radius-full);font-size:18px;">SAFE</span>
      {% endif %}
    </div>
  </div>
</div>

<!-- AI CONTRACT SUMMARY -->
{% if ai_analysis and ai_analysis.summary %}
<div class="card mb-4" style="background:var(--bg-card);backdrop-filter:blur(16px);border:1px solid var(--border-color);border-radius:var(--radius-2xl);width:100%;padding:24px;">
  <h5 style="color:var(--accent);font-weight:700;margin-bottom:12px;">&#x1f916; AI Contract Summary</h5>
  <hr style="border-color:var(--border-color);margin:12px 0;">
  <p style="color:var(--text-primary);font-size:16px;line-height:1.7;margin:0;">{{ ai_analysis.summary }}</p>
</div>
{% endif %}

<!-- RULE-BASED CLAUSES -->
<h4 style="font-size:22px;font-weight:700;color:var(--text-primary);margin-bottom:16px;">&#x1f4cc; Detected Clauses (Rule-Based)</h4>
<div class="card mb-4" style="background:var(--bg-card);backdrop-filter:blur(16px);border:1px solid var(--border-color);border-radius:var(--radius-2xl);overflow:hidden;width:100%;">
  <div class="table-responsive">
    <table class="table table-hover mb-0 align-middle" style="color:var(--text-secondary);">
      <thead>
        <tr style="background:rgba(26,36,57,0.5);border-bottom:1px solid var(--border-color);">
          <th class="px-4 py-3 text-uppercase small text-muted fw-bold" style="width:80px;">#</th>
          <th class="px-4 py-3 text-uppercase small text-muted fw-bold">Clause</th>
        </tr>
      </thead>
      <tbody>
        {% for clause in clauses %}
        <tr style="border-bottom:1px solid var(--border-light);" onmouseover="this.style.background='rgba(124,92,255,0.04)'" onmouseout="this.style.background=''">
          <td class="px-4 py-3"><span class="badge" style="background:var(--accent-light);color:var(--text-accent);font-weight:700;padding:4px 12px;border-radius:var(--radius-md);">{{ forloop.counter }}</span></td>
          <td class="px-4 py-3"><span class="badge rounded-pill" style="background:var(--info-bg);color:var(--info);padding:6px 14px;font-size:13px;">{{ clause.clause_name }}</span></td>
        </tr>
        {% empty %}
        <tr><td colspan="2" class="text-center px-4 py-4" style="color:var(--text-muted);">No Clauses Found</td></tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>

<!-- RULE-BASED RISKS -->
<h4 style="font-size:22px;font-weight:700;color:var(--text-primary);margin-bottom:16px;">&#x26a0; Risk Analysis (Rule-Based)</h4>
<div class="card mb-4" style="background:var(--bg-card);backdrop-filter:blur(16px);border:1px solid var(--border-color);border-radius:var(--radius-2xl);overflow:hidden;width:100%;">
  <div class="table-responsive">
    <table class="table table-hover mb-0 align-middle" style="color:var(--text-secondary);">
      <thead>
        <tr style="background:rgba(26,36,57,0.5);border-bottom:1px solid var(--border-color);">
          <th class="px-4 py-3 text-uppercase small text-muted fw-bold" style="width:80px;">#</th>
          <th class="px-4 py-3 text-uppercase small text-muted fw-bold">Risk Type</th>
          <th class="px-4 py-3 text-uppercase small text-muted fw-bold">Description</th>
        </tr>
      </thead>
      <tbody>
        {% for risk in risks %}
        <tr style="border-bottom:1px solid var(--border-light);" onmouseover="this.style.background='rgba(124,92,255,0.04)'" onmouseout="this.style.background=''">
          <td class="px-4 py-3"><span class="badge" style="background:var(--accent-light);color:var(--text-accent);font-weight:700;padding:4px 12px;border-radius:var(--radius-md);">{{ forloop.counter }}</span></td>
          <td class="px-4 py-3"><span class="badge rounded-pill" style="background:var(--danger-bg);color:var(--danger);padding:6px 14px;font-size:13px;">{{ risk.risk_type }}</span></td>
          <td class="px-4 py-3" style="color:var(--text-primary);font-size:15px;line-height:1.6;">{{ risk.description }}</td>
        </tr>
        {% empty %}
        <tr><td colspan="3" class="text-center px-4 py-4" style="color:var(--text-muted);">No Risk Detected</td></tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>

{% if ai_analysis and ai_analysis.risk_analysis %}
<h4 style="font-size:22px;font-weight:700;color:var(--text-primary);margin-bottom:16px;">&#x1f9e0; AI Risk Analysis</h4>
<div class="row g-4 mb-4">
  {% for risk in ai_analysis.risk_analysis %}
  <div class="col-12 col-md-6">
    <div class="card" style="background:var(--bg-card);backdrop-filter:blur(16px);border:1px solid var(--border-color);border-radius:var(--radius-2xl);height:100%;width:100%;padding:24px;">
      {% if risk.level == "High" %}
      <span class="badge mb-3" style="background:var(--danger-bg);color:var(--danger);padding:6px 16px;border-radius:var(--radius-full);font-size:13px;font-weight:600;">{{ risk.level }}</span>
      {% elif risk.level == "Medium" %}
      <span class="badge mb-3" style="background:var(--warning-bg);color:var(--warning);padding:6px 16px;border-radius:var(--radius-full);font-size:13px;font-weight:600;">{{ risk.level }}</span>
      {% else %}
      <span class="badge mb-3" style="background:var(--success-bg);color:var(--success);padding:6px 16px;border-radius:var(--radius-full);font-size:13px;font-weight:600;">{{ risk.level }}</span>
      {% endif %}
      <h6 style="font-weight:700;color:var(--text-primary);margin-bottom:12px;font-size:16px;">{{ risk.clause }}</h6>
      <div style="display:flex;flex-direction:column;gap:8px;">
        <p style="font-size:14px;color:var(--text-secondary);line-height:1.6;margin:0;"><strong style="color:var(--text-primary);">Explanation:</strong> {{ risk.explanation }}</p>
        <p style="font-size:14px;color:var(--text-secondary);line-height:1.6;margin:0;"><strong style="color:var(--text-primary);">Why Risky:</strong> {{ risk.why_risky }}</p>
        <p style="font-size:14px;color:var(--text-secondary);line-height:1.6;margin:0;"><strong style="color:var(--text-primary);">Legal Impact:</strong> {{ risk.legal_impact }}</p>
      </div>
    </div>
  </div>
  {% endfor %}
</div>
{% endif %}

{% if ai_analysis and ai_analysis.missing_clauses %}
<h4 style="font-size:22px;font-weight:700;color:var(--text-primary);margin-bottom:16px;">&#x1f50d; Missing Clause Detection</h4>
<div class="row g-4 mb-4">
  {% for item in ai_analysis.missing_clauses %}
  <div class="col-12 col-md-6">
    <div class="card" style="background:rgba(245,158,11,0.04);border:1px solid rgba(245,158,11,0.15);border-radius:var(--radius-2xl);height:100%;width:100%;padding:24px;">
      <h6 style="font-weight:700;color:var(--warning);margin-bottom:8px;font-size:16px;">&#x26d4; {{ item.clause }}</h6>
      <p style="font-size:14px;color:var(--text-secondary);line-height:1.6;margin:0;">{{ item.importance }}</p>
    </div>
  </div>
  {% endfor %}
</div>
{% endif %}

{% if ai_analysis and ai_analysis.recommendations %}
<h4 style="font-size:22px;font-weight:700;color:var(--text-primary);margin-bottom:16px;">&#x1f4a1; AI Recommendations</h4>
<div class="card mb-4" style="background:var(--bg-card);backdrop-filter:blur(16px);border:1px solid var(--border-color);border-radius:var(--radius-2xl);width:100%;padding:24px;">
  <ul style="margin:0;padding-left:20px;display:flex;flex-direction:column;gap:8px;">
    {% for rec in ai_analysis.recommendations %}
    <li style="color:var(--text-secondary);font-size:15px;line-height:1.6;">{{ rec }}</li>
    {% endfor %}
  </ul>
</div>
{% endif %}

{% if ai_analysis %}
<div class="row g-4 mb-4">
  <div class="col-12 col-md-4">
    <div class="card text-center" style="background:var(--bg-card);backdrop-filter:blur(16px);border:1px solid var(--border-color);border-radius:var(--radius-2xl);height:100%;width:100%;padding:24px;">
      <h5 style="color:var(--accent);font-weight:700;margin-bottom:12px;">&#x1f3af; AI Confidence</h5>
      <hr style="border-color:var(--border-color);margin:12px 0;">
      <h2 style="font-size:36px;font-weight:800;color:var(--accent);margin:0;">
        {% if ai_analysis.confidence and ai_analysis.confidence != "N/A" %}
          {{ ai_analysis.confidence }}%
        {% else %}
          N/A
        {% endif %}
      </h2>
    </div>
  </div>
  <div class="col-12 col-md-8">
    <div class="card" style="background:var(--bg-card);backdrop-filter:blur(16px);border:1px solid var(--border-color);border-radius:var(--radius-2xl);height:100%;width:100%;padding:24px;">
      <h5 style="color:var(--accent);font-weight:700;margin-bottom:12px;">&#x1f3f7; Contract Tags</h5>
      <hr style="border-color:var(--border-color);margin:12px 0;">
      {% if ai_analysis.tags %}
      <div class="d-flex flex-wrap gap-2">
        {% for tag in ai_analysis.tags %}
        <span class="badge rounded-pill" style="background:var(--accent-light);color:var(--text-accent);font-size:14px;padding:6px 16px;">{{ tag }}</span>
        {% endfor %}
      </div>
      {% else %}
      <p style="color:var(--text-muted);margin:0;font-size:15px;">No tags available.</p>
      {% endif %}
    </div>
  </div>
</div>
{% endif %}

{% if ai_analysis is None %}
<div class="card mb-4" style="background:var(--info-bg);border:1px solid rgba(59,130,246,0.2);border-radius:var(--radius-2xl);width:100%;padding:20px;">
  <p style="color:var(--info);font-size:15px;margin:0;"><i class="bi bi-info-circle me-2"></i>AI analysis is pending. The contract was analyzed using rule-based detection only.</p>
</div>
{% endif %}

<hr style="border-color:var(--border-color);margin:24px 0;">

<div class="d-flex gap-3 flex-wrap">
  <a href="{% url 'upload' %}" class="btn btn-accent"><i class="bi bi-upload me-1"></i>Upload Another Contract</a>
  <button onclick="window.print()" class="btn btn-ghost"><i class="bi bi-printer me-1"></i>Print Report</button>
  <a href="{% url 'download_report' contract.id %}" class="btn" style="background:var(--success-bg);color:var(--success);border:none;padding:10px 24px;border-radius:var(--radius-full);font-weight:600;"><i class="bi bi-download me-1"></i>Download PDF</a>
  <a href="{% url 'contracts_list' %}" class="btn btn-ghost"><i class="bi bi-folder me-1"></i>All Contracts</a>
</div>

{% endblock %}
"""

filepath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'contracts', 'templates', 'contracts', 'result.html')
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print(f'Written {len(content)} chars to {filepath}')
