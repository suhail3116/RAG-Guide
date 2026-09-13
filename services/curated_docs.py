"""
Curated authoritative documentation for topics requiring detailed engineering workflows,
modern UI libraries, and lifecycle methodologies for the offline RAG system.
"""

from typing import List, Dict

CURATED_DOCUMENTS: List[Dict[str, str]] = [
    {
        "title": "21st.dev UI and Component Library",
        "url": "https://21st.dev",
        "categories": ["Web development", "User interface", "React", "Frontend"],
        "full_text": """21st.dev is a modern open-source UI component platform and design ecosystem designed specifically for frontend engineers working with React, Next.js, Tailwind CSS, and Framer Motion. Often referred to as a curated marketplace and showcase for high-craft UI, 21st.dev enables developers to discover, preview, copy, and integrate production-grade interactive components into modern web applications.

Core Features and Architecture of 21st.dev:
1. Composable Copy-Paste Workflow: Built on the architectural philosophy pioneered by shadcn/ui, 21st.dev provides direct source code that developers own and customize within their project repository rather than installing an inflexible, locked npm dependency.
2. Technology Stack Compatibility: Components on 21st.dev are engineered using TypeScript, React, Tailwind CSS for styling, and Framer Motion for micro-interactions, layout animations, and fluid transitions.
3. Diverse Component Catalog: Includes sophisticated landing page hero sections, interactive bento grids, animated text gradients, glow buttons, cards with physics-based hover effects, command menus, modals, and responsive navigation bars.
4. Design Tokens and Theming: Clean separation between layout and presentation, allowing developers to adapt colors, borders, shadows, and typography to their project's custom theme using CSS variables and Tailwind configuration.
5. Developer Experience: Every component includes interactive live previews, dark mode toggles, device viewport resizing, and one-click copy commands for CLI-based installation or manual code injection.

In software engineering workflows, 21st.dev accelerates frontend prototyping, elevates aesthetic polish, and bridges the gap between Figma design systems and production-ready code."""
    },
    {
        "title": "GetLayers and Layered Software Architecture",
        "url": "https://en.wikipedia.org/wiki/Multitier_architecture",
        "categories": ["Software engineering", "Software architecture", "Design patterns"],
        "full_text": """Layered architecture (and layer design patterns such as GetLayers) is an essential software engineering paradigm that organizes a codebase into distinct horizontal layers, each possessing specific responsibilities and clear abstraction boundaries.

Key Layers in Modern Software Engineering:
1. Presentation Layer (UI / Client Layer): Responsible for rendering user interfaces, capturing user events, and formatting data for human viewing. In web and mobile apps, this consists of React components, HTML templates, view controllers, and design tokens.
2. Application / Service Layer (Business Logic): Orchestrates application use cases, workflows, transactional boundaries, and coordination between domain entities. It remains agnostic of how data is stored or how the UI is displayed.
3. Domain Layer (Core Business Rules): Contains core entities, domain models, business logic invariants, and enterprise rules that do not change regardless of framework or database choice.
4. Infrastructure and Data Access Layer (Persistence): Handles communication with external systems such as relational databases (PostgreSQL, MySQL), NoSQL stores, file systems, third-party REST/GraphQL APIs, and message brokers.

Layered UI Architecture (Design Systems & Tokens):
In frontend engineering, layered design (often referred to in design systems as layer architecture) divides styling into:
- Primitive Layer: Raw color palettes, base spacing units, and font definitions.
- Semantic Layer: Context-aware variables (e.g., surface-primary, text-muted, border-focus).
- Component Layer: Component-specific overrides and variant states (e.g., button-primary-hover).

Advantages of Layered Architecture:
- Separation of Concerns: Modifications in the database schema do not ripple into user interface components.
- Testability: Layers can be independently unit-tested using mocks and dependency injection.
- Reusability: Business logic in the service layer can power both a web application, mobile app, and CLI tool simultaneously."""
    },
    {
        "title": "Blender in Software Engineering and 3D Pipelines",
        "url": "https://www.blender.org/features/pipeline/",
        "categories": ["3D computer graphics", "Software engineering", "Game development"],
        "full_text": """Blender is an open-source 3D creation suite extensively integrated into software engineering pipelines, game development, spatial computing, simulation, and modern web application development.

Key Applications of Blender in Software Engineering:
1. Web 3D Asset Pipelines (Three.js & WebGL):
Software engineers use Blender to model, texture, rig, and optimize 3D assets before exporting them into standard web formats such as GLTF and GLB. These models are then rendered interactively in browser applications using WebGL engines such as Three.js, React Three Fiber (R3F), and Babylon.js. Blender's Draco mesh compression and texture packing ensure fast download times and 60 FPS rendering in web browsers.

2. Automated Headless Pipeline Scripting with Python (bpy API):
Blender features a complete Python API (`bpy`). Software engineers run Blender headlessly on servers and in CI/CD pipelines (`blender -b --python script.py`) to automate tasks including:
- Batch asset conversion between FBX, OBJ, USDZ, and GLTF.
- Procedural generation of 3D geometry from code or mathematical datasets.
- Automated Level of Detail (LOD) generation to reduce polygon counts for low-end hardware.
- Cloud rendering and automated thumbnail generation.

3. Simulation, Robotics, and Digital Twins:
In robotics and autonomous systems engineering, Blender is used to create accurate 3D CAD environments and physical robot meshes for physics simulators such as ROS (Robot Operating System), Gazebo, and NVIDIA Isaac Sim.

4. Game Engine Integration:
Engineers build continuous asset import pipelines connecting Blender to Unity, Unreal Engine, and Godot, enabling automatic asset synchronization whenever 3D models or animation rigs are updated."""
    },
    {
        "title": "Website Development Lifecycle and Step-by-Step Guide",
        "url": "https://en.wikipedia.org/wiki/Web_development",
        "categories": ["Web development", "Software engineering", "Internet"],
        "full_text": """The Website Development Lifecycle is a structured multi-phase engineering process used to plan, design, develop, test, deploy, and maintain robust web applications.

Step-by-Step Stages of Modern Website Development:

Phase 1: Discovery, Planning, and Technical Requirements
- Defining the target audience, business goals, and core user personas.
- Determining technical stack requirements: static vs. dynamic, Single Page Application (SPA), Server-Side Rendering (SSR), or Jamstack.
- Defining sitemaps and technical constraints (SEO, compliance, multilingual support).

Phase 2: UI/UX Wireframing and Prototyping
- Creating low-fidelity wireframes to establish layout structure, information hierarchy, and content blocks.
- Developing high-fidelity interactive prototypes in Figma or Sketch with design tokens, color systems, and typography scales.
- Usability testing of user flows before writing code.

Phase 3: Technology Stack Selection
- Frontend: HTML5, CSS3, modern JavaScript (ES6+), React.js, Next.js, or Vue.js.
- Styling: Tailwind CSS, CSS Modules, or UI libraries like 21st.dev and Bootstrap.
- Backend & API: Node.js (Express), Python (FastAPI/Django), or Go.
- Database: PostgreSQL, SQLite, MySQL, or MongoDB.

Phase 4: Frontend and Backend Development
- Component-driven frontend implementation: writing clean, modular components with accessible HTML tags and responsive layouts (flexbox/grid).
- Backend development: establishing RESTful or GraphQL endpoints, database models, session management, and authentication (JWT/OAuth2).
- Integration: connecting the frontend client to backend APIs using async/await and data fetching hooks.

Phase 5: Testing and Quality Assurance (QA)
- Cross-browser and responsive testing across mobile, tablet, and desktop screens.
- Automated testing: Unit testing with Jest/Vitest, end-to-end testing with Playwright or Cypress.
- Performance and Accessibility: Auditing with Google Lighthouse for Core Web Vitals (LCP, INP, CLS) and WCAG 2.1 AA compliance.

Phase 6: Deployment, CI/CD, and Hosting
- Setting up version control via Git and automated deployment pipelines via GitHub Actions.
- Hosting on edge and cloud platforms: Vercel, Netlify, AWS S3/CloudFront, or Docker containers.
- Configuring custom domain DNS, SSL/TLS certificates, and caching layers.

Phase 7: Monitoring and Maintenance
- Error logging with Sentry, traffic analytics, search engine indexing (XML sitemaps, robots.txt), and ongoing security patching."""
    },
    {
        "title": "Application Development Lifecycle and Step-by-Step Guide",
        "url": "https://en.wikipedia.org/wiki/Systems_development_life_cycle",
        "categories": ["Software engineering", "Mobile app development", "SDLC"],
        "full_text": """The Application Development Lifecycle (Software Development Life Cycle - SDLC) provides an iterative, disciplined methodology for engineering high-performance mobile, web, and desktop software applications.

Comprehensive Steps in Application Engineering:

Step 1: Ideation, Feasibility, and Scope Definition
- Identifying the core problem statement, value proposition, and user personas.
- Determining target runtime platforms: Mobile (iOS with Swift, Android with Kotlin, cross-platform with Flutter/React Native) or Desktop (Electron, Tauri).
- Drafting Functional Specifications and Non-Functional Requirements (throughput, latency, offline storage).

Step 2: Architecture and System Design
- Choosing an architectural pattern: Model-View-Controller (MVC), Clean Architecture, Hexagonal Architecture, or Event-Driven Microservices.
- Data Modeling: Designing relational schemas (PostgreSQL) or document structures, setting up indexing and database migrations.
- API Design: Designing idempotent REST or GraphQL interfaces with strict contract definitions (OpenAPI/Swagger).
- Security Architecture: Designing token-based authentication (OAuth2 / JWT), data encryption at rest (AES-256) and in transit (TLS 1.3).

Step 3: Agile Sprint Planning and Backlog Management
- Breaking down the system into user stories, tasks, and acceptance criteria.
- Setting up version control branches with Git branching strategies (Gitflow / Trunk-Based Development).

Step 4: Core Implementation and Clean Code
- Writing maintainable code adhering to SOLID principles and DRY (Don't Repeat Yourself).
- Implementing state management, local database caching for offline capability (SQLite, Realm, IndexedDB), and robust error handling.

Step 5: Testing and Quality Verification
- Unit Testing: Validating discrete logic units and utility methods with high test coverage.
- Integration Testing: Verifying database transactions, network responses, and background jobs.
- End-to-End (E2E) & Security Testing: Automated user workflow testing and vulnerability scans (static code analysis, dependency auditing).

Step 6: Release Engineering and Deployment
- Continuous Integration/Continuous Delivery (CI/CD): Automating build compilation, linting, test suites, and binary signing via GitHub Actions or Fastlane.
- App Store / Cloud Deployment: Submitting mobile binaries to Apple App Store and Google Play Store, or deploying cloud backends to Kubernetes / AWS ECS.

Step 7: Observability, Analytics, and Post-Launch Maintenance
- Real-time crash reporting (Crashlytics, Sentry), Application Performance Monitoring (APM), user feedback tracking, and regular patch releases."""
    }
]

def get_curated_documents() -> List[Dict[str, str]]:
    """Return the curated technical documents."""
    return CURATED_DOCUMENTS
