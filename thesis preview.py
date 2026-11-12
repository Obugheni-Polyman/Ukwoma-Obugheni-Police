from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak, Table, TableStyle, Flowable, KeepTogether

L = '/usr/share/fonts/truetype/liberation/'
for n, f in [('Serif', 'LiberationSerif-Regular'), ('Serif-B', 'LiberationSerif-Bold'), ('Serif-I', 'LiberationSerif-Italic'), ('Serif-BI', 'LiberationSerif-BoldItalic'), ('Sans', 'LiberationSans-Regular'), ('Sans-B', 'LiberationSans-Bold'), ('Sans-I', 'LiberationSans-Italic'), ('Sans-BI', 'LiberationSans-BoldItalic')]:
    pdfmetrics.registerFont(TTFont(n, L + f + '.ttf'))
pdfmetrics.registerFontFamily('Serif', normal='Serif', bold='Serif-B', italic='Serif-I', boldItalic='Serif-BI')
pdfmetrics.registerFontFamily('Sans', normal='Sans', bold='Sans-B', italic='Sans-I', boldItalic='Sans-BI')

NAVY = colors.HexColor('#0A2342'); GOLD = colors.HexColor('#D4AF37'); INK = colors.HexColor('#1c2420'); MUT = colors.HexColor('#5b6b62')
PALE = colors.HexColor('#F3F6FA'); CREAM = colors.HexColor('#FFF8E1'); LINE = colors.HexColor('#d9e0ea')
W, H = A4; M = 54
TITLE = 'A Psychological Study of the Impact of Cultural Barriers on Pastoral Counseling Effectiveness in Buguma City, Nigeria'
SITE = 'https://obugheni-polyman.com.ng/research.html'
WA = 'https://wa.me/2347035749180?text=I%20would%20like%20to%20buy%20the%20full%20thesis%20PDF'

def st(name, **k):
    base = dict(fontName='Serif', fontSize=11, leading=16, textColor=INK, spaceAfter=7)
    base.update(k); return ParagraphStyle(name, **base)
body = st('body', alignment=TA_JUSTIFY, fontSize=10.6, leading=14.8, spaceAfter=6)
small = st('small', fontSize=9.5, leading=13.5, textColor=MUT)
h1 = st('h1', fontName='Serif-B', fontSize=23, leading=28, textColor=NAVY, spaceAfter=4)
kick = st('kick', fontName='Sans-B', fontSize=8.5, leading=11, textColor=colors.HexColor('#8a6d00'), spaceAfter=3)
h2 = st('h2', fontName='Serif-B', fontSize=14, leading=18, textColor=NAVY, spaceBefore=8, spaceAfter=4)
bul = st('bul', leftIndent=14, bulletIndent=2, spaceAfter=3.5, fontSize=10.6, leading=14.6)
lbl = st('lbl', fontName='Sans-B', fontSize=9, leading=12, textColor=NAVY)

def head(kicker, title):
    return [Paragraph(kicker.upper(), kick), Paragraph(title, h1), Table([['']], colWidths=[46], rowHeights=[3], style=[('BACKGROUND', (0, 0), (-1, -1), GOLD)]), Spacer(1, 12)]

class TocLine(Flowable):
    def __init__(self, level, page, text):
        super().__init__(); self.level, self.page, self.text = level, page, text
        self.size = {'C': 11, 'F': 10, '1': 10, '2': 9.2, '3': 8.8}[level]
        self.font = 'Sans-B' if level == 'C' else 'Sans'
        self.indent = {'C': 0, 'F': 0, '1': 10, '2': 24, '3': 38}[level]
        self.pre = 9 if level == 'C' else 0
    def wrap(self, aw, ah):
        self.aw = aw; return aw, self.size + 5 + self.pre
    def draw(self):
        c = self.canv; y = 3
        c.setFont(self.font, self.size); c.setFillColor(NAVY if self.level == 'C' else INK)
        c.drawString(self.indent, y, self.text)
        c.drawRightString(self.aw, y, self.page)
        tw = c.stringWidth(self.text, self.font, self.size) + self.indent + 4; pw = c.stringWidth(self.page, self.font, self.size) + 4
        c.setStrokeColor(GOLD if self.level == 'C' else LINE); c.setDash(1, 2.5); c.setLineWidth(0.8)
        c.line(tw, y + 1.5, self.aw - pw, y + 1.5); c.setDash()

TOC = """F|ii|Declaration
F|iii|Certification
F|iv|Dedication
F|v|Abstract
F|xi|List of Tables
F|xiii|List of Figures
F|xiv|List of Abbreviations
C|1|Chapter One: Introduction
1|1|1.1 Background to the Study
1|2|1.2 Statement of the Problem
1|2|1.3 Aim and Objectives of the Study
2|2|1.3.1 Aim
2|3|1.3.2 Objectives
1|3|1.4 Research Questions
1|3|1.5 Research Hypotheses
1|4|1.6 Significance of the Study
1|4|1.7 Scope and Delimitation
2|4|1.7.1 Scope of the Study
2|5|1.7.2 Delimitation
1|5|1.8 Limitations of the Study
1|5|1.9 Operational Definition of Terms
C|8|Chapter Two: Review of Related Literature
1|8|2.0 Introduction
1|8|2.1 Historical Perspective on the Study
2|8|2.1.1 Pre-Colonial Helping Systems in Kalabari Society
2|9|2.1.2 The Missionary Encounter and the Introduction of Pastoral Counseling
2|9|2.1.3 The Rise of Pentecostalism and the Church as First Point of Call
2|9|2.1.4 Recent Institutional Responses and the Persisting Historical Gap
1|10|2.2 Theoretical Framework
2|10|2.2.1 Multicultural Counseling Theory (Sue & Sue, 2016)
2|11|2.2.2 African Psychology / Africentric Theory (Nwoye, 2017, 2021)
2|11|2.2.3 Social Cognitive Theory (Bandura, 1986)
2|12|2.2.4 Stigma Theory (Goffman, 1963; Corrigan & Watson, 2002)
2|12|2.2.5 Linking the Theories to the Study Variables
1|14|2.3 Theological Framework
2|14|2.3.1 Incarnational Theology
2|14|2.3.2 Holistic Salvation
2|15|2.3.3 Contextualization
1|15|2.4 Conceptual Framework
2|15|2.4.1 Key Concepts
2|16|2.4.2 Relationships Between Concepts
2|16|2.4.3 Conceptual Model Diagram
1|17|2.5 Conceptual Review
2|17|2.5.1 Concept of Culture
2|17|2.5.2 Concept of Pastoral Counseling
2|17|2.5.3 Concept of Cultural Barriers
2|18|2.5.4 Concept of Strategies to Mitigate Cultural Barriers
2|18|2.5.5 Concept of Pastoral Counseling Effectiveness
1|19|2.6 Current Trends in Culturally Responsive Pastoral Care
2|19|2.6.1 Decolonisation of Pastoral Care
2|19|2.6.2 Language and Localisation
2|19|2.6.3 Church-Community Collaboration
2|19|2.6.4 Mental Health Integration
1|20|2.7 Research Gaps
1|20|2.8 Chapter Summary
C|22|Chapter Three: Research Methodology
1|22|3.1 Introduction
1|22|3.2 Research Design
1|22|3.3 Location of the Study
1|23|3.4 Population of the Study
1|29|3.5 Sample Size and Sampling Technique
2|29|3.5.1 Sample Size: the Taro Yamane Computation
2|31|3.5.2 Sampling Technique
1|34|3.6 Research Instrument
1|36|3.7 Validity and Reliability of the Instrument
2|36|3.7.1 Validity
2|36|3.7.2 Reliability
2|36|3.7.3 Reliability Caveat
1|37|3.8 Data Collection, Procedure and Return Rate
2|37|3.8.1 Procedure
2|37|3.8.2 Explanation of the 100 Percent Return Rate
1|38|3.9 Data Analysis Techniques
1|38|3.10 Research Ethics
C|40|Chapter Four: Data Presentation and Analysis of Data
1|40|4.1 Introduction
1|40|4.2 Presentation of Findings
2|40|4.2.1 Demographical Presentation
1|48|4.3 Presentation and Interpretation of Analysis
2|48|4.3.1 Reliability
2|49|4.3.2 Tests of Normality
2|51|4.3.3 Validity Test
2|53|4.3.4 Descriptive Analysis and Answers to the Research Questions
3|53|4.3.4.1 Research Question One: cultural beliefs and practices
3|54|4.3.4.2 Research Question Two: cultural stigma
3|55|4.3.4.3 Research Question Three: preference for tradition
3|56|4.3.4.4 Research Question Four: language differences
3|56|4.3.4.5 Research Question Five: strategies for mitigating cultural barriers
3|57|4.3.4.6 Perceived Pastoral Counseling Effectiveness
3|58|4.3.4.7 Summary of the Research Questions
1|58|4.4 Spearman Rank Correlation and Multiple Linear Regression Results
2|58|4.4.1 Spearman Rank Correlation Results
2|61|4.4.2 Interpretation of the Multiple Regression Analysis
2|62|4.4.3 Testing Hypotheses Results
1|64|4.5 Supplementary Analyses
2|64|4.5.1 Sensitivity to the Two Low-Reliability Scales
2|64|4.5.2 Do Strategies Moderate the Effect of Barriers?
2|65|4.5.3 Differences by Respondent Characteristics
C|66|Chapter Five: Discussion of Findings
1|66|5.1 Introduction
1|66|5.2 Discussion of Findings by Objectives
2|66|5.2.1 Cultural Beliefs and Practices (Objective One)
2|66|5.2.2 Cultural Stigma (Objective Two)
2|66|5.2.3 Preference for Tradition (Objective Three)
2|67|5.2.4 Language Differences (Objective Four)
2|67|5.2.5 Strategies to Mitigate Cultural Barriers (Objective Five)
1|67|5.3 Combined Discussion of Correlation and Regression Findings
2|68|5.3.1 Findings in Relation to Theory
1|69|5.4 Comparison of Results with Previous Studies
1|71|5.5 Importance of the Findings
C|72|Chapter Six: Summary, Conclusion and Recommendations
1|72|6.0 Introduction
1|72|6.1 Summary of Findings
2|72|6.1.1 Summary of the Study
2|72|6.1.2 Key Findings
1|73|6.2 Conclusion
1|74|6.3 Recommendations
2|74|6.3.1 Recommendations for Action
2|75|6.3.2 Recommendations for Further Studies
1|75|6.4 Contributions to Knowledge
1|75|6.5 Limitations of the Study
C|77|References
C|80|Appendices
1|81|Appendix A: CBPCEQ Questionnaire
1|85|Appendix B: SPSS Variable View (Data Dictionary)
1|88|Appendix C: SPSS Output"""

def cover(c, d):
    c.saveState(); c.setFillColor(NAVY); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(colors.HexColor('#12335c')); c.circle(W - 40, H - 60, 210, fill=1, stroke=0)
    c.setFillColor(GOLD); c.rect(M, H - 118, 54, 4, fill=1, stroke=0)
    c.setFont('Sans-B', 10); c.setFillColor(GOLD); c.drawString(M, H - 100, 'FREE PREVIEW  ·  PHD THESIS')
    t = Paragraph(TITLE, ParagraphStyle('ct', fontName='Serif-B', fontSize=29, leading=36, textColor=colors.white))
    w, h = t.wrap(W - 2 * M, 400); t.drawOn(c, M, H - 160 - h)
    y = H - 160 - h - 34
    c.setFont('Serif-I', 14); c.setFillColor(colors.HexColor('#cfd7e6')); c.drawString(M, y, 'Doctor of Philosophy in Psychology and Biblical Counseling')
    c.setFillColor(GOLD); c.setFont('Serif-B', 20); c.drawString(M, y - 54, 'Ukwoma Obugheni Police')
    c.setFillColor(colors.white); c.setFont('Serif', 12)
    c.drawString(M, y - 76, 'Matriculation No. EIBCS2526P012')
    c.drawString(M, y - 94, 'El-Elyon International Bible College and Seminary, Abuja, Nigeria')
    c.drawString(M, y - 112, 'October 2026')
    c.setFillColor(GOLD); c.roundRect(M, 70, W - 2 * M, 74, 8, fill=1, stroke=0)
    c.setFillColor(NAVY); c.setFont('Sans-B', 11); c.drawString(M + 16, 122, 'This is a free preview. Read the full thesis:')
    c.setFont('Sans', 10.5); c.drawString(M + 16, 104, 'Six chapters, references and three appendices as a PDF.')
    c.setFont('Sans-B', 10.5); c.drawString(M + 16, 86, 'obugheni-polyman.com.ng/research.html')
    c.linkURL(SITE, (M, 70, W - M, 144), relative=0)
    c.restoreState()

def later(c, d):
    c.saveState(); c.setStrokeColor(GOLD); c.setLineWidth(1.2); c.line(M, 40, W - M, 40)
    c.setFont('Sans', 8); c.setFillColor(MUT)
    c.drawString(M, 28, 'Free preview  ·  Cultural Barriers and Pastoral Counseling Effectiveness in Buguma City, Nigeria')
    c.drawRightString(W - M, 28, 'Page %d' % d.page)
    c.setFillColor(GOLD); c.rect(0, H - 10, W, 10, fill=1, stroke=0); c.setFillColor(NAVY); c.rect(0, H - 10, W * 0.35, 10, fill=1, stroke=0)
    c.restoreState()

doc = BaseDocTemplate('/home/claude/thesis-preview.pdf', pagesize=A4, leftMargin=M, rightMargin=M, topMargin=M, bottomMargin=60,
                      title='Free Preview: ' + TITLE, author='Ukwoma Obugheni Police', subject='PhD thesis preview, Psychology and Biblical Counseling', keywords='pastoral counseling, cultural barriers, Kalabari, Buguma City, language, stigma, CBPCEQ')
fr = Frame(M, 60, W - 2 * M, H - M - 60, id='f', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
doc.addPageTemplates([PageTemplate(id='cover', frames=[fr], onPage=cover, autoNextPageTemplate='later'), PageTemplate(id='later', frames=[fr], onPage=later)])

def tile(num, label):
    return [Paragraph('<font name="Serif-B" size="24" color="#0A2342">%s</font>' % num, ParagraphStyle('t1', alignment=TA_CENTER, leading=28)), Paragraph('<font name="Sans" size="8.5" color="#5b6b62">%s</font>' % label, ParagraphStyle('t2', alignment=TA_CENTER, leading=11))]
tiles = Table([[tile('407', 'questionnaires returned'), tile('51', 'churches surveyed'), tile('38', 'questionnaire items'), tile('6', 'chapters + 3 appendices')]], colWidths=[(W - 2 * M) / 4] * 4)
tiles.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), CREAM), ('LINEABOVE', (0, 0), (-1, 0), 2.5, GOLD), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('TOPPADDING', (0, 0), (-1, -1), 9), ('BOTTOMPADDING', (0, 0), (-1, -1), 9), ('LINEAFTER', (0, 0), (-2, -1), 0.6, GOLD)]))

def B(t): return Paragraph(t, bul, bulletText='•')
story = [PageBreak()]
# --- page 2: at a glance
story += head('At a glance', 'What this study is about')
story += [Paragraph('This study examined how cultural barriers affect the effectiveness of pastoral counseling in <b>Buguma City</b>, headquarters of Asari-Toru Local Government Area, Rivers State, Nigeria. Buguma is a major Kalabari settlement of 39 Polo, where pastoral care works within a communal worldview shaped by belief in ancestral influence, respect for elders and the authority of the Amanyanabo and Council of Chiefs.', body), Spacer(1, 4), tiles, Spacer(1, 12)]
story += [Paragraph('What the study found', h2),
 B('<b>Language and stigma stood out.</b> Language differences (M = 4.12) and cultural stigma (M = 4.07) were the barriers most strongly endorsed. Preference for tradition (M = 3.63) followed, and cultural beliefs and practices (M = 3.21) was the weakest.'),
 B('<b>Counseling was rated effective</b> overall (M = 4.15), with at least 98.5% agreement on every item.'),
 B('<b>Respondents backed solutions.</b> Strategies to mitigate the barriers received the highest agreement (M = 4.24). Training pastors in Kalabari language and culture ranked first (M = 4.29).'),
 B('<b>Two predictors mattered most.</b> The regression model was significant, F(5, 401) = 10.95, p &lt; .001, R<super>2</super> = .120. Only language differences (&beta; = .20) and strategies (&beta; = .18) were independent predictors.'),
 B('<b>An honest caution.</b> Two scales had low reliability, so findings on those two constructs are less secure.')]
story += [Paragraph('What it recommends', h2),
 B('Kalabari language and cultural-competence training for pastors.'), B('Community psychoeducation to reduce stigma, and a guarantee of confidentiality.'), B('Culturally consistent involvement of family elders as partners.'), B('Referral networks between pastoral and clinical services.'), B('Combining biblical principles with cultural understanding.')]
des = [('Design', 'Descriptive cross-sectional correlational survey'), ('Setting', '51 PFN- and CAN-affiliated churches in Buguma City, Rivers State'), ('Population', 'About 5,000: 102 lead and assistant pastors and 4,898 adult members who had received counseling in the preceding 12 months'), ('Sample', '407: a census of all 102 pastors and 305 members chosen by proportionate stratified random selection'), ('Instrument', 'CBPCEQ questionnaire: 38 items, seven sections, 5-point scale'), ('Analysis', 'Frequencies, percentages, means, Pearson and Spearman correlations, multiple regression (0.05 level)')]
dt = Table([[Paragraph('<font name="Sans-B" size="8.5" color="#0A2342">%s</font>' % a, st('d1', spaceAfter=0, leading=12)), Paragraph('<font name="Sans" size="9.3" color="#1c2420">%s</font>' % b, st('d2', spaceAfter=0, leading=13))] for a, b in des], colWidths=[70, W - 2 * M - 70])
dt.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LINEBELOW', (0, 0), (-1, -1), 0.6, LINE), ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4), ('BACKGROUND', (0, 0), (0, -1), PALE)]))
story += [Paragraph('The study at a glance', h2), dt, PageBreak()]
# --- abstract
story += head('Abstract', 'The full abstract')
_body, body = body, st('abs', fontSize=9.9, leading=13.6, alignment=TA_JUSTIFY, spaceAfter=5)
story += [Paragraph('<font name="Sans-B" size="9" color="#0A2342">BACKGROUND AND THEORY</font>', st('x', spaceAfter=2)),
 Paragraph('This study examined the impact of cultural barriers on pastoral counseling effectiveness in Buguma City, headquarters of Asari-Toru Local Government Area, Rivers State, Nigeria. Buguma is a major Kalabari settlement of 39 Polo, where pastoral care operates within a communal worldview shaped by belief in ancestral influence and Owuamapu (water-deity worship), respect for elders, and the authority of the Amanyanabo and Council of Chiefs. The study was anchored on Multicultural Counseling Theory, African Psychology, Social Cognitive Theory and Stigma Theory. Each theory was linked to specific study variables: cultural beliefs and practices, cultural stigma, preference for tradition, language differences, and strategies to mitigate the barriers, with pastoral counseling effectiveness as the outcome.', body),
 Paragraph('<font name="Sans-B" size="9" color="#0A2342">METHOD</font>', st('x', spaceAfter=2)),
 Paragraph('A descriptive cross-sectional correlational survey was adopted. The estimated population was 5,000 (102 lead and assistant pastors and 4,898 adult members who had received counseling in the preceding 12 months) across 51 PFN- and CAN-affiliated churches. The Taro Yamane formula, n = N / [1 + N(e)<super>2</super>], with N = 5,000 and e = 0.05, gave 370.4, taken as 370; adding 10 percent (37) for anticipated non-response gave 407. Multi-stage sampling was used: all 51 churches identified by geo-mapping, a census of all 102 pastors, and proportionate stratified random selection of 305 members. The instrument was the researcher-developed Cultural Barriers and Pastoral Counseling Effectiveness Questionnaire (CBPCEQ), with 38 items in seven sections and a 5-point scale. All 407 questionnaires were returned complete (100% return rate) because they were administered face to face and collected on the spot; this describes returns among those who accepted a questionnaire, not a response rate among everyone approached. Data were analysed with frequencies, percentages, means, standard deviations, Pearson and Spearman correlations and multiple regression at the 0.05 level of significance.', body),
 Paragraph('<font name="Sans-B" size="9" color="#0A2342">FINDINGS</font>', st('x', spaceAfter=2)),
 Paragraph('All four cultural barriers were endorsed: language differences (M = 4.12, SD = 0.35), cultural stigma (M = 4.07, SD = 0.30), preference for tradition (M = 3.63, SD = 0.28) and cultural beliefs and practices (M = 3.21, SD = 0.27), the weakest. Pastoral counseling was rated effective (M = 4.15, SD = 0.29; at least 98.5% agreement on every item). Strategies to mitigate the barriers received the highest agreement (M = 4.24, SD = 0.40), with training pastors in Kalabari language and culture ranked first (M = 4.29). Correlations with effectiveness were small and positive: cultural beliefs and practices (r = .11, p = .030; &rho; = .09, p = .061), cultural stigma (r = .12, p = .013; &rho; = .09, p = .081), preference for tradition (r = .18; &rho; = .19; both p &lt; .001), language differences (r = .28; &rho; = .35; both p &lt; .001) and strategies (r = .24; &rho; = .34; both p &lt; .001). The regression model was significant, F(5, 401) = 10.95, p &lt; .001, R = .347, R<super>2</super> = .120, adjusted R<super>2</super> = .109, Durbin-Watson = 1.92, with no multicollinearity (tolerance .77 to .93; VIF 1.07 to 1.30). Only language differences (&beta; = .20, p &lt; .001) and strategies (&beta; = .18, p &lt; .001) were independent predictors.', body),
 Paragraph('<font name="Sans-B" size="9" color="#0A2342">INTERPRETATION, LIMITS AND RECOMMENDATIONS</font>', st('x', spaceAfter=2)),
 Paragraph('The positive direction of the relationships is opposite to the theoretical expectation that stronger barriers lower effectiveness. It is explained by the fact that every respondent had already received counseling, that scores clustered at the agreement end of the scale, and that agreement tendency or social desirability may have contributed. Two scales had low reliability (cultural beliefs and practices, &alpha; = .24; preference for tradition, &alpha; = .53), so findings on these two constructs are less secure; a sensitivity analysis with shortened scales left the main conclusions unchanged. The study recommends: (1) Kalabari language and cultural-competence training for pastors; (2) community psychoeducation to reduce stigma and a guarantee of confidentiality; (3) culturally consistent involvement of family elders as partners; (4) referral networks between pastoral and clinical services; and (5) combining biblical principles with cultural understanding.', body),
 Table([[Paragraph('<font name="Sans-B" size="9" color="#0A2342">KEYWORDS</font><br/><font name="Serif-I" size="10.5">Cultural barriers, pastoral counseling effectiveness, Kalabari, language barrier, stigma, Buguma City, CBPCEQ, pastoral training</font>', st('kw', leading=15, spaceAfter=0))]], colWidths=[W - 2 * M], style=[('BACKGROUND', (0, 0), (-1, -1), PALE), ('LINEBEFORE', (0, 0), (0, -1), 3, GOLD), ('TOPPADDING', (0, 0), (-1, -1), 9), ('BOTTOMPADDING', (0, 0), (-1, -1), 9), ('LEFTPADDING', (0, 0), (-1, -1), 12)]), PageBreak()]
body = _body
# --- contents
story += head('Table of contents', 'Everything in the full thesis')
story += [Paragraph('Page numbers refer to the full thesis.', small), Spacer(1, 4)]
for line in TOC.split('\n'):
    lv, pg, tx = line.split('|', 2); story.append(TocLine(lv, pg, tx))
story += [PageBreak()]
# --- inside
story += head('Inside the full thesis', 'Six chapters, references and three appendices')
chap = [('1', 'Introduction', 'Background, statement of the problem, aim and objectives, research questions, hypotheses, scope and key definitions.'),
 ('2', 'Review of related literature', 'The history of helping in Kalabari society, from pre-colonial systems through the missionary encounter to the rise of Pentecostalism; the four theories and the theological framework; the conceptual framework; current trends in culturally responsive pastoral care; and the research gaps.'),
 ('3', 'Research methodology', 'Design, location, population, the Taro Yamane sample size and sampling technique, the CBPCEQ instrument, validity and reliability, data collection, analysis and research ethics.'),
 ('4', 'Data presentation and analysis', 'Who responded, reliability, normality and validity tests, answers to all five research questions, correlation and regression results, hypothesis tests and supplementary analyses.'),
 ('5', 'Discussion of findings', 'Findings by objective, a combined reading of the correlation and regression results, links to theory and comparison with previous studies.'),
 ('6', 'Summary, conclusion and recommendations', 'Key findings, conclusion, recommendations for action and further study, contributions to knowledge and limitations.'),
 ('+', 'References and appendices', 'The reference list, the full CBPCEQ questionnaire, the SPSS data dictionary and the SPSS output.')]
rows = [[Paragraph('<font name="Serif-B" size="22" color="#D4AF37">%s</font>' % n, ParagraphStyle('n', alignment=TA_CENTER, leading=26)), [Paragraph('<font name="Serif-B" size="12.5" color="#0A2342">%s</font>' % t, st('ct2', leading=16, spaceAfter=2)), Paragraph('<font name="Sans" size="9.3" color="#33415c">%s</font>' % d, st('cd', leading=13.5, spaceAfter=0))]] for n, t, d in chap]
ct = Table(rows, colWidths=[40, W - 2 * M - 40]); ct.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LINEBELOW', (0, 0), (-1, -2), 0.6, LINE), ('TOPPADDING', (0, 0), (-1, -1), 9), ('BOTTOMPADDING', (0, 0), (-1, -1), 9), ('BACKGROUND', (0, 0), (0, -1), NAVY)]))
ct.setStyle(TableStyle([('TEXTCOLOR', (0, 0), (0, -1), colors.white)]))
story += [ct, Spacer(1, 16)]
story += [Paragraph('Who will find it useful', h2), Paragraph('Pastors and church counselors, church leaders, seminary and counseling students, researchers in psychology and theology, and organizations that work with faith communities in Nigeria and elsewhere.', body), Spacer(1, 6)]
story += [PageBreak()]
story += head('Continue reading', 'Get the full thesis')
story += [Paragraph('You have read the abstract and seen the full contents. The complete thesis is sold as a PDF with <b>six chapters, the reference list and three appendices</b>: the full CBPCEQ questionnaire, the SPSS data dictionary and the SPSS output.', body), Spacer(1, 4)]
steps = [('1', 'Open the research page', 'Go to obugheni-polyman.com.ng/research.html and choose how you would like to order.'), ('2', 'Pay securely', 'You see the exact amount on the payment page before you confirm.'), ('3', 'Receive your access', 'Your access is sent straight after payment. Message us on WhatsApp if anything is missing.')]
sr = [[Paragraph('<font name="Serif-B" size="20" color="#D4AF37">%s</font>' % n, ParagraphStyle('sn', alignment=TA_CENTER, leading=24)), [Paragraph('<font name="Serif-B" size="12" color="#0A2342">%s</font>' % t, st('s1', spaceAfter=1, leading=15)), Paragraph('<font name="Sans" size="9.5" color="#33415c">%s</font>' % d, st('s2', spaceAfter=0, leading=13.5))]] for n, t, d in steps]
stt = Table(sr, colWidths=[40, W - 2 * M - 40]); stt.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('BACKGROUND', (0, 0), (0, -1), NAVY), ('LINEBELOW', (0, 0), (-1, -2), 0.6, LINE), ('TOPPADDING', (0, 0), (-1, -1), 9), ('BOTTOMPADDING', (0, 0), (-1, -1), 9)]))
story += [stt, Spacer(1, 16)]
cta = Table([[[Paragraph('<font name="Sans-B" size="10.5" color="#0A2342"><link href="%s" color="#0b5cad">Open the research page: obugheni-polyman.com.ng/research.html</link></font>' % SITE, st('c3', spaceAfter=5)),
   Paragraph('<font name="Sans-B" size="10.5" color="#0A2342"><link href="%s" color="#0b5cad">Order on WhatsApp: +234 703 574 9180</link></font>' % WA, st('c4', spaceAfter=5)),
   Paragraph('<font name="Sans" size="8.5" color="#5b6b62">For personal and academic use and citation only. Please do not resell or share the file.</font>', st('c5', spaceAfter=0, leading=12))]]], colWidths=[W - 2 * M])
cta.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), CREAM), ('BOX', (0, 0), (-1, -1), 1.2, GOLD), ('TOPPADDING', (0, 0), (-1, -1), 14), ('BOTTOMPADDING', (0, 0), (-1, -1), 14), ('LEFTPADDING', (0, 0), (-1, -1), 16), ('RIGHTPADDING', (0, 0), (-1, -1), 16)]))
story += [cta, Paragraph('How to cite', h2), Paragraph('Ukwoma, O. P. (2026). <i>%s</i>. PhD thesis, El-Elyon International Bible College and Seminary, Abuja.' % TITLE, small), Paragraph('About the publisher', h2), Paragraph('Obugheni-Polyman Consulting Services is a CAC registered micro enterprise (BN 9903940) based in Abua/Odual, Rivers State, Nigeria, offering consulting, research, special education and training. Email: InfoOPCww@obugheni-polyman.com.ng', small)]
doc.build(story)
print('built')
