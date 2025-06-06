### Project: Website Relaunch for AG Computational Arithmetic Geometry

This document outlines a 4-month plan to redesign and enhance the research group's website.

---

### **1. Project Goals & Answers to Your Questions**

The main goal is to create a modern, professional, and easy-to-maintain website.

**Key Objectives:**

1.  **Modern UI/UX:** Implement a new, visually appealing design based on the provided examples (specifically inspired by `allanlab.org` and `unlv-spfg.github.io`), focusing on a clean layout that works well on all devices.
2.  **Simplified Content Management:** Make it extremely simple for group members to perform common tasks without writing code. This includes:
    *   Adding or updating personal member pages.
    *   Creating new pages for courses each semester under "Teaching".
    *   Uploading and linking to PDFs for publications or course materials.
3.  **Multilingual Support:** The entire website will be available in both German and English, with an easy-to-use language switcher.
4.  **CMS Integration:** To achieve the goal of easy content management, we will integrate `jekyll-admin`. This provides a graphical interface for editing content and uploading files, which runs on a local computer. This is the most direct way to fulfill the requirement of a system that allows content updates without diving into the codebase.

---

### **2. Four-Month Project Plan (English)**

#### **Month 1: Foundation & Design**

The focus of this month is to establish the new technical and visual foundation for the website.

*   **Week 1: Analysis & Setup**
    *   **Task:** Deeply analyze the structure of the example websites, particularly `allanlab.org` for its clean theme and `unlv-spfg.github.io` for its homepage structure.
    *   **Task:** Set up a new Jekyll project locally using a modern, flexible theme (e.g., `al-folio`, the theme from `allanlab.org`) as our base.
    *   **Deliverable:** A new, clean Jekyll project under version control (Git).

*   **Week 2: Homepage Mockup & Theme Customization**
    *   **Task:** Develop a functional mockup of the new homepage. This will incorporate the three-column layout with images for "News," "Research," and "Members," as requested.
    *   **Task:** We will use placeholder images initially, which can be replaced later.
    *   **Task:** Customize the theme's default colors, fonts, and styles to create a unique look, potentially aligning with Heidelberg University's branding.
    *   **Deliverable:** A working prototype of the new homepage.

*   **Week 3: Page Layouts & Navigation**
    *   **Task:** Create the basic page layouts for all main sections: `Research`, `Publications`, `Teaching`, `Members`, `Links`, and `Contact`.
    *   **Task:** Implement the main navigation menu to ensure a logical and user-friendly site structure.
    *   **Deliverable:** A clickable prototype with all main pages and a functioning navigation menu.

*   **Week 4: Present Mockups & Gather Feedback**
    *   **Task:** Prepare 2-3 slight variations of the design (e.g., different color schemes or header styles).
    *   **Task:** Present the prototypes to Prof. Böckle and the group to gather feedback.
    *   **Deliverable:** A final decision on the design direction for the website.

#### **Month 2: Content & Structure**

This month is dedicated to migrating content and building the new, flexible content structures.

*   **Week 5: Content Migration**
    *   **Task:** Carefully migrate all text and images from the current website into the new page layouts.
    *   **Task:** Ensure all content is correctly formatted and displayed.
    *   **Deliverable:** All existing content integrated into the new design.

*   **Week 6: Dynamic Content - Members & Publications**
    *   **Task:** Use Jekyll "Collections" to manage members and publications. This means each member and each publication will be a single, simple data file.
    *   **Task:** Create a template for individual member pages. Adding a new member will be as easy as creating a new file with their name, photo, and bio.
    *   **Deliverable:** A system for easily managing members and publications.

*   **Week 7: Dynamic Content - Teaching & PDFs**
    *   **Task:** Set up a Jekyll "Collection" for teaching. Each course will be its own file.
    *   **Task:** Create a template for course subpages, making it simple to add new courses each semester.
    *   **Task:** Implement and test the process for uploading and linking to PDFs.
    *   **Deliverable:** A structured, easy-to-update "Teaching" section.

*   **Week 8: Review & Documentation**
    *   **Task:** Review the new content structures with the group to ensure they are intuitive.
    *   **Task:** Create simple, clear documentation explaining how a non-technical user can add a new member, a new course, or a new publication.
    *   **Deliverable:** Finalized content structure and user documentation.

#### **Month 3: Advanced Features**

We'll now integrate the more complex features: multilingual support and the CMS.

*   **Weeks 9-10: Multilingual Support (DE/EN)**
    *   **Task:** Integrate the `jekyll-polyglot` plugin for managing multiple languages.
    *   **Task:** Duplicate the content structure to support both German and English. (Note: The actual translation of the content will need to be provided by the group).
    *   **Task:** Implement a language switcher in the website's header or footer.
    *   **Deliverable:** A fully bilingual website structure.

*   **Weeks 11-12: Content Management System (CMS)**
    *   **Task:** Create and configure a GitHub App to allow `Pages CMS` to securely connect to the website's repository.
    *   **Task:** Create the necessary `pagescms.yml` configuration file to define the editable sections (Members, Teaching, Publications).
    *   **Task:** Thoroughly test the process of creating/editing pages and uploading files through the online `Pages CMS` interface.
    *   **Deliverable:** A working and configured `Pages CMS` setup, accessible from a web browser.

#### **Month 4: Testing, Refinement & Deployment**

The final month is for ensuring everything is perfect before the official launch.

*   **Week 13: User Training & Testing**
    *   **Task:** Hold a training session with designated group members to teach them how to use the `Pages CMS` web interface.
    *   **Task:** Have them perform test updates from their own computers or phones: add a new course, upload a PDF, and edit a member page.
    *   **Deliverable:** User feedback on the `Pages CMS` workflow and the overall website.

*   **Week 14: Bug Fixing & Final Polish**
    *   **Task:** Address any bugs or usability issues discovered during user testing.
    *   **Task:** Perform a final review of all content in both languages, checking for broken links, missing images, and layout inconsistencies.
    *   **Deliverable:** A stable, polished, and release-ready website.

*   **Week 15: Documentation & Deployment Preparation**
    *   **Task:** Finalize all user documentation for future reference.
    *   **Task:** Prepare the site for deployment on GitHub Pages, including final configuration checks.
    *   **Deliverable:** Finalized documentation and a fully configured project ready for launch.

*   **Week 16: Deployment & Go-Live**
    *   **Task:** Deploy the new website, making it live.
    *   **Task:** Monitor the site for any post-launch issues.
    *   **Deliverable:** The new website is successfully launched and operational.

---

### **3. Viermonatiger Projektplan (Deutsch)**

#### **Monat 1: Fundament & Design**

Der Fokus dieses Monats liegt darauf, die neue technische und visuelle Grundlage für die Website zu schaffen.

*   **Woche 1: Analyse & Setup**
    *   **Aufgabe:** Detaillierte Analyse der Struktur der Beispiel-Websites, insbesondere `allanlab.org` für das klare Theme und `unlv-spfg.github.io` für die Homepage-Struktur.
    *   **Aufgabe:** Ein neues Jekyll-Projekt lokal aufsetzen, das ein modernes, flexibles Theme (z.B. `al-folio`, das Theme von `allanlab.org`) als Basis verwendet.
    *   **Ergebnis:** Ein neues, sauberes Jekyll-Projekt unter Versionskontrolle (Git).

*   **Woche 2: Homepage-Entwurf & Theme-Anpassung**
    *   **Aufgabe:** Entwicklung eines funktionalen Entwurfs der neuen Homepage. Dieser wird das gewünschte dreispaltige Layout mit Bildern für "News", "Forschung" und "Mitglieder" umsetzen.
    *   **Aufgabe:** Wir verwenden zunächst Platzhalterbilder, die später ersetzt werden können.
    *   **Aufgabe:** Anpassung der Standardfarben, Schriftarten und Stile des Themes, um ein einzigartiges Erscheinungsbild zu schaffen, das sich möglicherweise am Corporate Design der Universität Heidelberg orientiert.
    *   **Ergebnis:** Ein funktionierender Prototyp der neuen Homepage.

*   **Woche 3: Seitenlayouts & Navigation**
    *   **Aufgabe:** Erstellung der grundlegenden Seitenlayouts für alle Hauptbereiche: `Forschung`, `Publikationen`, `Lehre`, `Mitglieder`, `Links` und `Kontakt`.
    *   **Aufgabe:** Implementierung des Hauptnavigationsmenüs, um eine logische und benutzerfreundliche Seitenstruktur zu gewährleisten.
    *   **Ergebnis:** Ein klickbarer Prototyp mit allen Hauptseiten und einem funktionierenden Navigationsmenü.

*   **Woche 4: Präsentation der Entwürfe & Feedback einholen**
    *   **Aufgabe:** Vorbereitung von 2-3 leichten Variationen des Designs (z.B. unterschiedliche Farbschemata oder Header-Stile).
    *   **Aufgabe:** Präsentation der Prototypen vor Prof. Böckle und der Gruppe, um Feedback zu sammeln.
    *   **Ergebnis:** Eine endgültige Entscheidung über die Designrichtung für die Website.

#### **Monat 2: Inhalte & Struktur**

Dieser Monat ist dem Übertragen von Inhalten und dem Aufbau der neuen, flexiblen Inhaltsstrukturen gewidmet.

*   **Woche 5: Migration der Inhalte**
    *   **Aufgabe:** Sorgfältige Übertragung aller Texte und Bilder von der aktuellen Website in die neuen Seitenlayouts.
    *   **Aufgabe:** Sicherstellen, dass alle Inhalte korrekt formatiert und angezeigt werden.
    *   **Ergebnis:** Alle bestehenden Inhalte sind in das neue Design integriert.

*   **Woche 6: Dynamische Inhalte - Mitglieder & Publikationen**
    *   **Aufgabe:** Verwendung von Jekyll "Collections" zur Verwaltung von Mitgliedern und Publikationen. Das bedeutet, dass jedes Mitglied und jede Publikation eine einzelne, einfache Datendatei sein wird.
    *   **Aufgabe:** Erstellung einer Vorlage für einzelne Mitgliederseiten. Das Hinzufügen eines neuen Mitglieds wird so einfach wie das Erstellen einer neuen Datei mit Namen, Foto und Biografie.
    *   **Ergebnis:** Ein System zur einfachen Verwaltung von Mitgliedern und Publikationen.

*   **Woche 7: Dynamische Inhalte - Lehre & PDFs**
    *   **Aufgabe:** Einrichtung einer Jekyll "Collection" für die Lehre. Jeder Kurs wird eine eigene Datei sein.
    *   **Aufgabe:** Erstellung einer Vorlage für Kurs-Unterseiten, was das Hinzufügen neuer Kurse jedes Semesters vereinfacht.
    *   **Aufgabe:** Implementierung und Testen des Prozesses zum Hochladen und Verlinken von PDFs.
    *   **Ergebnis:** Ein strukturierter, leicht zu aktualisierender "Lehre"-Bereich.

*   **Woche 8: Überprüfung & Dokumentation**
    *   **Aufgabe:** Überprüfung der neuen Inhaltsstrukturen mit der Gruppe, um sicherzustellen, dass sie intuitiv sind.
    *   **Aufgabe:** Erstellung einer einfachen, klaren Dokumentation, die erklärt, wie ein nicht-technischer Benutzer ein neues Mitglied, einen neuen Kurs oder eine neue Publikation hinzufügen kann.
    *   **Ergebnis:** Abgeschlossene Inhaltsstruktur und Benutzerdokumentation.

#### **Monat 3: Fortgeschrittene Funktionen**

Jetzt integrieren wir die komplexeren Funktionen: Mehrsprachigkeit und das CMS.

*   **Wochen 9-10: Mehrsprachigkeit (DE/EN)**
    *   **Aufgabe:** Integration des `jekyll-polyglot`-Plugins zur Verwaltung mehrerer Sprachen.
    *   **Aufgabe:** Duplizierung der Inhaltsstruktur zur Unterstützung von Deutsch und Englisch. (Hinweis: Die eigentliche Übersetzung der Inhalte muss von der Gruppe bereitgestellt werden).
    *   **Aufgabe:** Implementierung eines Sprachumschalters im Header oder Footer der Website.
    *   **Ergebnis:** Eine vollständig zweisprachige Website-Struktur.

*   **Wochen 11-12: Content-Management-System (CMS)**
    *   **Aufgabe:** Erstellung und Konfiguration einer GitHub App, damit `Pages CMS` sich sicher mit dem Repository der Website verbinden kann.
    *   **Aufgabe:** Erstellung der notwendigen `pagescms.yml`-Konfigurationsdatei, um die bearbeitbaren Bereiche (Mitglieder, Lehre, Publikationen) zu definieren.
    *   **Aufgabe:** Gründliches Testen des Prozesses zum Erstellen/Bearbeiten von Seiten und zum Hochladen von Dateien über die Online-Oberfläche von `Pages CMS`.
    *   **Ergebnis:** Ein funktionierendes und konfiguriertes `Pages CMS`-Setup, das über einen Webbrowser zugänglich ist.

#### **Monat 4: Testen, Verfeinern & Bereitstellung**

Der letzte Monat dient dazu, sicherzustellen, dass vor dem offiziellen Start alles perfekt ist.

*   **Woche 13: Benutzerschulung & Testen**
    *   **Aufgabe:** Durchführung einer Schulung mit ausgewählten Gruppenmitgliedern, um ihnen die Verwendung der `Pages CMS`-Weboberfläche beizubringen.
    *   **Aufgabe:** Sie sollen Test-Updates von ihren eigenen Computern oder Telefonen durchführen: einen neuen Kurs hinzufügen, ein PDF hochladen und eine Mitgliederseite bearbeiten.
    *   **Ergebnis:** Benutzerfeedback zum `Pages CMS`-Workflow und zur gesamten Website.

*   **Woche 14: Fehlerbehebung & Feinschliff**
    *   **Aufgabe:** Behebung aller Fehler oder Usability-Probleme, die beim Benutzertest entdeckt wurden.
    *   **Aufgabe:** Durchführung einer abschließenden Überprüfung aller Inhalte in beiden Sprachen auf fehlerhafte Links, fehlende Bilder und Layout-Inkonsistenzen.
    *   **Ergebnis:** Eine stabile, polierte und veröffentlichungsreife Website.

*   **Woche 15: Dokumentation & Vorbereitung der Bereitstellung**
    *   **Aufgabe:** Fertigstellung der gesamten Benutzerdokumentation für zukünftige Referenzen.
    *   **Aufgabe:** Vorbereitung der Website für die Bereitstellung auf GitHub Pages, einschließlich abschließender Konfigurationsprüfungen.
    *   **Ergebnis:** Fertiggestellte Dokumentation und ein vollständig konfiguriertes Projekt, das startklar ist.

*   **Woche 16: Bereitstellung & Go-Live**
    *   **Aufgabe:** Bereitstellung der neuen Website, um sie live zu schalten.
    *   **Aufgabe:** Überwachung der Live-Site auf eventuelle Probleme nach dem Start.
    *   **Ergebnis:** Die neue Website ist erfolgreich gestartet und betriebsbereit. 