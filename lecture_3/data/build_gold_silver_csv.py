"""
Build resumes_final_with_gold_silver.csv by appending 10 gold/silver resumes
to the existing resumes_final.csv.
"""

import csv
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(SCRIPT_DIR, "resumes_final.csv")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "resumes_final_with_gold_silver.csv")


def make_html(resume_id, sections):
    """Build simple structured HTML for a resume given a list of (title, content_html) tuples."""
    parts = [f'<div class="resume" id="resume_{resume_id}">']
    for title, content in sections:
        parts.append(
            f'<div class="section">'
            f'<div class="sectiontitle">{title}</div>'
            f'<div class="content">{content}</div>'
            f'</div>'
        )
    parts.append("</div>")
    return "".join(parts)


def bullets(items):
    """Return an HTML unordered list from a list of strings."""
    li = "".join(f"<li>{item}</li>" for item in items)
    return f"<ul>{li}</ul>"


def job_block(title, company, location, dates, bullet_list):
    return (
        f'<span class="jobtitle">{title}</span> | '
        f'<span class="companyname">{company}</span> | {location} | {dates}'
        f'{bullets(bullet_list)}'
    )


def edu_line(degree, school, location, year):
    return f"<p>{degree} | {school} | {location} | {year}</p>"


# ---------------------------------------------------------------------------
# Define the 10 new resumes
# ---------------------------------------------------------------------------

NEW_RESUMES = []

# ===== g01 — Rachel Dominguez =====
_str = """         SENIOR FULL-STACK SOFTWARE ENGINEER       Summary     Senior Full-Stack Software Engineer with 8 years of professional experience designing and delivering enterprise web applications using .NET Core, React, and Microsoft SQL Server. Proven track record of building high-throughput RESTful APIs serving 50,000+ daily active users. Experienced in cloud-native architecture on AWS with a focus on performance, reliability, and security. Strong collaborator in Agile teams with a history of mentoring junior developers.       Experience      Senior Software Engineer     Mar 2021   to   Present      Capital One   -   McLean  ,   VA     Architected and developed a customer-facing loan origination platform using ASP.NET Core Web API, React (TypeScript), and SQL Server, processing 12,000 applications per day.  Designed and implemented Entity Framework Core data access layer with complex LINQ queries, reducing average API response time by 35% through query optimization and indexing strategies.  Led migration of legacy WCF services to RESTful microservices deployed on AWS ECS with Fargate, cutting infrastructure costs by 40%.  Implemented OAuth 2.0 / JWT-based authentication integrated with Active Directory for internal tools and customer-facing portals.  Built CI/CD pipelines in Azure DevOps deploying to AWS EC2 and S3, achieving zero-downtime deployments with blue-green strategy.  Mentored a team of 3 junior developers through code reviews, pair programming sessions, and weekly knowledge-sharing presentations.         Software Engineer     Jun 2018   to   Feb 2021      Booz Allen Hamilton   -   Washington  ,   DC     Built internal case management web application using ASP.NET MVC 5, Angular 8, and PostgreSQL for a federal government client, serving 2,000+ daily users.  Developed stored procedures and optimized SQL queries handling 5M+ row tables, reducing report generation time from 45 minutes to 3 minutes.  Integrated AWS Lambda functions for asynchronous document processing (PDF generation, OCR) with S3 event triggers.  Participated in Agile/Scrum ceremonies including sprint planning, daily standups, and retrospectives across a 12-person distributed team.  Wrote comprehensive unit tests using xUnit and integration tests with TestServer, maintaining 85%+ code coverage.         Junior Software Developer     Jul 2016   to   May 2018      Freddie Mac   -   McLean  ,   VA     Developed features for mortgage analytics dashboard using C# .NET Framework 4.6, jQuery, and SQL Server.  Built ADO.NET data access components for batch processing of mortgage loan data.  Created responsive front-end components using HTML5, CSS3, and Bootstrap.  Managed source control workflows using Git with feature branching and pull request reviews.         Education      Bachelor of Science  ,   Computer Science   2016     Virginia Tech   -   Blacksburg  ,   VA         Certifications     AWS Certified Developer - Associate (2022)   Microsoft Certified: Azure Developer Associate (2020)       Skills     C#, .NET Core, .NET Framework, ASP.NET MVC, ASP.NET Web API, Entity Framework, ADO.NET, React, TypeScript, Angular, JavaScript (ES6+), HTML5, CSS3, SQL Server, PostgreSQL, AWS (EC2, S3, Lambda, RDS, ECS), Azure DevOps, Docker, Git, xUnit, OAuth/JWT, REST API design, Agile/Scrum          """

_html = make_html("g01", [
    ("Summary", "<p>Senior Full-Stack Software Engineer with 8 years of professional experience designing and delivering enterprise web applications using .NET Core, React, and Microsoft SQL Server. Proven track record of building high-throughput RESTful APIs serving 50,000+ daily active users. Experienced in cloud-native architecture on AWS with a focus on performance, reliability, and security. Strong collaborator in Agile teams with a history of mentoring junior developers.</p>"),
    ("Experience",
     job_block("Senior Software Engineer", "Capital One", "McLean, VA", "Mar 2021 - Present", [
         "Architected and developed a customer-facing loan origination platform using ASP.NET Core Web API, React (TypeScript), and SQL Server, processing 12,000 applications per day.",
         "Designed and implemented Entity Framework Core data access layer with complex LINQ queries, reducing average API response time by 35% through query optimization and indexing strategies.",
         "Led migration of legacy WCF services to RESTful microservices deployed on AWS ECS with Fargate, cutting infrastructure costs by 40%.",
         "Implemented OAuth 2.0 / JWT-based authentication integrated with Active Directory for internal tools and customer-facing portals.",
         "Built CI/CD pipelines in Azure DevOps deploying to AWS EC2 and S3, achieving zero-downtime deployments with blue-green strategy.",
         "Mentored a team of 3 junior developers through code reviews, pair programming sessions, and weekly knowledge-sharing presentations.",
     ]) +
     job_block("Software Engineer", "Booz Allen Hamilton", "Washington, DC", "Jun 2018 - Feb 2021", [
         "Built internal case management web application using ASP.NET MVC 5, Angular 8, and PostgreSQL for a federal government client, serving 2,000+ daily users.",
         "Developed stored procedures and optimized SQL queries handling 5M+ row tables, reducing report generation time from 45 minutes to 3 minutes.",
         "Integrated AWS Lambda functions for asynchronous document processing (PDF generation, OCR) with S3 event triggers.",
         "Participated in Agile/Scrum ceremonies including sprint planning, daily standups, and retrospectives across a 12-person distributed team.",
         "Wrote comprehensive unit tests using xUnit and integration tests with TestServer, maintaining 85%+ code coverage.",
     ]) +
     job_block("Junior Software Developer", "Freddie Mac", "McLean, VA", "Jul 2016 - May 2018", [
         "Developed features for mortgage analytics dashboard using C# .NET Framework 4.6, jQuery, and SQL Server.",
         "Built ADO.NET data access components for batch processing of mortgage loan data.",
         "Created responsive front-end components using HTML5, CSS3, and Bootstrap.",
         "Managed source control workflows using Git with feature branching and pull request reviews.",
     ])
     ),
    ("Education", edu_line("Bachelor of Science, Computer Science", "Virginia Tech", "Blacksburg, VA", "2016")),
    ("Certifications", "<p>AWS Certified Developer - Associate (2022)</p><p>Microsoft Certified: Azure Developer Associate (2020)</p>"),
    ("Skills", "<p>C#, .NET Core, .NET Framework, ASP.NET MVC, ASP.NET Web API, Entity Framework, ADO.NET, React, TypeScript, Angular, JavaScript (ES6+), HTML5, CSS3, SQL Server, PostgreSQL, AWS (EC2, S3, Lambda, RDS, ECS), Azure DevOps, Docker, Git, xUnit, OAuth/JWT, REST API design, Agile/Scrum</p>"),
])
NEW_RESUMES.append(("g01", _str, _html))

# ===== g02 — Marcus Whitfield =====
_str = """         FULL-STACK SOFTWARE ENGINEER       Summary     Full-Stack Software Engineer with 10 years of experience building enterprise applications across financial services and healthcare. Deep expertise in C#/.NET ecosystem, modern JavaScript frameworks, and SQL database design. Passionate about clean architecture, test-driven development, and shipping reliable software on AWS infrastructure.       Experience      Lead Software Engineer     Jan 2020   to   Present      JPMorgan Chase   -   Columbus  ,   OH     Lead a team of 6 engineers building a real-time trade surveillance platform using .NET 6 Web API, React 18, and SQL Server 2019.  Designed event-driven microservices architecture using RabbitMQ for inter-service communication, processing 200,000+ trade events per hour.  Implemented complex SQL Server stored procedures and Entity Framework Core mappings for multi-tenant data isolation.  Deployed containerized services to AWS ECS with infrastructure-as-code using CloudFormation, managing 15+ microservices.  Established CI/CD pipelines using Jenkins and Docker, reducing deployment cycle from 2 weeks to daily releases.  Championed adoption of structured logging (Serilog) and distributed tracing for production observability.         Senior Software Engineer     Aug 2017   to   Dec 2019      Nationwide Insurance   -   Columbus  ,   OH     Developed policyholder self-service portal using ASP.NET Core MVC, Vue.js, and Oracle DB, serving 500,000+ policyholders.  Built RESTful APIs consumed by mobile and web clients, implementing rate limiting and API versioning best practices.  Migrated on-premises SQL Server databases to AWS RDS, designing backup and failover strategies.  Conducted code reviews for a team of 8 and led weekly architecture discussions.         Software Developer     Jun 2014   to   Jul 2017      Accenture   -   Chicago  ,   IL     Built custom CRM modules for enterprise clients using C# .NET Framework, ASP.NET Web Forms, and SQL Server.  Developed front-end interfaces using JavaScript, jQuery, and KnockoutJS with responsive CSS layouts.  Wrote T-SQL stored procedures, views, and functions for complex reporting requirements.  Worked in Scrum teams with 2-week sprint cycles across 3 simultaneous client engagements.         Education      Bachelor of Science  ,   Software Engineering   2014     Ohio State University   -   Columbus  ,   OH         Skills     C#, .NET 6, .NET Framework, ASP.NET Core, ASP.NET MVC, Entity Framework Core, React, Vue.js, JavaScript (ES6+), TypeScript, HTML5, CSS3, SQL Server, Oracle, PostgreSQL, AWS (EC2, ECS, RDS, S3, CloudFormation), RabbitMQ, Docker, Jenkins, Git, Serilog, xUnit, NUnit, REST API design, microservices, Agile/Scrum          """

_html = make_html("g02", [
    ("Summary", "<p>Full-Stack Software Engineer with 10 years of experience building enterprise applications across financial services and healthcare. Deep expertise in C#/.NET ecosystem, modern JavaScript frameworks, and SQL database design. Passionate about clean architecture, test-driven development, and shipping reliable software on AWS infrastructure.</p>"),
    ("Experience",
     job_block("Lead Software Engineer", "JPMorgan Chase", "Columbus, OH", "Jan 2020 - Present", [
         "Lead a team of 6 engineers building a real-time trade surveillance platform using .NET 6 Web API, React 18, and SQL Server 2019.",
         "Designed event-driven microservices architecture using RabbitMQ for inter-service communication, processing 200,000+ trade events per hour.",
         "Implemented complex SQL Server stored procedures and Entity Framework Core mappings for multi-tenant data isolation.",
         "Deployed containerized services to AWS ECS with infrastructure-as-code using CloudFormation, managing 15+ microservices.",
         "Established CI/CD pipelines using Jenkins and Docker, reducing deployment cycle from 2 weeks to daily releases.",
         "Championed adoption of structured logging (Serilog) and distributed tracing for production observability.",
     ]) +
     job_block("Senior Software Engineer", "Nationwide Insurance", "Columbus, OH", "Aug 2017 - Dec 2019", [
         "Developed policyholder self-service portal using ASP.NET Core MVC, Vue.js, and Oracle DB, serving 500,000+ policyholders.",
         "Built RESTful APIs consumed by mobile and web clients, implementing rate limiting and API versioning best practices.",
         "Migrated on-premises SQL Server databases to AWS RDS, designing backup and failover strategies.",
         "Conducted code reviews for a team of 8 and led weekly architecture discussions.",
     ]) +
     job_block("Software Developer", "Accenture", "Chicago, IL", "Jun 2014 - Jul 2017", [
         "Built custom CRM modules for enterprise clients using C# .NET Framework, ASP.NET Web Forms, and SQL Server.",
         "Developed front-end interfaces using JavaScript, jQuery, and KnockoutJS with responsive CSS layouts.",
         "Wrote T-SQL stored procedures, views, and functions for complex reporting requirements.",
         "Worked in Scrum teams with 2-week sprint cycles across 3 simultaneous client engagements.",
     ])
     ),
    ("Education", edu_line("Bachelor of Science, Software Engineering", "Ohio State University", "Columbus, OH", "2014")),
    ("Skills", "<p>C#, .NET 6, .NET Framework, ASP.NET Core, ASP.NET MVC, Entity Framework Core, React, Vue.js, JavaScript (ES6+), TypeScript, HTML5, CSS3, SQL Server, Oracle, PostgreSQL, AWS (EC2, ECS, RDS, S3, CloudFormation), RabbitMQ, Docker, Jenkins, Git, Serilog, xUnit, NUnit, REST API design, microservices, Agile/Scrum</p>"),
])
NEW_RESUMES.append(("g02", _str, _html))

# ===== g03 — Priya Chandrasekaran =====
_str = """         SENIOR SOFTWARE ENGINEER       Summary     Senior Software Engineer with 7 years of experience delivering full-stack web applications in fast-paced Agile environments. Specializes in .NET Core microservices, Angular, and cloud-native development on AWS. Strong database design skills with Microsoft SQL Server and PostgreSQL. Known for bridging the gap between product requirements and scalable technical solutions.       Experience      Senior Software Engineer     Apr 2021   to   Present      Fidelity Investments   -   Boston  ,   MA     Designed and built a portfolio rebalancing tool using ASP.NET Core Web API, Angular 14, and SQL Server serving 30,000+ financial advisors.  Implemented complex domain logic using Entity Framework Core with repository and unit-of-work patterns.  Built real-time notification system using AWS SNS/SQS integrated with .NET background services.  Deployed applications on AWS EC2 behind Application Load Balancers with auto-scaling groups.  Led migration from AngularJS to Angular 14, incrementally modernizing the front-end over 6 months.  Created comprehensive API documentation using Swagger/OpenAPI and maintained Postman test collections.         Software Engineer     Sep 2019   to   Mar 2021      Wayfair   -   Boston  ,   MA     Developed supplier onboarding platform using .NET Core 3.1, React, and PostgreSQL handling 2,000+ supplier accounts.  Built database schemas and wrote optimized queries, including full-text search and materialized views in PostgreSQL.  Implemented CI/CD using GitHub Actions deploying to AWS ECS with Docker containers.  Integrated Stripe payment APIs and built webhook handlers for order fulfillment workflows.         Software Developer     Jun 2017   to   Aug 2019      Raytheon Technologies   -   Waltham  ,   MA     Built internal project tracking application using ASP.NET MVC, JavaScript/jQuery, and SQL Server for defense program teams.  Developed ADO.NET data access layer with parameterized queries and connection pooling.  Designed and maintained SQL Server database schemas, writing stored procedures for weekly status reporting.  Participated in Agile ceremonies and contributed to team wiki documentation.         Education      Master of Science  ,   Computer Science   2017     Northeastern University   -   Boston  ,   MA      Bachelor of Technology  ,   Information Technology   2015     Anna University   -   Chennai  ,   India         Skills     C#, .NET Core, .NET Framework, ASP.NET Core Web API, ASP.NET MVC, Entity Framework Core, ADO.NET, Angular, React, JavaScript (ES6+), TypeScript, HTML5, CSS3, SQL Server, PostgreSQL, AWS (EC2, S3, SQS, SNS, ECS, RDS), Docker, GitHub Actions, Git, Swagger/OpenAPI, xUnit, REST API design, Agile/Scrum          """

_html = make_html("g03", [
    ("Summary", "<p>Senior Software Engineer with 7 years of experience delivering full-stack web applications in fast-paced Agile environments. Specializes in .NET Core microservices, Angular, and cloud-native development on AWS. Strong database design skills with Microsoft SQL Server and PostgreSQL. Known for bridging the gap between product requirements and scalable technical solutions.</p>"),
    ("Experience",
     job_block("Senior Software Engineer", "Fidelity Investments", "Boston, MA", "Apr 2021 - Present", [
         "Designed and built a portfolio rebalancing tool using ASP.NET Core Web API, Angular 14, and SQL Server serving 30,000+ financial advisors.",
         "Implemented complex domain logic using Entity Framework Core with repository and unit-of-work patterns.",
         "Built real-time notification system using AWS SNS/SQS integrated with .NET background services.",
         "Deployed applications on AWS EC2 behind Application Load Balancers with auto-scaling groups.",
         "Led migration from AngularJS to Angular 14, incrementally modernizing the front-end over 6 months.",
         "Created comprehensive API documentation using Swagger/OpenAPI and maintained Postman test collections.",
     ]) +
     job_block("Software Engineer", "Wayfair", "Boston, MA", "Sep 2019 - Mar 2021", [
         "Developed supplier onboarding platform using .NET Core 3.1, React, and PostgreSQL handling 2,000+ supplier accounts.",
         "Built database schemas and wrote optimized queries, including full-text search and materialized views in PostgreSQL.",
         "Implemented CI/CD using GitHub Actions deploying to AWS ECS with Docker containers.",
         "Integrated Stripe payment APIs and built webhook handlers for order fulfillment workflows.",
     ]) +
     job_block("Software Developer", "Raytheon Technologies", "Waltham, MA", "Jun 2017 - Aug 2019", [
         "Built internal project tracking application using ASP.NET MVC, JavaScript/jQuery, and SQL Server for defense program teams.",
         "Developed ADO.NET data access layer with parameterized queries and connection pooling.",
         "Designed and maintained SQL Server database schemas, writing stored procedures for weekly status reporting.",
         "Participated in Agile ceremonies and contributed to team wiki documentation.",
     ])
     ),
    ("Education",
     edu_line("Master of Science, Computer Science", "Northeastern University", "Boston, MA", "2017") +
     edu_line("Bachelor of Technology, Information Technology", "Anna University", "Chennai, India", "2015")),
    ("Skills", "<p>C#, .NET Core, .NET Framework, ASP.NET Core Web API, ASP.NET MVC, Entity Framework Core, ADO.NET, Angular, React, JavaScript (ES6+), TypeScript, HTML5, CSS3, SQL Server, PostgreSQL, AWS (EC2, S3, SQS, SNS, ECS, RDS), Docker, GitHub Actions, Git, Swagger/OpenAPI, xUnit, REST API design, Agile/Scrum</p>"),
])
NEW_RESUMES.append(("g03", _str, _html))

# ===== g04 — Daniel Okonkwo =====
_str = """         FULL-STACK SOFTWARE ENGINEER       Summary     Full-Stack Software Engineer with 6 years of professional experience and a PhD in Applied Physics. Transitioned from computational modeling to enterprise software development, bringing strong analytical skills and mathematical rigor to complex engineering problems. Proficient in C#/.NET, React, SQL Server, and AWS cloud services.       Experience      Software Engineer II     Aug 2021   to   Present      Microsoft   -   Redmond  ,   WA     Develops features for Azure DevOps Server using ASP.NET Core, React (TypeScript), and SQL Server across a globally distributed team of 20 engineers.  Implemented Entity Framework Core data models for work item tracking with complex relational schemas and migration strategies.  Built interactive dashboards and data visualization components using React, D3.js, and the Fluent UI component library.  Designed RESTful API endpoints following Microsoft API guidelines, serving 100,000+ daily API calls.  Wrote performance benchmarks and optimized hot-path SQL queries, reducing P95 latency by 25%.  Deployed features behind feature flags using LaunchDarkly, enabling gradual rollouts to 1M+ users.         Software Developer     Jan 2019   to   Jul 2021      Pacific Northwest National Laboratory   -   Richland  ,   WA     Built scientific data management platform using .NET Core Web API, Angular 11, and PostgreSQL for research teams.  Developed stored procedures and database optimization strategies for time-series data storage (50GB+ daily ingestion).  Integrated AWS S3 for large dataset storage with Lambda-triggered ETL pipelines.  Created Docker-based development environments and deployed to AWS EC2 instances.         Postdoctoral Research Associate     Sep 2016   to   Dec 2018      MIT   -   Cambridge  ,   MA     Developed computational fluid dynamics simulation software in C++ and Python, publishing 4 peer-reviewed papers.  Built data visualization web tools using Flask (Python) and JavaScript for research collaboration.  Managed Linux HPC cluster administration and job scheduling for 30-person research group.         Education      PhD  ,   Applied Physics   2016     Stanford University   -   Stanford  ,   CA      Bachelor of Science  ,   Physics   2010     University of Chicago   -   Chicago  ,   IL         Certifications     AWS Certified Solutions Architect - Associate (2022)       Skills     C#, .NET Core, ASP.NET Core Web API, Entity Framework Core, React, TypeScript, Angular, JavaScript (ES6+), D3.js, HTML5, CSS3, SQL Server, PostgreSQL, AWS (EC2, S3, Lambda, RDS), Docker, Git, Azure DevOps, Python, C++, REST API design, Agile/Scrum, data visualization          """

_html = make_html("g04", [
    ("Summary", "<p>Full-Stack Software Engineer with 6 years of professional experience and a PhD in Applied Physics. Transitioned from computational modeling to enterprise software development, bringing strong analytical skills and mathematical rigor to complex engineering problems. Proficient in C#/.NET, React, SQL Server, and AWS cloud services.</p>"),
    ("Experience",
     job_block("Software Engineer II", "Microsoft", "Redmond, WA", "Aug 2021 - Present", [
         "Develops features for Azure DevOps Server using ASP.NET Core, React (TypeScript), and SQL Server across a globally distributed team of 20 engineers.",
         "Implemented Entity Framework Core data models for work item tracking with complex relational schemas and migration strategies.",
         "Built interactive dashboards and data visualization components using React, D3.js, and the Fluent UI component library.",
         "Designed RESTful API endpoints following Microsoft API guidelines, serving 100,000+ daily API calls.",
         "Wrote performance benchmarks and optimized hot-path SQL queries, reducing P95 latency by 25%.",
         "Deployed features behind feature flags using LaunchDarkly, enabling gradual rollouts to 1M+ users.",
     ]) +
     job_block("Software Developer", "Pacific Northwest National Laboratory", "Richland, WA", "Jan 2019 - Jul 2021", [
         "Built scientific data management platform using .NET Core Web API, Angular 11, and PostgreSQL for research teams.",
         "Developed stored procedures and database optimization strategies for time-series data storage (50GB+ daily ingestion).",
         "Integrated AWS S3 for large dataset storage with Lambda-triggered ETL pipelines.",
         "Created Docker-based development environments and deployed to AWS EC2 instances.",
     ]) +
     job_block("Postdoctoral Research Associate", "MIT", "Cambridge, MA", "Sep 2016 - Dec 2018", [
         "Developed computational fluid dynamics simulation software in C++ and Python, publishing 4 peer-reviewed papers.",
         "Built data visualization web tools using Flask (Python) and JavaScript for research collaboration.",
         "Managed Linux HPC cluster administration and job scheduling for 30-person research group.",
     ])
     ),
    ("Education",
     edu_line("PhD, Applied Physics", "Stanford University", "Stanford, CA", "2016") +
     edu_line("Bachelor of Science, Physics", "University of Chicago", "Chicago, IL", "2010")),
    ("Certifications", "<p>AWS Certified Solutions Architect - Associate (2022)</p>"),
    ("Skills", "<p>C#, .NET Core, ASP.NET Core Web API, Entity Framework Core, React, TypeScript, Angular, JavaScript (ES6+), D3.js, HTML5, CSS3, SQL Server, PostgreSQL, AWS (EC2, S3, Lambda, RDS), Docker, Git, Azure DevOps, Python, C++, REST API design, Agile/Scrum, data visualization</p>"),
])
NEW_RESUMES.append(("g04", _str, _html))

# ===== g05 — Katherine Brennan =====
_str = """         SENIOR SOFTWARE ENGINEER       Summary     Senior Software Engineer with 9 years of experience building scalable web applications in healthcare and insurance domains. Expert-level proficiency in the Microsoft .NET stack, modern front-end frameworks, and relational database systems. Strong advocate for secure coding practices and OWASP compliance. Experienced in leading technical initiatives and driving architectural decisions.       Experience      Senior Software Engineer     May 2020   to   Present      UnitedHealth Group   -   Minneapolis  ,   MN     Leads development of provider credentialing platform using .NET 6 Web API, React, and SQL Server 2019, managing credentials for 100,000+ healthcare providers.  Architected multi-layer application with clean architecture pattern: domain, application, infrastructure, and presentation layers.  Designed and implemented complex SQL Server schemas with temporal tables for audit compliance, including stored procedures for batch credential verification.  Built front-end SPA using React 18 with Redux Toolkit for state management and Material UI component library.  Implemented OWASP Top 10 security controls including input validation, CSRF protection, and secure header configuration.  Led team of 5 in migrating from on-premises Windows servers to AWS, deploying on EC2 with RDS (SQL Server) and ElastiCache (Redis).         Software Engineer     Jan 2017   to   Apr 2020      Epic Systems   -   Verona  ,   WI     Built clinical workflow modules in C# .NET Framework using ASP.NET MVC and proprietary front-end frameworks.  Developed HL7 FHIR-compliant RESTful APIs for interoperability with external healthcare systems.  Optimized Entity Framework queries and wrote raw SQL for performance-critical reporting modules on multi-billion-row databases.  Conducted security code reviews and remediated vulnerabilities identified in penetration testing.         Junior Developer     Jun 2015   to   Dec 2016      Travelers Insurance   -   Hartford  ,   CT     Developed claims processing features using C# .NET Framework, ASP.NET Web Forms, and SQL Server.  Built front-end components using JavaScript, jQuery, and Bootstrap for responsive design.  Wrote NUnit tests for business logic layers and participated in integration testing cycles.  Managed code in Git with Azure DevOps (formerly TFS) for source control and build pipelines.         Education      Bachelor of Science  ,   Computer Science   2015     University of Wisconsin-Madison   -   Madison  ,   WI         Certifications     Microsoft Certified: Azure Developer Associate (2021)   AWS Certified Developer - Associate (2023)   Certified Scrum Developer (CSD)       Skills     C#, .NET 6, .NET Framework, ASP.NET Core, ASP.NET MVC, ASP.NET Web API, Entity Framework, ADO.NET, React, Redux, JavaScript (ES6+), TypeScript, HTML5, CSS3, jQuery, SQL Server, PostgreSQL, Redis, AWS (EC2, RDS, S3, ElastiCache), Azure DevOps, Docker, Git, NUnit, xUnit, OAuth/JWT, OWASP, HL7 FHIR, REST API design, clean architecture, Agile/Scrum          """

_html = make_html("g05", [
    ("Summary", "<p>Senior Software Engineer with 9 years of experience building scalable web applications in healthcare and insurance domains. Expert-level proficiency in the Microsoft .NET stack, modern front-end frameworks, and relational database systems. Strong advocate for secure coding practices and OWASP compliance. Experienced in leading technical initiatives and driving architectural decisions.</p>"),
    ("Experience",
     job_block("Senior Software Engineer", "UnitedHealth Group", "Minneapolis, MN", "May 2020 - Present", [
         "Leads development of provider credentialing platform using .NET 6 Web API, React, and SQL Server 2019, managing credentials for 100,000+ healthcare providers.",
         "Architected multi-layer application with clean architecture pattern: domain, application, infrastructure, and presentation layers.",
         "Designed and implemented complex SQL Server schemas with temporal tables for audit compliance, including stored procedures for batch credential verification.",
         "Built front-end SPA using React 18 with Redux Toolkit for state management and Material UI component library.",
         "Implemented OWASP Top 10 security controls including input validation, CSRF protection, and secure header configuration.",
         "Led team of 5 in migrating from on-premises Windows servers to AWS, deploying on EC2 with RDS (SQL Server) and ElastiCache (Redis).",
     ]) +
     job_block("Software Engineer", "Epic Systems", "Verona, WI", "Jan 2017 - Apr 2020", [
         "Built clinical workflow modules in C# .NET Framework using ASP.NET MVC and proprietary front-end frameworks.",
         "Developed HL7 FHIR-compliant RESTful APIs for interoperability with external healthcare systems.",
         "Optimized Entity Framework queries and wrote raw SQL for performance-critical reporting modules on multi-billion-row databases.",
         "Conducted security code reviews and remediated vulnerabilities identified in penetration testing.",
     ]) +
     job_block("Junior Developer", "Travelers Insurance", "Hartford, CT", "Jun 2015 - Dec 2016", [
         "Developed claims processing features using C# .NET Framework, ASP.NET Web Forms, and SQL Server.",
         "Built front-end components using JavaScript, jQuery, and Bootstrap for responsive design.",
         "Wrote NUnit tests for business logic layers and participated in integration testing cycles.",
         "Managed code in Git with Azure DevOps (formerly TFS) for source control and build pipelines.",
     ])
     ),
    ("Education", edu_line("Bachelor of Science, Computer Science", "University of Wisconsin-Madison", "Madison, WI", "2015")),
    ("Certifications", "<p>Microsoft Certified: Azure Developer Associate (2021)</p><p>AWS Certified Developer - Associate (2023)</p><p>Certified Scrum Developer (CSD)</p>"),
    ("Skills", "<p>C#, .NET 6, .NET Framework, ASP.NET Core, ASP.NET MVC, ASP.NET Web API, Entity Framework, ADO.NET, React, Redux, JavaScript (ES6+), TypeScript, HTML5, CSS3, jQuery, SQL Server, PostgreSQL, Redis, AWS (EC2, RDS, S3, ElastiCache), Azure DevOps, Docker, Git, NUnit, xUnit, OAuth/JWT, OWASP, HL7 FHIR, REST API design, clean architecture, Agile/Scrum</p>"),
])
NEW_RESUMES.append(("g05", _str, _html))

# ===== s01 — Tyler Nakamura =====
_str = """         SOFTWARE DEVELOPER       Summary     Software Developer with 1.5 years of professional experience building web applications. Enthusiastic learner with exposure to full-stack development using .NET and JavaScript. Seeking opportunities to grow technical skills and contribute to team-oriented development environments.       Experience      Junior Software Developer     Jan 2024   to   Present      Accenture   -   Arlington  ,   VA     Assists in developing internal HR dashboard using ASP.NET Core and Bootstrap under supervision of senior engineers.  Writes unit tests using xUnit for existing C# business logic classes.  Fixes bugs in JavaScript front-end code and updates CSS styling per design specifications.  Participates in daily standups and sprint planning sessions as part of a 10-person Scrum team.  Created SQL queries to extract data for monthly reporting spreadsheets from SQL Server.         Software Development Intern     May 2023   to   Aug 2023      Deloitte   -   Washington  ,   DC     Built prototype employee directory page using React and a mock REST API during summer internship.  Wrote Python scripts to automate data cleaning tasks for the analytics team.  Shadowed senior developers during code reviews and architecture discussions.         Education      Bachelor of Science  ,   Information Systems   2023     George Mason University   -   Fairfax  ,   VA         Skills     C#, ASP.NET Core (basic), JavaScript, React (basic), HTML5, CSS3, Bootstrap, SQL Server (basic queries), Python, Git, xUnit, Agile/Scrum          """

_html = make_html("s01", [
    ("Summary", "<p>Software Developer with 1.5 years of professional experience building web applications. Enthusiastic learner with exposure to full-stack development using .NET and JavaScript. Seeking opportunities to grow technical skills and contribute to team-oriented development environments.</p>"),
    ("Experience",
     job_block("Junior Software Developer", "Accenture", "Arlington, VA", "Jan 2024 - Present", [
         "Assists in developing internal HR dashboard using ASP.NET Core and Bootstrap under supervision of senior engineers.",
         "Writes unit tests using xUnit for existing C# business logic classes.",
         "Fixes bugs in JavaScript front-end code and updates CSS styling per design specifications.",
         "Participates in daily standups and sprint planning sessions as part of a 10-person Scrum team.",
         "Created SQL queries to extract data for monthly reporting spreadsheets from SQL Server.",
     ]) +
     job_block("Software Development Intern", "Deloitte", "Washington, DC", "May 2023 - Aug 2023", [
         "Built prototype employee directory page using React and a mock REST API during summer internship.",
         "Wrote Python scripts to automate data cleaning tasks for the analytics team.",
         "Shadowed senior developers during code reviews and architecture discussions.",
     ])
     ),
    ("Education", edu_line("Bachelor of Science, Information Systems", "George Mason University", "Fairfax, VA", "2023")),
    ("Skills", "<p>C#, ASP.NET Core (basic), JavaScript, React (basic), HTML5, CSS3, Bootstrap, SQL Server (basic queries), Python, Git, xUnit, Agile/Scrum</p>"),
])
NEW_RESUMES.append(("s01", _str, _html))

# ===== s02 — Amanda Kowalski =====
_str = """         FRONT-END SOFTWARE ENGINEER       Summary     Front-End Software Engineer with 10 years of experience building responsive, accessible web interfaces. Specializes in JavaScript ecosystem including React, Next.js, and Node.js. Passionate about user experience, component-driven design systems, and modern CSS architecture.       Experience      Senior Front-End Engineer     Mar 2020   to   Present      Shopify   -   Ottawa  ,   ON (Remote)     Leads front-end architecture for merchant analytics dashboard built in React 18, Next.js 14, and TypeScript serving 500,000+ merchants.  Designed and maintained Polaris-based component library with 60+ reusable components, reducing feature development time by 30%.  Built GraphQL client layer using Apollo Client with optimistic updates, caching strategies, and error boundary patterns.  Implemented server-side rendering and incremental static regeneration for SEO-critical merchant storefront pages.  Mentors 4 junior front-end developers through code reviews and pair programming.         Front-End Developer     Jul 2017   to   Feb 2020      HubSpot   -   Cambridge  ,   MA     Built marketing automation UI components using React, Redux, and Sass for the HubSpot CRM platform.  Developed custom data visualization components using D3.js and Recharts for campaign analytics.  Implemented responsive layouts and accessibility (WCAG 2.1 AA) across 20+ product screens.  Wrote comprehensive Jest and React Testing Library test suites with 90%+ component coverage.         Web Developer     Jun 2014   to   Jun 2017      Digital Agency (Freelance)   -   Boston  ,   MA     Built marketing websites and e-commerce storefronts for 30+ clients using WordPress, PHP, JavaScript, and CSS.  Developed custom WordPress themes and plugins for client-specific functionality.  Created responsive email templates and landing pages for marketing campaigns.         Education      Bachelor of Fine Arts  ,   Graphic Design   2014     Rhode Island School of Design   -   Providence  ,   RI         Skills     JavaScript (ES6+), TypeScript, React, Next.js, Node.js, GraphQL, Apollo Client, Redux, HTML5, CSS3, Sass, Tailwind CSS, D3.js, Jest, React Testing Library, Webpack, Vite, Git, Figma, responsive design, accessibility (WCAG), component libraries          """

_html = make_html("s02", [
    ("Summary", "<p>Front-End Software Engineer with 10 years of experience building responsive, accessible web interfaces. Specializes in JavaScript ecosystem including React, Next.js, and Node.js. Passionate about user experience, component-driven design systems, and modern CSS architecture.</p>"),
    ("Experience",
     job_block("Senior Front-End Engineer", "Shopify", "Ottawa, ON (Remote)", "Mar 2020 - Present", [
         "Leads front-end architecture for merchant analytics dashboard built in React 18, Next.js 14, and TypeScript serving 500,000+ merchants.",
         "Designed and maintained Polaris-based component library with 60+ reusable components, reducing feature development time by 30%.",
         "Built GraphQL client layer using Apollo Client with optimistic updates, caching strategies, and error boundary patterns.",
         "Implemented server-side rendering and incremental static regeneration for SEO-critical merchant storefront pages.",
         "Mentors 4 junior front-end developers through code reviews and pair programming.",
     ]) +
     job_block("Front-End Developer", "HubSpot", "Cambridge, MA", "Jul 2017 - Feb 2020", [
         "Built marketing automation UI components using React, Redux, and Sass for the HubSpot CRM platform.",
         "Developed custom data visualization components using D3.js and Recharts for campaign analytics.",
         "Implemented responsive layouts and accessibility (WCAG 2.1 AA) across 20+ product screens.",
         "Wrote comprehensive Jest and React Testing Library test suites with 90%+ component coverage.",
     ]) +
     job_block("Web Developer", "Digital Agency (Freelance)", "Boston, MA", "Jun 2014 - Jun 2017", [
         "Built marketing websites and e-commerce storefronts for 30+ clients using WordPress, PHP, JavaScript, and CSS.",
         "Developed custom WordPress themes and plugins for client-specific functionality.",
         "Created responsive email templates and landing pages for marketing campaigns.",
     ])
     ),
    ("Education", edu_line("Bachelor of Fine Arts, Graphic Design", "Rhode Island School of Design", "Providence, RI", "2014")),
    ("Skills", "<p>JavaScript (ES6+), TypeScript, React, Next.js, Node.js, GraphQL, Apollo Client, Redux, HTML5, CSS3, Sass, Tailwind CSS, D3.js, Jest, React Testing Library, Webpack, Vite, Git, Figma, responsive design, accessibility (WCAG), component libraries</p>"),
])
NEW_RESUMES.append(("s02", _str, _html))

# ===== s03 — Kevin Boateng =====
_str = """         EMBEDDED SYSTEMS ENGINEER       Summary     Embedded Systems Engineer with 8 years of experience developing firmware and low-level software for IoT devices and industrial control systems. Proficient in C, C++, and real-time operating systems. Experienced in hardware-software integration, communication protocol implementation, and safety-critical system development.       Experience      Senior Embedded Software Engineer     Apr 2020   to   Present      Honeywell   -   Charlotte  ,   NC     Develops firmware for industrial HVAC control systems using C and FreeRTOS on ARM Cortex-M microcontrollers.  Implemented MQTT and Modbus communication protocols for IoT device connectivity to cloud monitoring platforms.  Designed and coded safety-critical alarm logic compliant with IEC 61508 SIL 2 requirements.  Optimized memory usage and power consumption for battery-operated sensor nodes, extending battery life by 40%.  Led hardware-software integration testing using oscilloscopes, logic analyzers, and JTAG debuggers.         Embedded Software Developer     Jun 2018   to   Mar 2020      John Deere   -   Moline  ,   IL     Developed CAN bus communication drivers for agricultural vehicle telematics modules in C.  Built diagnostic tools using C++ and Qt for manufacturing line firmware validation.  Wrote automated test harnesses using Python for hardware-in-the-loop testing.         Firmware Engineer     Aug 2016   to   May 2018      General Electric (GE Aviation)   -   Cincinnati  ,   OH     Developed real-time flight data acquisition software in C for DO-178C Level B certification.  Implemented ARINC 429 and MIL-STD-1553 avionics bus interfaces.  Performed static code analysis using LDRA and Polyspace for safety compliance.         Education      Bachelor of Science  ,   Electrical Engineering   2016     Georgia Institute of Technology   -   Atlanta  ,   GA         Certifications     Certified LabVIEW Associate Developer (2019)       Skills     C, C++, FreeRTOS, ARM Cortex-M, MQTT, Modbus, CAN bus, ARINC 429, Python (scripting), Qt, JTAG, oscilloscope, logic analyzer, Git, LDRA, Polyspace, IEC 61508, DO-178C, IoT, real-time systems, firmware development          """

_html = make_html("s03", [
    ("Summary", "<p>Embedded Systems Engineer with 8 years of experience developing firmware and low-level software for IoT devices and industrial control systems. Proficient in C, C++, and real-time operating systems. Experienced in hardware-software integration, communication protocol implementation, and safety-critical system development.</p>"),
    ("Experience",
     job_block("Senior Embedded Software Engineer", "Honeywell", "Charlotte, NC", "Apr 2020 - Present", [
         "Develops firmware for industrial HVAC control systems using C and FreeRTOS on ARM Cortex-M microcontrollers.",
         "Implemented MQTT and Modbus communication protocols for IoT device connectivity to cloud monitoring platforms.",
         "Designed and coded safety-critical alarm logic compliant with IEC 61508 SIL 2 requirements.",
         "Optimized memory usage and power consumption for battery-operated sensor nodes, extending battery life by 40%.",
         "Led hardware-software integration testing using oscilloscopes, logic analyzers, and JTAG debuggers.",
     ]) +
     job_block("Embedded Software Developer", "John Deere", "Moline, IL", "Jun 2018 - Mar 2020", [
         "Developed CAN bus communication drivers for agricultural vehicle telematics modules in C.",
         "Built diagnostic tools using C++ and Qt for manufacturing line firmware validation.",
         "Wrote automated test harnesses using Python for hardware-in-the-loop testing.",
     ]) +
     job_block("Firmware Engineer", "General Electric (GE Aviation)", "Cincinnati, OH", "Aug 2016 - May 2018", [
         "Developed real-time flight data acquisition software in C for DO-178C Level B certification.",
         "Implemented ARINC 429 and MIL-STD-1553 avionics bus interfaces.",
         "Performed static code analysis using LDRA and Polyspace for safety compliance.",
     ])
     ),
    ("Education", edu_line("Bachelor of Science, Electrical Engineering", "Georgia Institute of Technology", "Atlanta, GA", "2016")),
    ("Certifications", "<p>Certified LabVIEW Associate Developer (2019)</p>"),
    ("Skills", "<p>C, C++, FreeRTOS, ARM Cortex-M, MQTT, Modbus, CAN bus, ARINC 429, Python (scripting), Qt, JTAG, oscilloscope, logic analyzer, Git, LDRA, Polyspace, IEC 61508, DO-178C, IoT, real-time systems, firmware development</p>"),
])
NEW_RESUMES.append(("s03", _str, _html))

# ===== s04 — Jennifer Huang =====
_str = """         ASPIRING SOFTWARE ENGINEER       Summary     Recent computer science graduate and aspiring software engineer with internship experience and strong academic background. Completed capstone project building a full-stack web application. Eager to apply classroom knowledge of data structures, algorithms, and software engineering principles in a professional setting.       Experience      Software Engineering Intern     May 2024   to   Aug 2024      IBM   -   Research Triangle Park  ,   NC     Contributed bug fixes to an internal Spring Boot microservice handling employee onboarding workflows.  Wrote JUnit tests for REST API endpoints and improved test coverage from 60% to 72%.  Built a small React dashboard component displaying team velocity metrics using Chart.js.  Participated in Agile sprint ceremonies and presented demo of completed work to stakeholders.         Teaching Assistant, Data Structures & Algorithms     Aug 2023   to   May 2024      NC State University   -   Raleigh  ,   NC     Held weekly office hours helping 200+ students with Java programming assignments.  Graded assignments and provided detailed feedback on algorithm complexity analysis.         Capstone Project     Jan 2024   to   May 2024      NC State University     Built a campus event discovery web app using Node.js (Express), React, and MongoDB.  Implemented user authentication with Passport.js and session management.  Deployed to Heroku with GitHub Actions for continuous deployment.         Education      Bachelor of Science  ,   Computer Science   2024     North Carolina State University   -   Raleigh  ,   NC         Skills     Java, JavaScript, React (basic), Node.js (basic), Python, HTML5, CSS3, MongoDB, SQL (coursework), Spring Boot (basic), Git, JUnit, data structures, algorithms          """

_html = make_html("s04", [
    ("Summary", "<p>Recent computer science graduate and aspiring software engineer with internship experience and strong academic background. Completed capstone project building a full-stack web application. Eager to apply classroom knowledge of data structures, algorithms, and software engineering principles in a professional setting.</p>"),
    ("Experience",
     job_block("Software Engineering Intern", "IBM", "Research Triangle Park, NC", "May 2024 - Aug 2024", [
         "Contributed bug fixes to an internal Spring Boot microservice handling employee onboarding workflows.",
         "Wrote JUnit tests for REST API endpoints and improved test coverage from 60% to 72%.",
         "Built a small React dashboard component displaying team velocity metrics using Chart.js.",
         "Participated in Agile sprint ceremonies and presented demo of completed work to stakeholders.",
     ]) +
     '<span class="jobtitle">Teaching Assistant, Data Structures &amp; Algorithms</span> | <span class="companyname">NC State University</span> | Raleigh, NC | Aug 2023 - May 2024' +
     bullets([
         "Held weekly office hours helping 200+ students with Java programming assignments.",
         "Graded assignments and provided detailed feedback on algorithm complexity analysis.",
     ]) +
     '<span class="jobtitle">Capstone Project</span> | <span class="companyname">NC State University</span> | Jan 2024 - May 2024' +
     bullets([
         "Built a campus event discovery web app using Node.js (Express), React, and MongoDB.",
         "Implemented user authentication with Passport.js and session management.",
         "Deployed to Heroku with GitHub Actions for continuous deployment.",
     ])
     ),
    ("Education", edu_line("Bachelor of Science, Computer Science", "North Carolina State University", "Raleigh, NC", "2024")),
    ("Skills", "<p>Java, JavaScript, React (basic), Node.js (basic), Python, HTML5, CSS3, MongoDB, SQL (coursework), Spring Boot (basic), Git, JUnit, data structures, algorithms</p>"),
])
NEW_RESUMES.append(("s04", _str, _html))

# ===== s05 — Ryan Gallagher =====
_str = """         DEVOPS AND INFRASTRUCTURE ENGINEER       Summary     DevOps and Infrastructure Engineer with 9 years of experience managing cloud infrastructure, CI/CD pipelines, and container orchestration platforms. Specializes in automating deployment workflows, monitoring production systems, and maintaining high-availability environments on AWS and Azure.       Experience      Senior DevOps Engineer     Feb 2021   to   Present      Netflix   -   Los Gatos  ,   CA     Manages Kubernetes clusters running 200+ microservices across AWS regions using Terraform and Helm charts.  Built and maintains CI/CD pipelines in Spinnaker and Jenkins for 50+ engineering teams, supporting 500+ deployments per week.  Designed observability stack using Prometheus, Grafana, and PagerDuty for real-time alerting on SLA violations.  Implemented infrastructure-as-code for AWS resources (EC2, ECS, RDS, S3, Lambda, CloudFront) using Terraform modules.  Led incident response and post-mortem processes for production outages, reducing MTTR by 45%.         DevOps Engineer     Mar 2018   to   Jan 2021      Atlassian   -   San Francisco  ,   CA     Built Docker-based build environments and managed container registries for internal development teams.  Automated AWS infrastructure provisioning using CloudFormation and Ansible.  Implemented centralized logging using ELK stack (Elasticsearch, Logstash, Kibana) processing 2TB+ logs daily.  Managed PostgreSQL and MySQL database backups, replication, and failover configurations.         Systems Administrator     Jul 2015   to   Feb 2018      Rackspace   -   San Antonio  ,   TX     Administered Linux (RHEL, Ubuntu) and Windows Server environments for managed hosting clients.  Configured and maintained Apache, Nginx, and IIS web servers.  Wrote Bash and PowerShell scripts for automated server provisioning and patching.  Monitored systems using Nagios and New Relic, maintaining 99.95% uptime SLAs.         Education      Bachelor of Science  ,   Information Technology   2015     University of Texas at San Antonio   -   San Antonio  ,   TX         Certifications     AWS Certified Solutions Architect - Professional (2022)   Certified Kubernetes Administrator (CKA) (2021)   HashiCorp Certified: Terraform Associate (2020)       Skills     AWS (EC2, ECS, RDS, S3, Lambda, CloudFront, VPC, IAM), Terraform, Kubernetes, Docker, Helm, Jenkins, Spinnaker, Ansible, CloudFormation, Prometheus, Grafana, ELK stack, Bash, Python, PowerShell, Linux (RHEL, Ubuntu), Nginx, PostgreSQL, MySQL, Git, PagerDuty, incident response, infrastructure-as-code          """

_html = make_html("s05", [
    ("Summary", "<p>DevOps and Infrastructure Engineer with 9 years of experience managing cloud infrastructure, CI/CD pipelines, and container orchestration platforms. Specializes in automating deployment workflows, monitoring production systems, and maintaining high-availability environments on AWS and Azure.</p>"),
    ("Experience",
     job_block("Senior DevOps Engineer", "Netflix", "Los Gatos, CA", "Feb 2021 - Present", [
         "Manages Kubernetes clusters running 200+ microservices across AWS regions using Terraform and Helm charts.",
         "Built and maintains CI/CD pipelines in Spinnaker and Jenkins for 50+ engineering teams, supporting 500+ deployments per week.",
         "Designed observability stack using Prometheus, Grafana, and PagerDuty for real-time alerting on SLA violations.",
         "Implemented infrastructure-as-code for AWS resources (EC2, ECS, RDS, S3, Lambda, CloudFront) using Terraform modules.",
         "Led incident response and post-mortem processes for production outages, reducing MTTR by 45%.",
     ]) +
     job_block("DevOps Engineer", "Atlassian", "San Francisco, CA", "Mar 2018 - Jan 2021", [
         "Built Docker-based build environments and managed container registries for internal development teams.",
         "Automated AWS infrastructure provisioning using CloudFormation and Ansible.",
         "Implemented centralized logging using ELK stack (Elasticsearch, Logstash, Kibana) processing 2TB+ logs daily.",
         "Managed PostgreSQL and MySQL database backups, replication, and failover configurations.",
     ]) +
     job_block("Systems Administrator", "Rackspace", "San Antonio, TX", "Jul 2015 - Feb 2018", [
         "Administered Linux (RHEL, Ubuntu) and Windows Server environments for managed hosting clients.",
         "Configured and maintained Apache, Nginx, and IIS web servers.",
         "Wrote Bash and PowerShell scripts for automated server provisioning and patching.",
         "Monitored systems using Nagios and New Relic, maintaining 99.95% uptime SLAs.",
     ])
     ),
    ("Education", edu_line("Bachelor of Science, Information Technology", "University of Texas at San Antonio", "San Antonio, TX", "2015")),
    ("Certifications", "<p>AWS Certified Solutions Architect - Professional (2022)</p><p>Certified Kubernetes Administrator (CKA) (2021)</p><p>HashiCorp Certified: Terraform Associate (2020)</p>"),
    ("Skills", "<p>AWS (EC2, ECS, RDS, S3, Lambda, CloudFront, VPC, IAM), Terraform, Kubernetes, Docker, Helm, Jenkins, Spinnaker, Ansible, CloudFormation, Prometheus, Grafana, ELK stack, Bash, Python, PowerShell, Linux (RHEL, Ubuntu), Nginx, PostgreSQL, MySQL, Git, PagerDuty, incident response, infrastructure-as-code</p>"),
])
NEW_RESUMES.append(("s05", _str, _html))


# ---------------------------------------------------------------------------
# Read existing CSV and write combined output
# ---------------------------------------------------------------------------

def main():
    # Read existing rows
    with open(INPUT_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        existing_rows = list(reader)

    print(f"Read {len(existing_rows)} existing rows from {INPUT_PATH}")

    # Build new rows
    new_rows = []
    for rid, resume_str, resume_html in NEW_RESUMES:
        new_rows.append({
            "ID": rid,
            "Resume_str": resume_str,
            "Resume_html": resume_html,
        })

    all_rows = existing_rows + new_rows

    # Write output
    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["ID", "Resume_str", "Resume_html"],
                                quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"Wrote {len(all_rows)} rows to {OUTPUT_PATH}")

    # Verify
    with open(OUTPUT_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        gold = [r for r in rows if r["ID"].startswith("g")]
        silver = [r for r in rows if r["ID"].startswith("s")]
        print(f"Verification - Total: {len(rows)}, Gold: {len(gold)}, Silver: {len(silver)}")


if __name__ == "__main__":
    main()
