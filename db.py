import os
import sqlite3
from flask import current_app, g


OPPORTUNITIES = [
 
    # =========================================================================
    # 1. PROGRAMMING / COMPUTER SCIENCE
    # =========================================================================
    (
        "USACO — USA Computing Olympiad",
        "contest",
        "Free online algorithmic programming contests (December–March), open to all skill levels "
        "from beginner to advanced. Top performers are invited to a national training camp and can "
        "represent the USA at the International Olympiad in Informatics.",
        "U.S. only — any middle or high school student interested in programming, "
        "no prior contest experience required. (Non-U.S. students may compete unofficially.)",
        "Four online contests, roughly monthly, December through March",
        "https://usaco.org",
    ),
    (
        "Congressional App Challenge",
        "contest",
        "Nationwide coding competition run by the U.S. House of Representatives. Students build any "
        "software project — app, game, web tool, AI project — individually or in teams of up to four. "
        "District winners are displayed in the U.S. Capitol and invited to the #HouseOfCode reception. "
        "AI-assisted development is allowed if fully disclosed.",
        "U.S. only — middle and high school students who live or attend school in a participating "
        "congressional district. Any skill level; beginners explicitly welcome.",
        "Registration opens ~May, submissions due late October (2026 cycle: October 26, 2026, 12:00 ET)",  # VERIFIED
        "https://www.congressionalappchallenge.us",
    ),
    (
        "picoCTF",
        "contest",
        "Free capture-the-flag cybersecurity competition from Carnegie Mellon. Beginner-friendly "
        "puzzle-style challenges in reverse engineering, cryptography, web exploitation and forensics. "
        "Practice gym stays open year-round after the live event.",
        "Global — anyone can play; official prizes are limited to U.S. middle and high school students. "
        "No prior security experience required.",
        "Annual live competition in March; practice challenges available year-round",
        "https://picoctf.org",
    ),
    (
        "CyberPatriot — National Youth Cyber Defense Competition",
        "contest",
        "Team-based cyber defense competition where students harden virtual machines against "
        "simulated attacks. Includes free training materials and a large scholarship pool for finalists.",
        "U.S., Canada and DoD schools — middle and high school teams, formed through a school, "
        "JROTC unit, or approved youth organization",
        "Team registration in the fall; qualification rounds run November through February",
        "https://www.uscyberpatriot.org",
    ),
    (
        "Google Summer of Code",
        "internship",
        "Paid remote program where contributors work 90–350 hours on a real open source project "
        "with a mentor from the organization. Stipend varies by country. One of the strongest "
        "resume items available to someone with no formal work history.",
        "Global — 18+ and new to open source contribution. University students, self-taught developers, "
        "and career changers are all eligible; a degree is not required.",
        "Organizations announced ~February; contributor applications typically late March–early April",
        "https://summerofcode.withgoogle.com",
    ),
    (
        "Outreachy",
        "internship",
        "Paid, fully remote three-month open source internships (~$7,000 stipend) with mentorship, "
        "aimed at people underrepresented in tech. Includes a required contribution period before "
        "final selection, which doubles as free portfolio work.",
        "Global — 18+, underrepresented in tech in your country/region, available ~40 hrs/week "
        "for the internship term. Not limited to students.",
        "Two cohorts per year: applications ~January–February and ~August–September",
        "https://www.outreachy.org",
    ),
    (
        "MLH Fellowship",
        "internship",
        "12-week remote fellowship by Major League Hacking. Tracks in open source software, "
        "site reliability engineering, and production engineering, working in small pods with "
        "a dedicated mentor. Some tracks are paid.",
        "Global — 18+ students and recent grads. Portfolio matters more than GPA.",
        "Multiple cohorts per year (spring, summer, fall); applications open ~2–3 months prior",
        "https://fellowship.mlh.io",
    ),
    (
        "MLH Hackathons",
        "contest",
        "The largest network of student hackathons worldwide — hundreds of in-person and online "
        "events per year, most free with travel reimbursement, food, and sponsor prizes. "
        "The fastest way to build a portfolio and a network from zero.",
        "Global — most events accept 18+; a growing number of high-school-specific events exist. "
        "Beginners are the majority at most events.",
        "Rolling — events run year-round, registration typically 2–6 weeks in advance",
        "https://mlh.io/seasons",
    ),
    (
        "Hack Club",
        "community",
        "Global network of teen-run coding clubs plus a very active Slack. Runs its own grant programs, "
        "hardware giveaways, hackathons, and travel-funded events. Also funds students who start a "
        "club at their own school.",
        "Global — teenagers roughly 13–18. No experience required; you can join the Slack alone "
        "or start a club at your school.",
        "Rolling — join anytime; individual grant programs have their own cycles",
        "https://hackclub.com",
    ),
    (
        "Codeforces",
        "contest",
        "The largest competitive programming platform in the world. Free rated contests several times "
        "a week, an enormous problem archive, and a rating system that is directly recognized by "
        "recruiters at trading firms and big tech.",
        "Global — anyone, any age, free account. Div. 3 and Div. 4 rounds are designed for beginners.",
        "Rolling — multiple contests per week, year-round",
        "https://codeforces.com",
    ),
    (
        "AtCoder",
        "contest",
        "Japanese competitive programming platform with weekly beginner (ABC) and advanced (ARC/AGC) "
        "contests, fully translated into English. Clean beginner ramp and a rating recognized by "
        "Japanese employers.",
        "Global — anyone, any age, free account",
        "Rolling — weekly contests, usually Saturday/Sunday",
        "https://atcoder.jp",
    ),
    (
        "Kaggle Competitions",
        "contest",
        "Machine learning competitions with real datasets and, in many cases, real prize money "
        "($10k–$100k+). Public notebooks make it one of the best places to learn applied ML by "
        "reading other people's solutions.",
        "Global — free account, 13+ to participate; 18+ (or guardian consent) for prize-bearing "
        "competitions. 'Getting Started' competitions are permanently open and beginner-oriented.",
        "Rolling — new competitions launch continuously, typically 2–3 month windows",
        "https://www.kaggle.com/competitions",
    ),
    (
        "International Olympiad in Informatics (IOI)",
        "contest",
        "The world championship of high school algorithmic programming. Each country sends up to "
        "four students selected through a national olympiad chain. Medal winners are actively "
        "recruited by top universities worldwide.",
        "Global — high school students under 20, selected through their own country's national "
        "informatics olympiad. Entry point is the national olympiad, not IOI directly.",
        "National selection rounds run autumn through spring; IOI itself is held in August",
        "https://ioinformatics.org",
    ),
    (
        "ICPC — International Collegiate Programming Contest",
        "contest",
        "The oldest and most prestigious team programming contest for university students. "
        "Teams of three solve algorithmic problems on one shared computer, progressing from "
        "regional to world finals.",
        "Global — university students (undergraduate and early graduate) competing in teams of three "
        "registered through their institution",
        "Regional contests run September–December; World Finals in the following year",
        "https://icpc.global",
    ),
    (
        "Advent of Code",
        "contest",
        "Free daily programming puzzles released every December 1–25. Language-agnostic, "
        "escalating in difficulty, with a huge community solving in public. Excellent for building "
        "a consistent public commit history.",
        "Global — anyone, any age, any language, completely free",
        "December 1–25 each year; past years remain permanently playable",
        "https://adventofcode.com",
    ),
    (
        "Technovation Girls",
        "contest",
        "Global 12-week program where teams of girls build a mobile app or AI project addressing "
        "a community problem, supported by an industry mentor, and pitch it in a worldwide competition "
        "with cash prizes.",
        "Global — girls and gender-expansive youth aged 8–18, in teams of 1–5 with an adult mentor. "
        "No coding experience required.",
        "Season runs roughly January–April; team registration opens in the autumn",
        "https://www.technovation.org",
    ),
    (
        "NCWIT Aspirations in Computing Award",
        "stipend",
        "National recognition program for young women and gender-nonconforming students in computing. "
        "Winners get cash awards, scholarships, internship pipelines with partner companies, and "
        "lifetime access to a very well-connected alumni network.",
        "U.S. only — students in grades 9–12 who identify as women, genderqueer, or non-binary",
        "Application typically opens early September, closes early November",
        "https://www.aspirations.org",
    ),
    (
        "Girls Who Code Summer Programs",
        "mentor",
        "Free virtual summer programs (Summer Immersion Program and self-paced pathways) covering "
        "web development, data science, and cybersecurity, with industry mentorship and a "
        "capstone project. Need-based stipends available.",
        "U.S. + select international — students in grades 9–12 who identify as girls or non-binary. "
        "Absolute beginners welcome.",
        "Applications typically open in January, close in March; program runs in summer",
        "https://girlswhocode.com",
    ),
    (
        "MIT Beaver Works Summer Institute",
        "internship",
        "Free four-week residential STEM program at MIT with tracks in autonomous racecars, "
        "UAV design, quantum computing, medical robotics, and AI. Requires completion of a "
        "rigorous online prerequisite course during the spring.",
        "U.S. only — rising high school seniors, U.S. citizens or permanent residents. "
        "Selection is based on the online prerequisite course, not just grades.",
        "Application typically due in January; online prerequisite runs spring; program in summer",
        "https://beaverworks.ll.mit.edu/CMS/bw/bwsi",
    ),
    (
        "GitHub Campus Experts",
        "community",
        "Training program that turns students into community leaders on their own campus: public "
        "speaking, technical writing, and event organizing, plus GitHub swag, credits, and "
        "direct access to the GitHub Education team.",
        "Global — university students 18+ who want to build a tech community at their school",
        "Applications reviewed on a rolling basis",
        "https://education.github.com/experts",
    ),
    (
        "Amazon Future Engineer Scholarship",
        "stipend",
        "Scholarship of up to $40,000 over four years plus a guaranteed paid Amazon internship offer "
        "for recipients pursuing computer science.",
        "U.S. only — high school seniors from under-resourced backgrounds planning to study "
        "computer science or a related field",
        "Application typically opens in the autumn, closes in January",
        "https://www.amazonfutureengineer.com",
    ),
    (
        "AI4ALL Summer Programs",
        "internship",
        "University-hosted summer programs (Stanford, Princeton, CMU, Berkeley and others) that "
        "teach AI fundamentals through applied research projects with faculty mentors, aimed at "
        "students underrepresented in AI.",
        "U.S. + some international — typically rising high school juniors and seniors; "
        "individual university sites set their own criteria. Most are free or need-based.",
        "Applications typically open December–February for summer cohorts",
        "https://ai-4-all.org",
    ),
 
    # =========================================================================
    # 2. MATH, SCIENCE & RESEARCH
    # =========================================================================
    (
        "Regeneron Science Talent Search",
        "contest",
        "The nation's oldest and most prestigious STEM research competition. Students submit "
        "original independent research; 300 scholars and 40 finalists are named, competing for "
        "a $250,000 grand prize from a pool of over $1.8 million.",
        "U.S. only — students in their final year of secondary school in the U.S. or its territories, "
        "regardless of citizenship, plus U.S. citizens living abroad. Independent (not team) research only.",
        "Application opens June 1, closes November 5, 2026 at 8pm ET for the 2027 cycle",  # VERIFIED
        "https://www.societyforscience.org/regeneron-sts",
    ),
    (
        "Regeneron International Science and Engineering Fair (ISEF)",
        "contest",
        "The world's largest pre-college science competition, with roughly $9 million in awards. "
        "Students qualify by winning an affiliated regional or national fair, then compete across "
        "22 scientific categories.",
        "Global — students in grades 9–12 (roughly ages 14–20) who advance through an ISEF-affiliated "
        "fair in their region or country",
        "Affiliated fairs run January–April; ISEF finals in May",
        "https://www.societyforscience.org/isef",
    ),
    (
        "Breakthrough Junior Challenge",
        "contest",
        "Global science video competition: explain a big idea in physics, life sciences, or mathematics "
        "in under two minutes. Winner receives a $250,000 post-secondary scholarship, their teacher "
        "gets $50,000, and their school gets a $100,000 science lab.",
        "Global — ages 13–18, any country, free to enter, submissions in English. "
        "Homeschooled students eligible.",
        "Submissions open ~May, close September 15; peer review phase runs to September 30",  # VERIFIED
        "https://breakthroughjuniorchallenge.org",
    ),
    (
        "Davidson Fellows Scholarship",
        "stipend",
        "Scholarships of $50,000, $25,000, and $10,000 for young people who have completed a "
        "significant piece of work in science, technology, mathematics, music, literature, "
        "philosophy, or 'outside the box'.",
        "U.S. only — under 18 as of a set date, U.S. citizens or permanent residents. "
        "No minimum age; the work matters, not the grade level.",
        "Application typically opens in the autumn, closes mid-February",
        "https://www.davidsongifted.org/gifted-programs/fellows-scholarship",
    ),
    (
        "MIT PRIMES / PRIMES-USA",
        "mentor",
        "Year-long free research mentorship in mathematics (and, for local students, computer science "
        "and computational biology). Students work weekly with an MIT graduate student or postdoc "
        "and produce a real research paper. Structured in four phases across the calendar year.",
        "U.S. only — high school sophomores and juniors. MIT PRIMES for those within driving distance "
        "of Boston; PRIMES-USA is remote for the rest of the U.S. Requires solving a hard problem set.",
        "Application link appears in September; deadline around November 30 / December 1",  # VERIFIED
        "https://math.mit.edu/research/highschool/primes/",
    ),
    (
        "CrowdMath (MIT PRIMES + Art of Problem Solving)",
        "mentor",
        "Free open, collaborative online research project in mathematics: hundreds of students "
        "worldwide work on the same unsolved problems, mentored by MIT researchers, and co-author "
        "the resulting paper. The rare research opportunity with no admissions gate.",
        "Global — any high school or college student, anywhere in the world, including those "
        "outside the U.S. who cannot apply to PRIMES. Open enrollment.",
        "New project launches each spring; participation is open throughout the year",
        "https://artofproblemsolving.com/polymath",
    ),
    (
        "Research Science Institute (RSI)",
        "internship",
        "Six-week fully free residential research program at MIT — widely considered the most "
        "selective high school STEM program in the world. Students complete original research "
        "with a mentor and present a paper and conference-style talk.",
        "Global — high school juniors; international students apply through partner organizations "
        "in their own country. Extremely competitive (roughly 5% acceptance).",
        "U.S. application typically due in January; international deadlines vary by country partner",
        "https://www.cee.org/programs/research-science-institute",
    ),
    (
        "Summer Science Program (SSP)",
        "internship",
        "Residential 39-day research program in astrophysics, biochemistry, genomics, or synthetic "
        "chemistry, where teams complete a real research project (e.g. determining an asteroid's orbit) "
        "from raw observation to published result. Need-blind admission with substantial financial aid.",
        "U.S. + international — students who have completed their junior year (or equivalent) "
        "with strong math and science preparation",
        "Application typically opens in December, closes in February",
        "https://summerscience.org",
    ),
    (
        "Simons Summer Research Program",
        "internship",
        "Paid seven-week hands-on research internship at Stony Brook University, where students "
        "join a faculty lab, produce a written abstract and a research poster, and receive a stipend.",
        "U.S. only — high school juniors (must be 16 by program start), U.S. citizens or permanent residents",
        "Application typically opens in December, closes in early February",
        "https://www.stonybrook.edu/simons",
    ),
    (
        "Clark Scholars Program (Texas Tech)",
        "internship",
        "Seven-week intensive summer research program with a $750 tuition-free stipend, room and board "
        "included. Only 12 students admitted per year across all fields, including engineering and CS.",
        "U.S. + international — students at least 17 years old by program start who have not yet "
        "graduated high school",
        "Application typically due in February",
        "https://www.depts.ttu.edu/honors/academicsandenrichment/affiliatedandhighschool/clarks",
    ),
    (
        "Garcia Summer Research Program (Stony Brook)",
        "internship",
        "Seven-week polymer science and materials research program. Students often co-author "
        "published papers and place well at ISEF and Regeneron STS. Tuition-based with financial aid.",
        "U.S. + international — high school students 16+ with strong science background",
        "Application typically opens in January, closes in March",
        "https://www.stonybrook.edu/garcia",
    ),
    (
        "NASA OSTEM Internships",
        "internship",
        "Paid internship through NASA's Office of STEM Engagement. Interns work directly with NASA "
        "scientists and engineers on real projects in space science, robotics, AI, aeronautics, or "
        "climate research, either on-site at a NASA center or remotely.",
        "U.S. only — U.S. citizens, 16+ at time of application, GPA 3.0+, enrolled full-time "
        "(high school through graduate level). All majors welcome; prior experience not required.",
        "Three sessions per year. Spring 2027: September 14, 2026. Summer 2027: February 26, 2027. "
        "Fall 2027: May 21, 2027.",  # VERIFIED
        "https://intern.nasa.gov",
    ),
    (
        "NASA SEES High School Summer Intern Program",
        "internship",
        "NASA + UT Austin program combining online coursework with an on-site research session in "
        "Austin. Projects use real NASA Earth observation and astronomy data; many students go on "
        "to present at ISEF.",
        "U.S. only — current high school sophomores and juniors, U.S. citizens",
        "Application typically opens in December, closes in February; program runs in summer",
        "https://www.csr.utexas.edu/education-outreach/sees-internship/",
    ),
    (
        "Perimeter Institute ISSYP",
        "internship",
        "Free two-week theoretical physics program (in-person in Canada plus a virtual edition) "
        "run by the Perimeter Institute, covering quantum mechanics, relativity, and cosmology "
        "with working physicists.",
        "Global — students aged 16+ in their final years of secondary school, from any country",
        "Application typically opens in January, closes in March",
        "https://perimeterinstitute.ca/international-summer-school-young-physicists",
    ),
    (
        "AMC / AIME / USAMO (MAA competitions)",
        "contest",
        "The main U.S. mathematics competition ladder: AMC 8/10/12, then AIME, then USAMO/USAJMO, "
        "then MOP and the International Mathematical Olympiad team. Strong AMC scores are directly "
        "cited on U.S. college applications.",
        "U.S. + international sites — AMC 8 for middle school, AMC 10/12 for high school. "
        "Register through a school or an approved testing center.",
        "AMC 10/12 in November; AIME in February; USAMO in March",
        "https://maa.org/student-programs/amc/",
    ),
    (
        "International Mathematical Olympiad (IMO)",
        "contest",
        "The world championship of high school mathematics, with teams of six from over 100 countries. "
        "Entry is through your own country's national olympiad chain.",
        "Global — secondary school students under 20, selected via national olympiads",
        "National rounds run autumn through spring; IMO held in July",
        "https://www.imo-official.org",
    ),
    (
        "MATHCOUNTS",
        "contest",
        "National middle school math competition series with school, chapter, state, and national "
        "rounds, plus a year-round free problem-of-the-week program.",
        "U.S. only — students in grades 6–8, registered through a school or homeschool group",
        "School rounds in winter; chapter competitions February; nationals in May",
        "https://www.mathcounts.org",
    ),
    (
        "Science Olympiad",
        "contest",
        "Team competition across 23 events spanning biology, chemistry, physics, earth science, "
        "and engineering build events. Combines lab skills, written tests, and hands-on device building.",
        "U.S. only — teams from middle schools (Div. B) and high schools (Div. C)",
        "Invitationals in winter; regionals and states February–April; nationals in May",
        "https://www.soinc.org",
    ),
    (
        "USA Biology / Chemistry / Physics Olympiads",
        "contest",
        "National subject olympiads (USABO, USNCO, USAPhO) selecting teams for the international "
        "biology, chemistry, and physics olympiads. Free study materials and past exams available.",
        "U.S. only — high school students, registered through a school or approved center. "
        "Most countries run an equivalent national olympiad — check your own country's chain.",
        "Open exams run January–March depending on subject",
        "https://www.usabo-trc.org",
    ),
    (
        "Thermo Fisher Junior Innovators Challenge",
        "contest",
        "The premier national STEM research competition for middle schoolers (formerly Broadcom MASTERS). "
        "Students qualify through affiliated science fairs and compete in team challenges for awards "
        "up to $25,000.",
        "U.S. only — students in grades 6–8 nominated through an affiliated science fair",
        "Nominations follow spring science fairs; application typically due in June",
        "https://www.societyforscience.org/jic/",
    ),
    (
        "Zooniverse",
        "volunteer",
        "The largest citizen science platform in the world — classify galaxies, transcribe historical "
        "records, identify wildlife, annotate medical data. Contributions have led to real published "
        "papers with volunteer co-authors.",
        "Global — anyone, any age, no account required to start. Free.",
        "Rolling — hundreds of active projects at any time",
        "https://www.zooniverse.org",
    ),
 
    # =========================================================================
    # 3. ENGINEERING & ROBOTICS
    # =========================================================================
    (
        "FIRST Robotics Competition",
        "contest",
        "Team-based robotics competition combining engineering, programming, and business skills. "
        "Teams design, build, and program a robot for that year's game, with help from industry mentors. "
        "Over $80 million in scholarships available to participants.",
        "Global — high school students (grades 9–12), no prior robotics or engineering experience "
        "required; teams join via a school or club. FIRST operates in 100+ countries.",
        "Build season runs January–April; team registration opens in the fall",
        "https://www.firstinspires.org/robotics/frc",
    ),
    (
        "FIRST Tech Challenge (FTC)",
        "contest",
        "Smaller-scale robotics competition than FRC, with lower cost and team sizes of ~10. Robots are "
        "built from a modular kit and programmed in Java or Blocks — the best entry point for schools "
        "without a big budget.",
        "Global — students in grades 7–12; teams can be formed by a school, club, or group of families",
        "Season kickoff in September; competitions run November through spring",
        "https://www.firstinspires.org/robotics/ftc",
    ),
    (
        "VEX Robotics Competition",
        "contest",
        "The largest robotics competition in the world by team count, with divisions from elementary "
        "through university. Lower entry cost than FIRST and a very large scholarship pool at worlds.",
        "Global — elementary through university students, in 70+ countries",
        "Season runs roughly August through May, with worlds in the spring",
        "https://www.vexrobotics.com/competition",
    ),
    (
        "Conrad Challenge",
        "contest",
        "Innovation and entrepreneurship competition where teams develop a commercially viable product "
        "addressing aerospace, cyber-technology, energy, health, or transformation. Judged by industry "
        "professionals; winners receive seed funding and patent support.",
        "Global — students aged 13–18 anywhere in the world, in teams of 2–5 with an adult coach",
        "Registration opens in the fall; activation stage due ~November, innovation stage ~January",
        "https://www.conradchallenge.org",
    ),
    (
        "The American Rocketry Challenge",
        "contest",
        "The world's largest student rocket contest. Teams design, build, and launch a model rocket "
        "meeting precise altitude and flight-duration targets, competing for over $100,000 in prizes.",
        "U.S. only — students in grades 6–12, in teams of 3–10 with an adult advisor",
        "Registration opens in the fall; qualification flights due in the spring",
        "https://rocketcontest.org",
    ),
    (
        "MATE ROV Competition",
        "contest",
        "Underwater robotics competition where teams build a remotely operated vehicle to complete "
        "mission tasks modeled on real ocean industry work, and pitch it as a mock company.",
        "Global — students from elementary through university, in 30+ countries",
        "Regional events run in the spring; world championship in the summer",
        "https://materovcompetition.org",
    ),
 
    # =========================================================================
    # 4. WRITING, ARTS & HUMANITIES
    # =========================================================================
    (
        "Scholastic Art & Writing Awards",
        "contest",
        "The country's longest-running recognition program for creative teens in 29 categories of "
        "art and writing. National medalists are eligible for scholarships up to $12,500 and are "
        "exhibited at Carnegie Hall.",
        "U.S. + Canada — students in grades 7–12 in the U.S., U.S. territories, or Canada, "
        "plus American schools abroad",
        "Submissions open October 1; regional deadlines vary, typically December–January",
        "https://www.artandwriting.org",
    ),
    (
        "YoungArts",
        "stipend",
        "National awards program in visual, literary, design, and performing arts. Winners receive "
        "cash awards up to $10,000, a week-long intensive in Miami with master artists, and lifelong "
        "access to the YoungArts alumni network. Also the sole nominator for U.S. Presidential Scholars in the Arts.",
        "U.S. only — artists aged 15–18 or in grades 10–12, U.S. citizens or permanent residents",
        "Application typically opens in the spring, closes in October",
        "https://youngarts.org",
    ),
    (
        "The Adroit Journal Summer Mentorship Program",
        "mentor",
        "Free five-week online one-on-one mentorship in poetry or prose with a working writer, "
        "typically an MFA student or published author. Highly regarded and completely free.",
        "Global — secondary school students anywhere in the world, including international applicants",
        "Application typically opens in February, closes in March; program runs June–July",
        "https://theadroitjournal.org/mentorship/",
    ),
    (
        "Iowa Young Writers' Studio",
        "internship",
        "Summer creative writing program from the University of Iowa — the most prestigious writing "
        "school in the U.S. Offered as a two-week residential session and a free/low-cost online option. "
        "Need-based aid available.",
        "U.S. + international — students currently in grades 10–12",
        "Residential application typically due in February; online sessions have separate deadlines",
        "https://iyws.clas.uiowa.edu",
    ),
    (
        "The Concord Review",
        "contest",
        "The only journal in the world that publishes academic history papers by secondary students. "
        "Publication is a genuinely rare credential; the associated Emerson Prize awards $3,000.",
        "Global — secondary students anywhere in the world may submit an original history essay "
        "(typically 4,000–6,000 words)",
        "Rolling submissions with four quarterly deadlines (Feb 1, May 1, Aug 1, Nov 1)",
        "https://www.tcr.org",
    ),
    (
        "John Locke Institute Essay Competition",
        "contest",
        "Global essay competition across philosophy, politics, economics, history, psychology, "
        "theology, and law. Winners receive scholarships toward John Locke programs, and shortlisted "
        "essays carry real weight with UK and U.S. admissions.",
        "Global — students aged 18 or under on the submission deadline; a separate junior category "
        "exists for those 14 and under. Free to enter.",
        "Questions released in the winter; submissions typically due end of June",
        "https://www.johnlockeinstitute.com/essay-competition",
    ),
    (
        "The New York Times Learning Network Contests",
        "contest",
        "A dozen free contests per school year — personal narrative, editorial writing, podcast, "
        "review, STEM writing, profile, 15-second video, summer reading. Winners are published by "
        "the Times, which is a strong portfolio item.",
        "Global — students aged 11–19 worldwide (some contests restrict to 13+). Free to enter.",
        "Rolling — a different contest runs almost every month, September through June",
        "https://www.nytimes.com/section/learning/contests",
    ),
    (
        "National History Day",
        "contest",
        "Year-long project-based competition where students produce a documentary, exhibit, paper, "
        "performance, or website on an annual historical theme, advancing from school to national contest.",
        "U.S. + international affiliates — students in grades 6–12",
        "School and regional contests run in the winter and spring; nationals in June",
        "https://www.nhd.org",
    ),
    (
        "Poetry Out Loud",
        "contest",
        "National poetry recitation competition run by the NEA and Poetry Foundation, progressing "
        "from classroom to state to national finals, with $50,000 in awards.",
        "U.S. only — high school students, entering through their school",
        "School contests in the autumn/winter; state finals in March; nationals in the spring",
        "https://www.poetryoutloud.org",
    ),
    (
        "Bennington Young Writers Awards",
        "contest",
        "Annual competition in poetry, fiction, and nonfiction judged by Bennington faculty, with "
        "cash prizes and scholarship consideration.",
        "Global — students in grades 9–12 anywhere in the world. Free to enter.",
        "Submissions typically open in September, close in November",
        "https://www.bennington.edu/events/young-writers-awards",
    ),
    (
        "Telluride Association Summer Seminar (TASS)",
        "internship",
        "Completely free six-week residential humanities seminar (all costs including travel covered) "
        "focused on critical Black studies and anti-oppressive studies, taught at a college level "
        "with a strong discussion-based format.",
        "U.S. + international — current high school sophomores and juniors, from any country",
        "Application typically opens in November, closes in early January",
        "https://www.tellurideassociation.org/our-programs/high-school-students/",
    ),
    (
        "Doodle for Google",
        "contest",
        "Annual art competition where students reinterpret the Google logo around a yearly theme. "
        "National winner receives a $55,000 scholarship and a $50,000 technology grant for their school.",
        "U.S. only — students in grades K–12",
        "Submissions typically open in January, close in March",
        "https://doodles.google.com/d4g/",
    ),
    (
        "National Speech & Debate Association",
        "contest",
        "The largest competitive speech and debate network in the U.S., with local, state, and national "
        "tournaments across Lincoln-Douglas, Policy, Public Forum, Congress, and speech events. "
        "One of the highest-transfer skill sets a student can build.",
        "U.S. + international affiliates — middle and high school students, competing through a "
        "school chapter",
        "Tournament season runs September through May; nationals in June",
        "https://www.speechanddebate.org",
    ),
 
    # =========================================================================
    # 5. BUSINESS, ECONOMICS & ENTREPRENEURSHIP
    # =========================================================================
    (
        "Diamond Challenge",
        "contest",
        "Global high school entrepreneurship competition run by the University of Delaware, with "
        "two tracks (business concept and social innovation) and over $100,000 in awards. Provides "
        "a free structured curriculum, so it doubles as a course.",
        "Global — students aged 14–18 in any country, in teams of 2–4 with an adult advisor. Free to enter.",
        "Registration opens in the autumn; written submissions typically due in January",
        "https://diamondchallenge.org",
    ),
    (
        "Blue Ocean Student Entrepreneur Competition",
        "contest",
        "Fully virtual, free pitch competition based on Blue Ocean Strategy. Teams submit a video pitch "
        "for a new venture; no travel or entry fee, which makes it one of the most accessible "
        "international competitions available.",
        "Global — high school students anywhere in the world, individually or in teams. Free.",
        "Registration opens in the autumn; submissions typically due in February",
        "https://www.blueoceancompetition.org",
    ),
    (
        "Wharton Global High School Investment Competition",
        "contest",
        "Ten-week team competition where students manage a simulated $100,000 portfolio and, more "
        "importantly, write a real investment strategy for a fictional client. Finalists present at "
        "Wharton. Free to enter.",
        "Global — students aged 14–18 in teams of 4–7 with a teacher advisor, from any country",
        "Registration typically closes in late September; trading runs October–December",
        "https://globalyouth.wharton.upenn.edu/high-school-investment-competition/",
    ),
    (
        "DECA",
        "contest",
        "Career and technical student organization with role-play and written-event competitions in "
        "marketing, finance, hospitality, and entrepreneurship, advancing from district to state to "
        "international career development conference.",
        "U.S., Canada + international — high school and college students, through a school chapter",
        "District competitions in the winter; state in spring; ICDC in April",
        "https://www.deca.org",
    ),
    (
        "FBLA — Future Business Leaders of America",
        "contest",
        "Business-focused student organization with over 70 competitive events including coding, "
        "cybersecurity, website design, and business plan pitches, plus a large scholarship pool.",
        "U.S. + international chapters — middle school, high school, and college students",
        "Regional and state conferences run winter–spring; national leadership conference in June",
        "https://www.fbla.org",
    ),
    (
        "National Economics Challenge",
        "contest",
        "The largest economics competition in the U.S., testing micro, macro, and international "
        "economics in a team format, with a national final and cash prizes.",
        "U.S. only — high school students in teams of 3–4, entering through a school",
        "Online qualifying round in the spring; national finals in May",
        "https://www.councilforeconed.org/national-economics-challenge/",
    ),
    (
        "Junior Achievement",
        "mentor",
        "Programs connecting students with volunteer mentors from local businesses for financial "
        "literacy, entrepreneurship, and career-readiness training, including the JA Company Program "
        "where students actually launch and run a small business.",
        "Global — JA Worldwide operates in 100+ countries; programs delivered through partner schools "
        "for students of any age",
        "Rolling — programs run throughout the school year",
        "https://www.juniorachievement.org",
    ),
    (
        "Emergent Ventures (Mercatus Center)",
        "stipend",
        "Fast, low-bureaucracy grants and fellowships for ambitious projects — often $5,000–$50,000, "
        "frequently awarded to teenagers with an unusual idea. Application is a short form, decisions "
        "often come within weeks.",
        "Global — no age limit, no institutional affiliation required, any country. "
        "Awarded on the strength of the idea alone.",
        "Rolling — applications accepted continuously",
        "https://www.mercatus.org/emergent-ventures",
    ),
    (
        "1517 Fund / Medici Project",
        "stipend",
        "Grants of $1,000 and up for young people building something outside of formal institutions — "
        "explicitly aimed at 'dropouts, misfits, and self-taught builders'. Also runs larger "
        "pre-seed investments.",
        "Global — no degree or age requirement; the fund specifically targets people who are not "
        "on a conventional academic track",
        "Rolling — applications accepted continuously",
        "https://www.1517fund.com",
    ),
    (
        "Z Fellows",
        "stipend",
        "One-week intensive program plus a $10,000 investment for young technical founders, with "
        "mentorship from founders and investors. Very short application, very fast decisions.",
        "Global — young builders and founders, typically teens to mid-twenties; remote-friendly",
        "Rolling cohorts throughout the year",
        "https://www.zfellows.com",
    ),
    (
        "Thiel Fellowship",
        "stipend",
        "$200,000 over two years for people who leave or skip university to build a company or "
        "research project, plus access to the Thiel network. Deliberately anti-credential.",
        "Global — 22 years old or younger at the time of application, any country. "
        "Requires committing to not being enrolled full-time during the fellowship.",
        "Annual cycle; applications typically close in the winter",
        "https://thielfellowship.org",
    ),
    (
        "LaunchX",
        "internship",
        "Summer entrepreneurship program (in-person at university campuses and online) where teams "
        "actually incorporate and launch a startup during the program, with mentorship from founders "
        "and VCs. Paid, with need-based aid.",
        "Global — high school students, international applicants accepted",
        "Applications open in the autumn with rolling admission rounds through the spring",
        "https://launchx.com",
    ),
 
    # =========================================================================
    # 6. VOLUNTEERING, CIVIC & LEADERSHIP
    # =========================================================================
    (
        "DoSomething.org",
        "volunteer",
        "Platform connecting teens with social-impact campaigns — climate, civic engagement, "
        "community service. Most campaigns take under an hour and many carry scholarship "
        "entries for participants.",
        "U.S. + global participation — any teen aged 13–25, no prior volunteer experience needed",
        "Rolling — new campaigns open throughout the year",
        "https://dosomething.org",
    ),
    (
        "Key Club International",
        "volunteer",
        "Student-led service organization (sponsored by Kiwanis) running community service projects "
        "through local high school chapters, with leadership roles and regional/international conferences. "
        "Also administers its own scholarship programs.",
        "Global — high school students in 38+ countries, joining through a local school chapter",
        "Rolling — join anytime through your school's chapter",
        "https://www.keyclub.org",
    ),
    (
        "Prudential Emerging Visionaries",
        "stipend",
        "Awards of $5,000–$15,000 plus mentorship and a summit in Newark for young people solving "
        "financial or social challenges in their community. Replaced the older Prudential Spirit of "
        "Community Awards.",
        "U.S. only — students aged 14–18 with an existing project or a clear plan",
        "Application typically opens in September, closes in early November",
        "https://www.prudential.com/links/about/corporate-social-responsibility/emerging-visionaries",
    ),
    (
        "The Congressional Award",
        "volunteer",
        "The U.S. Congress's own award for young people, earned by logging hours across four areas: "
        "voluntary public service, personal development, physical fitness, and an expedition. "
        "Non-competitive — everyone who completes the hours earns the medal.",
        "U.S. only — ages 13.5 to 23. No GPA requirement, no competition, no cost.",
        "Rolling — register anytime and start logging hours",
        "https://congressionalaward.org",
    ),
    (
        "United States Senate Youth Program",
        "stipend",
        "One week in Washington D.C. meeting senators, cabinet members, and Supreme Court justices, "
        "plus a $10,000 undergraduate scholarship. Two students per state per year.",
        "U.S. only — high school juniors and seniors currently serving in an elected student "
        "leadership position. Selected by each state's education department.",
        "State-level deadlines fall in the autumn (varies by state, often September–October)",
        "https://ussenateyouth.org",
    ),
    (
        "Gloria Barron Prize for Young Heroes",
        "stipend",
        "Awards $10,000 each to 25 young people who have led a significant service project "
        "benefiting people or the environment.",
        "U.S. + Canada — young people aged 8–18 who have led a project of their own",
        "Application typically opens in January, closes in April",
        "https://barronprize.org",
    ),
    (
        "Peace First",
        "stipend",
        "Mini-grants of $250–$1,000 plus digital mentorship for young people launching a social "
        "change project in their own community. Deliberately low barrier — designed to fund a "
        "first attempt, not a polished organization.",
        "Global — young people aged 13–25 in any country",
        "Rolling — applications reviewed continuously",
        "https://www.peacefirst.org",
    ),
    (
        "Boys State / Girls State (American Legion)",
        "volunteer",
        "Week-long immersive civics program where students build a mock state government from the "
        "ground up. Two delegates per state advance to Boys/Girls Nation in Washington D.C. "
        "Usually free or heavily sponsored.",
        "U.S. only — rising high school seniors, nominated through a school or American Legion post",
        "Selection happens in the winter/spring; programs run in June",
        "https://www.legion.org/boysnation",
    ),
    (
        "Model United Nations",
        "contest",
        "Simulated diplomacy conferences at school, national, and international level (including "
        "Harvard MUN, THIMUN, and hundreds of regional events). Builds research, public speaking, "
        "and negotiation under pressure.",
        "Global — middle school through university students, usually via a school delegation, "
        "though independent delegates are accepted at many conferences",
        "Conferences run year-round; the largest cluster in the autumn and winter",
        "https://www.unausa.org/model-un/",
    ),
    (
        "VolunteerMatch",
        "volunteer",
        "The largest volunteer opportunity database in the U.S., with a strong filter for "
        "virtual/remote roles — useful for students who need service hours but cannot travel.",
        "Global for virtual roles, U.S.-centric for in-person — free account, most roles 16+ "
        "or 18+ but many accept younger volunteers with a guardian",
        "Rolling — new listings added daily",
        "https://www.volunteermatch.org",
    ),
    (
        "UN Volunteers — Online Volunteering",
        "volunteer",
        "Remote volunteering assignments with UN agencies and NGOs worldwide: translation, "
        "research, web development, design, data analysis. Assignments range from a few hours "
        "to several months and come with a formal certificate.",
        "Global — 18+, any country, free. Skills matter more than credentials.",
        "Rolling — new assignments posted continuously",
        "https://www.onlinevolunteering.org",
    ),
 
    # =========================================================================
    # 7. SCHOLARSHIPS & FINANCIAL AID
    # =========================================================================
    (
        "Coca-Cola Scholars Program",
        "stipend",
        "Achievement-based scholarship of $20,000 for 150 graduating high school seniors, based on "
        "leadership and service rather than financial need. Phase 1 requires no essays, transcript, "
        "or recommendation letters — an unusually low-effort first round for a major award.",
        "U.S. only — high school seniors graduating in the current academic year, unweighted GPA 3.0+, "
        "U.S. citizens/nationals/permanent residents attending school in the 50 states or D.C.",
        "Opens August 3, closes September 30, 2026 at 5pm ET for the 2027 cycle",  # VERIFIED
        "https://www.coca-colascholarsfoundation.org",
    ),
    (
        "QuestBridge National College Match",
        "stipend",
        "Full four-year scholarship (tuition, housing, books — full cost of attendance) at one of "
        "QuestBridge's 50+ partner colleges for high-achieving students from low-income backgrounds. "
        "Matched students receive a binding early admission.",
        "U.S. only — high school seniors with a strong academic record and demonstrated financial "
        "need (typically household income under ~$65,000). U.S. citizens, permanent residents, "
        "DACA and undocumented students are eligible.",
        "Application due around late September; match results announced in early December",
        "https://www.questbridge.org",
    ),
    (
        "QuestBridge College Prep Scholars",
        "stipend",
        "The junior-year version of QuestBridge: free summer programs at partner colleges, college "
        "admissions conferences, essay support, and a significant advantage in the senior-year "
        "National College Match.",
        "U.S. only — high school juniors from low-income backgrounds with strong academics",
        "Application typically due in late March",
        "https://www.questbridge.org/high-school-students/college-prep-scholars",
    ),
    (
        "The Gates Scholarship",
        "stipend",
        "Full-ride scholarship covering the entire cost of attendance not met by other aid, for 300 "
        "students per year, at any accredited U.S. college.",
        "U.S. only — high school seniors who are Pell-eligible, U.S. citizens/nationals/permanent "
        "residents, and from a minority ethnic background (African-American, American Indian/Alaska "
        "Native, Asian & Pacific Islander American, or Hispanic American)",
        "Application typically opens in July, closes mid-September",
        "https://www.thegatesscholarship.org",
    ),
    (
        "Jack Kent Cooke Foundation — Young Scholars Program",
        "stipend",
        "Five-year pre-college scholarship starting in 8th grade: personalized advising, summer program "
        "funding, laptop and internet support, and a pipeline into the Cooke College Scholarship "
        "(up to $55,000/year).",
        "U.S. only — current 7th graders with high academic achievement and financial need",
        "Application typically opens in January, closes in April",
        "https://www.jkcf.org/our-scholarships/young-scholars-program/",
    ),
    (
        "Dell Scholars Program",
        "stipend",
        "$20,000 plus a laptop, textbook credits, and — unusually — ongoing personal support and "
        "emergency funds throughout college. Explicitly rewards grit over perfect grades "
        "(minimum GPA is only 2.4).",
        "U.S. only — high school seniors who are Pell-eligible and have participated in an approved "
        "college readiness program",
        "Application typically opens in October, closes December 1",
        "https://www.dellscholars.org",
    ),
    (
        "Horatio Alger National Scholarship",
        "stipend",
        "$25,000 scholarships awarded specifically to students who have overcome significant adversity. "
        "GPA requirement is a modest 2.0, so effort-to-reward ratio is high.",
        "U.S. only — high school juniors/seniors with critical financial need (household income "
        "under ~$65,000) who have faced and overcome adversity",
        "Application typically opens in the spring, closes October 25",
        "https://scholars.horatioalger.org",
    ),
    (
        "Elks Most Valuable Student Scholarship",
        "stipend",
        "500 four-year scholarships ranging from $4,000 to $50,000, judged on scholarship, leadership, "
        "and financial need. Notably open to all majors and does not require Elks membership.",
        "U.S. only — high school seniors who are U.S. citizens",
        "Application typically opens in August, closes in November",
        "https://www.elks.org/scholars/",
    ),
    (
        "Burger King Scholars",
        "stipend",
        "Scholarships from $1,000 to $60,000, with a very simple application and a large number of "
        "awards — one of the best odds-to-effort ratios among corporate scholarships.",
        "U.S., Canada + Puerto Rico — high school seniors, GPA 2.5+; employees and their families "
        "also eligible",
        "Application typically opens in October, closes in December",
        "https://burgerkingscholars.com",
    ),
    (
        "Ron Brown Scholar Program",
        "stipend",
        "$40,000 ($10,000/year) plus a highly active lifetime network. The community and mentorship "
        "are widely regarded as more valuable than the money itself.",
        "U.S. only — Black/African American high school seniors, U.S. citizens or permanent residents",
        "Early deadline in November; final deadline in January",
        "https://www.ronbrown.org",
    ),
    (
        "Stamps Scholars",
        "stipend",
        "Full-ride merit scholarship plus a personal enrichment fund (typically $10,000–$15,000) for "
        "research, travel, or internships, at 30+ partner universities. Applied for through the "
        "partner university's own admissions process.",
        "U.S. + international at some partners — apply to a Stamps partner university and be "
        "nominated; requirements vary by school",
        "Follows each partner university's admissions deadlines (typically November–January)",
        "https://www.stampsfoundation.org",
    ),
    (
        "Bold.org",
        "stipend",
        "Scholarship platform with hundreds of small, highly specific scholarships ($500–$25,000) — "
        "many with tiny applicant pools because the criteria are so narrow. Free, no essay required "
        "for many listings.",
        "U.S.-focused with some international listings — high school, college, and graduate students",
        "Rolling — new scholarships added weekly with individual deadlines",
        "https://bold.org",
    ),
    (
        "Fastweb",
        "stipend",
        "The largest free scholarship search database in the U.S. (1.5+ million scholarships). "
        "Best used as a systematic weekly habit rather than a one-time search.",
        "U.S. only — free account for high school, college, and graduate students",
        "Rolling — matched scholarships have individual deadlines year-round",
        "https://www.fastweb.com",
    ),
 
    # =========================================================================
    # 8. INTERNATIONAL / NON-U.S. STUDENTS
    # =========================================================================
    (
        "United World Colleges (UWC)",
        "stipend",
        "Two-year International Baccalaureate education at one of 18 UWC schools worldwide, "
        "selected through a national committee in your own country. Most students receive full or "
        "partial need-based scholarships, and UWC graduates access the Davis UWC Scholars program "
        "for U.S. university funding.",
        "Global — students aged 16–19, applying through the national committee of their own country "
        "of residence. Selection is based on potential, not just grades.",
        "National committee deadlines vary by country, most falling between September and January",
        "https://www.uwc.org",
    ),
    (
        "European Solidarity Corps",
        "volunteer",
        "EU-funded volunteering placements of 2 weeks to 12 months in another European country, with "
        "travel, accommodation, food, insurance, and pocket money fully covered.",
        "EU + partner countries — young people aged 18–30 legally resident in a participating country. "
        "No qualifications required.",
        "Rolling — placements posted continuously on the European Youth Portal",
        "https://youth.europa.eu/solidarity_en",
    ),
    (
        "Erasmus+ Youth Exchanges",
        "volunteer",
        "Short (5–21 day) funded group exchanges in another European country on themes like climate, "
        "entrepreneurship, digital skills, or inclusion. Travel and accommodation covered; usually "
        "found through a local youth NGO.",
        "EU + partner countries — young people aged 13–30, applying via a participating youth "
        "organization in their country",
        "Rolling — projects announced year-round by national agencies and youth NGOs",
        "https://erasmus-plus.ec.europa.eu",
    ),
    (
        "DAAD Scholarships (Germany)",
        "stipend",
        "The German Academic Exchange Service funds study, research, and summer language courses in "
        "Germany at all levels, including undergraduate options. Germany's public universities also "
        "charge little to no tuition even without a scholarship.",
        "Global — requirements vary by programme; there are dedicated tracks for undergraduates, "
        "graduates, and researchers from most countries",
        "Deadlines vary by programme and country, many falling between October and March",
        "https://www.daad.de/en/",
    ),
    (
        "Holland Scholarship",
        "stipend",
        "€5,000 first-year scholarship for non-EEA students starting a bachelor's or master's degree "
        "at a participating Dutch university. Applied for directly through the chosen institution.",
        "Non-EEA international students — applying to a participating Dutch research university "
        "or university of applied sciences",
        "Deadlines set by each institution, typically February 1 or May 1",
        "https://www.studyinnl.org/finances/holland-scholarship",
    ),
    (
        "African Leadership Academy",
        "stipend",
        "Two-year pre-university programme in South Africa combining A-Levels with entrepreneurial "
        "leadership and African studies, with substantial need-based financial aid and a strong "
        "university placement pipeline.",
        "Africa + diaspora — students aged 15–19 from any African country",
        "Application typically opens in the autumn, closes in the winter",
        "https://www.africanleadershipacademy.org",
    ),
    (
        "Genius Olympiad",
        "contest",
        "International high school project competition on environmental themes across science, "
        "business, design, writing, art, music, and short film — an unusually broad set of categories "
        "for one event. Held at Rochester Institute of Technology.",
        "Global — high school students aged 13–19 from any country",
        "Submissions typically due in March; finals held in June",
        "https://www.geniusolympiad.org",
    ),
 
    # =========================================================================
    # 9. FREE STRUCTURED LEARNING
    # =========================================================================
    (
        "Harvard CS50x",
        "course",
        "Harvard's introduction to computer science, free on edX. C, Python, SQL, JavaScript, and "
        "a final project. Widely regarded as the best free CS course in existence; a free certificate "
        "is available from Harvard's own site.",
        "Global — anyone, any age, no prerequisites. Completely free (paid verified certificate optional).",
        "Rolling — self-paced, always open",
        "https://cs50.harvard.edu/x/",
    ),
    (
        "Stanford Code in Place",
        "course",
        "Free five-week Python course taught by Stanford, replicating the first half of Stanford's "
        "CS106A, with a live section leader and small group sessions. Runs once a year with tens "
        "of thousands of participants worldwide.",
        "Global — adults and students of any background with no programming experience. Free.",
        "Applications typically open in February–March; course runs April–May",
        "https://codeinplace.stanford.edu",
    ),
    (
        "freeCodeCamp",
        "course",
        "Free full curriculum with certifications in responsive web design, JavaScript algorithms, "
        "front-end libraries, data analysis with Python, machine learning, and more. Each "
        "certification requires building five real projects.",
        "Global — anyone, any age, entirely free with no paywall",
        "Rolling — fully self-paced",
        "https://www.freecodecamp.org",
    ),
    (
        "The Odin Project",
        "course",
        "Free open-source full-stack web development curriculum (JavaScript or Ruby paths) built "
        "around shipping real projects rather than watching videos. Strong Discord community.",
        "Global — anyone, any age, free",
        "Rolling — fully self-paced",
        "https://www.theodinproject.com",
    ),
    (
        "MIT OpenCourseWare",
        "course",
        "Essentially the entire MIT undergraduate and graduate curriculum published free: lecture "
        "notes, problem sets, exams, and video lectures across every department.",
        "Global — anyone, any age, free, no registration required",
        "Rolling — always available",
        "https://ocw.mit.edu",
    ),
    (
        "Coursera Financial Aid",
        "course",
        "Coursera grants full fee waivers for individual courses and many specializations to anyone "
        "who applies and states their financial situation. Approval rates are high and the application "
        "takes about fifteen minutes — most students never learn this exists.",
        "Global — anyone, any age, any country. Requires two short written answers.",
        "Rolling — apply for any course at any time; review takes ~15 days",
        "https://www.coursera.org/learn",
    ),
    (
        "Art of Problem Solving (AoPS) — Alcumus & Videos",
        "course",
        "Free adaptive math problem system (Alcumus), full video series aligned to the AMC ladder, "
        "and an active community forum. The de facto training ground for U.S. competition math.",
        "Global — anyone, any age; the free tier is substantial even without paid classes",
        "Rolling — always available",
        "https://artofproblemsolving.com/alcumus",
    ),
    (
        "Exercism",
        "course",
        "Free coding practice across 70+ programming languages with human mentorship — volunteer "
        "mentors review your solutions and give real feedback, which is rare in free platforms.",
        "Global — anyone, any age, free including mentorship",
        "Rolling — self-paced, always open",
        "https://exercism.org",
    ),
    (
        "US Youth Soccer Olympic Development Program (ODP)",
        "contest",
        "The main identification pathway in American youth soccer. Players try out at state level, "
        "advance to regional camps, and the strongest are seen by college coaches and national team "
        "scouts. Even players who do not advance get evaluated by licensed coaches and gain a "
        "verifiable credential for college recruiting.",
        "U.S. only — players roughly ages 11–19, registered through their state youth soccer "
        "association. Open tryouts; no club affiliation required in most states.",
        "State tryouts typically run May–July; regional camps follow in the winter",
        "https://www.usyouthsoccer.org/programs/odp/",
    ),
    (
        "MLS NEXT",
        "contest",
        "The elite youth competition platform run by Major League Soccer, covering U13–U19. Clubs "
        "play a national schedule with mandatory scouting coverage, and the MLS NEXT Flex and "
        "All-Star events are watched directly by pro academies and Division I programs.",
        "U.S. + Canada — players U13 through U19 who make the roster of an MLS NEXT member club. "
        "Entry is through club tryouts, usually held in late spring.",
        "Season runs September through June; club tryouts typically May–June",
        "https://www.mlssoccer.com/mlsnext/",
    ),
    (
        "ECNL — Elite Clubs National League",
        "contest",
        "The largest elite youth soccer league in the U.S. for both boys and girls, and the primary "
        "recruiting ground for NCAA college soccer. Includes a formal college recruiting program with "
        "coach databases and showcase events attended by hundreds of programs.",
        "U.S. only — players U13–U19 rostered at a member club. ECNL Regional League offers a "
        "lower-barrier entry point for players not yet at national level.",
        "Season runs autumn through spring; showcase events cluster in winter and summer",
        "https://www.theecnl.com",
    ),
    (
        "U.S. Soccer Referee Certification",
        "internship",
        "Get licensed as a soccer referee starting at age 13. The Grassroots course is online plus a "
        "short in-person session, and certified referees are paid per match — typically $30–$80 a game, "
        "with youth referees often working 2–4 matches a weekend. Rare combination of a real paid job, "
        "a credential, and staying inside the sport.",
        "U.S. only — minimum age 13, no playing experience required. Registration through your "
        "state referee association; small course fee, usually recovered within two weekends of work.",
        "Rolling — courses run year-round, heaviest before spring and autumn seasons",
        "https://learning.ussoccer.com",
    ),
    (
        "NCAA Eligibility Center",
        "community",
        "Mandatory free registration for any student hoping to play NCAA Division I or II sports. "
        "Certifies your academic record and amateur status. Registering early is the single most "
        "common thing recruited athletes get wrong — many lose eligibility over coursework they took "
        "in 9th grade without checking the approved course list.",
        "U.S. + international — any student-athlete planning to compete in college sports. "
        "Register in 9th or 10th grade; the Profile Page account is free.",
        "Rolling — register anytime, ideally by sophomore year",
        "https://web3.ncaa.org/ecwr3/",
    ),
    (
        "Wendy's High School Heisman",
        "stipend",
        "National award for student-athletes who combine varsity sport, strong academics, and "
        "community involvement. State and national winners receive recognition and scholarship "
        "money, and the application itself is short compared to most national awards.",
        "U.S. only — high school seniors with a 3.0+ GPA who have participated in at least one "
        "of 47 recognized varsity sports",
        "Application typically opens in August, closes in early October",
        "https://www.wendyshighschoolheisman.com",
    ),
    (
        "National Football Foundation Scholar-Athlete Awards",
        "stipend",
        "Scholarships for high school football players who excel academically, awarded through "
        "local NFF chapters. Chapter-level awards have far smaller applicant pools than national "
        "scholarships, so the odds are unusually good.",
        "U.S. only — high school football players, nominated through a school or a local NFF chapter",
        "Chapter deadlines vary, typically autumn through winter",
        "https://footballfoundation.org",
    ),
    (
        "Special Olympics Unified Champion Schools",
        "volunteer",
        "Inclusive sports programming where students without intellectual disabilities play on "
        "unified teams alongside athletes with disabilities. Also includes youth leadership roles "
        "for organizing events — a strong service credential that involves actual sport rather than "
        "generic volunteer hours.",
        "U.S. + global affiliates — students of any age, through a participating school. Free.",
        "Rolling — programs run throughout the school year",
        "https://www.specialolympics.org/unified-champion-schools",
    ),
    (
        "USA Sport Coaching Certifications (SafeSport + Grassroots)",
        "internship",
        "Entry-level coaching licenses in soccer, basketball and other sports, available to "
        "teenagers. Certified youth coaches are paid to run camps and clinics — often $15–$25/hour — "
        "and it is one of the few sports credentials that converts directly into income before college.",
        "U.S. only — typically 16+ for paid coaching roles, 13+ for assistant/volunteer roles. "
        "SafeSport training is free and required.",
        "Rolling — online modules available year-round",
        "https://learning.ussoccer.com",
    ),
 
    # =========================================================================
    # 11. MEDICINE & HEALTH SCIENCES
    # =========================================================================
    (
        "HOSA — Future Health Professionals",
        "contest",
        "Career organization for students heading into healthcare, with 60+ competitive events "
        "from clinical nursing and sports medicine to medical innovation and health informatics. "
        "Regional, state and international conferences, plus a substantial scholarship pool.",
        "U.S. + international chapters — middle school, high school and college students, "
        "through a school chapter",
        "Regional events in winter, state in spring, international conference in June",
        "https://hosa.org",
    ),
    (
        "NIH Summer Internship Program (SIP)",
        "internship",
        "Paid 8-week summer research internship at the National Institutes of Health — the largest "
        "biomedical research agency in the world. Interns join a real lab, present a poster at the "
        "NIH Summer Poster Day, and are paid a monthly stipend.",
        "U.S. only — U.S. citizens or permanent residents, 17+ by June, enrolled at least half-time "
        "in high school, college or graduate school",
        "Application typically opens in November, closes in February",
        "https://www.training.nih.gov/programs/sip",
    ),
    (
        "Stanford Institutes of Medicine Summer Research Program (SIMR)",
        "internship",
        "Eight-week paid biomedical research internship at Stanford (minimum $500 stipend, need-based "
        "additional support). Students join one of eight institutes — immunology, neurobiology, "
        "cancer biology, bioengineering and others — and produce a research poster.",
        "U.S. only — current high school juniors and seniors, 16+ by program start, "
        "U.S. citizens or permanent residents living in the Bay Area or able to commute",
        "Application typically opens in December, closes in late February",
        "https://simr.stanford.edu",
    ),
    (
        "American Red Cross Youth Volunteer Program",
        "volunteer",
        "Structured volunteering in disaster response, blood drive support, and health education, "
        "with formal training and certificates. One of the few programs where a teenager gets "
        "genuine emergency-response credentials rather than generic service hours.",
        "U.S. only — most roles 16+, some youth club roles from 13. Free training provided.",
        "Rolling — apply anytime through your local chapter",
        "https://www.redcross.org/volunteer/become-a-volunteer.html",
    ),
    (
        "MedStart / Hospital Volunteer Programs (Junior Volunteers)",
        "volunteer",
        "Most large U.S. hospitals run junior volunteer programs where students assist in patient "
        "transport, information desks, and unit support. Direct clinical exposure, and hospital "
        "supervisors write the most credible recommendation letters a pre-med applicant can get.",
        "U.S. only — typically 14–18, requires a health screening and a semester-long commitment. "
        "Apply directly to your nearest hospital's volunteer services department.",
        "Rolling — most programs recruit in spring for summer and in autumn for the school year",
        "https://www.aha.org",
    ),
 
    # =========================================================================
    # 12. MUSIC, FILM & PERFORMING ARTS
    # =========================================================================
    (
        "NAfME All-National Honor Ensembles",
        "contest",
        "The top national ensemble for high school musicians — concert band, symphony orchestra, "
        "mixed choir, jazz ensemble and guitar ensemble. Selection is by recorded audition, and "
        "participation is a nationally recognized credential for conservatory applications.",
        "U.S. only — students in grades 9–12 who are members of NAfME, selected by recorded audition",
        "Auditions typically due in May; the event is held in the autumn",
        "https://nafme.org/programs/all-national-honor-ensembles/",
    ),
    (
        "From the Top / Jack Kent Cooke Young Artist Award",
        "stipend",
        "$10,000 award plus a performance on NPR's From the Top for exceptional young classical "
        "musicians with financial need. Selected artists also receive career development support "
        "and national broadcast exposure.",
        "U.S. only — classical musicians roughly ages 8–18 with demonstrated financial need",
        "Application typically opens in the autumn, closes in the winter",
        "https://www.fromthetop.org",
    ),
    (
        "All American High School Film Festival",
        "contest",
        "The largest student film festival in the world, screening at a Times Square theater in "
        "New York with over $500,000 in scholarship prizes. Categories cover narrative, documentary, "
        "animation, music video, screenwriting and cinematography.",
        "Global with U.S. focus — high school students, individually or in teams. Submission fee "
        "with fee waivers available.",
        "Submissions typically open in the spring, close in June; festival held in October",
        "https://hsfilmfest.com",
    ),
    (
        "Interlochen Arts Camp Scholarships",
        "stipend",
        "Summer arts intensive in music, theatre, dance, creative writing, film and visual arts. "
        "Interlochen awards significant need-based and merit aid — over half of students receive "
        "financial support — making one of the most prestigious arts camps genuinely accessible.",
        "Global with U.S. focus — students in grades 3–12, admitted by audition or portfolio",
        "Application typically opens in the autumn; scholarship priority deadlines in January",
        "https://www.interlochen.org/camp",
    ),
    (
        "National YoungArts Presidential Scholars Pathway",
        "contest",
        "Beyond the main YoungArts award, winners are the sole nominee pool for U.S. Presidential "
        "Scholars in the Arts. Includes master classes with working artists and lifelong access to "
        "an alumni network that includes Kerry Washington, Timothée Chalamet and Viola Davis.",
        "U.S. only — artists aged 15–18 or in grades 10–12, U.S. citizens or permanent residents",
        "Application typically opens in the spring, closes in October",
        "https://youngarts.org",
    ),
 
    # =========================================================================
    # 13. LAW, GOVERNMENT & PUBLIC SERVICE
    # =========================================================================
    (
        "National High School Mock Trial Championship",
        "contest",
        "Students argue a full simulated court case as attorneys and witnesses, advancing from "
        "county to state to national championship. Judged by practicing attorneys and real judges — "
        "the closest thing to genuine legal experience available before law school.",
        "U.S. only — high school students in teams, competing through a school or a state bar "
        "association program",
        "State competitions run winter through spring; nationals in May",
        "https://www.nationalmocktrial.org",
    ),
    (
        "United States Senate Page Program",
        "internship",
        "Paid semester working on the Senate floor in Washington D.C. — delivering legislation, "
        "preparing the chamber, and attending a dedicated Senate Page School. Roughly 30 positions "
        "per session nationwide, appointed by individual senators.",
        "U.S. only — high school juniors who are 16–17 years old, with a 3.0+ GPA. "
        "Apply directly through your own U.S. senator's office.",
        "Deadlines set individually by each senator's office; typically several months in advance",
        "https://www.senate.gov/reference/reference_index_subjects/Pages_vrd.htm",
    ),
    (
        "Teen Court / Youth Court Volunteer",
        "volunteer",
        "Real diversion courts where teenagers serve as jurors, attorneys and bailiffs for actual "
        "first-time juvenile offenders, with sentences that carry legal weight. Free training in "
        "legal procedure, and a genuinely unusual line on an application.",
        "U.S. only — typically ages 13–18, through a county or city youth court program. "
        "Over 1,000 programs operate nationwide.",
        "Rolling — most programs train new volunteers each semester",
        "https://www.globalyouthjustice.org",
    ),
    (
        "Boys & Girls Clubs Youth of the Year",
        "stipend",
        "Signature recognition program with local, state and national rounds. National Youth of the "
        "Year receives a $145,000 scholarship, and state winners receive $20,000 — one of the largest "
        "award ladders open to students without exceptional test scores.",
        "U.S. only — Boys & Girls Club members aged 14–18 who have been active for at least one year",
        "Local rounds in winter; state in spring; nationals in September",
        "https://www.bgca.org/programs/youth-of-the-year/",
    ),
 
    # =========================================================================
    # 14. SKILLED TRADES, CULINARY & AGRICULTURE
    # =========================================================================
    (
        "SkillsUSA Championships",
        "contest",
        "The largest skilled trades competition in the U.S. — over 100 events covering welding, "
        "automotive service, culinary arts, carpentry, cosmetology, cybersecurity and 3D visualization. "
        "Industry sponsors award tool packages, scholarships and direct job offers to medalists.",
        "U.S. only — high school and college students in career and technical education programs, "
        "through a school chapter",
        "District and state competitions run February–April; nationals in June",
        "https://www.skillsusa.org",
    ),
    (
        "National FFA Organization",
        "contest",
        "Agricultural education organization with 25+ career development events (agribusiness, "
        "veterinary science, agricultural mechanics, food science) plus the Supervised Agricultural "
        "Experience where students run a real enterprise. Awards over $2 million in scholarships annually.",
        "U.S. only — students in grades 7–12 enrolled in an agricultural education program. "
        "Urban and suburban chapters are increasingly common.",
        "Chapter activities year-round; state conventions in spring; national convention in October",
        "https://www.ffa.org",
    ),
    (
        "FCCLA — Family, Career and Community Leaders of America",
        "contest",
        "Competitive events in culinary arts, baking and pastry, fashion design, interior design, "
        "early childhood education, and hospitality. One of the few national organizations where "
        "these skills are treated as a serious competitive career track.",
        "U.S. only — middle school through college students, through a school chapter",
        "Regional and state events run winter through spring; national leadership conference in July",
        "https://fcclainc.org",
    ),
    (
        "C-CAP — Careers through Culinary Arts Program",
        "stipend",
        "Culinary scholarship competition awarding millions annually in cooking school scholarships, "
        "plus paid internships and job placement. Students compete in a live practical cooking exam "
        "judged by working chefs.",
        "U.S. only — high school students in participating C-CAP cities and school districts",
        "Preliminary competitions in the winter; finals in the spring",
        "https://www.ccapinc.org",
    ),
    (
        "mikeroweWORKS Work Ethic Scholarship",
        "stipend",
        "Scholarships for students pursuing skilled trades — welding, HVAC, plumbing, electrical, "
        "diesel mechanics. Requires signing a work ethic pledge rather than writing academic essays, "
        "and deliberately rewards attitude over GPA.",
        "U.S. only — students enrolling in an accredited trade or vocational program. No age limit.",
        "Application typically opens in February, closes in May",
        "https://www.mikeroweworks.org/scholarship/",
    ),
 
    # =========================================================================
    # 15. AVIATION & MILITARY PATHWAYS
    # =========================================================================
    (
        "Civil Air Patrol Cadet Program",
        "community",
        "The U.S. Air Force auxiliary youth program: free orientation flights, flight academy "
        "scholarships covering a private pilot license, search-and-rescue training, and leadership "
        "ranks. Cadets who complete key milestones enter military service at advanced pay grade.",
        "U.S. only — ages 12 through 18 (may continue to 21). Low annual membership fee with "
        "waivers available.",
        "Rolling — join a local squadron at any time",
        "https://www.gocivilairpatrol.com",
    ),
    (
        "EAA Young Eagles + Ray Aviation Scholarship",
        "stipend",
        "Free introductory flights for youth, plus the Ray Aviation Scholarship, which covers up to "
        "$11,000 toward a private pilot certificate. One of the only paths to a pilot license that "
        "does not require family money.",
        "U.S. only — Young Eagles flights for ages 8–17; Ray Scholarship for ages 16–18 nominated "
        "through a local EAA chapter",
        "Young Eagles rallies run year-round; Ray Scholarship nominations through local chapters",
        "https://www.eaa.org/eaa/youth/free-ye-flights",
    ),
    (
        "Air Force / Army / Navy JROTC Scholarships",
        "stipend",
        "JROTC units offer leadership training, flight simulation, cyber competitions and drill, "
        "plus dedicated scholarship pools and advanced enlistment rank. Participation carries no "
        "military service obligation.",
        "U.S. only — high school students at a school with a JROTC unit",
        "Enrollment follows the school year; scholarship applications typically in winter",
        "https://www.airforce.com/education/jrotc",
    ),
 
    # =========================================================================
    # 16. LANGUAGES & INTERNATIONAL EXCHANGE
    # =========================================================================
    (
        "NSLI-Y — National Security Language Initiative for Youth",
        "stipend",
        "Fully funded U.S. State Department scholarship for intensive study of Arabic, Chinese, "
        "Hindi, Indonesian, Korean, Persian, Russian, Swahili or Turkish — summer or academic year "
        "abroad with a host family. Covers everything including international airfare.",
        "U.S. only — U.S. citizens aged 15–18 with a 2.5+ GPA. No prior language study required "
        "for most languages.",
        "Application typically opens in September, closes in early November",
        "https://www.nsliforyouth.org",
    ),
    (
        "CBYX — Congress-Bundestag Youth Exchange",
        "stipend",
        "Fully funded academic year in Germany: language training, high school placement, and a "
        "host family, entirely paid by the U.S. and German governments. Includes a vocational track "
        "for students interested in trades rather than university.",
        "U.S. only — U.S. citizens aged 15–18 at program start. No prior German required.",
        "Application typically closes in December or January",
        "https://www.usagermanyscholarship.org",
    ),
    (
        "Kennedy-Lugar Youth Exchange and Study (YES) Abroad",
        "stipend",
        "Fully funded academic year abroad in countries with significant Muslim populations, "
        "run by the U.S. State Department. Covers all costs, and alumni gain access to a large "
        "international network and follow-on grant programs.",
        "U.S. only — U.S. citizens aged 15–18 with a 3.0+ GPA",
        "Application typically opens in September, closes in December",
        "https://yes-abroad.org",
    ),
]
 
 
import os
import sqlite3
from flask import current_app, g

SEED_OPPORTUNITIES = OPPORTUNITIES


def get_db():
  if "db" not in g:
    db_path = current_app.config["DATABASE_PATH"]
    g.db = sqlite3.connect(db_path)
    g.db.row_factory = sqlite3.Row
    g.db.execute("PRAGMA foreign_keys = ON")
  return g.db


def close_db(e=None):
  db = g.pop("db", None)
  if db is not None:
    db.close()


def init_db(app):
  db_path = app.config["DATABASE_PATH"]
  is_new = not os.path.exists(db_path)

  conn = sqlite3.connect(db_path)
  conn.execute("PRAGMA foreign_keys = ON")

  schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
  with open(schema_path, "r", encoding="utf-8") as f:
    conn.executescript(f.read())

  cur = conn.execute("SELECT COUNT(*) FROM opportunities")
  has_data = cur.fetchone()[0] > 0

  if not has_data:
    conn.executemany(
        """INSERT INTO opportunities (title, category, description, audience, deadline, link)
           VALUES (?, ?, ?, ?, ?, ?)""",
        SEED_OPPORTUNITIES,
    )

  conn.commit()
  conn.close()

 
  app.teardown_appcontext(close_db)
  return is_new