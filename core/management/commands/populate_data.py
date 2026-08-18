from django.core.management.base import BaseCommand
from core.models import (
    Profile, Skill, Experience, Project,
    Certification, Education, SocialLink, SEOSettings
)
from datetime import date


class Command(BaseCommand):
    help = 'Populate the database with resume data for Gagan Sahu'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Populating portfolio data from resume...'))

        self._create_profile()
        self._create_skills()
        self._create_experience()
        self._create_projects()
        self._create_certifications()
        self._create_education()
        self._create_social_links()
        self._create_seo()

        self.stdout.write(self.style.SUCCESS('[OK] Portfolio data populated successfully!'))

    def _create_profile(self):
        Profile.objects.all().delete()
        Profile.objects.create(
            full_name="Gagan Sahu",
            title="Full Stack Web Developer",
            email="karanme390@gmail.com",
            phone="9074681763",
            linkedin="https://www.linkedin.com/in/gagan-sahu-0405a9354",
            github="https://github.com/Gaganme390",
            location="Bhilai, Chhattisgarh, India",
            hero_tagline="Crafting Digital Experiences That Leave a Mark",
            hero_subtitles="Full Stack Developer,MERN Stack Engineer,Cloud Architect,Django Developer,UI/UX Enthusiast,ServiceNow Specialist",
            professional_summary=(
                "A versatile Full Stack Web Developer who bridges the gap between elegant "
                "frontend experiences and robust backend architectures. Proficient in JavaScript, "
                "the MERN stack, Python, and Django — with hands-on expertise in cloud deployment "
                "on AWS, containerization with Docker, and enterprise workflow automation through "
                "ServiceNow. I don't just write code; I engineer solutions that scale, perform, "
                "and delight users."
            ),
            about_me=(
                "My journey into software engineering began with a curiosity that refused to be "
                "contained by textbooks. Armed with a background in Microbiology and a Post Graduate "
                "Diploma in Computer Applications, I made a deliberate pivot into technology — driven "
                "by the conviction that the most impactful solutions emerge at the intersection of "
                "diverse disciplines.\n\n"
                "At i-Connectresources International, I evolved from an IT Intern into a Web Developer, "
                "rapidly mastering the MERN stack while contributing to production-grade applications "
                "that serve real users. From building responsive React interfaces with pixel-perfect "
                "precision to architecting Django REST APIs that handle complex data pipelines, every "
                "project has sharpened my craft.\n\n"
                "What sets me apart is my full-spectrum approach to development. On the frontend, I "
                "create immersive user experiences with React.js, TypeScript, and Redux Toolkit — "
                "interfaces that feel alive and responsive. On the backend, I engineer scalable APIs "
                "with Django, Node.js, and Express, backed by PostgreSQL, MongoDB, and Elasticsearch "
                "for intelligent data retrieval.\n\n"
                "My passion extends beyond traditional web development. I've integrated AI-powered "
                "features like deep-learning stylometry models and vector databases for semantic search, "
                "containerized multi-service architectures with Docker, and deployed applications on AWS "
                "with production-grade security. I've also brought enterprise workflow automation to life "
                "through ServiceNow, earning multiple certifications along the way.\n\n"
                "I believe great software isn't just functional — it's an experience. Every line of code "
                "I write is guided by a commitment to performance optimization, clean architecture, and "
                "the relentless pursuit of user delight. Whether it's debugging a race condition at "
                "midnight or designing an analytics dashboard that makes complex data feel simple, I bring "
                "the same intensity and craftsmanship to every challenge."
            ),
            years_experience=2,
            projects_completed=6,
            certifications_count=7,
            resume_file="resume/Gagan_Sahu_Resume.pdf",
            meta_description=(
                "Gagan Sahu — Full Stack Web Developer specializing in MERN Stack, Django, "
                "AWS Cloud, and ServiceNow. Building scalable, performant digital experiences."
            ),
        )
        self.stdout.write(self.style.SUCCESS('  [OK] Profile created'))

    def _create_skills(self):
        Skill.objects.all().delete()
        skills_data = [
            # Frontend
            ('React.js', 'frontend', 90, '#61DAFB', 0),
            ('JavaScript', 'frontend', 88, '#F7DF1E', 1),
            ('TypeScript', 'frontend', 80, '#3178C6', 2),
            ('HTML5', 'frontend', 95, '#E34F26', 3),
            ('CSS3', 'frontend', 92, '#1572B6', 4),
            ('Tailwind CSS', 'frontend', 85, '#06B6D4', 5),
            ('Vite', 'frontend', 78, '#646CFF', 6),
            # Backend
            ('Python', 'backend', 85, '#3776AB', 0),
            ('Django', 'backend', 82, '#092E20', 1),
            ('Node.js', 'backend', 85, '#339933', 2),
            ('Express.js', 'backend', 82, '#000000', 3),
            ('PHP', 'backend', 65, '#777BB4', 4),
            # Databases
            ('MongoDB', 'database', 80, '#47A248', 0),
            ('PostgreSQL', 'database', 78, '#4169E1', 1),
            ('MySQL', 'database', 75, '#4479A1', 2),
            ('Elasticsearch', 'database', 70, '#005571', 3),
            # Cloud & DevOps
            ('Docker', 'cloud', 78, '#2496ED', 0),
            ('AWS', 'cloud', 75, '#FF9900', 1),
            ('Azure VM', 'cloud', 65, '#0078D4', 2),
            ('Git', 'cloud', 88, '#F05032', 3),
            # Enterprise
            ('ServiceNow', 'enterprise', 85, '#81B5A1', 0),
            ('SAP', 'enterprise', 55, '#0FAAFF', 1),
            ('Oracle ERP', 'enterprise', 50, '#F80000', 2),
            # State Management
            ('Redux Toolkit', 'state', 82, '#764ABC', 0),
        ]
        for name, category, proficiency, color, order in skills_data:
            Skill.objects.create(
                name=name,
                category=category,
                proficiency=proficiency,
                color=color,
                order=order,
                is_featured=True,
            )
        self.stdout.write(self.style.SUCCESS(f'  [OK] {len(skills_data)} skills created'))

    def _create_experience(self):
        Experience.objects.all().delete()
        Experience.objects.create(
            title="Web Developer",
            company="i-Connectresources International Pvt. Ltd.",
            location="Bhilai, Chhattisgarh",
            start_date=date(2025, 4, 1),
            end_date=None,
            is_current=True,
            description=(
                "Leading front-end development and driving backend integration initiatives "
                "at a dynamic IT consultancy. Spearheading cloud deployment strategies and "
                "enterprise workflow automation to deliver high-impact digital solutions."
            ),
            responsibilities=[
                "Architected and enhanced user interfaces using React.js and Tailwind CSS, "
                "delivering polished, performant user experiences across multiple client projects.",
                "Developed and maintained RESTful APIs with Node.js and Express.js, ensuring "
                "robust backend integration and seamless data flow.",
                "Led AWS cloud deployment initiatives, implementing secure and scalable hosting "
                "solutions with optimized CI/CD pipelines.",
                "Engineered ServiceNow IT workflow automations, reducing manual process overhead "
                "and streamlining internal operations.",
                "Championed debugging and performance optimization practices, establishing quality "
                "benchmarks for the development team."
            ],
            achievements=[
                "Successfully delivered multiple production-grade web applications.",
                "Improved application performance through systematic optimization.",
                "Automated critical IT workflows using ServiceNow platform."
            ],
            technologies=[
                "React.js", "Tailwind CSS", "Node.js", "Express.js",
                "AWS", "ServiceNow", "JavaScript", "Git"
            ],
            order=0,
        )
        Experience.objects.create(
            title="IT Intern",
            company="i-Connectresources International Pvt. Ltd.",
            location="Bhilai, Chhattisgarh",
            start_date=date(2024, 2, 1),
            end_date=date(2025, 4, 1),
            is_current=False,
            description=(
                "Built a strong foundation in full-stack development during an intensive "
                "internship, contributing to real-world MERN stack projects while gaining "
                "hands-on experience in cloud deployment and enterprise automation."
            ),
            responsibilities=[
                "Designed and implemented responsive front-end interfaces using React.js and "
                "Tailwind CSS, focusing on intuitive user experience design.",
                "Developed foundational backend skills through API development with Node.js "
                "and Express.js, contributing to production services.",
                "Assisted in deploying web applications on AWS, learning secure and scalable "
                "cloud hosting practices from senior engineers.",
                "Contributed to ServiceNow IT workflow automation projects, gaining hands-on "
                "experience with enterprise service management platforms.",
                "Focused on debugging methodologies and performance optimization techniques, "
                "improving application reliability and load times."
            ],
            achievements=[
                "Rapidly progressed from intern to developer role based on performance.",
                "Gained proficiency in the complete MERN stack within the first 6 months.",
                "Contributed to ServiceNow automation projects, earning platform certifications."
            ],
            technologies=[
                "React.js", "Tailwind CSS", "Node.js", "Express.js",
                "AWS", "ServiceNow", "MongoDB", "JavaScript"
            ],
            order=1,
        )
        self.stdout.write(self.style.SUCCESS('  [OK] 2 experience entries created'))

    def _create_projects(self):
        Project.objects.all().delete()

        Project.objects.create(
            title="VerityAI",
            slug="verityai",
            tagline="Academic Integrity Platform — AI-Powered Plagiarism & Authorship Detection",
            role="Full-Stack Developer",
            overview=(
                "VerityAI is a cutting-edge academic integrity platform engineered to combat "
                "plagiarism, AI-generated text, and ghostwriting in educational institutions. "
                "The platform provides a comprehensive suite of tools that empower faculty to "
                "maintain academic standards while giving students transparent feedback on their "
                "submissions. Built with a modern microservices architecture, VerityAI leverages "
                "deep learning stylometry models and vector databases to perform hybrid "
                "semantic-keyword searches with exceptional accuracy."
            ),
            problem_statement=(
                "Educational institutions worldwide face an escalating challenge: the rise of "
                "AI-generated content and sophisticated plagiarism techniques that traditional "
                "detection tools cannot identify. Faculty members need a platform that goes "
                "beyond simple text matching — one that understands writing patterns, detects "
                "AI authorship, and provides actionable insights with high confidence."
            ),
            features=[
                "Dual-portal architecture with dedicated Student and Faculty dashboards",
                "AI-powered plagiarism detection using deep-learning stylometry models",
                "Hybrid semantic-keyword search powered by pgvector and Elasticsearch",
                "Asynchronous processing pipeline for large-scale submission analysis",
                "Real-time progress tracking with WebSocket-based status updates",
                "Detailed originality reports with source attribution and confidence scores",
                "Bulk submission upload and batch processing capabilities",
                "Role-based access control with institutional SSO integration"
            ],
            challenges=[
                "Resolving complex API schema conflicts between frontend and backend services during rapid iteration cycles",
                "Optimizing SQL search performance for hybrid semantic-keyword queries across millions of document vectors",
                "Containerizing multiple interdependent services while maintaining development-production parity",
                "Implementing asynchronous task pipelines that gracefully handle failures and provide real-time progress feedback"
            ],
            technologies=[
                "React.js", "TypeScript", "Redux Toolkit", "Python", "Django",
                "Celery", "Redis", "PostgreSQL", "pgvector", "Docker",
                "REST APIs", "Deep Learning"
            ],
            architecture=(
                "VerityAI follows a containerized microservices architecture. The React/TypeScript "
                "frontend communicates with a Django REST Framework backend through versioned APIs. "
                "Document analysis is handled by an asynchronous pipeline using Celery workers and "
                "Redis as the message broker. PostgreSQL with the pgvector extension serves as the "
                "primary database, enabling efficient vector similarity searches alongside traditional "
                "relational queries. All services are containerized with Docker and orchestrated "
                "through Docker Compose."
            ),
            lessons_learned=(
                "Building VerityAI taught me the critical importance of designing APIs contract-first, "
                "especially in a team environment where frontend and backend evolve in parallel. I "
                "deepened my expertise in asynchronous architectures, learning how to design robust "
                "task pipelines that handle failures gracefully. The project also gave me hands-on "
                "experience with vector databases and semantic search — technologies that are "
                "reshaping how we interact with information."
            ),
            accent_color="#6C63FF",
            is_featured=True,
            order=1,
        )

        Project.objects.create(
            title="LearningOutcomeOS",
            slug="learningoutcomeos",
            tagline="K-12 Analytics Platform — Curriculum Mapping & Progress Automation",
            role="Full-Stack Developer",
            overview=(
                "LearningOutcomeOS is an enterprise-grade school management and analytics portal "
                "designed to transform how K-12 institutions track student progress and align "
                "curriculum with learning standards. The platform automates progress tracking, "
                "maps curriculum standards to learning outcomes, and provides administrators with "
                "powerful analytical dashboards to make data-driven decisions about educational "
                "program effectiveness."
            ),
            problem_statement=(
                "K-12 institutions struggle with fragmented data systems that make it nearly "
                "impossible to track whether curriculum delivery actually achieves intended learning "
                "outcomes. Teachers spend hours on manual reporting, administrators lack visibility "
                "into program-level trends, and there's no standardized way to map course content "
                "to educational standards across departments."
            ),
            features=[
                "Interactive analytical dashboards with Recharts for real-time data visualization",
                "Curriculum-to-standard mapping engine with drag-and-drop interface",
                "Automated progress tracking with customizable rubrics and grading scales",
                "Multi-tenant architecture supporting multiple schools and districts",
                "Safari-compatible date handling and cross-browser optimization",
                "Secure file upload with filtered validation and malware scanning",
                "Role-based dashboards for teachers, administrators, and district managers"
            ],
            challenges=[
                "Debugging Safari-specific date parsing issues that caused data corruption in progress timelines",
                "Resolving complex state synchronization bugs and race conditions in the Redux store",
                "Containerizing frontend, backend, and MySQL database modules to achieve development-production parity",
                "Implementing Django rate-limiters and security headers to meet enterprise security requirements"
            ],
            technologies=[
                "React 19", "Redux", "Recharts", "Django REST Framework",
                "MySQL", "Docker Compose", "Python", "JavaScript"
            ],
            architecture=(
                "LearningOutcomeOS uses a monolithic Django REST Framework backend serving a React 19 "
                "SPA frontend. The application is containerized using Docker Compose with separate "
                "containers for the frontend build server, Django backend, and MySQL database. State "
                "management is handled by Redux with carefully designed selectors to prevent unnecessary "
                "re-renders on data-heavy dashboard views."
            ),
            lessons_learned=(
                "This project was a masterclass in cross-browser compatibility and enterprise security. "
                "Debugging Safari-specific date parsing issues taught me to never trust browser-specific "
                "implementations for critical data operations. I also gained deep expertise in Docker Compose "
                "orchestration and learned how to implement Django security best practices including rate "
                "limiting, secure headers, and file upload validation."
            ),
            accent_color="#00C9A7",
            is_featured=True,
            order=2,
        )

        Project.objects.create(
            title="Intelligent HR Management",
            slug="intelligent-hr-management",
            tagline="ServiceNow Custom App — Enterprise HR Workflow Automation",
            role="ServiceNow Developer",
            overview=(
                "Intelligent HR Management is a custom-built enterprise application on the ServiceNow "
                "platform that revolutionizes human resources operations. The application automates "
                "critical HR workflows including employee onboarding, leave management, document "
                "lifecycle tracking, and compliance reporting — transforming manual, error-prone "
                "processes into streamlined digital workflows that save hundreds of person-hours annually."
            ),
            problem_statement=(
                "Enterprise HR departments often rely on disparate systems and manual processes for "
                "onboarding, leave management, and document tracking. This fragmentation leads to "
                "delayed onboarding, lost documents, compliance gaps, and frustrated employees. "
                "There was a need for a unified platform that automates these workflows while "
                "integrating with existing enterprise systems."
            ),
            features=[
                "Automated employee onboarding workflows with multi-stage approval chains",
                "Intelligent leave tracking with policy enforcement and calendar integration",
                "Document lifecycle management with automated retention and compliance rules",
                "Service Portal pages with intuitive self-service interfaces for employees",
                "Integration Hub spokes connecting ServiceNow with external HR and payroll systems",
                "Custom catalog items with dynamic forms and conditional logic",
                "Real-time dashboards for HR managers with KPI tracking"
            ],
            challenges=[
                "Designing complex multi-stage workflows that handle edge cases like partial approvals and escalations",
                "Building custom REST integrations to connect ServiceNow with legacy enterprise systems",
                "Creating responsive Service Portal pages that work across all devices and browsers",
                "Implementing role-based access control that satisfies enterprise security and compliance requirements"
            ],
            technologies=[
                "ServiceNow", "App Engine Studio", "Integration Hub",
                "Service Portal", "REST APIs", "Flow Designer",
                "JavaScript", "Glide API"
            ],
            architecture=(
                "Built entirely on the ServiceNow platform using App Engine Studio. The application "
                "leverages Flow Designer for workflow automation, Integration Hub for external system "
                "connectivity, and Service Portal for the user-facing interface. Custom REST integrations "
                "enable bi-directional data flow with external HR and payroll systems."
            ),
            lessons_learned=(
                "This project deepened my understanding of enterprise workflow design and the importance "
                "of handling edge cases in automated processes. I learned how to leverage the ServiceNow "
                "platform's capabilities including Flow Designer, Integration Hub, and App Engine Studio "
                "to build production-grade enterprise applications."
            ),
            accent_color="#FF6B6B",
            is_featured=True,
            order=3,
        )

        Project.objects.create(
            title="Oncology Healthcare Platform",
            slug="oncology-healthcare-platform",
            tagline="Clinical UI — Patient Timeline & Oncology Metrics Visualization",
            role="Frontend Developer",
            overview=(
                "The Oncology Healthcare Platform is a specialized clinical application designed to "
                "help healthcare professionals visualize and track critical patient data in oncology "
                "care. The platform provides intuitive, responsive interfaces for viewing patient "
                "timelines, treatment histories, and vital oncology metrics — enabling clinicians "
                "to make informed decisions quickly and confidently."
            ),
            problem_statement=(
                "Oncology healthcare teams work with vast amounts of complex patient data spread "
                "across multiple systems. Clinicians need a unified, intuitive interface that "
                "presents patient timelines and critical metrics at a glance — one that works "
                "flawlessly on both desktop workstations and mobile devices during rounds."
            ),
            features=[
                "Responsive clinical screens optimized for both desktop and mobile viewports",
                "Patient timeline visualization with treatment history and milestone tracking",
                "Critical oncology metrics dashboards with real-time data rendering",
                "Standardized layout system ensuring consistency across complex medical records",
                "Accessible design following healthcare UI/UX best practices",
                "Print-optimized views for clinical documentation"
            ],
            challenges=[
                "Rendering complex medical record layouts consistently across mobile and desktop viewports",
                "Designing intuitive visualizations for multi-dimensional oncology data without overwhelming clinicians",
                "Ensuring accessibility compliance for healthcare applications"
            ],
            technologies=[
                "React.js", "CSS3", "Responsive Design", "JavaScript",
                "Healthcare UI/UX", "Data Visualization"
            ],
            architecture=(
                "A React.js single-page application with a component-based architecture designed "
                "for healthcare data visualization. The frontend uses a standardized layout system "
                "with responsive breakpoints optimized for clinical workflows."
            ),
            lessons_learned=(
                "Working on healthcare software taught me the paramount importance of accessibility, "
                "data accuracy, and responsive design in high-stakes environments. I learned how to "
                "present complex multi-dimensional data in ways that support clinical decision-making "
                "rather than overwhelm practitioners."
            ),
            accent_color="#4ECDC4",
            is_featured=True,
            order=4,
        )

        Project.objects.create(
            title="Auction Product Dashboard",
            slug="auction-product-dashboard",
            tagline="Real-Time Bidding Dashboard — High-Performance State Management",
            role="Frontend Developer",
            overview=(
                "The Auction Product Dashboard is a high-performance real-time bidding interface "
                "designed for auction platforms. The dashboard handles rapid state updates from "
                "concurrent bidders while maintaining a smooth, responsive user experience — even "
                "under heavy load with thousands of simultaneous price updates."
            ),
            problem_statement=(
                "Real-time auction platforms face a unique challenge: the UI must reflect rapidly "
                "changing bid prices from hundreds of concurrent users without introducing latency "
                "or visual glitches. Traditional state management approaches create bottlenecks "
                "that result in stale prices, missed bids, and frustrated users."
            ),
            features=[
                "Real-time bidding interface with sub-second state updates",
                "High-performance rendering optimized for concurrent price changes",
                "Live bid history tracking with animated transitions",
                "Optimistic UI updates with server reconciliation",
                "Responsive dashboard layout for desktop and tablet use"
            ],
            challenges=[
                "Resolving latency issues in state updates during high-concurrency bidding scenarios",
                "Implementing optimistic UI patterns that gracefully handle server-side bid rejections",
                "Optimizing React render cycles to prevent jank during rapid data updates"
            ],
            technologies=[
                "React.js", "Redux", "WebSocket", "JavaScript",
                "Performance Optimization", "Real-Time Data"
            ],
            architecture=(
                "A React.js frontend with Redux for centralized state management, connected to "
                "a WebSocket server for real-time bid updates. The architecture uses memoized "
                "selectors and virtualized lists to maintain 60fps rendering during high-frequency "
                "data updates."
            ),
            lessons_learned=(
                "This project was an intensive exercise in performance optimization. I learned how "
                "to profile React applications, identify unnecessary re-renders, and implement "
                "strategies like memoization, virtualization, and optimistic updates to maintain "
                "smooth performance under extreme data throughput."
            ),
            accent_color="#FFD93D",
            is_featured=True,
            order=5,
        )
        Project.objects.create(
            title="G.D. Goenka School, Ayodhya",
            slug="gd-goenka-school-ayodhya",
            tagline="Where Heritage Inspires the Future — Premium CBSE Educational Platform & Campus",
            role="Lead Frontend & Creative UI/UX Developer",
            overview=(
                "The official digital web experience for G.D. Goenka Public School Ayodhya. "
                "Architected as a flagship educational platform blending heritage-inspired editorial "
                "design with futuristic interactive web technology. Built with React, Vite, Framer Motion, "
                "and GSAP, the platform features fluid scroll-driven animations, magnetic interactions, "
                "an interactive curriculum explorer, admissions workflows, and comprehensive school leadership showcases."
            ),
            problem_statement=(
                "Top-tier educational institutions need digital platforms that reflect world-class standards, "
                "convey institutional heritage, and engage prospective parents and students with smooth, interactive "
                "storytelling without sacrificing performance, SEO rankings, or mobile responsiveness."
            ),
            features=[
                "Smooth scroll-triggered timeline animations and parallax sections powered by GSAP",
                "Magnetic buttons, cursor micro-interactions, and fluid transitions using Framer Motion",
                "Admissions 2026-27 interactive inquiry portal and step-by-step application workflow",
                "Dedicated modules for CBSE Academics, STEM Innovation Labs, and Goenkan Leadership Academy",
                "Mobile-first responsive architecture with custom typography (DM Serif Display & Manrope)",
                "Sub-second page load times with Vite bundle optimization and Rolldown chunking",
                "Full SEO optimization with structured JSON-LD Schema markup for Google search visibility"
            ],
            challenges=[
                "Orchestrating multi-layered GSAP timeline animations alongside React component lifecycle for seamless 60fps rendering",
                "Ensuring high accessibility and readability across diverse screen sizes while maintaining sophisticated luxury design typography",
                "Optimizing dynamic visual assets and font loading to achieve near-perfect Core Web Vitals scores on Render"
            ],
            technologies=[
                "React 18", "Vite", "Framer Motion", "GSAP", "JavaScript (ES6+)",
                "Tailwind CSS", "Lucide Icons", "Rolldown", "HTML5", "Render"
            ],
            architecture=(
                "Constructed on a Vite-powered React Single-Page Application (SPA) architecture with modular component "
                "hierarchy. Employs Framer Motion for declarative UI state animations and GSAP ScrollTrigger for viewport "
                "timeline sequences, optimized with modern code-splitting and automated CI/CD on Render."
            ),
            lessons_learned=(
                "Mastered combining advanced imperative animation libraries with React state management, designing "
                "high-conversion institutional landing experiences, and fine-tuning Core Web Vitals for maximum performance."
            ),
            github_link="https://github.com/Gaganme390/Sparkle-World-Studio",
            demo_link="https://gd-goenka-ayodhya.onrender.com/",
            accent_color="#E5A93B",
            is_featured=True,
            order=0,
        )
        self.stdout.write(self.style.SUCCESS('  [OK] 6 projects created'))

    def _create_certifications(self):
        Certification.objects.all().delete()
        certs = [
            ("ServiceNow Certified System Administrator", "ServiceNow", "servicenow",
             "The gold-standard certification for ServiceNow platform administration, validating expertise in platform configuration, system management, and service delivery."),
            ("ServiceNow Micro-Certification: Service Portal", "ServiceNow", "servicenow",
             "Specialized certification in building and customizing ServiceNow Service Portal pages and widgets."),
            ("ServiceNow Micro-Certification: Integration Hub", "ServiceNow", "servicenow",
             "Certification validating expertise in connecting ServiceNow with external systems using Integration Hub spokes and REST APIs."),
            ("ServiceNow Micro-Certification: Automated Test Framework", "ServiceNow", "servicenow",
             "Certification in automated testing within the ServiceNow platform using ATF."),
            ("ServiceNow Micro-Certification: Predictive Intelligence", "ServiceNow", "servicenow",
             "Certification in leveraging ServiceNow's AI and machine learning capabilities for predictive analytics."),
            ("ServiceNow Micro-Certification: Flow Designer", "ServiceNow", "servicenow",
             "Certification in building automated workflows using ServiceNow Flow Designer."),
            ("Crash Course on Python", "Google (Coursera)", "programming",
             "Google's comprehensive Python programming certification covering fundamentals, data structures, and scripting."),
        ]
        for i, (name, issuer, category, desc) in enumerate(certs):
            Certification.objects.create(
                name=name,
                issuer=issuer,
                category=category,
                description=desc,
                date_earned=date(2024, 1, 1),
                order=i,
            )
        self.stdout.write(self.style.SUCCESS(f'  [OK] {len(certs)} certifications created'))

    def _create_education(self):
        Education.objects.all().delete()
        edu_data = [
            ("Post Graduate Diploma in Computer Applications", "Computer Applications",
             "Rungta College Of Science & Technology", 2023, "63%",
             "Advanced coursework in programming, database management, and software engineering."),
            ("Bachelor of Science in Microbiology", "Microbiology",
             "Rungta College Of Science & Technology", 2022, "77%",
             "Undergraduate degree with a strong foundation in analytical thinking and scientific methodology."),
            ("Higher Secondary (12th)", "Science",
             "Chhattisgarh Board of Secondary Education", 2018, "63%",
             "Completed higher secondary education with a focus on science subjects."),
            ("High School (10th)", "General",
             "Chhattisgarh Board of Secondary Education", 2016, "78%",
             "Completed high school education with strong academic performance."),
        ]
        for i, (degree, field, inst, year, gpa, desc) in enumerate(edu_data):
            Education.objects.create(
                degree=degree,
                field=field,
                institution=inst,
                graduation_year=year,
                gpa=gpa,
                description=desc,
                order=i,
            )
        self.stdout.write(self.style.SUCCESS(f'  [OK] {len(edu_data)} education entries created'))

    def _create_social_links(self):
        SocialLink.objects.all().delete()
        links = [
            ('linkedin', 'https://www.linkedin.com/in/gagan-sahu-0405a9354', 0),
            ('github', 'https://github.com/Gaganme390', 1),
            ('email', 'mailto:karanme390@gmail.com', 2),
        ]
        for platform, url, order in links:
            SocialLink.objects.create(platform=platform, url=url, order=order, is_visible=True)
        self.stdout.write(self.style.SUCCESS(f'  [OK] {len(links)} social links created'))

    def _create_seo(self):
        SEOSettings.objects.all().delete()
        seo_data = [
            ('home', 'Gagan Sahu — Full Stack Web Developer | MERN, Django, AWS',
             'Portfolio of Gagan Sahu, a Full Stack Web Developer specializing in MERN Stack, Django, AWS Cloud, and ServiceNow. Explore projects, skills, and experience.'),
            ('projects', 'Projects — Gagan Sahu Portfolio',
             'Explore featured projects by Gagan Sahu including VerityAI, LearningOutcomeOS, and enterprise applications.'),
        ]
        for page, title, desc in seo_data:
            SEOSettings.objects.create(page_name=page, title=title, meta_description=desc)
        self.stdout.write(self.style.SUCCESS('  [OK] SEO settings created'))
