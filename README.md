Python-SOPMI-IR
===============

Python implementation of Turney's 2001 PMI-IR method utilizing Google instead of AltaVista, which now uses Yahoo search.

Features
--------
No POS tagging, no tokenization, no bells and whistles. This code only does Google searches, response parsing, basic math, and result caching to reduce redundant search queries.

Accuracy
--------
Okay. It depends what you put in and what pre-screening has been done for words with no, limited, or ambiguous orientation. I should type up a more substantial writeup about it soon.

Warnings
--------
This script totally violates the Google Terms of Service and you probably shouldn't use it.
