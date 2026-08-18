"""
RAG Engine for the Portfolio AI Assistant.
Uses rule-based semantic intent matching combined with TF-IDF retrieval
to provide accurate, contextual, and formatted answers about Gagan Sahu's portfolio.
"""
import re
import math
from collections import Counter
from core.models import Profile, Skill, Experience, Project, Certification, Education, SocialLink


class PortfolioRAG:
    """Retrieval-Augmented Generation engine for portfolio content."""

    def __init__(self):
        self.documents = []
        self.doc_labels = []
        self.idf = {}
        self.doc_tfs = []
        self._build_index()

    def _build_index(self):
        """Index all portfolio content into searchable documents."""
        self.documents = []
        self.doc_labels = []

        # Profile
        profile = Profile.objects.first()
        if profile:
            self._add_doc(
                f"About Gagan Sahu bio summary profile background: {profile.professional_summary} {profile.about_me}",
                "profile"
            )
            self._add_doc(
                f"Contact info email phone linkedin github location address: Email is {profile.email}. "
                f"Phone is {profile.phone}. LinkedIn is {profile.linkedin}. GitHub is {profile.github}. "
                f"Location is {profile.location}.",
                "contact"
            )

        # Skills
        skills_by_cat = {}
        for skill in Skill.objects.filter(is_featured=True):
            cat = skill.get_category_display()
            if cat not in skills_by_cat:
                skills_by_cat[cat] = []
            skills_by_cat[cat].append(skill.name)
        if skills_by_cat:
            skills_text = "Technical skills and technologies programming languages frameworks tools: "
            for cat, names in skills_by_cat.items():
                skills_text += f"{cat}: {', '.join(names)}. "
            self._add_doc(skills_text, "skills")

        # Experience
        for exp in Experience.objects.all():
            resp_text = ' '.join(exp.responsibilities) if exp.responsibilities else ''
            tech_text = ', '.join(exp.technologies) if exp.technologies else ''
            self._add_doc(
                f"Work experience employment job role company: {exp.title} at {exp.company} in {exp.location}. "
                f"Duration: {exp.duration_display()}. {exp.description} "
                f"Responsibilities: {resp_text} Technologies: {tech_text}",
                f"experience_{exp.id}"
            )

        # Projects
        for project in Project.objects.all():
            features_text = ' '.join(project.features) if project.features else ''
            challenges_text = ' '.join(project.challenges) if project.challenges else ''
            tech_text = ', '.join(project.technologies) if project.technologies else ''
            self._add_doc(
                f"Project portfolio application software: {project.title}. {project.tagline}. Role: {project.role}. "
                f"Overview: {project.overview} "
                f"Problem: {project.problem_statement} "
                f"Features: {features_text} "
                f"Challenges: {challenges_text} "
                f"Technologies: {tech_text} "
                f"Architecture: {project.architecture} "
                f"Lessons: {project.lessons_learned}",
                f"project_{project.slug}"
            )

        # Certifications
        cert_texts = []
        for cert in Certification.objects.all():
            cert_texts.append(f"{cert.name} by {cert.issuer}: {cert.description}")
        if cert_texts:
            self._add_doc(
                "Certifications awards credentials licenses ServiceNow Coursera: " + " ".join(cert_texts),
                "certifications"
            )

        # Education
        edu_texts = []
        for edu in Education.objects.all():
            edu_texts.append(
                f"{edu.degree} in {edu.field} from {edu.institution}, "
                f"graduated {edu.graduation_year}, GPA: {edu.gpa}"
            )
        if edu_texts:
            self._add_doc(
                "Education background degree college university qualification school academics: " + " ".join(edu_texts),
                "education"
            )

        # Build IDF
        self._compute_idf()

    def _add_doc(self, text, label):
        self.documents.append(text.lower())
        self.doc_labels.append(label)

    def _tokenize(self, text):
        return re.findall(r'\b[a-z0-9]+(?:\.[a-z0-9]+)*\b', text.lower())

    def _compute_idf(self):
        n = len(self.documents)
        if n == 0:
            return
        df = Counter()
        self.doc_tfs = []
        for doc in self.documents:
            tokens = self._tokenize(doc)
            tf = Counter(tokens)
            self.doc_tfs.append(tf)
            for token in set(tokens):
                df[token] += 1
        self.idf = {
            token: math.log((n + 1) / (count + 1)) + 1
            for token, count in df.items()
        }

    def _score_document(self, query_tokens, doc_tf):
        score = 0
        for token in query_tokens:
            if token in doc_tf:
                tf = 1 + math.log(doc_tf[token]) if doc_tf[token] > 0 else 0
                idf = self.idf.get(token, 1)
                score += tf * idf
        return score

    def retrieve(self, query, top_k=3):
        """Retrieve the most relevant documents for a query."""
        if not self.documents:
            self._build_index()
        query_tokens = self._tokenize(query)
        scores = []
        for i, doc_tf in enumerate(self.doc_tfs):
            score = self._score_document(query_tokens, doc_tf)
            scores.append((score, i))
        scores.sort(reverse=True)
        results = []
        for score, idx in scores[:top_k]:
            if score > 0:
                results.append({
                    'text': self.documents[idx],
                    'label': self.doc_labels[idx],
                    'score': score
                })
        return results

    def generate_response(self, query):
        """Generate an accurate response based on query intent & semantic context."""
        q = query.lower().strip()

        # 1. Greetings & Meta
        if q in ['hi', 'hello', 'hey', 'greetings', 'hola', 'namaste']:
            return {
                'text': (
                    "👋 Hello! I'm Gagan's AI Portfolio Assistant.\n\n"
                    "Feel free to ask me anything about:\n"
                    "• **Projects** he has built\n"
                    "• **Skills** & technologies (React, Django, Python, MERN, AWS, ServiceNow)\n"
                    "• **Work Experience** at i-Connectresources\n"
                    "• **Certifications** & Education\n"
                    "• **Contact details** or **Resume download**!"
                ),
                'action': None
            }

        # 2. Resume / CV Intent
        if any(kw in q for kw in ['resume', 'cv', 'curriculum vitae', 'download resume', 'get resume']):
            return {
                'text': (
                    "📄 You can view and download Gagan's complete resume in PDF format below:"
                ),
                'action': 'download_resume',
                'action_url': '/download-resume/'
            }

        # 3. Contact / Social Links Intent
        if any(kw in q for kw in ['contact', 'email', 'phone', 'call', 'number', 'reach', 'hire', 'linkedin', 'github', 'social', 'address', 'location', 'where is he']):
            profile = Profile.objects.first()
            if profile:
                response = f"📫 **Get in Touch with Gagan Sahu:**\n\n"
                if profile.email:
                    response += f"📧 **Email:** [{profile.email}](mailto:{profile.email})\n"
                if profile.linkedin:
                    response += f"💼 **LinkedIn:** [{profile.linkedin}]({profile.linkedin})\n"
                if profile.github:
                    response += f"💻 **GitHub:** [{profile.github}]({profile.github})\n"
                if profile.phone:
                    response += f"📱 **Phone:** {profile.phone}\n"
                if profile.location:
                    response += f"📍 **Location:** {profile.location}\n"
                response += "\nYou can also leave a direct message using the **Contact Form** below on the website!"
                return {'text': response, 'action': None}

        # 4. Specific Project Match
        projects = Project.objects.all()
        for p in projects:
            title_lower = p.title.lower()
            slug_lower = p.slug.lower()
            # Match project name or keywords
            match_keywords = [title_lower, slug_lower]
            if 'sparkle' in title_lower or 'goenka' in title_lower:
                match_keywords.extend(['sparkle', 'goenka', 'ayodhya'])
            if 'verity' in title_lower:
                match_keywords.append('verity')
            if 'learning' in title_lower:
                match_keywords.extend(['learningoutcome', 'outcomeos'])
            if 'auction' in title_lower:
                match_keywords.extend(['auction', 'bidding'])
            if 'oncology' in title_lower or 'cancer' in title_lower:
                match_keywords.extend(['oncology', 'cancer', 'healthcare'])
            if 'hr' in title_lower or 'management' in title_lower:
                match_keywords.extend(['hr management', 'human resource', 'intelligent hr'])

            if any(kw in q for kw in match_keywords if len(kw) > 2):
                return {'text': self._format_single_project(p), 'action': None}

        # 5. General Projects List Intent
        if any(kw in q for kw in ['project', 'projects', 'what has he built', 'what did he build', 'what did he make', 'built', 'created', 'portfolio works', 'applications', 'work done']):
            return {'text': self._format_all_projects(), 'action': None}

        # 6. Skills & Tech Stack Intent
        if any(kw in q for kw in ['skill', 'skills', 'technology', 'technologies', 'tech stack', 'languages', 'tools', 'frameworks', 'know', 'frontend', 'backend', 'database', 'cloud', 'devops', 'servicenow']):
            return {'text': self._format_skills_response(q), 'action': None}

        # 7. Experience / Work History Intent
        if any(kw in q for kw in ['experience', 'work', 'working', 'job', 'company', 'companies', 'intern', 'internship', 'career', 'i-connectresources', 'current role']):
            return {'text': self._format_experience_response(q), 'action': None}

        # 8. Certifications Intent
        if any(kw in q for kw in ['certification', 'certifications', 'certificate', 'certificates', 'certified', 'award', 'credential', 'license']):
            return {'text': self._format_certifications_response(), 'action': None}

        # 9. Education Intent
        if any(kw in q for kw in ['education', 'degree', 'college', 'university', 'school', 'academics', 'qualification', 'study', 'studied', 'microbiology', 'pgdca', 'rungta']):
            return {'text': self._format_education_response(), 'action': None}

        # 10. About / Bio Intent
        if any(kw in q for kw in ['who is', 'about', 'bio', 'background', 'summary', 'profile', 'introduce', 'overview', 'gagan sahu']):
            return {'text': self._format_profile_response(q), 'action': None}

        # 11. Fallback: RAG TF-IDF Retrieval
        results = self.retrieve(q, top_k=3)
        if not results or results[0]['score'] == 0:
            return {
                'text': (
                    "I'm not completely sure about that. Try asking about:\n"
                    "• **Projects** (e.g., *'Tell me about VerityAI'* or *'What projects has he worked on?'*)\n"
                    "• **Skills** (e.g., *'What backend technologies does he use?'*)\n"
                    "• **Experience** (e.g., *'Where does he work?'*)\n"
                    "• **Certifications** or **Education**"
                ),
                'action': None
            }

        response_text = self._format_retrieved_response(q, results)
        return {'text': response_text, 'action': None}

    def _format_all_projects(self):
        projects = Project.objects.all()
        if not projects.exists():
            return "No projects found in the portfolio."

        response = f"🚀 **Gagan has worked on {projects.count()} major projects:**\n\n"
        for p in projects:
            tech_str = ', '.join(p.technologies[:5]) if p.technologies else 'Various'
            response += f"### 🔹 **{p.title}**\n"
            if p.tagline:
                response += f"*{p.tagline}*\n"
            response += f"• **Overview:** {p.overview[:160]}...\n"
            response += f"• **Tech Stack:** `{tech_str}`\n"
            
            links = []
            if p.demo_link:
                links.append(f"[🌐 Live Demo]({p.demo_link})")
            if p.github_link:
                links.append(f"[💻 GitHub]({p.github_link})")
            links.append(f"[📄 Case Study](/project/{p.slug}/)")
            response += f"• **Links:** {' | '.join(links)}\n\n"

        response += "💡 *Tip: Ask me about any specific project (e.g., 'Tell me more about VerityAI' or 'Sparkle World Studio') for a deeper dive!*"
        return response

    def _format_single_project(self, project):
        tech_text = ', '.join(project.technologies) if project.technologies else 'N/A'
        response = (
            f"## 🚀 {project.title}\n"
            f"**{project.tagline}**\n\n"
            f"• **Role:** {project.role or 'Full Stack Developer'}\n"
            f"• **Technologies:** `{tech_text}`\n\n"
            f"### 📋 Overview\n{project.overview}\n\n"
        )
        if project.features:
            response += "### ✨ Key Features\n"
            for f in project.features[:5]:
                response += f"- {f}\n"
            response += "\n"

        if project.challenges:
            response += "### ⚡ Challenges & Solutions\n"
            for c in project.challenges[:3]:
                response += f"- {c}\n"
            response += "\n"

        links = []
        if project.demo_link:
            links.append(f"[🌐 Live Demo]({project.demo_link})")
        if project.github_link:
            links.append(f"[💻 GitHub Repository]({project.github_link})")
        links.append(f"[📄 Full Case Study](/project/{project.slug}/)")
        response += f"🔗 **Links:** {' | '.join(links)}"
        return response

    def _format_profile_response(self, query):
        profile = Profile.objects.first()
        if not profile:
            return "Profile information is not available."

        return (
            f"👨‍💻 **Gagan Sahu** — {profile.title}\n"
            f"📍 Based in {profile.location}\n\n"
            f"{profile.professional_summary}\n\n"
            f"📊 **Quick Highlights:**\n"
            f"• **Experience:** {profile.years_experience}+ years in Full-Stack & MERN development\n"
            f"• **Projects Completed:** {profile.projects_completed} production-grade applications\n"
            f"• **Certifications:** {profile.certifications_count} professional credentials (ServiceNow, Python)\n\n"
            f"Feel free to ask about his **skills**, **projects**, or **experience**!"
        )

    def _format_skills_response(self, query):
        skills_by_cat = {}
        all_skills = []
        for skill in Skill.objects.filter(is_featured=True):
            cat = skill.get_category_display()
            if cat not in skills_by_cat:
                skills_by_cat[cat] = []
            skills_by_cat[cat].append(skill.name)
            all_skills.append(skill.name)

        # Check if query asks about a specific skill
        for skill_name in all_skills:
            if skill_name.lower() in query:
                projects_matching = [
                    p.title for p in Project.objects.all()
                    if p.technologies and any(skill_name.lower() in t.lower() for t in p.technologies)
                ]
                reply = f"✅ **Yes! Gagan is proficient in {skill_name}.**\n\n"
                if projects_matching:
                    reply += f"He has used **{skill_name}** in the following projects:\n"
                    for p in projects_matching:
                        reply += f"• **{p}**\n"
                return reply

        # Otherwise, output all categorized skills
        response = "🛠️ **Gagan's Technical & Professional Skills:**\n\n"
        for cat, skills in skills_by_cat.items():
            response += f"• **{cat}:** {', '.join(skills)}\n"
        return response

    def _format_experience_response(self, query):
        experiences = Experience.objects.all()
        if not experiences.exists():
            return "Experience information is not available."

        response = "💼 **Gagan's Professional Experience:**\n\n"
        for exp in experiences:
            tech_text = ', '.join(exp.technologies) if exp.technologies else ''
            status = "(Current Role)" if exp.is_current else ""
            response += (
                f"### 🏢 **{exp.title}** {status}\n"
                f"**{exp.company}** | 📅 {exp.duration_display()} | 📍 {exp.location}\n\n"
                f"{exp.description}\n\n"
            )
            if exp.responsibilities:
                response += "**Key Responsibilities & Contributions:**\n"
                for r in exp.responsibilities[:4]:
                    response += f"• {r}\n"
                response += "\n"

            if tech_text:
                response += f"**Technologies:** `{tech_text}`\n\n---\n\n"
        return response

    def _format_certifications_response(self):
        certs = Certification.objects.all()
        if not certs.exists():
            return "Certification information is not available."

        response = f"🏆 **Gagan holds {certs.count()} Professional Certifications:**\n\n"
        for cert in certs:
            response += f"• **{cert.name}** — *{cert.issuer}*\n"
            if cert.description:
                response += f"  _{cert.description}_\n"
        return response

    def _format_education_response(self):
        edus = Education.objects.all()
        if not edus.exists():
            return "Education information is not available."

        response = "🎓 **Educational Background:**\n\n"
        for edu in edus:
            response += (
                f"• **{edu.degree}** ({edu.field})\n"
                f"  🏛️ {edu.institution} | 📅 Graduated {edu.graduation_year} | 📊 Score: {edu.gpa}\n\n"
            )
        return response

    def _format_retrieved_response(self, query, results):
        primary = results[0]
        label = primary['label']

        if label == 'profile':
            return self._format_profile_response(query)
        elif label == 'skills':
            return self._format_skills_response(query)
        elif label.startswith('project_'):
            slug = label.replace('project_', '')
            try:
                p = Project.objects.get(slug=slug)
                return self._format_single_project(p)
            except Project.DoesNotExist:
                pass
        elif label.startswith('experience_'):
            return self._format_experience_response(query)
        elif label == 'certifications':
            return self._format_certifications_response()
        elif label == 'education':
            return self._format_education_response()
        elif label == 'contact':
            return self._format_profile_response(query)

        return self._format_profile_response(query)


# Singleton instance
_rag_instance = None


def get_rag():
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = PortfolioRAG()
    return _rag_instance


def refresh_rag():
    global _rag_instance
    _rag_instance = PortfolioRAG()
