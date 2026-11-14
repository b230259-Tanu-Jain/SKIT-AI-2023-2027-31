import subprocess
from collections import defaultdict
import datetime
import io
import os
import sys
import html
import re
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# -------------------------------------------------------------
# CONFIGURATION: Institution & Department Details
# -------------------------------------------------------------
COLLEGE_NAME = "Swami Keshvanand Institute of Technology,Management & Gramothan, Jaipur"
DEPARTMENT_NAME = "Department of Computer Science & Engineering"
# -------------------------------------------------------------
def get_repo_info():
    """Extracts the exact repository name and branch reliably in GitHub Codespaces."""
    repo_name = "Project-Repository"
    branch_name = "main"
    try:
        root_path = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], encoding='utf-8').strip()
        repo_name = os.path.basename(root_path)
    except Exception:
        try:
            remote_url = subprocess.check_output(['git', 'config', '--get', 'remote.origin.url'], encoding='utf-8').strip()
            repo_name = remote_url.rstrip('/').split('/')[-1].replace('.git', '')
        except Exception:
            repo_name = os.path.basename(os.getcwd())
    try:
        branch_name = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], encoding='utf-8').strip()
    except Exception:
        pass
    return repo_name, branch_name
def get_git_metrics(interval="weekly"):
    """
    Parses Git commit logs.
    Supported intervals: 'weekly', 'monthly', 'final'
    """
    today = datetime.date.today()
    git_args = ['git', 'log', '--no-merges', '--pretty=format:COMMIT|||%h|||%an|||%ad|||%s', '--date=short', '--numstat']
    
    if interval == "weekly":
        since_date = (today - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
        git_args.append(f"--since={since_date}")
        scope_title = f"Last 7 Days (Since {since_date})"
    elif interval == "monthly":
        since_date = (today - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
        git_args.append(f"--since={since_date}")
        scope_title = f"Last 30 Days (Since {since_date})"
    else:
        scope_title = "Complete Project Lifecycle (All Commits)"
    try:
        raw_output = subprocess.check_output(git_args, encoding='utf-8', errors='replace')
    except subprocess.CalledProcessError:
        print("[ERROR] Git command failed. Please ensure you are inside a Git repository.")
        return None, None, None, scope_title
    students = defaultdict(lambda: {"commits": 0, "added": 0, "deleted": 0, "active_days": set()})
    timeline_activity = defaultdict(lambda: defaultdict(int))
    student_logs = defaultdict(list)
    current_author = None
    current_date_str = None

    for line in raw_output.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('COMMIT|||'):
            parts = line.split('|||')
            if len(parts) >= 5:
                sha = parts[1].strip()
                author = parts[2].strip()
                date_str = parts[3].strip()
                msg = parts[4].strip()
            else:
                continue
                
            # --- IGNORE AUTOMATED BOTS ---
            if "bot" in author.lower() or "github-actions" in author.lower():
                current_author = None
                continue
            # -----------------------------
            
            current_author = author
            current_date_str = date_str
            
            students[current_author]["commits"] += 1
            students[current_author]["active_days"].add(current_date_str)
            student_logs[current_author].append((date_str, sha, msg))
            
            try:
                dt = datetime.datetime.strptime(current_date_str, "%Y-%m-%d").date()
                if interval == "weekly":
                    period_key = dt.strftime("%a (%b %d)")
                elif interval == "monthly":
                    period_key = f"{dt.isocalendar()[0]}-W{dt.isocalendar()[1]:02d}"
                else:
                    period_key = dt.strftime("%Y-%m")
                timeline_activity[period_key][current_author] += 1
            except Exception:
                pass

        elif current_author and not line.startswith('COMMIT|||'):
            parts = line.split()
            if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
                students[current_author]["added"] += int(parts[0])
                students[current_author]["deleted"] += int(parts[1])

    return students, timeline_activity, student_logs, scope_title

def create_charts(students, timeline_activity, interval):
    """Generates readable workload and trend charts."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.2))
    authors = list(students.keys())
    periods = sorted(timeline_activity.keys())

    def short_label(name, limit=20):
        return name if len(name) <= limit else name[:limit - 1] + "…"

    if periods and authors:
        for author in authors:
            counts = [timeline_activity[p].get(author, 0) for p in periods]
            ax1.plot(periods, counts, marker="o", linewidth=1.8,
                     label=short_label(author), markersize=3)
        ax1.set_title(f"Commit Timeline ({interval.capitalize()})",
                      fontsize=10, fontweight="bold", pad=9)
        ax1.set_ylabel("Commits", fontsize=8)
        ax1.tick_params(axis="x", labelrotation=35, labelsize=7)
        ax1.tick_params(axis="y", labelsize=7)
        ax1.grid(True, linestyle="--", alpha=0.4)
        ax1.legend(fontsize=6.5, loc="best", frameon=False)
    else:
        ax1.text(0.5, 0.5, "No commits found in this interval",
                 ha="center", va="center", transform=ax1.transAxes)
        ax1.set_axis_off()

    if authors:
        net_loc = [students[a]["added"] - students[a]["deleted"] for a in authors]
        labels = [short_label(a, 22) for a in authors]
        palette = ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F"]
        positions = list(range(len(authors)))
        bars = ax2.barh(positions, net_loc,
                        color=[palette[i % len(palette)] for i in positions],
                        height=0.58)
        ax2.set_yticks(positions)
        ax2.set_yticklabels(labels, fontsize=7)
        ax2.invert_yaxis()
        ax2.set_title("Net Lines of Code", fontsize=10, fontweight="bold", pad=9)
        ax2.set_xlabel("LOC (Added - Deleted)", fontsize=8)
        ax2.tick_params(axis="x", labelsize=7)
        ax2.grid(axis="x", linestyle="--", alpha=0.4)
        ax2.set_axisbelow(True)
        for bar, value in zip(bars, net_loc):
            offset = 3 if value >= 0 else -3
            alignment = "left" if value >= 0 else "right"
            ax2.annotate(f"{value:,}",
                         (value, bar.get_y() + bar.get_height() / 2),
                         xytext=(offset, 0), textcoords="offset points",
                         va="center", ha=alignment, fontsize=6.5)
    else:
        ax2.text(0.5, 0.5, "No LOC changes recorded",
                 ha="center", va="center", transform=ax2.transAxes)
        ax2.set_axis_off()

    fig.tight_layout(pad=1.5)
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format="png", dpi=220, bbox_inches="tight")
    plt.close(fig)
    img_buffer.seek(0)
    return Image(img_buffer, width=500, height=190)


def format_commit_message(message):
    """Convert simple Markdown emphasis and inline code to ReportLab markup."""
    escaped = html.escape(message or "(No commit message)")
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escaped)
    escaped = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', escaped)
    return escaped

def generate_pdf(interval="weekly"):
    repo_name, branch_name = get_repo_info()
    students, timeline_activity, student_logs, scope_title = get_git_metrics(interval)

    if students is None:
        return

    date_stamp = datetime.date.today().strftime("%Y-%m-%d")
    
    if interval == "weekly":
        report_title = "Weekly Progress Report (Form-3)"
        doc_name = f"{repo_name}_Weekly_Progress_Report_Form-3_{date_stamp}.pdf"
    elif interval == "monthly":
        report_title = "Monthly Progress Report (Form-3)"
        doc_name = f"{repo_name}_Monthly_Progress_Report_Form-3_{date_stamp}.pdf"
    else:
        report_title = "Final Project Evaluation Report"
        doc_name = f"{repo_name}_Final_Report_{date_stamp}.pdf"

    doc = SimpleDocTemplate(
        doc_name,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()
    
    college_style = ParagraphStyle(
        'CollegeStyle', parent=styles['Heading1'],
        fontSize=13.5, leading=17, textColor=colors.HexColor("#0F172A"), alignment=1, spaceAfter=2
    )
    dept_style = ParagraphStyle(
        'DeptStyle', parent=styles['Normal'],
        fontSize=9.5, leading=13, textColor=colors.HexColor("#475569"), alignment=1, spaceAfter=6
    )
    title_style = ParagraphStyle(
        'TitleStyle', parent=styles['Heading2'],
        fontSize=13, leading=17, textColor=colors.HexColor("#1A365D"), alignment=1, spaceAfter=5
    )
    repo_style = ParagraphStyle(
        'RepoStyle', parent=styles['Normal'],
        fontSize=9.5, leading=14, textColor=colors.HexColor("#0F172A"), spaceAfter=3
    )
    meta_style = ParagraphStyle(
        'MetaStyle', parent=styles['Normal'],
        fontSize=8.5, textColor=colors.HexColor("#64748B"), spaceAfter=8
    )
    section_style = ParagraphStyle(
        'SectionStyle', parent=styles['Heading2'],
        fontSize=10.5, leading=14, textColor=colors.HexColor("#0F172A"), spaceBefore=7, spaceAfter=4
    )
    sub_section_style = ParagraphStyle(
        'SubSectionStyle', parent=styles['Heading3'],
        fontSize=8.7, leading=10, textColor=colors.HexColor("#2563EB"),
        spaceBefore=2, spaceAfter=1, keepWithNext=0
    )
    msg_style = ParagraphStyle(
        'MsgStyle', parent=styles['Normal'],
        fontSize=7.6, leading=9.4, textColor=colors.HexColor("#1E293B"), wordWrap='CJK'
    )
    meta_cell_style = ParagraphStyle(
        'MetaCellStyle', parent=styles['Normal'],
        fontSize=8, leading=10, textColor=colors.HexColor("#475569"), alignment=1
    )
    marks_style = ParagraphStyle(
        'MarksStyle', parent=styles['Normal'],
        fontSize=9, leading=12, textColor=colors.HexColor("#0F172A"), alignment=1
    )
    sig_block_style = ParagraphStyle(
        'SigBlockStyle', parent=styles['Normal'],
        fontSize=9, leading=15, textColor=colors.HexColor("#0F172A"), alignment=0
    )

    story = []

    # 1. Header with College & Department Name and Form-3 Title
    story.append(Paragraph(f"<b>{html.escape(COLLEGE_NAME)}</b>", college_style))
    story.append(Paragraph(f"<b>{html.escape(DEPARTMENT_NAME)}</b>", dept_style))
    story.append(Paragraph(f"<u><b>{report_title}</b></u>", title_style))
    story.append(Spacer(1, 3))

    # 2. Metadata (Repo, Branch, Scope, Date)
    story.append(Paragraph(f"<b>Project Repository:</b> <font color='#2563EB'><b>{html.escape(repo_name)}</b></font> &nbsp;|&nbsp; <b>Branch:</b> <code>{html.escape(branch_name)}</code>", repo_style))
    story.append(Paragraph(f"<b>Evaluation Window:</b> {scope_title} &nbsp;|&nbsp; <b>Generated On:</b> {datetime.date.today().strftime('%B %d, %Y')}", meta_style))

    # 3. Individual Summary Table
    story.append(Paragraph("1. Individual Contribution Breakdown", section_style))
    total_commits = sum(data["commits"] for data in students.values())
    header_cell_style = ParagraphStyle(
        "SummaryHeader", parent=styles["Normal"], fontSize=7.2, leading=8.5,
        textColor=colors.whitesmoke, alignment=1, fontName="Helvetica-Bold"
    )
    summary_cell_style = ParagraphStyle(
        "SummaryCell", parent=styles["Normal"], fontSize=7.2, leading=8.8,
        textColor=colors.HexColor("#1E293B"), alignment=1, wordWrap="CJK"
    )
    table_data = [[
        Paragraph("Student Name", header_cell_style),
        Paragraph("Commits (%)", header_cell_style),
        Paragraph("Lines Added", header_cell_style),
        Paragraph("Lines Deleted", header_cell_style),
        Paragraph("Net LOC", header_cell_style),
        Paragraph("Active Days", header_cell_style)
    ]]

    if students:
        for name, data in students.items():
            pct = (data["commits"] / total_commits * 100) if total_commits > 0 else 0
            net = data["added"] - data["deleted"]
            values = [name, f"{data['commits']} ({pct:.1f}%)",
                      f"+{data['added']:,}", f"-{data['deleted']:,}",
                      f"{net:,}", f"{len(data['active_days'])} days"]
            table_data.append([
                Paragraph(html.escape(str(value)), summary_cell_style)
                for value in values
            ])
    else:
        table_data.append([
            Paragraph("No commits found in this period. Run with 'final' to see all commits.",
                      summary_cell_style), "-", "-", "-", "-", "-"
        ])

    table = Table(table_data, colWidths=[155, 75, 75, 75, 75, 85], repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E293B")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(table)
    story.append(Spacer(1, 6))

    # 4. Visual Charts
    story.append(Paragraph("2. Visual Trends & Volume", section_style))
    chart_image = create_charts(students, timeline_activity, interval)
    story.append(chart_image)
    story.append(Spacer(1, 6))

    # 5. Detailed Commit Logs per Student WITH Vertically Merged Mentor Marks
    story.append(Paragraph(f"3. Detailed Commit Logs & Mentor Evaluation ({interval.capitalize()})", section_style))
    if not student_logs:
        story.append(Paragraph("<i>No commit logs found for this timeframe.</i>", styles['Normal']))
    else:
        for student_name, logs in student_logs.items():
            student_section = []
            student_section.append(Paragraph(
                f"<b>Student:</b> {html.escape(student_name)} — <i>{len(logs)} commit(s)</i>",
                sub_section_style
            ))
            
            log_table_data = [["Date", "Hash", "Commit Message", "Mentor Marks (/10)"]]
            
            # Place the clean marking line in the first row
            first_date, first_sha, first_msg = logs[0]
            safe_msg = format_commit_message(first_msg)
            log_table_data.append([
                Paragraph(first_date, meta_cell_style),
                Paragraph(f"<code>{first_sha}</code>", meta_cell_style),
                Paragraph(safe_msg, msg_style),
                Paragraph("<b>_____ / 10</b>", marks_style)
            ])
            
            # Subsequent commit rows have blank placeholder for merged cell
            for date_val, sha_val, msg_val in logs[1:]:
                safe_msg = format_commit_message(msg_val)
                log_table_data.append([
                    Paragraph(date_val, meta_cell_style),
                    Paragraph(f"<code>{sha_val}</code>", meta_cell_style),
                    Paragraph(safe_msg, msg_style),
                    ""
                ])
            
            num_rows = len(log_table_data)
            log_table = Table(
                log_table_data,
                colWidths=[62, 48, 330, 100],
                repeatRows=1,
                splitByRow=1,
                splitInRow=1
            )
            
            t_style = [
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#475569")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (3, 0), (3, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 7.2),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 4),
                ('RIGHTPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ('ROWBACKGROUNDS', (0, 1), (2, -1), [colors.white, colors.HexColor("#F8FAFC")]),
                # Keep mentor marks in a normal cell so the table can split across pages.
                ('VALIGN', (3, 1), (3, -1), 'TOP'),
                ('BACKGROUND', (3, 1), (3, 1), colors.HexColor("#FEF3C7")),
                ('BACKGROUND', (3, 2), (3, -1), colors.white)
            ]
            
            log_table.setStyle(TableStyle(t_style))
            student_section.append(log_table)
            student_section.append(Spacer(1, 2))
            story.extend(student_section)  # Continue with the next student in any remaining page space.

    # 6. Symmetrical Signatures
    story.append(Spacer(1, 16))
    
    mentor_cell = [
        Paragraph("<b>Name:</b> ___________________________", sig_block_style),
        Paragraph("<b>Designation:</b> Project Mentor", sig_block_style),
        Spacer(1, 6),
        Paragraph("<b>Signature:</b> ________________________", sig_block_style),
    ]
    
    coordinator_cell = [
        Paragraph("<b>Name:</b> ___________________________", sig_block_style),
        Paragraph("<b>Designation:</b> Lab Coordinator", sig_block_style),
        Spacer(1, 6),
        Paragraph("<b>Signature:</b> ________________________", sig_block_style),
    ]

    sig_table = Table([[mentor_cell, coordinator_cell]], colWidths=[270, 270])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (0, -1), 0),
        ('LEFTPADDING', (1, 0), (1, -1), 40),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
    ]))
    
    story.append(KeepTogether(sig_table))

    doc.build(story)
    print(f"\n[SUCCESS] Generated: {doc_name}")
    print(f" -> Found {len(students)} student(s) and {total_commits} total commits.")

if __name__ == "__main__":
    chosen_interval = sys.argv[1].lower() if len(sys.argv) > 1 else "weekly"
    generate_pdf(chosen_interval)
