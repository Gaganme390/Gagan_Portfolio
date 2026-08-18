"""
RAG Engine for the Portfolio AI Assistant.
Uses TF-IDF based retrieval to find relevant portfolio content
and constructs context-aware responses without requiring external API keys.
"""
import re
import math
from collections import Counter
from core.models import Profile, Skill, Experience, Project, Certification, Education


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
                f"About Gagan Sahu: {profile.professional_summary} {profile.about_me}",
                "profile"
            )
            self._add_doc(
                f"Contact information: Email is {profile.email}. "
                f"Phone is {profile.phone}. LinkedIn is {profile.linkedin}. "
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
            skills_text = "Technical skills and technologies: "
            for cat, names in skills_by_cat.items():
                skills_text += f"{cat}: {', '.join(names)}. "
            self._add_doc(skills_text, "skills")

        # Experience
        for exp in Experience.objects.all():
            resp_text = ' '.join(exp.responsibilities) if exp.responsibilities else ''
            tech_text = ', '.join(exp.technologies) if exp.technologies else ''
            self._add_doc(
                f"Work experience: {exp.title} at {exp.company} in {exp.location}. "
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
                f"Project: {project.title}. {project.tagline}. Role: {project.role}. "
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
                "Certifications and awards: " + " ".join(cert_texts),
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
                "Education background: " + " ".join(edu_texts),
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
        """Generate a response using retrieved context."""
        query_lower = query.lower().strip()

        # Handle special commands
        if any(kw in query_lower for kw in ['download resume', 'download cv', 'get resume']):
            return {
                'text': "You can download Gagan's resume by clicking the button below!",
                'action': 'download_resume',
                'action_url': '/download-resume/'
            }

        if any(kw in query_lower for kw in ['contact', 'reach', 'email', 'hire']):
            profile = Profile.objects.first()
            if profile:
                return {
                    'text': (
                        f"You can reach Gagan through:\n\n"
                        f"📧 **Email:** {profile.email}\n"
                        f"🔗 **LinkedIn:** {profile.linkedin}\n"
                        f"📱 **Phone:** {profile.phone}\n\n"
                        f"Or use the contact form at the bottom of this page!"
                    ),
                    'action': None
                }

        # Retrieve relevant context
        results = self.retrieve(query, top_k=3)

        if not results:
            return {
                'text': (
                    "I don't have specific information about that. "
                    "Try asking about Gagan's projects, skills, experience, "
                    "certifications, or education!"
                ),
                'action': None
            }

        # Build response from context
        response = self._format_response(query_lower, results)
        return {'text': response, 'action': None}

    def _format_response(self, query, results):
        """Format a natural response from retrieved documents."""
        primary = results[0]
        label = primary['label']

        if label == 'profile':
            return self._format_profile_response(query)
        elif label == 'skills':
            return self._format_skills_response(query)
        elif label.startswith('project_'):
            slug = label.replace('project_', '')
            return self._format_project_response(slug)
        elif label.startswith('experience_'):
            return self._format_experience_response(query)
        elif label == 'certifications':
            return self._format_certifications_response()
        elif label == 'education':
            return self._format_education_response()
        elif label == 'contact':
            profile = Profile.objects.first()
            if profile:
                return (
                    f"📧 **Email:** {profile.email}\n"
                    f"🔗 **LinkedIn:** {profile.linkedin}\n"
                    f"📱 **Phone:** {profile.phone}\n"
                    f"📍 **Location:** {profile.location}"
                )

        # Fallback: return relevant excerpt
        return primary['text'][:500] + "..."

    def _format_profile_response(self, query):
        profile = Profile.objects.first()
        if not profile:
            return "Profile information is not available."
        if any(kw in query for kw in ['who is', 'tell me about', 'about']):
            return (
                f"**{profile.full_name}** is a {profile.title} based in {profile.location}.\n\n"
                f"{profile.professional_summary}\n\n"
                f"With **{profile.years_experience}+ years** of experience, "
                f"**{profile.projects_completed} projects** completed, and "
                f"**{profile.certifications_count} certifications** earned, "
                f"Gagan brings a unique blend of technical depth and practical expertise."
            )
        return profile.professional_summary

    def _format_skills_response(self, query):
        skills_by_cat = {}
        for skill in Skill.objects.filter(is_featured=True):
            cat = skill.get_category_display()
            if cat not in skills_by_cat:
                skills_by_cat[cat] = []
            skills_by_cat[cat].append(skill.name)

        # Check if asking about specific technology
        for cat, skills in skills_by_cat.items():
            for skill in skills:
                if skill.lower() in query:
                    projects = Project.objects.filter(
                        technologies__contains=[skill]
                    )
                    proj_names = [p.title for p in projects] if projects else []
                    response = f"Yes! Gagan is proficient in **{skill}** ({cat})."
                    if proj_names:
                        response += f"\n\nProjects using {skill}: {', '.join(proj_names)}"
                    return response

        response = "Here are Gagan's technical skills:\n\n"
        for cat, skills in skills_by_cat.items():
            response += f"**{cat}:** {', '.join(skills)}\n"
        return response

    def _format_project_response(self, slug):
        try:
            project = Project.objects.get(slug=slug)
        except Project.DoesNotExist:
            return "Project details are not available."

        tech_text = ', '.join(project.technologies) if project.technologies else 'N/A'
        response = (
            f"## {project.title}\n"
            f"*{project.tagline}*\n\n"
            f"**Role:** {project.role}\n\n"
            f"{project.overview}\n\n"
            f"**Technologies:** {tech_text}\n\n"
        )
        if project.lessons_learned:
            response += f"**Key Takeaways:** {project.lessons_learned[:200]}..."
        return response

    def _format_experience_response(self, query):
        experiences = Experience.objects.all()
        response = "Here's Gagan's professional experience:\n\n"
        for exp in experiences:
            tech_text = ', '.join(exp.technologies) if exp.technologies else ''
            response += (
                f"### {exp.title} at {exp.company}\n"
                f"📅 {exp.duration_display()} | 📍 {exp.location}\n\n"
                f"{exp.description}\n\n"
                f"**Tech Stack:** {tech_text}\n\n---\n\n"
            )
        return response

    def _format_certifications_response(self):
        certs = Certification.objects.all()
        response = "Here are Gagan's certifications:\n\n"
        for cert in certs:
            response += f"🏆 **{cert.name}** — {cert.issuer}\n"
        return response

    def _format_education_response(self):
        edus = Education.objects.all()
        response = "Here's Gagan's educational background:\n\n"
        for edu in edus:
            response += (
                f"🎓 **{edu.degree}**\n"
                f"   {edu.institution} — {edu.graduation_year} | GPA: {edu.gpa}\n\n"
            )
        return response


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
