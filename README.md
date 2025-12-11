# CSB Project 1

**WARNING: This project contains intentional vulnerabilities for educational purposes.**

**DO NOT use in production!**

A simple Django-based notes application where users can create, view, and transfer notes between accounts. This project intentionally contains five common OWASP security vulnerabilities for educational purposes: broken access control, exposed SECRET_KEY, DEBUG mode enabled, XSS via |safe filter, and missing CSRF protection. Each flaw includes commented fixes in the code.
