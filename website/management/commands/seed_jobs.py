
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model

from website.models import JobPosting


class Command(BaseCommand):
    help = "Seed 20 sample job postings across the USA"

    def handle(self, *args, **options):
        User = get_user_model()

        posted_by = (
            User.objects.filter(is_superuser=True).first()
            or User.objects.filter(is_staff=True).first()
        )

        today = timezone.localdate()

        jobs = [
            {
                "title": "Senior Python Developer",
                "department": "Engineering",
                "location": "Austin, TX, USA",
                "employment_type": "FULL_TIME",
                "experience": "4–7 years",
                "salary": "$120,000–$150,000 per year",
                "short_description": "Build scalable Python and Django applications for enterprise customers.",
                "description": "Join our engineering team to design, build, and maintain reliable web applications and backend services. You will collaborate with product managers, designers, and engineers to deliver secure and scalable software.",
                "requirements": "Strong Python and Django skills; REST APIs; PostgreSQL; Git; testing; application security; experience deploying production applications.",
                "responsibilities": "Design backend services; develop APIs; optimize database queries; write unit tests; review code; troubleshoot production issues; collaborate across teams.",
            },
            {
                "title": "DevOps Engineer",
                "department": "Cloud & Infrastructure",
                "location": "Dallas, TX, USA",
                "employment_type": "FULL_TIME",
                "experience": "3–6 years",
                "salary": "$110,000–$140,000 per year",
                "short_description": "Automate deployments and improve cloud infrastructure reliability.",
                "description": "Work with development and operations teams to build dependable deployment pipelines, automate infrastructure, and improve system observability across cloud environments.",
                "requirements": "Linux; Git; CI/CD; Docker; cloud platforms such as AWS or Azure; scripting with Python or Bash; infrastructure as code.",
                "responsibilities": "Maintain pipelines; automate infrastructure; monitor system health; manage deployments; improve reliability; document operational procedures.",
            },
            {
                "title": "Power Platform Developer",
                "department": "Business Applications",
                "location": "Houston, TX, USA",
                "employment_type": "FULL_TIME",
                "experience": "3–5 years",
                "salary": "$100,000–$130,000 per year",
                "short_description": "Develop business applications and automated workflows using Microsoft Power Platform.",
                "description": "Build business solutions that streamline operational processes using Power Apps, Power Automate, and Dataverse. Work with stakeholders to translate business needs into maintainable applications.",
                "requirements": "Power Apps; Power Automate; Power Fx; Dataverse; connectors; security roles; application lifecycle management.",
                "responsibilities": "Build canvas apps; develop cloud flows; integrate business systems; troubleshoot workflows; manage solutions; document technical designs.",
            },
            {
                "title": "Frontend React Developer",
                "department": "Product Engineering",
                "location": "San Antonio, TX, USA",
                "employment_type": "FULL_TIME",
                "experience": "2–5 years",
                "salary": "$95,000–$125,000 per year",
                "short_description": "Create responsive web experiences with React and modern JavaScript.",
                "description": "Develop accessible, responsive user interfaces for customer-facing products. Collaborate with designers and backend engineers to deliver consistent and performant experiences.",
                "requirements": "React; JavaScript or TypeScript; HTML; CSS; REST APIs; Git; responsive design; frontend testing.",
                "responsibilities": "Build reusable components; integrate APIs; improve performance; fix UI issues; write tests; collaborate on design implementation.",
            },
            {
                "title": "Data Analyst",
                "department": "Analytics",
                "location": "Fort Worth, TX, USA",
                "employment_type": "FULL_TIME",
                "experience": "2–4 years",
                "salary": "$75,000–$95,000 per year",
                "short_description": "Turn business data into reports, dashboards, and actionable insights.",
                "description": "Analyze business datasets and develop reports that help teams understand operational performance, identify trends, and make data-informed decisions.",
                "requirements": "SQL; Excel; Power BI or Tableau; data cleaning; visualization; analytical thinking; communication skills.",
                "responsibilities": "Prepare datasets; create dashboards; validate metrics; identify trends; document findings; present insights to stakeholders.",
            },
            {
                "title": "Cloud Solutions Architect",
                "department": "Cloud Engineering",
                "location": "Remote - United States",
                "employment_type": "REMOTE",
                "experience": "7–10 years",
                "salary": "$150,000–$185,000 per year",
                "short_description": "Design secure and scalable cloud architectures for distributed teams.",
                "description": "Lead cloud architecture initiatives for applications and data platforms. Evaluate technical options and develop architectures that balance security, scalability, reliability, and cost.",
                "requirements": "AWS or Azure architecture; networking; IAM; cloud security; infrastructure as code; disaster recovery; architecture documentation.",
                "responsibilities": "Design cloud solutions; review architectures; define standards; advise engineering teams; optimize costs; guide cloud migrations.",
            },
            {
                "title": "Full Stack Developer",
                "department": "Software Engineering",
                "location": "Remote - United States",
                "employment_type": "REMOTE",
                "experience": "3–5 years",
                "salary": "$105,000–$135,000 per year",
                "short_description": "Build end-to-end web applications with modern frontend and backend technologies.",
                "description": "Develop complete web application features from user interface to database. Work remotely with a cross-functional team to ship reliable, maintainable software.",
                "requirements": "React or Angular; Python, Java, or Node.js; REST APIs; SQL; Git; testing; application security.",
                "responsibilities": "Build frontend and backend features; implement APIs; maintain databases; review code; test releases; resolve defects.",
            },
            {
                "title": "Remote Technical Support Specialist",
                "department": "Customer Support",
                "location": "Remote - United States",
                "employment_type": "REMOTE",
                "experience": "1–3 years",
                "salary": "$55,000–$70,000 per year",
                "short_description": "Help customers troubleshoot software and technical issues remotely.",
                "description": "Provide responsive technical assistance to customers through digital support channels. Investigate reported issues and coordinate escalations with engineering when necessary.",
                "requirements": "Troubleshooting; customer communication; ticketing systems; basic networking; Windows; documentation skills.",
                "responsibilities": "Respond to tickets; diagnose issues; document resolutions; escalate complex incidents; maintain support knowledge articles.",
            },
            {
                "title": "Cybersecurity Analyst",
                "department": "Information Security",
                "location": "Remote - United States",
                "employment_type": "REMOTE",
                "experience": "2–5 years",
                "salary": "$95,000–$125,000 per year",
                "short_description": "Monitor security events and help protect enterprise systems and data.",
                "description": "Support security monitoring and incident response activities across enterprise systems. Investigate alerts, identify potential threats, and recommend practical security improvements.",
                "requirements": "Security monitoring; SIEM tools; networking; incident response; access controls; vulnerability management.",
                "responsibilities": "Review security alerts; investigate suspicious activity; document incidents; assist with vulnerability remediation; improve security procedures.",
            },
            {
                "title": "Digital Marketing Specialist",
                "department": "Marketing",
                "location": "Remote - United States",
                "employment_type": "REMOTE",
                "experience": "2–4 years",
                "salary": "$65,000–$85,000 per year",
                "short_description": "Manage digital campaigns, content performance, and marketing analytics.",
                "description": "Plan and optimize digital marketing campaigns across search, social, email, and content channels. Use analytics to measure performance and improve campaign outcomes.",
                "requirements": "SEO; digital advertising; analytics; content marketing; campaign reporting; written communication.",
                "responsibilities": "Plan campaigns; optimize content; track performance; prepare reports; coordinate creative work; recommend improvements.",
            },
            {
                "title": "Business Analyst",
                "department": "Business Operations",
                "location": "New York, NY, USA",
                "employment_type": "FULL_TIME",
                "experience": "3–5 years",
                "salary": "$90,000–$115,000 per year",
                "short_description": "Translate business needs into clear requirements and delivery plans.",
                "description": "Work with business stakeholders and technology teams to understand operational challenges, document requirements, and support delivery of process improvements.",
                "requirements": "Requirements gathering; process mapping; stakeholder management; SQL fundamentals; Agile; documentation.",
                "responsibilities": "Conduct discovery sessions; document requirements; maintain user stories; coordinate testing; track issues; communicate project progress.",
            },
            {
                "title": "Java Backend Developer",
                "department": "Engineering",
                "location": "Chicago, IL, USA",
                "employment_type": "FULL_TIME",
                "experience": "3–6 years",
                "salary": "$105,000–$135,000 per year",
                "short_description": "Develop reliable backend services using Java and Spring Boot.",
                "description": "Build and maintain backend components for business applications. Collaborate with engineers to improve service quality, database performance, and API reliability.",
                "requirements": "Java; Spring Boot; REST APIs; SQL; JUnit; Git; application security; debugging.",
                "responsibilities": "Develop backend features; maintain APIs; optimize queries; write tests; review code; troubleshoot application issues.",
            },
            {
                "title": "QA Automation Engineer",
                "department": "Quality Engineering",
                "location": "Denver, CO, USA",
                "employment_type": "FULL_TIME",
                "experience": "2–5 years",
                "salary": "$85,000–$110,000 per year",
                "short_description": "Build automated test suites to improve software quality and release confidence.",
                "description": "Develop and maintain automated tests for web applications and APIs. Partner with engineering teams to identify defects early and strengthen release processes.",
                "requirements": "Python or Java; Selenium or Playwright; API testing; test design; CI pipelines; Git.",
                "responsibilities": "Create test scripts; maintain automation frameworks; report defects; validate fixes; integrate tests into CI/CD; publish test results.",
            },
            {
                "title": "HR Operations Coordinator",
                "department": "Human Resources",
                "location": "Phoenix, AZ, USA",
                "employment_type": "FULL_TIME",
                "experience": "1–3 years",
                "salary": "$55,000–$68,000 per year",
                "short_description": "Support employee onboarding, HR records, and workforce operations.",
                "description": "Assist the HR team with employee lifecycle processes, onboarding coordination, records administration, and internal communications while maintaining confidentiality.",
                "requirements": "HR administration; organization; communication; spreadsheets; HR systems; confidentiality.",
                "responsibilities": "Coordinate onboarding; maintain records; schedule meetings; support HR reporting; answer routine employee questions.",
            },
            {
                "title": "Product Design Intern",
                "department": "Product Design",
                "location": "Austin, TX, USA",
                "employment_type": "INTERNSHIP",
                "experience": "Entry level / Students",
                "salary": "$25–$32 per hour",
                "short_description": "Support user research and UI/UX design for digital products.",
                "description": "Work alongside product designers to explore user needs, create interface concepts, and contribute to prototypes and design documentation.",
                "requirements": "Design portfolio; Figma fundamentals; user-centered design; communication; willingness to learn.",
                "responsibilities": "Assist with wireframes; create prototypes; support research; document design patterns; incorporate feedback.",
            },
            {
                "title": "Junior Software Developer",
                "department": "Engineering",
                "location": "Columbus, OH, USA",
                "employment_type": "INTERNSHIP",
                "experience": "Entry level / 0–1 years",
                "salary": "$24–$30 per hour",
                "short_description": "Gain hands-on experience building and testing software with an engineering team.",
                "description": "Contribute to supervised development tasks, bug fixes, testing, and documentation while learning professional software engineering practices.",
                "requirements": "Basic programming in Python, Java, or JavaScript; Git fundamentals; problem-solving; willingness to learn.",
                "responsibilities": "Implement small features; fix bugs; write tests; participate in code reviews; document changes; learn team workflows.",
            },
            {
                "title": "Freelance UX/UI Designer",
                "department": "Design",
                "location": "Remote - United States",
                "employment_type": "CONTRACT",
                "experience": "3–6 years",
                "salary": "$55–$85 per hour",
                "short_description": "Design polished web and mobile interfaces on a project basis.",
                "description": "Collaborate with product stakeholders to create user flows, wireframes, prototypes, and production-ready design specifications for digital products.",
                "requirements": "Figma; UI/UX design; responsive design; prototyping; design systems; portfolio demonstrating completed work.",
                "responsibilities": "Gather design requirements; develop concepts; create prototypes; present design options; incorporate feedback; deliver design assets.",
            },
            {
                "title": "IT Project Manager",
                "department": "Technology Operations",
                "location": "Seattle, WA, USA",
                "employment_type": "FULL_TIME",
                "experience": "5–8 years",
                "salary": "$115,000–$145,000 per year",
                "short_description": "Coordinate technology projects, delivery schedules, budgets, and stakeholders.",
                "description": "Lead cross-functional technology projects from planning through delivery. Coordinate teams, manage risks, communicate progress, and support successful project outcomes.",
                "requirements": "Project planning; Agile or hybrid delivery; risk management; stakeholder communication; project tracking tools.",
                "responsibilities": "Maintain project plans; coordinate teams; track milestones; manage risks; report status; facilitate delivery meetings.",
            },
            {
                "title": "Data Engineer",
                "department": "Data Platform",
                "location": "Remote - United States",
                "employment_type": "REMOTE",
                "experience": "3–6 years",
                "salary": "$115,000–$150,000 per year",
                "short_description": "Build data pipelines and dependable analytics infrastructure.",
                "description": "Design and maintain data pipelines that support reporting and analytics. Collaborate with analysts and engineers to improve data quality, availability, and performance.",
                "requirements": "SQL; Python; ETL/ELT; data modeling; cloud data services; orchestration; data quality practices.",
                "responsibilities": "Develop pipelines; validate data; optimize processing; monitor jobs; maintain documentation; support analytics users.",
            },
            {
                "title": "Customer Success Manager",
                "department": "Customer Success",
                "location": "Boston, MA, USA",
                "employment_type": "FULL_TIME",
                "experience": "3–5 years",
                "salary": "$85,000–$115,000 per year",
                "short_description": "Help customers achieve value from products through onboarding and ongoing support.",
                "description": "Build strong customer relationships, coordinate onboarding, track customer goals, and work with internal teams to resolve concerns and improve customer outcomes.",
                "requirements": "Customer relationship management; communication; account planning; problem-solving; CRM tools; presentation skills.",
                "responsibilities": "Lead onboarding; conduct customer reviews; track success metrics; coordinate issue resolution; identify retention risks; share customer feedback.",
            },
            {
                "title": "Part-Time Office Administrator",
                "department": "Administration",
                "location": "Plano, TX, USA",
                "employment_type": "PART_TIME",
                "experience": "1–3 years",
                "salary": "$22–$30 per hour",
                "short_description": "Provide part-time administrative support for office operations.",
                "description": "Support daily office activities, maintain records, coordinate meetings, and assist the team with administrative tasks in a professional office environment.",
                "requirements": "Organization; communication; Microsoft Office; record keeping; scheduling; attention to detail.",
                "responsibilities": "Coordinate calendars; maintain files; prepare documents; support meetings; manage routine office requests; assist with reporting.",
            },
        ]

        created_count = 0
        updated_count = 0

        for job_data in jobs:
            defaults = {
                **job_data,
                "is_active": True,
                "posted_by": posted_by,
                "deadline": today + timedelta(days=30),
            }

            job, created = JobPosting.objects.update_or_create(
                title=job_data["title"],
                location=job_data["location"],
                defaults=defaults,
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Created: {job.title}")
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f"Updated: {job.title}")
                )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Seeding complete. Created: {created_count}, "
                f"Updated: {updated_count}, Total seeded: {len(jobs)}"
            )
        )
