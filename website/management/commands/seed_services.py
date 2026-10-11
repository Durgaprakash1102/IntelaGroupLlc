
from django.core.management.base import BaseCommand
from django.db import transaction

from website.models import Service


SERVICES = [
    {
        "title": "Application Development",
        "short_description": "Custom applications designed around your business requirements and workflows.",
        "description": """
Application Development

Application development is one of the key services where we focus on delivering a positive business impact without unnecessary impediments or delays. We improve application performance, reliability, and quality by following established Software Development Life Cycle (SDLC) practices. Our development approach adapts to the scale, complexity, and objectives of each project.

We develop customizable applications and components for a variety of business needs, including custom application development, mobile applications, database applications, and enterprise application solutions. Our team works closely with clients to understand their requirements and translate them into practical, maintainable software solutions.

We also incorporate DevOps practices where appropriate to improve collaboration between development and operations teams. Our aim is to shorten development cycles, enable continuous delivery, improve software quality, and provide solutions that align with each client's business goals.
        """.strip(),
        "is_active": True,
    },
    {
        "title": "Software Development",
        "short_description": "Software solutions focused on usability, flexibility, and business needs.",
        "description": """
Software Development

Intela Group provides software development services designed to address business challenges and support organizational growth. We work with clients to understand their objectives, existing processes, and technical requirements before designing and implementing suitable software solutions.

Our development process covers requirement analysis, solution design, implementation, testing, deployment, and ongoing improvements. We emphasize readable code, maintainable architecture, usability, performance, and security throughout the development lifecycle.

By following appropriate development methodologies and quality practices, we help businesses build software that can adapt to changing requirements. Our goal is to deliver dependable solutions that improve operational efficiency and provide long-term business value.
        """.strip(),
        "is_active": True,
    },
    {
        "title": "Artificial Intelligence Solutions",
        "short_description": "AI-powered solutions to streamline business operations and support decisions.",
        "description": """
Artificial Intelligence Solutions

Artificial intelligence can help organizations process information, identify patterns, and improve the way everyday business activities are performed. Intela Group develops AI-enabled solutions based on specific business objectives, available data, and operational requirements.

Our approach begins with identifying suitable use cases, evaluating data readiness, and determining where AI can provide measurable value. Depending on the project, solutions may include intelligent document processing, text analysis, classification, recommendations, forecasting, and decision-support capabilities.

We focus on practical implementation, responsible use, and integration with existing business systems. Our goal is to help organizations reduce repetitive effort, improve access to information, and make more informed decisions while maintaining appropriate human oversight.
        """.strip(),
        "is_active": True,
    },
    {
        "title": "Generative AI & LLM Development",
        "short_description": "Generative AI applications using large language models and business data.",
        "description": """
Generative AI & LLM Development

Generative AI and large language models create opportunities to improve how businesses interact with information, create content, and complete knowledge-intensive tasks. Intela Group helps organizations explore and implement generative AI applications that address clearly defined business needs.

Our services can include LLM-powered chat applications, document question-answering systems, content assistance, knowledge retrieval, summarization, and workflow support. Where appropriate, we can connect language models with approved business documents, internal knowledge sources, and existing applications.

We consider accuracy, privacy, security, response quality, and operational cost when designing these solutions. Through evaluation, testing, and iterative improvement, we aim to develop useful AI applications that complement employees' work and fit into existing business processes.
        """.strip(),
        "is_active": True,
    },
    {
        "title": "AI Agents & Copilots",
        "short_description": "AI assistants that support users with information and defined business tasks.",
        "description": """
AI Agents & Copilots

AI agents and copilots can help employees access information, navigate business processes, and complete defined tasks through conversational interfaces. Intela Group designs assistant experiences around the workflows, knowledge sources, and operational boundaries of each organization.

Depending on the use case, an assistant may answer questions, retrieve approved information, summarize documents, guide users through procedures, or invoke authorized tools and APIs. We define the tasks an agent can perform, the information it can access, and the situations that require human review or approval.

Our implementation approach emphasizes usefulness, controlled access, testing, monitoring, and clear escalation paths. The objective is to provide practical AI assistance that supports productivity while respecting business rules and security requirements.
        """.strip(),
        "is_active": True,
    },
    {
        "title": "Machine Learning & Predictive Analytics",
        "short_description": "Data-driven models that identify patterns and help forecast outcomes.",
        "description": """
Machine Learning & Predictive Analytics

Machine learning helps organizations discover patterns in historical data and use those patterns to estimate possible future outcomes. Intela Group supports the development of predictive solutions tailored to relevant business questions and available datasets.

Our work can include data preparation, feature engineering, model selection, training, evaluation, and deployment planning. Depending on the requirements, applications may involve forecasting, classification, anomaly detection, customer analysis, demand estimation, or risk assessment.

We evaluate model performance against appropriate metrics and consider data quality, potential bias, and limitations when interpreting results. Our goal is to provide useful analytical capabilities that complement business expertise and support better-informed planning and decision-making.
        """.strip(),
        "is_active": True,
    },
    {
        "title": "Intelligent Process Automation",
        "short_description": "Workflow automation combining business rules, APIs, and AI where appropriate.",
        "description": """
Intelligent Process Automation

Intelligent process automation combines workflow orchestration, business rules, system integrations, and selected AI capabilities to reduce repetitive manual work. Intela Group helps organizations identify processes that can be streamlined through reliable, well-defined automation.

Solutions may include document handling, data extraction, application updates, approval workflows, scheduled processing, and integration between business systems. We assess process steps, exceptions, dependencies, and validation requirements before selecting suitable automation technologies.

We emphasize error handling, auditability, security, and operational visibility. By automating appropriate activities while retaining human oversight for exceptions and sensitive decisions, organizations can improve consistency, reduce processing effort, and make their operations more efficient.
        """.strip(),
        "is_active": True,
    },
    {
        "title": "Mobile Application Development",
        "short_description": "Mobile experiences designed for customer and employee needs.",
        "description": """
Mobile Application Development

Mobile applications give customers and employees convenient access to services, information, and business workflows. Intela Group develops mobile application solutions based on the intended audience, platform requirements, user experience, and business objectives.

Our process includes requirements gathering, interface planning, application development, integration with backend services, testing, and deployment preparation. We consider usability, responsiveness, performance, accessibility, and secure handling of user information throughout development.

Whether an application supports customer engagement, internal operations, field activities, or digital services, we focus on creating experiences that are practical and maintainable. Our objective is to align mobile functionality with business requirements and provide a consistent experience across supported devices.
        """.strip(),
        "is_active": True,
    },
    {
        "title": "Cloud Computing & Engineering",
        "short_description": "Cloud infrastructure and application environments designed around business needs.",
        "description": """
Cloud Computing & Engineering

Cloud engineering helps organizations design, deploy, and operate infrastructure and applications using cloud platforms. Intela Group works with businesses to evaluate workloads, technical requirements, availability needs, security considerations, and cost objectives when planning cloud environments.

Our services can include cloud architecture planning, environment configuration, compute and storage setup, networking, identity integration, monitoring, and workload deployment. We consider reliability, scalability, backup requirements, access controls, and operational responsibilities during implementation.

Our approach is guided by the needs of each workload rather than a one-size-fits-all architecture. The objective is to help organizations establish cloud environments that support their applications, improve operational flexibility, and provide a foundation for future growth.
        """.strip(),
        "is_active": True,
    },
    {
        "title": "DevOps & CI/CD Engineering",
        "short_description": "Automated build, testing, release, and deployment pipelines.",
        "description": """
DevOps & CI/CD Engineering

DevOps practices improve collaboration between development and operations teams while making software delivery more repeatable and efficient. Intela Group helps organizations establish delivery workflows that reduce manual effort and improve visibility across the software lifecycle.

Our services can include continuous integration and continuous delivery pipelines, automated build and test stages, deployment workflows, environment configuration, release controls, and pipeline troubleshooting. We select tools and practices according to the client's technology stack and delivery requirements.

We also consider version control, approvals, secrets management, rollback strategies, monitoring, and deployment reliability. Our goal is to help teams release changes more consistently, identify problems earlier, and maintain better control over application delivery.
        """.strip(),
        "is_active": True,
    },
    {
        "title": "Infrastructure as Code",
        "short_description": "Repeatable infrastructure provisioning using version-controlled configuration.",
        "description": """
Infrastructure as Code

Infrastructure as Code enables teams to define and manage infrastructure through configuration files rather than relying exclusively on manual setup. Intela Group helps organizations adopt repeatable provisioning practices that improve consistency across development, testing, and production environments.

Depending on the technology stack, implementations may use tools such as Terraform or other suitable infrastructure automation technologies. Activities can include resource definitions, environment configuration, reusable modules, state management, change planning, and integration with CI/CD pipelines.

We emphasize version control, reviewable changes, controlled access, and predictable deployments. By documenting infrastructure in maintainable configurations, organizations can reduce configuration drift, simplify environment creation, and improve the repeatability of infrastructure operations.
        """.strip(),
        "is_active": True,
    },
    {
        "title": "Cloud Migration & Modernization",
        "short_description": "Plan and modernize applications and workloads for cloud environments.",
        "description": """
Cloud Migration & Modernization

Cloud migration and modernization help organizations evaluate existing applications and infrastructure and determine how they can move toward suitable cloud environments. Intela Group supports planning based on business priorities, application dependencies, security, availability, and cost considerations.

Our approach may include workload assessment, dependency mapping, migration planning, environment preparation, data migration coordination, application deployment, and post-migration validation. Depending on the application, modernization may involve configuration changes, platform updates, managed services, or architectural improvements.

We recognize that not every workload requires the same migration strategy. Our aim is to help organizations reduce migration risks, maintain business continuity, and establish a practical path toward more maintainable and scalable environments.
        """.strip(),
        "is_active": True,
    },
    {
        "title": "Data Engineering",
        "short_description": "Data pipelines and platforms that make information easier to use.",
        "description": """
Data Engineering

Data engineering focuses on collecting, transforming, organizing, and delivering data so that it can be used reliably across business applications and analytical workflows. Intela Group helps organizations develop data pipelines and supporting platforms that align with their information requirements.

Our services can include source integration, extraction and transformation, data validation, scheduled processing, pipeline orchestration, and preparation of datasets for reporting or machine learning. We consider data quality, traceability, reliability, and access requirements throughout implementation.

Well-designed data pipelines make information easier to discover, maintain, and use. Our objective is to help businesses establish dependable data foundations that support operational reporting, analysis, and data-driven initiatives.
        """.strip(),
        "is_active": True,
    },
    {
        "title": "Business Intelligence & Reporting",
        "short_description": "Dashboards and reports that turn business data into actionable insights.",
        "description": """
Business Intelligence & Reporting

Business intelligence helps organizations understand performance by presenting relevant information through structured reports, dashboards, and key performance indicators. Intela Group develops reporting solutions that help stakeholders monitor operations and evaluate progress against business objectives.

Our work may include gathering reporting requirements, identifying data sources, defining metrics, preparing datasets, designing visualizations, and configuring scheduled reports. We focus on presenting information clearly so that users can understand trends, compare results, and identify areas that require attention.

We also consider data accuracy, refresh schedules, permissions, and report usability. Our aim is to make business information easier to interpret and help teams use consistent, timely insights in their planning and decision-making.
        """.strip(),
        "is_active": True,
    },
    {
        "title": "Data Analytics",
        "short_description": "Analyze business data to identify trends, patterns, and opportunities.",
        "description": """
Data Analytics

Data analytics helps organizations examine information to understand past performance, identify patterns, and investigate business questions. Intela Group supports analytical initiatives that turn available data into meaningful findings for operational and strategic use.

Our services may include data cleaning, exploratory analysis, trend identification, segmentation, statistical analysis, and preparation of analytical summaries. We work to understand the context behind the data and select methods appropriate to the questions being investigated.

We emphasize data quality, clear interpretation, and communication of findings. By presenting results in a practical and understandable way, we help stakeholders recognize opportunities, investigate issues, and make decisions informed by evidence.
        """.strip(),
        "is_active": True,
    },
    {
        "title": "Cybersecurity & Application Security",
        "short_description": "Security practices that help protect applications, systems, and data.",
        "description": """
Cybersecurity & Application Security

Cybersecurity and application security help organizations reduce risks to their systems, applications, infrastructure, and information. Intela Group supports security-focused engineering practices that are aligned with project requirements and the organization's risk management approach.

Activities may include secure development guidance, access-control reviews, dependency assessment, configuration reviews, vulnerability management support, and integration of security checks into development workflows. The specific scope depends on the systems involved and the agreed engagement.

We encourage security to be considered throughout design, development, testing, deployment, and maintenance rather than as a final step. Our objective is to help teams identify weaknesses earlier, strengthen protective controls, and improve awareness of security responsibilities.
        """.strip(),
        "is_active": True,
    },
    {
        "title": "API Development & Integration",
        "short_description": "Connect applications and services through reliable APIs.",
        "description": """
API Development & Integration

APIs allow applications and services to exchange information through defined interfaces. Intela Group designs and implements API solutions that support integration, automation, and consistent communication between business systems.

Our services may include REST API development, endpoint design, request validation, authentication integration, data transformation, error handling, documentation, and integration testing. We consider performance, versioning, access control, and compatibility with the systems that consume each API.

Whether connecting internal applications or integrating approved third-party services, we focus on predictable behavior and maintainable interfaces. Our goal is to help organizations reduce disconnected workflows and create reliable paths for data exchange.
        """.strip(),
        "is_active": True,
    },
    {
        "title": "Enterprise Software Integration",
        "short_description": "Connect business applications, databases, and enterprise platforms.",
        "description": """
Enterprise Software Integration

Enterprise software integration connects business applications and information systems so that data and processes can move between them more consistently. Intela Group helps organizations assess integration requirements and implement suitable connections between existing platforms.

Depending on the environment, work may include application interfaces, database connectivity, data mapping, synchronization workflows, event-driven communication, and integration testing. We consider system dependencies, error recovery, data consistency, and access permissions when designing integration solutions.

Our approach aims to reduce manual data entry, minimize disconnected processes, and improve information availability across teams. We prioritize maintainable integrations that fit the organization's existing technology landscape and operational requirements.
        """.strip(),
        "is_active": True,
    },
    {
        "title": "Application Maintenance",
        "short_description": "Application support, troubleshooting, upgrades, and performance improvements.",
        "description": """
Application Maintenance

Applications require ongoing attention to remain reliable, secure, and aligned with changing business requirements. Intela Group supports application maintenance activities that help organizations manage issues, improve performance, and keep software operating effectively.

Our services can include troubleshooting, defect resolution, dependency updates, compatibility improvements, performance analysis, technical documentation, and implementation of approved enhancements. We assess reported issues and prioritize work based on business impact and agreed support requirements.

We also recognize the importance of controlled changes, regression testing, and release planning. Our objective is to help organizations maintain application stability while improving usability, maintainability, and operational reliability over time.
        """.strip(),
        "is_active": True,
    },
    {
        "title": "Digital Media",
        "short_description": "Digital content and online communication support for your brand.",
        "description": """
Digital Media

Digital media helps organizations communicate their messages, share information, and present their brand across online channels. Intela Group supports digital media activities aligned with a client's communication objectives, audience, and brand guidelines.

Services may include digital content preparation, campaign asset coordination, online communication materials, and support for publishing content across selected digital channels. We focus on consistency, clarity, and suitability for the intended audience and platform.

By aligning content with business priorities and maintaining a consistent presentation, organizations can improve how they communicate with customers, partners, and other stakeholders. The scope of each engagement is shaped by the client's goals and communication requirements.
        """.strip(),
        "is_active": True,
    },
    {
        "title": "Social Media",
        "short_description": "Social content and channel support to help businesses connect with audiences.",
        "description": """
Social Media

Social media provides businesses with channels to share updates, communicate with audiences, and maintain an online presence. Intela Group supports social media activities based on each client's brand identity, audience, and communication priorities.

Support may include content planning, post preparation, publishing coordination, channel consistency, and review of engagement information. We encourage organizations to use clear messaging and a suitable publishing schedule that reflects their objectives and available resources.

Our focus is on helping businesses maintain organized and consistent communication across selected social channels. Activities and reporting can be tailored to the agreed scope, while account access and publishing approvals remain under appropriate client control.
        """.strip(),
        "is_active": True,
    },
    {
        "title": "Staffing Solutions",
        "short_description": "Flexible workforce solutions, from temporary assignments to permanent hiring.",
        "description": """
Staffing Solutions

Staffing solutions help organizations address workforce requirements by identifying suitable candidates for defined roles and business needs. Intela Group supports staffing engagements based on the skills, experience, availability, and hiring timelines specified by clients.

Our approach may include understanding role requirements, coordinating candidate sourcing, reviewing relevant qualifications, arranging interviews, and supporting communication throughout the selection process. Staffing arrangements can be structured around temporary assignments or permanent hiring requirements, subject to the agreed engagement.

We focus on clear communication, role alignment, and coordination between clients and candidates. Our objective is to help organizations address workforce needs while supporting an organized and professional recruitment experience.
        """.strip(),
        "is_active": True,
    },
    {
        "title": "Professional Services",
        "short_description": "Professional support aligned with organizational needs.",
        "description": """
Professional Services

Professional services provide organizations with specialized support for defined business, operational, and project requirements. Intela Group works with clients to understand the outcomes they need and identify suitable professional resources or service arrangements.

Depending on the engagement, support may involve project coordination, business operations, documentation, administrative activities, process improvement, or other agreed professional functions. Role expectations, deliverables, timelines, and responsibilities are established according to the client's requirements.

We emphasize professional communication, clear expectations, and dependable coordination. Our goal is to help organizations access appropriate support for their initiatives while maintaining alignment with internal processes and business priorities.
        """.strip(),
        "is_active": True,
    },
    {
        "title": "Financial Services",
        "short_description": "Financial and accounting talent support based on business requirements.",
        "description": """
Financial Services

Financial services support can help organizations address finance and accounting workforce requirements. Intela Group works with clients to understand the responsibilities, experience, and skills needed for finance-related roles and suitable staffing arrangements.

Depending on the engagement, requirements may include accounting support, financial reporting assistance, accounts payable and receivable, reconciliation support, financial operations, or other defined business functions. Candidate requirements and responsibilities are established by the client and aligned with the role.

We focus on identifying relevant skills and supporting a structured recruitment process. Any financial activities are performed by appropriately qualified personnel under the client's applicable policies, controls, and professional requirements.
        """.strip(),
        "is_active": True,
    },
    {
        "title": "Contracting",
        "short_description": "Contract-based talent for defined roles and time periods.",
        "description": """
Contracting

Contracting enables organizations to engage talent for specific projects, defined responsibilities, or agreed periods of time. Intela Group supports contract staffing requirements by working with clients to understand the role, expected deliverables, required experience, and engagement duration.

Our process may include role clarification, candidate sourcing, qualification review, interview coordination, and communication regarding assignment expectations. We aim to align candidate capabilities with the technical and professional requirements of each position.

Clear responsibilities, engagement terms, timelines, and communication help support effective contract assignments. Our goal is to help clients address temporary or project-based workforce needs with an organized and transparent process.
        """.strip(),
        "is_active": True,
    },
    {
        "title": "Direct Hire Strategy",
        "short_description": "Recruitment support for permanent positions and long-term team building.",
        "description": """
Direct Hire Strategy

Direct hire recruitment focuses on identifying candidates for permanent positions within an organization. Intela Group supports clients in defining hiring requirements and coordinating a recruitment process that considers both role-specific capabilities and longer-term organizational needs.

Our services may include position requirement discussions, candidate sourcing, qualification screening, interview coordination, and support with candidate communication. We work with the client's hiring team to understand required experience, responsibilities, and relevant selection criteria.

By maintaining clear communication and structured candidate evaluation, we help organizations make informed hiring decisions. The objective is to support sustainable team building through a recruitment process aligned with business priorities and the requirements of each position.
        """.strip(),
        "is_active": True,
    },
    {
        "title": "Onsite Recruitment",
        "short_description": "Recruitment support coordinated with a client's team.",
        "description": """
Onsite Recruitment

Onsite recruitment provides recruitment coordination and support in close collaboration with a client's internal team. This approach can help organizations manage hiring activities when direct coordination, regular communication, and visibility into recruitment priorities are important.

Depending on the engagement, activities may include gathering hiring requirements, coordinating candidate pipelines, scheduling interviews, tracking recruitment progress, and communicating with hiring managers and candidates. Responsibilities and working arrangements are defined with the client before the engagement begins.

We focus on coordination, process consistency, and timely communication. Our goal is to support the client's recruitment operations while working within its established hiring policies, tools, and approval processes.
        """.strip(),
        "is_active": True,
    },
    {
        "title": "Offshore Outsourcing",
        "short_description": "An offshore delivery or staffing model based on agreed business requirements.",
        "description": """
Offshore Outsourcing

Offshore outsourcing allows organizations to arrange selected services or work activities through an offshore delivery model. Intela Group helps clients evaluate their requirements, define the expected scope, and establish suitable arrangements for collaboration and delivery.

Depending on the engagement, services may involve technology support, software-related activities, business operations, or other agreed functions. We consider communication channels, time-zone coordination, responsibilities, deliverables, access requirements, and operational dependencies when planning the engagement.

Clear service expectations and appropriate governance are important to effective offshore collaboration. Our aim is to support a workable delivery model that aligns with client objectives, maintains visibility into progress, and defines responsibilities for the parties involved.
        """.strip(),
        "is_active": True,
    },
    {
        "title": "Payroll – HR Services",
        "short_description": "Payroll and HR support for workforce administration.",
        "description": """
Payroll – HR Services

Payroll and HR services support the administrative activities associated with workforce management. Intela Group helps organizations identify and coordinate support for defined payroll and human resources operational requirements.

Depending on the agreed scope, activities may include payroll data coordination, employee information administration, attendance inputs, documentation support, onboarding coordination, and assistance with HR processes. The exact responsibilities depend on the client's systems, policies, applicable requirements, and service arrangement.

We emphasize accuracy, confidentiality, appropriate access controls, and clear process documentation. Our goal is to support organized workforce administration while ensuring that sensitive employee information is handled according to the client's procedures and applicable obligations.
        """.strip(),
        "is_active": True,
    },
    {
        "title": "US IT Staffing",
        "short_description": "IT talent sourcing for US-based roles and workforce requirements.",
        "description": """
US IT Staffing

US IT staffing supports organizations seeking technology professionals for roles based in the United States. Intela Group works with clients to understand technical requirements, experience expectations, work arrangements, and hiring timelines for each position.

Depending on the role, requirements may include software development, cloud engineering, DevOps, data, cybersecurity, quality assurance, business analysis, or other technology skills. Recruitment support can include candidate sourcing, resume review, interview coordination, and communication throughout the selection process.

We focus on matching candidate qualifications to the defined position and maintaining clear communication with hiring teams. Employment eligibility, engagement terms, and other applicable requirements are considered according to the client's process and the circumstances of each role.
        """.strip(),
        "is_active": True,
    },
    {
        "title": "Recruitment Process Outsourcing (RPO)",
        "short_description": "Recruitment process support aligned with a company's hiring needs.",
        "description": """
Recruitment Process Outsourcing (RPO)

Recruitment Process Outsourcing provides a structured approach to supporting some or all of an organization's recruitment activities. Intela Group works with clients to understand hiring volumes, recruitment workflows, reporting needs, and the responsibilities that should be included in an RPO engagement.

Depending on the agreed scope, services may include recruitment planning, candidate sourcing, screening coordination, interview scheduling, pipeline tracking, stakeholder communication, and recruitment reporting. Processes are aligned with the client's hiring policies, systems, and approval requirements.

We emphasize consistency, transparency, and measurable process coordination. Our objective is to help organizations manage recruitment activities more effectively while maintaining visibility into progress and keeping hiring decisions with the appropriate client stakeholders.
        """.strip(),
        "is_active": True,
    },
    {
        "title": "Recruitment Request for Proposal (RFP)",
        "short_description": "A structured process for inviting recruitment agencies to submit proposals.",
        "description": """
Recruitment Request for Proposal (RFP)

A recruitment Request for Proposal provides a structured way for organizations to communicate staffing requirements and evaluate proposals from recruitment service providers. Intela Group supports the organization and coordination of recruitment RFP activities according to the client's procurement and hiring objectives.

Support may include documenting role categories, expected service scope, recruitment volumes, timelines, submission requirements, evaluation criteria, and reporting expectations. Clear requirements help prospective providers understand the engagement and prepare comparable proposals.

We focus on organized documentation, consistent communication, and transparent evaluation criteria. The aim is to help clients manage recruitment sourcing initiatives in a structured way while leaving final provider selection and commercial approvals with the appropriate decision-makers.
        """.strip(),
        "is_active": True,
    },
]


class Command(BaseCommand):
    help = "Create or update the 32 Intela Group services."

    @transaction.atomic
    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for item in SERVICES:
            defaults = {
                "short_description": item["short_description"],
                "description": item["description"],
                "is_active": item["is_active"],
            }

            service, created = Service.objects.update_or_create(
                title=item["title"],
                defaults=defaults,
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Created: {service.title}")
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f"Updated: {service.title}")
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nFinished. Created: {created_count}; "
                f"updated: {updated_count}; "
                f"total services processed: {len(SERVICES)}."
            )
        )
